# 🏛️ Sistem Informasi Data Desa Way Ilahan

Website Transparansi Data dan Keuangan Desa Way Ilahan - Kecamatan Pulau Panggung, Kabupaten Tanggamus, Provinsi Lampung

🌐 **Live Demo**: https://rizkisyamsulh354-svg.github.io/datadesa1/

## 📋 Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Arsitektur](#arsitektur)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Struktur Proyek](#struktur-proyek)

## ✨ Fitur Utama

### Fitur Publik
- 📄 **Halaman Beranda** - Dashboard dengan informasi desa terkini
- 👥 **Profil Desa** - Informasi lengkap tentang desa
- 📰 **Berita Desa** - Publikasi berita dan informasi terbaru
- 🖼️ **Galeri Kegiatan** - Upload dan tampilkan foto/video kegiatan
- 📁 **Dokumen Publik** - Distribusi dokumen resmi
- 👨‍👩‍👧‍👦 **Data Penduduk** - Informasi demografi masyarakat
- 💰 **APB Desa** - Transparansi anggaran dan realisasi keuangan
- 💬 **Kotak Pengaduan** - Sarana aspirasi masyarakat

### Fitur Admin
- 🔐 **Sistem Login** - Autentikasi admin
- 📊 **Dashboard** - Overview statistik
- ✏️ **Kelola Berita** - Buat, edit, hapus berita
- 🎨 **Kelola Galeri** - Manajemen upload foto dan video
- 📄 **Kelola Dokumen** - Publikasi dokumen resmi
- 📢 **Respon Pengaduan** - Kelola pengaduan masyarakat
- 👥 **Kelola Data Penduduk** - CRUD data kependudukan
- 💼 **Kelola Aparatur** - Data pejabat desa
- 📈 **Kelola APB** - Input anggaran dan realisasi
- ⚙️ **Pengaturan Lengkap** - Edit profil, password, dan account

## 🏗️ Arsitektur

Aplikasi ini menggunakan **arsitektur microservices** yang modern:

```
┌─────────────────────────────────────┐
│   GitHub Pages (Frontend)           │
│   - Static HTML/CSS/JS              │
│   - URL: *.github.io/datadesa1      │
│   - Folder: /docs                   │
└────────────┬────────────────────────┘
             │ CORS API Calls
             ↓
┌─────────────────────────────────────┐
│   Backend API (Flask)               │
│   - REST API Endpoints              │
│   - Database Management             │
│   - Admin Panel                     │
│   - Deployed: Render / Railway      │
└─────────────────────────────────────┘
```

**Keuntungan Arsitektur ini:**
✅ Frontend static → CDN friendly, fast loading  
✅ Backend terpisah → scalable, mudah di-maintain  
✅ Deployment mudah → GitHub Pages free, backend di Render free  
✅ CORS enabled → secure cross-origin requests  
✅ API-first → mudah di-extend atau integrate dengan aplikasi lain  

## 🚀 Quick Start

### Development Lokal
```bash
# 1. Setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# 2. Jalankan Backend
python run.py              # Port 5000

# 3. Jalankan Frontend (Terminal baru)
cd docs
python -m http.server 8000  # Port 8000

# 4. Buka di browser
# Frontend: http://localhost:8000
# Admin:    http://localhost:5000/auth/login
```

Lihat **[QUICKSTART.md](QUICKSTART.md)** untuk detail lebih lengkap.

## 🌐 Deployment

### Frontend → GitHub Pages
```bash
# Otomatis via GitHub Actions
# Folder /docs di-deploy sebagai static site
```

> Frontend statis ini sudah dapat dijalankan sepenuhnya tanpa Python atau backend.

### Backend → Render (opsional)
1. Buat account di [render.com](https://render.com)
2. Connect GitHub repository
3. Deploy Web Service dengan `render.yaml`
4. Copy API URL dari Render
5. Update di `docs/js/app.js`

> Jika kamu hanya ingin website statis di GitHub Pages, bagian backend tidak wajib.

Lihat **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** untuk panduan lengkap.

## 💻 Persyaratan Sistem

- Python 3.8+
- Flask 2.3.2+
- SQLAlchemy
- Flask-CORS
- Gunicorn (untuk production)
- Browser modern (Chrome, Firefox, Safari, Edge)

## 📥 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/rizkisyamsulh354-svg/datadesa1.git
cd datadesa1
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
```bash
python run.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## ⚙️ Konfigurasi

### Akun Default
- **Username**: admin
- **Password**: admin123
- ⚠️ Ubah password setelah login pertama!

## 🚀 Penggunaan

### Akses Website
- **Halaman Publik**: http://localhost:5000/
- **Admin Login**: http://localhost:5000/auth/login

## 🔐 Keamanan

- ✅ Password hashing
- ✅ Session management
- ✅ CSRF protection
- ✅ SQL Injection prevention
- ✅ File upload validation
- ✅ Role-based access control

## 📁 Struktur Proyek

```
datadesa1/
├── app/
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   ├── models.py            # Database models
│   ├── routes.py            # API routes
│   └── __init__.py          # App initialization
├── config.py                # Configuration
├── run.py                   # Main entry point
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

---

**Versi**: 1.0.0  
**Status**: Active Development