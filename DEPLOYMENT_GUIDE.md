# 🚀 Panduan Deployment Aplikasi Desa Way Ilahan

Aplikasi ini terdiri dari **2 bagian terpisah** yang harus di-deploy secara terpisah:

## 📋 Struktur Aplikasi

```
Frontend (GitHub Pages) ← API Calls → Backend (Render/Railway)
   /docs/                              /app/
```

---

## 1️⃣ Frontend - Deploy ke GitHub Pages

### Langkah-langkah:

#### A. Push code ke GitHub
```bash
git add .
git commit -m "Add GitHub Pages support"
git push origin main
```

#### B. Aktifkan GitHub Pages di Repository
1. Buka **Settings** → **Pages**
2. Pilih **Source**: `Deploy from a branch`
3. Branch: `main` | Folder: `/docs`
4. Klik **Save**
5. GitHub akan generate URL seperti: `https://rizkisyamsulh354-svg.github.io/datadesa1/`

#### C. Update API URL
Edit file `docs/js/app.js` baris pertama:

```javascript
// Ubah dari ini:
const API_BASE_URL = 'http://localhost:5000/api';

// Menjadi URL backend Anda:
const API_BASE_URL = 'https://your-backend-url.com/api';
```

---

## 2️⃣ Backend - Deploy ke Render (Rekomendasi)

### Persiapan:

#### A. Install Render CLI (Optional)
```bash
npm install -g @render-com/cli
```

#### B. Buat `render.yaml`
```yaml
services:
  - type: web
    name: datadesa-backend
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: datadesa
          property: connectionString
    databases:
      - name: datadesa
        databaseName: datadesa_db
        user: datadesa_user

```

#### C. Login ke Render
```bash
# Buka https://render.com dan login
# Atau gunakan CLI:
render login
```

#### D. Deploy Project
1. Buka **Render Dashboard**: https://dashboard.render.com
2. Klik **+ New** → **Web Service**
3. Pilih **GitHub** atau upload repository
4. Isi form:
   - **Name**: `datadesa-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free

5. Klik **Create Web Service**
6. Tunggu deployment selesai (~5 menit)
7. Copy URL backend yang di-generate (contoh: `https://datadesa-backend.onrender.com`)

#### E. Setup Database (Render)
1. Di Render Dashboard → **Databases** → **+ New** → **PostgreSQL**
2. Database Name: `datadesa_db`
3. User: `datadesa_user`
4. Region: pilih yang terdekat
5. Copy connection string dan update di environment variables backend

---

## 3️⃣ Update Konfigurasi

### A. Update `config.py`
```python
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-datadesa-way-ilahan'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'doc', 'docx', 'xls', 'xlsx'}
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_REFRESH_EACH_REQUEST = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Untuk Render, gunakan PostgreSQL jika di-setup
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///datadesa.db'

# ... rest of config
```

### B. Update Render Environment Variables
Di Render Dashboard → Web Service → Environment:

```
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key-here
DATABASE_URL=postgresql://user:password@host/database (jika menggunakan PostgreSQL)
```

---

## 4️⃣ Setup CORS di Frontend

File `docs/js/app.js` sudah menggunakan CORS yang tepat. Backend sudah di-setup dengan:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## 5️⃣ Testing Deployment

### Cek Frontend
```bash
# Buka di browser:
https://rizkisyamsulh354-svg.github.io/datadesa1/
```

### Cek Backend
```bash
# Test API endpoint:
curl https://your-backend-url.com/api/stats

# Harusnya return JSON
```

### Debug CORS Issues
Jika ada error CORS di console, pastikan:
1. Backend API URL benar di `docs/js/app.js`
2. Backend punya `Flask-CORS` installed
3. Backend punya route `/api/` dengan CORS enabled

---

## 6️⃣ Maintenance & Updates

### Update Frontend
```bash
# Edit di docs/
# Commit & push
git add docs/
git commit -m "Update frontend"
git push origin main
# GitHub Pages otomatis update dalam beberapa detik
```

### Update Backend
```bash
# Edit di app/
# Push ke GitHub
git add app/
git commit -m "Update backend"
git push origin main
# Render akan otomatis rebuild & redeploy
```

---

## 7️⃣ Troubleshooting

### Frontend tidak load
- Check GitHub Pages settings aktif
- Check `/docs` folder exist
- Clear browser cache

### API tidak bisa connect
- Check backend URL benar di `app.js`
- Check backend status di Render dashboard
- Check CORS enabled di backend

### Database connection error
- Check DATABASE_URL environment variable
- Check database server running
- Test connection dengan psql/CLI

### File uploads tidak muncul
- Setup file storage (Render free tier tidak support persistent storage)
- Gunakan cloud storage seperti **AWS S3** atau **Google Cloud Storage**
- Atau gunakan paid Render plan untuk persistent storage

---

## 8️⃣ Alternatif Hosting Backend

### Jika Render tidak sesuai, coba:

**Railway** (Rekomendasi)
- https://railway.app
- 1000 free credits/bulan
- Lebih stabil untuk database

**Fly.io**
- https://fly.io
- Free tier untuk 1 shared-cpu app

**Vercel** (untuk Serverless)
- https://vercel.com
- Deploy Flask dengan serverless functions
- Butuh restructure code ke serverless format

**Heroku** (Berbayar, sudah tidak free)
- https://heroku.com
- $7/bulan minimum

---

## 🔒 Security Checklist

- [ ] Change default admin password (admin123)
- [ ] Set strong SECRET_KEY di environment
- [ ] Enable HTTPS (automatic pada Render/GitHub Pages)
- [ ] Setup environment variables (jangan hardcode credentials)
- [ ] Limit file upload size
- [ ] Add rate limiting untuk API
- [ ] Setup SSL certificate (automatic)
- [ ] Regular database backups

---

## 📞 Support

Jika ada pertanyaan:
- GitHub Issues
- Email: admin@desa-way-ilahan.local
- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com

---

## ✅ Deployment Checklist

Frontend (GitHub Pages):
- [ ] Push code ke GitHub
- [ ] Aktifkan GitHub Pages
- [ ] Update API URL di app.js
- [ ] Test di browser
- [ ] Set custom domain (optional)

Backend (Render):
- [ ] Create Render account
- [ ] Create Web Service
- [ ] Setup database (optional)
- [ ] Set environment variables
- [ ] Copy API URL
- [ ] Test API endpoints

Final:
- [ ] Update frontend dengan backend URL
- [ ] Test full application flow
- [ ] Monitor Render dashboard
- [ ] Setup monitoring alerts

---

**Last Updated**: 2024
**Status**: ✅ Ready for production
