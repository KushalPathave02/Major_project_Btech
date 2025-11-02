from flask import Blueprint, jsonify, current_app
from flask import g
from bson import ObjectId
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import json
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

@forecast_bp.route('/forecast/test', methods=['GET'])
def test_forecast():
    """Test endpoint to check LSTM availability"""
    return jsonify({
        'status': 'ok',
        'tensorflow_available': TENSORFLOW_AVAILABLE,
        'message': 'Forecast service is running',
        'lstm_ready': TENSORFLOW_AVAILABLE,
        'endpoint': '/forecast'
    })

@forecast_bp.route('/forecast/demo', methods=['GET'])
def demo_forecast():
    """Demo endpoint with sample data for testing"""
    try:
        # Sample monthly expenses data
        sample_data = [
            {'month': '2024-01', 'expense': 1500.0},
            {'month': '2024-02', 'expense': 1600.0},
            {'month': '2024-03', 'expense': 1450.0},
            {'month': '2024-04', 'expense': 1700.0},
            {'month': '2024-05', 'expense': 1550.0},
            {'month': '2024-06', 'expense': 1650.0}
        ]
        
        # Simple moving average of last 3 months
        recent_expenses = [1700.0, 1550.0, 1650.0]  # Last 3 months
        forecast_value = sum(recent_expenses) / len(recent_expenses)
        
        return jsonify({
            'history': sample_data,
            'forecast': {
                'month': '2024-07',
                'expense': round(forecast_value, 2)
            },
            'message': 'Demo forecast with sample data',
            'method': 'moving_average_demo'
        })
    except Exception as e:
        return jsonify({
            'error': f'Demo error: {str(e)}',
            'message': 'Demo forecast failed'
        }), 500

@forecast_bp.route('/forecast/public', methods=['GET'])
def public_forecast():
    """Public forecast endpoint for testing (no auth required)"""
    try:
        print("🔍 Public forecast endpoint called...")
        print(f"📊 TensorFlow Available: {TENSORFLOW_AVAILABLE}")
        
        # Return demo data for now - you can modify this later
        sample_data = [
            {'month': '2024-08', 'expense': 1500.0},
            {'month': '2024-09', 'expense': 1600.0},
            {'month': '2024-10', 'expense': 1450.0},
            {'month': '2024-11', 'expense': 1700.0}
        ]
        
        # Simple forecast
        recent_expenses = [1600.0, 1450.0, 1700.0]  # Last 3 months
        forecast_value = sum(recent_expenses) / len(recent_expenses)
        
        return jsonify({
            'history': sample_data,
            'forecast': {
                'month': '2024-12',
                'expense': round(forecast_value, 2)
            },
            'message': 'Public forecast endpoint working - authentication not required',
            'method': 'moving_average',
            'tensorflow_available': TENSORFLOW_AVAILABLE
        })
    except Exception as e:
        print(f"❌ Error in public forecast: {str(e)}")
        return jsonify({
            'error': f'Public forecast error: {str(e)}',
            'message': 'Public forecast failed'
        }), 500

@forecast_bp.route('/forecast', methods=['GET'])
@token_required
def get_forecast():
    try:
        print("🔍 Forecast endpoint called...")
        print(f"📊 TensorFlow Available: {TENSORFLOW_AVAILABLE}")
        
        # Early check for database connection
        if get_db is None:
            print("❌ Database connection not initialized")
            return jsonify({
                'error': 'Database connection not available',
                'history': [],
                'forecast': None
            }), 500
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
        
        # Check if TensorFlow is available - if not, use simple forecasting
        if not TENSORFLOW_AVAILABLE:
            print("⚠️ TensorFlow not available, using simple moving average forecast")
            # Simple moving average forecast (last 3 months average)
            recent_values = monthly_expenses.tail(min(3, len(monthly_expenses))).values
            forecast_value = float(np.mean(recent_values))
            next_month = monthly_expenses.index[-1] + 1
            
            return jsonify({
                'history': [{'month': str(m), 'expense': float(v)} for m, v in monthly_expenses.items()],
                'forecast': {
                    'month': str(next_month),
                    'expense': forecast_value
                },
                'message': 'Simple moving average forecast (TensorFlow not available)',
                'method': 'moving_average'
            })
        
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
            
            # Build lightweight LSTM model for memory efficiency
            model = keras.Sequential([
                layers.Input(shape=(WINDOW_SIZE, 1)),
                layers.LSTM(20, return_sequences=False),  # Reduced from 50 to 20, removed second LSTM
                layers.Dense(10),                         # Reduced from 25 to 10
                layers.Dense(1)
            ])
            
            model.compile(optimizer='adam', loss='mse')
            
            # Train model (with minimal epochs for memory efficiency)
            model.fit(X, y_target, epochs=10, batch_size=1, verbose=0)
            
            # Forecast next month
            last_sequence = y_scaled[-WINDOW_SIZE:].reshape(1, WINDOW_SIZE, 1)
            forecast_scaled = model.predict(last_sequence, verbose=0)
            forecast_value = scaler.inverse_transform(forecast_scaled)[0][0]
            
            # Clean up memory
            del model, X, y_target, y_scaled, last_sequence, forecast_scaled
            import gc
            gc.collect()
            
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
        print(f"❌ Critical error in forecast endpoint: {str(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': f'Server error: {str(e)}',
            'message': 'Failed to generate forecast',
            'debug': {
                'tensorflow_available': TENSORFLOW_AVAILABLE,
                'error_type': type(e).__name__
            }
        }), 500
