# 🚀 Panduan Menjalankan Aplikasi Desa Way Ilahan

## Langkah 1: Persiapan

Pastikan Anda sudah berada di direktori proyek:
```bash
cd /workspaces/datadesa1
```

## Langkah 2: Jalankan Aplikasi

### Opsi 1: Jalankan Langsung
```bash
python run.py
```

Aplikasi akan berjalan di:
- 🌐 http://localhost:5000 (lokal)
- 🌐 http://0.0.0.0:5000 (akses jaringan)

Output yang akan muncul:
```
Admin default account created: username=admin, password=admin123
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Opsi 2: Jalankan dengan Port Berbeda
```bash
python run.py --port 8000
```

## Langkah 3: Akses Aplikasi

### Halaman Publik
Buka browser dan akses:
```
http://localhost:5000
```

Anda akan melihat:
- ✅ Homepage dengan statistik desa
- ✅ Menu navigasi: Beranda, Profil Desa, Berita, Galeri, Dokumen, Pengaduan
- ✅ Informasi Desa Way Ilahan

### Login Admin
Klik **Admin** di navbar atau akses:
```
http://localhost:5000/auth/login
```

Masukkan kredensial:
- **Username**: admin
- **Password**: admin123

## Langkah 4: Fitur-Fitur Utama

### Dashboard Admin
Setelah login, Anda akan melihat dashboard dengan:
- 📊 Statistik jumlah berita, pengaduan, penduduk
- 📝 Daftar berita terbaru
- 💬 Pengaduan baru
- ⚡ Menu akses cepat

### Menu Utama Admin

#### 1. **Profil Desa**
- Edit nama desa, kecamatan, kabupaten, provinsi
- Ubah visi, misi, sejarah desa
- Upload logo desa
- Update kontak kantor

#### 2. **Berita**
- 📝 Lihat daftar semua berita
- ➕ Tambah berita baru
  - Isi judul, konten (dengan editor WYSIWYG)
  - Upload thumbnail
  - Pilih status publikasi
- ✏️ Edit berita
- 🗑️ Hapus berita

#### 3. **Galeri**
- 🖼️ Lihat semua foto dan video
- ➕ Upload file baru
  - Tipe: Foto atau Video
  - Kategori: Dokumentasi, Kegiatan, Infrastruktur, dll
  - Deskripsi dan judul
- 🗑️ Hapus file

#### 4. **Dokumen Publik**
- 📄 Lihat semua dokumen
- ➕ Upload dokumen
  - Jenis: PDF, DOC, Excel, dll
  - Deskripsi
  - File maksimal 50MB
- ⬇️ Download dokumen
- 🗑️ Hapus dokumen

#### 5. **Pengaduan**
- 💬 Lihat semua pengaduan masyarakat
- 🔍 Filter berdasarkan status: Baru, Diproses, Ditanggapi, Selesai
- 📖 Lihat detail pengaduan
- 💌 Tulis respons untuk pengaduan
- ✅ Ubah status pengaduan

#### 6. **Data Penduduk**
- 👥 Lihat daftar penduduk
- 🔍 Filter berdasarkan dusun
- ➕ Tambah penduduk baru
  - NIK, nama, tempat/tanggal lahir
  - Jenis kelamin, agama, status perkawinan
  - Pendidikan, pekerjaan
  - Alamat lengkap
- ✏️ Edit data penduduk
- 🗑️ Hapus data penduduk

#### 7. **APB Desa**
- 💰 Lihat anggaran dan realisasi
- 📊 Filter berdasarkan tahun
- ➕ Tambah anggaran baru
  - Kategori: Operasional, Pembangunan, Pemberdayaan
  - Sub kategori dan uraian
  - Jumlah anggaran dan realisasi
- ✏️ Edit anggaran
- 🗑️ Hapus anggaran

#### 8. **Aparatur Desa**
- 👔 Lihat daftar pejabat desa
- ➕ Tambah pejabat
  - Nama, jabatan, nomor identitas
  - Kontak (HP, email)
  - Upload foto
  - Tanggal mulai jabatan
- ✏️ Edit data pejabat
- 🗑️ Hapus pejabat

#### 9. **Pengaturan Akun**
- 🔑 Ubah password
- 👤 Update nama dan email
- ⚙️ Konfigurasi akun pribadi

#### 10. **Kelola Pengguna** (Admin)
- 👨‍💼 Lihat daftar semua admin
- ➕ Tambah admin baru
- ✏️ Edit admin
- 🗑️ Hapus admin

## Langkah 5: Fitur-Fitur Publik

### Halaman Beranda
- Informasi statistik desa
- Profil singkat desa
- Berita terbaru (6 berita)
- Tombol akses cepat ke menu

### Profil Desa
- Logo dan nama desa
- Lokasi geografis
- Visi dan misi
- Sejarah desa
- Daftar aparatur dengan foto

### Berita
- Daftar semua berita
- Pencarian dan filter
- Pagination (10 berita per halaman)

### Detail Berita
- Artikel lengkap
- Tanggal publikasi
- Penulis
- Jumlah views
- Berita terkait

### Galeri
- Grid foto dan video
- Filter kategori
- Pagination (12 item per halaman)
- Modal viewer untuk preview

### Dokumen Publik
- Tabel dokumen
- Filter berdasarkan jenis
- Tombol download
- Informasi tanggal upload

### Data Penduduk
- Tabel informasi penduduk
- Filter berdasarkan dusun
- Pagination (20 baris per halaman)

### APB Desa
- Tabel anggaran
- Tabel realisasi
- Filter berdasarkan tahun
- Ringkasan total

### Pengaduan
- Form pengaduan publik
- Input: nama, email, HP
- Kategori pengaduan
- Subjek dan isi pengaduan
- Tombol kirim

## Langkah 6: Troubleshooting

### Aplikasi tidak berjalan
```bash
# Pastikan Python 3.8+
python --version

# Install dependencies lagi
pip install -r requirements.txt

# Hapus database dan buat ulang
rm datadesa.db
python run.py
```

### Port sudah digunakan
```bash
# Gunakan port berbeda
python run.py --port 8000

# Atau cari proses yang menggunakan port 5000
lsof -i :5000
```

### Database error
```bash
# Reset database
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.drop_all()
>>>     db.create_all()
>>> exit()

# Atau jalankan seed lagi
python seed.py
```

### Lupa password admin
1. Edit file `app/models.py` dan cari class `Admin`
2. Jalankan:
```python
python
>>> from app import create_app, db
>>> from app.models import Admin
>>> from werkzeug.security import generate_password_hash
>>> app = create_app()
>>> with app.app_context():
>>>     admin = Admin.query.filter_by(username='admin').first()
>>>     admin.password_hash = generate_password_hash('newpassword123')
>>>     db.session.commit()
>>> exit()
```

## Langkah 7: Hentikan Aplikasi

Tekan **CTRL+C** di terminal untuk menghentikan aplikasi.

## 💡 Tips & Trik

1. **Auto-reload**: Aplikasi otomatis reload ketika file berubah (debug mode)
2. **Database Auto-create**: Database otomatis dibuat di path `datadesa.db`
3. **Upload Folder Auto-create**: Folder uploads otomatis dibuat
4. **Rich Text Editor**: Gunakan TinyMCE untuk menulis berita dengan formatting
5. **CSV Export**: Bisa export data ke CSV dari beberapa halaman
6. **Responsive Design**: Aplikasi responsive untuk mobile, tablet, desktop

## 🔐 Keamanan

- ⚠️ Ubah password default setelah login pertama
- ⚠️ Jangan bagikan akses admin ke orang tidak berwenang
- ⚠️ Backup database secara berkala: `cp datadesa.db datadesa_backup.db`
- ⚠️ Di production, ubah SECRET_KEY di config.py

## 📚 Dokumentasi Lengkap

Lihat `README.md` untuk dokumentasi lengkap.

## ❓ FAQ

**Q: Bisakah saya mengubah port?**
A: Ya, jalankan `python run.py --port 8000`

**Q: Bagaimana cara backup database?**
A: Copy file `datadesa.db` ke lokasi aman

**Q: Bisakah saya menambah admin lain?**
A: Ya, di halaman admin dashboard klik "Kelola Pengguna"

**Q: Berapa ukuran maksimal file upload?**
A: 50MB per file

**Q: Apakah perlu koneksi internet?**
A: Tidak, berjalan offline. TinyMCE CDN memerlukan internet.

---

**Happy Coding! 🎉**

Untuk bantuan lebih lanjut, lihat log aplikasi di terminal.
