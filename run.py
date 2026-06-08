from app import create_app, db
from app.models import Admin
import os

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Create initial admin if doesn't exist
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Admin': Admin}

# Create initial admin account
with app.app_context():
    db.create_all()
    
    # Check if admin already exists
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(
            username='admin',
            email='admin@desa-way-ilahan.local',
            full_name='Administrator',
            is_active=True
        )
        admin.set_password('admin123')  # Change this password after login
        db.session.add(admin)
        db.session.commit()
        print("Admin default account created: username=admin, password=admin123")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
