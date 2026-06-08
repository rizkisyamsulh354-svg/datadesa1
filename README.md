# 🏛️ Sistem Informasi Data Desa Way Ilahan

Website Transparansi Data dan Keuangan Desa Way Ilahan - Kecamatan Pulau Panggung, Kabupaten Tanggamus, Provinsi Lampung

## 📋 Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Penggunaan](#penggunaan)
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

## 💻 Persyaratan Sistem

- Python 3.8+
- Flask 2.3.2+
- SQLAlchemy
- SQLite3
- Browser modern

## 📥 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/datadesa1.git
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