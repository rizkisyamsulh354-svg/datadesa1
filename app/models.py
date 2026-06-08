from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    """Admin user model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Berita(db.Model):
    """Village news model"""
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    konten = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    thumbnail = db.Column(db.String(255))
    penulis = db.Column(db.String(120), nullable=False)
    tanggal_publikasi = db.Column(db.DateTime, default=datetime.utcnow)
    dibuat_pada = db.Column(db.DateTime, default=datetime.utcnow)
    diupdate_pada = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Berita {self.judul}>'

class Galeri(db.Model):
    """Gallery model for photos and videos"""
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.Text)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # photo, video
    kategori = db.Column(db.String(100), default='Kegiatan Desa')
    tanggal_upload = db.Column(db.DateTime, default=datetime.utcnow)
    uploader = db.Column(db.String(120))
    
    def __repr__(self):
        return f'<Galeri {self.judul}>'

class DokumenPublik(db.Model):
    """Public documents model"""
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.Text)
    file_path = db.Column(db.String(255), nullable=False)
    jenis_dokumen = db.Column(db.String(100))  # Berita Acara, SK, Laporan, etc
    tanggal_upload = db.Column(db.DateTime, default=datetime.utcnow)
    diupdate_pada = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    uploader = db.Column(db.String(120))
    
    def __repr__(self):
        return f'<DokumenPublik {self.judul}>'

class Pengaduan(db.Model):
    """Public complaint model"""
    id = db.Column(db.Integer, primary_key=True)
    nama_pelapor = db.Column(db.String(120), nullable=False)
    email_pelapor = db.Column(db.String(120), nullable=False)
    nomor_hp = db.Column(db.String(20))
    kategori = db.Column(db.String(100))  # Pengaduan, Saran, Pertanyaan
    subjek = db.Column(db.String(255), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Baru')  # Baru, Diproses, Ditanggapi, Selesai
    tanggal_dibuat = db.Column(db.DateTime, default=datetime.utcnow)
    tanggal_direspon = db.Column(db.DateTime)
    respon_admin = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Pengaduan {self.subjek}>'

class DataPenduduk(db.Model):
    """Population data model"""
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16), unique=True, nullable=False)
    nama = db.Column(db.String(120), nullable=False)
    tempat_lahir = db.Column(db.String(100))
    tanggal_lahir = db.Column(db.Date)
    jenis_kelamin = db.Column(db.String(20))
    agama = db.Column(db.String(50))
    status_perkawinan = db.Column(db.String(50))
    pendidikan = db.Column(db.String(100))
    pekerjaan = db.Column(db.String(100))
    alamat = db.Column(db.Text)
    dusun = db.Column(db.String(50))
    rw = db.Column(db.String(10))
    rt = db.Column(db.String(10))
    
    def __repr__(self):
        return f'<DataPenduduk {self.nama}>'

class ApbDes(db.Model):
    """Village Budget model"""
    id = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.Integer, nullable=False)
    kategori = db.Column(db.String(100), nullable=False)
    sub_kategori = db.Column(db.String(100))
    uraian = db.Column(db.Text)
    anggaran = db.Column(db.Float, nullable=False)
    realisasi = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='Anggaran')  # Anggaran, Realisasi
    tanggal_dibuat = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ApbDes {self.tahun}-{self.kategori}>'

class AparaturDesa(db.Model):
    """Village officials/apparatus model"""
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    jabatan = db.Column(db.String(100), nullable=False)
    nomor_identitas = db.Column(db.String(50))
    alamat = db.Column(db.Text)
    nomor_hp = db.Column(db.String(20))
    email = db.Column(db.String(120))
    foto = db.Column(db.String(255))
    tanggal_mulai_jabatan = db.Column(db.Date)
    keterangan = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AparaturDesa {self.nama}-{self.jabatan}>'

class ProfilDesa(db.Model):
    """Village profile information"""
    id = db.Column(db.Integer, primary_key=True)
    nama_desa = db.Column(db.String(120), nullable=False)
    kecamatan = db.Column(db.String(100), nullable=False)
    kabupaten = db.Column(db.String(100), nullable=False)
    provinsi = db.Column(db.String(100), nullable=False)
    luas_desa = db.Column(db.Float)
    jumlah_penduduk = db.Column(db.Integer)
    juml_keluarga = db.Column(db.Integer)
    visi = db.Column(db.Text)
    misi = db.Column(db.Text)
    sejarah_desa = db.Column(db.Text)
    logo = db.Column(db.String(255))
    kontak_kantor = db.Column(db.String(20))
    email_desa = db.Column(db.String(120))
    alamat_kantor = db.Column(db.Text)
    diupdate_pada = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProfilDesa {self.nama_desa}>'

class ActivityLog(db.Model):
    """Admin activity log model"""
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    aktivitas = db.Column(db.String(255), nullable=False)
    modul = db.Column(db.String(100))
    deskripsi = db.Column(db.Text)
    tanggal_aktivitas = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActivityLog {self.aktivitas}>'
