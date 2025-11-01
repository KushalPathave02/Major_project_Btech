from flask import Blueprint, jsonify, current_app, request
from flask import g
from bson import ObjectId
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import json
from functools import wraps
from sklearn.preprocessing import MinMaxScaler
from middleware import token_required

# TensorFlow for LSTM
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    tf = None
    TENSORFLOW_AVAILABLE = False

get_db = None  # Will be set by the app
forecast_bp = Blueprint('forecast', __name__)

def init_app(db_func):
    global get_db
    get_db = db_func

def add_cors_headers(response):
    """Add CORS headers to the response"""
    response.headers.add('Access-Control-Allow-Origin', 'https://major-project-btech-1.onrender.com')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

def handle_options_request():
    """Handle OPTIONS request for CORS preflight"""
    response = jsonify({'status': 'success', 'message': 'CORS preflight successful'})
    return add_cors_headers(response), 200

@forecast_bp.route('/test', methods=['GET', 'OPTIONS'])
def test_forecast():
    """Test endpoint to check LSTM availability"""
    if request.method == 'OPTIONS':
        return handle_options_request()
        
    response = jsonify({
        'status': 'ok',
        'tensorflow_available': TENSORFLOW_AVAILABLE,
        'message': 'Forecast service is running',
        'lstm_ready': TENSORFLOW_AVAILABLE,
        'endpoint': '/api/forecast'
    })

@forecast_bp.route('/forecast', methods=['GET', 'OPTIONS'])
@token_required
def get_forecast():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return handle_options_request()
        
    try:
        print("🔍 Forecast endpoint called...")
        print(f"📊 TensorFlow Available: {TENSORFLOW_AVAILABLE}")
        # Per-user transactions only; no global file fallback to avoid leaking data
        db = get_db()
        user_id = g.user_id
        transactions = list(db.transactions.find({
            'user_id': user_id
        }, {
            'date': 1,
            'amount': 1,
            '_id': 0,
            'category': 1,
            'type': 1
        }))

        print(f"📊 Found {len(transactions)} transactions for user {user_id}")
        
        if not transactions:
            return jsonify({
                'history': [],
                'forecast': None,
                'message': 'No transactions yet for forecasting. Please upload your transaction data first.',
                'debug': {
                    'user_id': str(user_id),
                    'transaction_count': 0,
                    'tensorflow_available': TENSORFLOW_AVAILABLE
                }
            })

        # Normalize and filter transactions into a DataFrame
        # Prefer expenses: negative amounts, or type 'debit', or category 'expense'
        normalized = []
        for tx in transactions:
            amt = tx.get('amount')
            dt = tx.get('date')
            cat = str(tx.get('category', '')).lower()
            ttype = str(tx.get('type', '')).lower()
            # parse date to ISO
            try:
                date_val = pd.to_datetime(dt)
            except Exception:
                continue
            try:
                amt_val = float(amt)
            except Exception:
                continue
            is_expense = (amt_val < 0) or (ttype == 'debit') or ('expense' in cat)
            normalized.append({'date': date_val, 'amount': amt_val, 'is_expense': is_expense})

        if not normalized:
            return jsonify({
                'history': [],
                'forecast': None,
                'message': 'No valid transactions found for forecasting'
            })

        df = pd.DataFrame(normalized)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        # Keep only expense rows
        df = df[df['is_expense']]
        # Use absolute values for expenses
        df['amount'] = df['amount'].abs()
        
        # Group by month and sum expenses
        monthly_expenses = df.groupby('month')['amount'].sum()
        
        if len(monthly_expenses) < 6:  # Need at least 6 data points for LSTM
            return jsonify({
                'history': [{'month': str(m), 'expense': float(v)} for m, v in monthly_expenses.items()],
                'forecast': None,
                'message': 'Need at least 6 months of data for LSTM forecasting'
            })
        
        # Check if TensorFlow is available
        if not TENSORFLOW_AVAILABLE:
            return jsonify({
                'error': 'TensorFlow not available for LSTM forecasting',
                'history': [{'month': str(m), 'expense': float(v)} for m, v in monthly_expenses.items()],
                'forecast': None
            }), 500
        
        # Convert to numeric values for LSTM
        y = monthly_expenses.astype(float).values
        
        try:
            # Prepare data for LSTM
            scaler = MinMaxScaler()
            y_scaled = scaler.fit_transform(y.reshape(-1, 1))
            
            # Create sequences for LSTM (use 3 months to predict next month)
            WINDOW_SIZE = min(3, len(y_scaled) - 1)
            X, y_target = [], []
            
            for i in range(WINDOW_SIZE, len(y_scaled)):
                X.append(y_scaled[i-WINDOW_SIZE:i, 0])
                y_target.append(y_scaled[i, 0])
            
            X = np.array(X)
            y_target = np.array(y_target)
            
            if len(X) < 3:
                return jsonify({
                    'error': 'Insufficient data for LSTM training',
                    'history': [{'month': str(m), 'expense': float(v)} for m, v in monthly_expenses.items()],
                    'forecast': None
                }), 500
            
            # Reshape for LSTM [samples, time steps, features]
            X = X.reshape((X.shape[0], X.shape[1], 1))
            
            # Build LSTM model
            model = keras.Sequential([
                layers.Input(shape=(WINDOW_SIZE, 1)),
                layers.LSTM(50, return_sequences=True),
                layers.LSTM(50),
                layers.Dense(25),
                layers.Dense(1)
            ])
            
            model.compile(optimizer='adam', loss='mse')
            
            # Train model (with minimal epochs for speed)
            model.fit(X, y_target, epochs=50, batch_size=1, verbose=0)
            
            # Forecast next month
            last_sequence = y_scaled[-WINDOW_SIZE:].reshape(1, WINDOW_SIZE, 1)
            forecast_scaled = model.predict(last_sequence, verbose=0)
            forecast_value = scaler.inverse_transform(forecast_scaled)[0][0]
            
            next_month = monthly_expenses.index[-1] + 1
            
            # Prepare response
            history = [{
                'month': str(month),
                'expense': float(amount)
            } for month, amount in monthly_expenses.items()]
            
            return jsonify({
                'history': history,
                'forecast': {
                    'month': str(next_month),
                    'expense': float(forecast_value)
                },
                'message': 'LSTM forecast generated successfully'
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Error in forecasting: {str(e)}',
                'history': [{'month': str(m), 'expense': float(v)} for m, v in monthly_expenses.items()],
                'forecast': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'message': 'Failed to generate forecast'
        }), 500
