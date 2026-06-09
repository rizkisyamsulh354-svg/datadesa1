# 🚀 Quick Start - Development Local

## Prasyarat
- Python 3.8+
- Git
- Pip

## Setup Awal

### 1. Clone Repository
```bash
git clone https://github.com/rizkisyamsulh354-svg/datadesa1.git
cd datadesa1
```

### 2. Buat Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment
```bash
# Copy .env.example ke .env
cp .env.example .env

# Edit .env jika perlu (opsional, sudah ada default)
```

### 5. Initialize Database
```bash
python run.py
# Database akan dibuat otomatis
# Admin default: username=admin, password=admin123
```

## Menjalankan Aplikasi

### Backend
```bash
# Terminal 1
python run.py
# Akan jalan di http://localhost:5000
```

### Frontend Development
```bash
# Terminal 2 - Simple HTTP Server untuk test GitHub Pages locally
cd docs
python -m http.server 8000
# Buka http://localhost:8000
```

### Keduanya berjalan
- Backend: http://localhost:5000
  - Admin: http://localhost:5000/auth/login
  - API: http://localhost:5000/api/stats
- Frontend: http://localhost:8000

## Development Workflow

### Edit Backend
```bash
# app/routes.py, app/models.py, config.py
# Changes akan di-reload otomatis (DEBUG=True)
```

### Edit Frontend
```bash
# docs/index.html, docs/css/style.css, docs/js/app.js
# Refresh browser untuk melihat changes
```

### Test API Endpoints
```bash
# Gunakan curl atau Postman
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/berita
curl http://localhost:5000/api/penduduk
```

## Database Management

### Reset Database
```bash
# Delete database.db jika ada di instance/
rm instance/datadesa.db

# Re-run untuk create database baru
python run.py
```

### Seed Data (jika ada script)
```bash
python seed.py
```

### Database Admin
```bash
# Flask shell
flask shell

# Di dalam shell:
>>> from app.models import Berita
>>> berita = Berita.query.all()
>>> for b in berita:
...     print(b.judul)
```

## Troubleshooting

### Port 5000 sudah terpakai
```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### ModuleNotFoundError
```bash
# Pastikan venv activated
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Database locked error
```bash
# Kill Flask process dan try again
# Atau delete database dan reset
```

### CORS errors di frontend
- Pastikan backend running di port 5000
- Cek frontend URL di app.js: `const API_BASE_URL = 'http://localhost:5000/api'`

## Deployment

Setelah development selesai:

### Push ke GitHub
```bash
git add .
git commit -m "Update aplikasi"
git push origin main
```

### Deploy ke Production
Lihat `DEPLOYMENT_GUIDE.md`

## Struktur Project

```
datadesa1/
├── app/                 # Backend Flask
│   ├── __init__.py
│   ├── api.py          # API endpoints
│   ├── routes.py       # Web routes
│   ├── models.py       # Database models
│   ├── static/         # Uploads & static files
│   └── templates/      # Jinja2 templates (optional)
├── docs/               # Frontend untuk GitHub Pages
│   ├── index.html      # Main page
│   ├── css/style.css   # Styling
│   └── js/app.js       # JavaScript logic
├── config.py           # Configuration
├── run.py              # Entry point
├── requirements.txt    # Dependencies
└── README.md
```

## Tips & Tricks

### Hot reload backend
```python
# Di run.py
app.run(debug=True, reload=True)
```

### View database
```bash
# Gunakan SQLite Browser
# atau CLI:
sqlite3 instance/datadesa.db
```

### Clear database
```bash
rm instance/datadesa.db
python run.py  # Akan create baru
```

### Test API dengan Postman
- Import `http://localhost:5000/api/*`
- Environment: `{{ base_url }}` = `http://localhost:5000/api`

## Next Steps

1. ✅ Jalankan locally dengan panduan ini
2. 📝 Edit data via admin panel (http://localhost:5000/auth/login)
3. 🧪 Test di frontend (http://localhost:8000)
4. 🚀 Deploy ke GitHub Pages + Render
5. 🎉 Share dengan masyarakat!

---

**Butuh bantuan?** Lihat `DEPLOYMENT_GUIDE.md` atau `RUNNING_INSTRUCTIONS.md`
