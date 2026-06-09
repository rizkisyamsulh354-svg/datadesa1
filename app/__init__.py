from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import config
from app.models import db, Admin

login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Enable CORS for GitHub Pages
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu.'
    
    # Create upload folder if not exists
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'gallery'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
    
    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import public_bp, admin_bp, auth_bp
    from app.api import api_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Halaman tidak ditemukan'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Terjadi kesalahan pada server'}, 500
    
    # Shell context processor
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Admin': Admin}
    
    return app
