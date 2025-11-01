from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

import database

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
database.init_app(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_default_secret_key')

# Mail configuration (use free Gmail SMTP for dev). Set these in .env
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER', '')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('EMAIL_USER', ''))

mail = Mail(app)

# CORS Configuration
# Allow both production and development frontend domains
allowed_origins = [
    'https://major-project-btech-1.onrender.com',
    'http://localhost:3000',  # For local development
    'http://127.0.0.1:3000'   # For local development
]

# Add public base URL if set (for local network access)
public_base = os.getenv('APP_PUBLIC_BASE_URL')
if public_base:
    allowed_origins.append(public_base)
    try:
        import urllib.parse as _urlparse
        parsed = _urlparse.urlparse(public_base)
        if parsed.scheme and parsed.hostname:
            allowed_origins.append(f"{parsed.scheme}://{parsed.hostname}:3000")
    except Exception:
        pass

# Add frontend URL from environment variable if set
frontend_url = os.getenv('FRONTEND_URL')
if frontend_url and frontend_url not in allowed_origins:
    allowed_origins.append(frontend_url)

# Configure CORS with the allowed origins
CORS(
    app,
    resources={
        r"/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "expose_headers": ["Content-Range", "X-Content-Range"]
        }
    }
)

# Health check route
@app.route('/')
def index():
    return 'Financial Analytics Dashboard API'

# Register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.transactions import transactions_bp
from routes.export import export_bp
from routes.analytics import analytics_bp
from routes.messages import messages_bp
from routes.gemini import gemini_bp
from routes.settings import settings_bp
from routes.users import users_bp
from routes.wallet import wallet_bp
from routes.forecast import forecast_bp

# Initialize blueprints with database connection
from database import get_db as get_db_func
from routes.forecast import init_app as init_forecast
init_forecast(get_db_func)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(export_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(gemini_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(users_bp)
app.register_blueprint(wallet_bp)
# Register forecast blueprint with URL prefix
app.register_blueprint(forecast_bp, url_prefix='/api')

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    # Prefer explicit APP_HOST, otherwise derive from APP_PUBLIC_BASE_URL, else 0.0.0.0
    host = os.environ.get('APP_HOST')
    if not host:
        base = os.environ.get('APP_PUBLIC_BASE_URL')
        if base:
            try:
                import urllib.parse as _urlparse
                _p = _urlparse.urlparse(base)
                host = _p.hostname or '0.0.0.0'
            except Exception:
                host = '0.0.0.0'
        else:
            host = '0.0.0.0'
    app.run(host=host, debug=True, port=port)
