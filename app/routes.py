from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app.models import (
    db, Admin, Berita, Galeri, DokumenPublik, Pengaduan, DataPenduduk, 
    ApbDes, AparaturDesa, ProfilDesa, ActivityLog
)

# Create blueprints
public_bp = Blueprint('public', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def log_activity(admin_id, aktivitas, modul, deskripsi=''):
    """Log admin activity"""
    log = ActivityLog(
        admin_id=admin_id,
        aktivitas=aktivitas,
        modul=modul,
        deskripsi=deskripsi
    )
    db.session.add(log)
    db.session.commit()

# ============= AUTH ROUTES =============
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            admin.last_login = datetime.utcnow()
            db.session.commit()
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Username atau password salah', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda berhasil logout', 'success')
    return redirect(url_for('public.index'))

# ============= PUBLIC ROUTES =============

@public_bp.route('/')
def index():
    profil = ProfilDesa.query.first()
    berita_terbaru = Berita.query.filter_by(is_published=True).order_by(Berita.tanggal_publikasi.desc()).limit(6).all()
    total_penduduk = db.session.query(db.func.count(DataPenduduk.id)).scalar()
    
    return render_template('public/index.html', 
                         profil=profil, 
                         berita_terbaru=berita_terbaru,
                         total_penduduk=total_penduduk)

@public_bp.route('/profil-desa')
def profil_desa():
    profil = ProfilDesa.query.first()
    aparatur = AparaturDesa.query.all()
    return render_template('public/profil_desa.html', profil=profil, aparatur=aparatur)

@public_bp.route('/berita')
def berita():
    page = request.args.get('page', 1, type=int)
    berita = Berita.query.filter_by(is_published=True).order_by(
        Berita.tanggal_publikasi.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('public/berita.html', berita=berita)

@public_bp.route('/berita/<string:slug>')
def detail_berita(slug):
    berita = Berita.query.filter_by(slug=slug).first_or_404()
    berita.views += 1
    db.session.commit()
    
    berita_terkait = Berita.query.filter_by(is_published=True).filter(
        Berita.id != berita.id
    ).order_by(Berita.tanggal_publikasi.desc()).limit(3).all()
    
    return render_template('public/detail_berita.html', berita=berita, berita_terkait=berita_terkait)

@public_bp.route('/galeri')
def galeri():
    page = request.args.get('page', 1, type=int)
    kategori = request.args.get('kategori', '')
    
    query = Galeri.query
    if kategori:
        query = query.filter_by(kategori=kategori)
    
    galeri = query.order_by(Galeri.tanggal_upload.desc()).paginate(page=page, per_page=12)
    
    kategori_list = db.session.query(Galeri.kategori).distinct().all()
    kategori_list = [k[0] for k in kategori_list if k[0]]
    
    return render_template('public/galeri.html', galeri=galeri, kategori_list=kategori_list)

@public_bp.route('/dokumen-publik')
def dokumen_publik():
    page = request.args.get('page', 1, type=int)
    jenis = request.args.get('jenis', '')
    
    query = DokumenPublik.query
    if jenis:
        query = query.filter_by(jenis_dokumen=jenis)
    
    dokumen = query.order_by(DokumenPublik.tanggal_upload.desc()).paginate(page=page, per_page=10)
    
    jenis_list = db.session.query(DokumenPublik.jenis_dokumen).distinct().all()
    jenis_list = [j[0] for j in jenis_list if j[0]]
    
    return render_template('public/dokumen_publik.html', dokumen=dokumen, jenis_list=jenis_list)

@public_bp.route('/apb-desa')
def apb_desa():
    tahun = request.args.get('tahun', datetime.now().year, type=int)
    
    tahun_list = db.session.query(ApbDes.tahun).distinct().order_by(ApbDes.tahun.desc()).all()
    tahun_list = [t[0] for t in tahun_list]
    
    anggaran = ApbDes.query.filter_by(tahun=tahun, status='Anggaran').all()
    realisasi = ApbDes.query.filter_by(tahun=tahun, status='Realisasi').all()
    
    total_anggaran = sum(a.anggaran for a in anggaran)
    total_realisasi = sum(r.realisasi for r in realisasi)
    
    return render_template('public/apb_desa.html',
                         anggaran=anggaran,
                         realisasi=realisasi,
                         tahun=tahun,
                         tahun_list=tahun_list,
                         total_anggaran=total_anggaran,
                         total_realisasi=total_realisasi)

@public_bp.route('/data-penduduk')
def data_penduduk():
    page = request.args.get('page', 1, type=int)
    dusun = request.args.get('dusun', '')
    
    query = DataPenduduk.query
    if dusun:
        query = query.filter_by(dusun=dusun)
    
    data = query.order_by(DataPenduduk.nama).paginate(page=page, per_page=20)
    
    dusun_list = db.session.query(DataPenduduk.dusun).distinct().all()
    dusun_list = [d[0] for d in dusun_list if d[0]]
    
    return render_template('public/data_penduduk.html', data=data, dusun_list=dusun_list)

@public_bp.route('/pengaduan', methods=['GET', 'POST'])
def pengaduan():
    if request.method == 'POST':
        try:
            pengaduan = Pengaduan(
                nama_pelapor=request.form.get('nama'),
                email_pelapor=request.form.get('email'),
                nomor_hp=request.form.get('nomor_hp'),
                kategori=request.form.get('kategori'),
                subjek=request.form.get('subjek'),
                isi=request.form.get('isi'),
                status='Baru'
            )
            db.session.add(pengaduan)
            db.session.commit()
            flash('Pengaduan Anda berhasil dikirim. Terima kasih!', 'success')
            return redirect(url_for('public.pengaduan'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('public/pengaduan.html')

# ============= ADMIN ROUTES =============

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_berita = Berita.query.count()
    total_pengaduan = Pengaduan.query.count()
    total_penduduk = DataPenduduk.query.count()
    
    pengaduan_baru = Pengaduan.query.filter_by(status='Baru').count()
    berita_terbaru = Berita.query.order_by(Berita.tanggal_publikasi.desc()).limit(5).all()
    pengaduan_terbaru = Pengaduan.query.order_by(Pengaduan.tanggal_dibuat.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_berita=total_berita,
                         total_pengaduan=total_pengaduan,
                         total_penduduk=total_penduduk,
                         pengaduan_baru=pengaduan_baru,
                         berita_terbaru=berita_terbaru,
                         pengaduan_terbaru=pengaduan_terbaru)

# ============ ADMIN BERITA ROUTES =============

@admin_bp.route('/berita')
@login_required
def kelola_berita():
    page = request.args.get('page', 1, type=int)
    berita = Berita.query.order_by(Berita.tanggal_publikasi.desc()).paginate(page=page, per_page=10)
    return render_template('admin/berita/list.html', berita=berita)

@admin_bp.route('/berita/tambah', methods=['GET', 'POST'])
@login_required
def tambah_berita():
    if request.method == 'POST':
        try:
            judul = request.form.get('judul')
            slug = request.form.get('judul').lower().replace(' ', '-')
            
            # Check if slug exists
            existing = Berita.query.filter_by(slug=slug).first()
            if existing:
                slug = f"{slug}-{datetime.now().timestamp()}"
            
            berita = Berita(
                judul=judul,
                konten=request.form.get('konten'),
                slug=slug,
                penulis=current_user.full_name,
                is_published=request.form.get('is_published') == 'on'
            )
            
            # Handle thumbnail upload
            if 'thumbnail' in request.files:
                file = request.files['thumbnail']
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"berita_{datetime.now().timestamp()}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    berita.thumbnail = filename
            
            db.session.add(berita)
            db.session.commit()
            
            log_activity(current_user.id, 'Tambah Berita', 'Berita', f'Judul: {judul}')
            flash('Berita berhasil ditambahkan', 'success')
            return redirect(url_for('admin.kelola_berita'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/berita/form.html', action='Tambah')

@admin_bp.route('/berita/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_berita(id):
    berita = Berita.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            berita.judul = request.form.get('judul')
            berita.konten = request.form.get('konten')
            berita.is_published = request.form.get('is_published') == 'on'
            berita.diupdate_pada = datetime.utcnow()
            
            # Handle thumbnail upload
            if 'thumbnail' in request.files:
                file = request.files['thumbnail']
                if file and allowed_file(file.filename):
                    # Delete old file
                    if berita.thumbnail:
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], berita.thumbnail)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    filename = secure_filename(f"berita_{datetime.now().timestamp()}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    berita.thumbnail = filename
            
            db.session.commit()
            
            log_activity(current_user.id, 'Edit Berita', 'Berita', f'Judul: {berita.judul}')
            flash('Berita berhasil diupdate', 'success')
            return redirect(url_for('admin.kelola_berita'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/berita/form.html', berita=berita, action='Edit')

@admin_bp.route('/berita/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_berita(id):
    berita = Berita.query.get_or_404(id)
    try:
        # Delete thumbnail
        if berita.thumbnail:
            old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], berita.thumbnail)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        db.session.delete(berita)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus Berita', 'Berita', f'Judul: {berita.judul}')
        flash('Berita berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_berita'))

# ============ ADMIN GALERI ROUTES =============

@admin_bp.route('/galeri')
@login_required
def kelola_galeri():
    page = request.args.get('page', 1, type=int)
    galeri = Galeri.query.order_by(Galeri.tanggal_upload.desc()).paginate(page=page, per_page=12)
    return render_template('admin/galeri/list.html', galeri=galeri)

@admin_bp.route('/galeri/tambah', methods=['GET', 'POST'])
@login_required
def tambah_galeri():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(f"galeri_{datetime.now().timestamp()}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'gallery', filename)
                file.save(filepath)
                
                ext = filename.rsplit('.', 1)[1].lower()
                file_type = 'video' if ext in ['mp4', 'avi', 'mov'] else 'photo'
                
                galeri = Galeri(
                    judul=request.form.get('judul'),
                    deskripsi=request.form.get('deskripsi'),
                    file_path=filename,
                    file_type=file_type,
                    kategori=request.form.get('kategori', 'Kegiatan Desa'),
                    uploader=current_user.full_name
                )
                
                db.session.add(galeri)
                db.session.commit()
                
                log_activity(current_user.id, 'Upload Galeri', 'Galeri', f'File: {filename}')
                flash('File galeri berhasil diupload', 'success')
                return redirect(url_for('admin.kelola_galeri'))
            else:
                flash('Format file tidak didukung', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/galeri/form.html')

@admin_bp.route('/galeri/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_galeri(id):
    galeri = Galeri.query.get_or_404(id)
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'gallery', galeri.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.session.delete(galeri)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus Galeri', 'Galeri', f'File: {galeri.file_path}')
        flash('File galeri berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_galeri'))

# ============ ADMIN DOKUMEN PUBLIK ROUTES =============

@admin_bp.route('/dokumen')
@login_required
def kelola_dokumen():
    page = request.args.get('page', 1, type=int)
    dokumen = DokumenPublik.query.order_by(DokumenPublik.tanggal_upload.desc()).paginate(page=page, per_page=10)
    return render_template('admin/dokumen/list.html', dokumen=dokumen)

@admin_bp.route('/dokumen/tambah', methods=['GET', 'POST'])
@login_required
def tambah_dokumen():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(f"dokumen_{datetime.now().timestamp()}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'documents', filename)
                file.save(filepath)
                
                dokumen = DokumenPublik(
                    judul=request.form.get('judul'),
                    deskripsi=request.form.get('deskripsi'),
                    file_path=filename,
                    jenis_dokumen=request.form.get('jenis_dokumen'),
                    uploader=current_user.full_name
                )
                
                db.session.add(dokumen)
                db.session.commit()
                
                log_activity(current_user.id, 'Upload Dokumen', 'Dokumen', f'File: {filename}')
                flash('Dokumen berhasil diupload', 'success')
                return redirect(url_for('admin.kelola_dokumen'))
            else:
                flash('Format file tidak didukung', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/dokumen/form.html')

@admin_bp.route('/dokumen/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_dokumen(id):
    dokumen = DokumenPublik.query.get_or_404(id)
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'documents', dokumen.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.session.delete(dokumen)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus Dokumen', 'Dokumen', f'File: {dokumen.file_path}')
        flash('Dokumen berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_dokumen'))

# ============ ADMIN PENGADUAN ROUTES =============

@admin_bp.route('/pengaduan')
@login_required
def kelola_pengaduan():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Pengaduan.query
    if status:
        query = query.filter_by(status=status)
    
    pengaduan = query.order_by(Pengaduan.tanggal_dibuat.desc()).paginate(page=page, per_page=10)
    
    return render_template('admin/pengaduan/list.html', pengaduan=pengaduan, filter_status=status)

@admin_bp.route('/pengaduan/<int:id>', methods=['GET', 'POST'])
@login_required
def detail_pengaduan(id):
    pengaduan = Pengaduan.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            pengaduan.status = request.form.get('status')
            pengaduan.respon_admin = request.form.get('respon')
            pengaduan.tanggal_direspon = datetime.utcnow()
            
            db.session.commit()
            
            log_activity(current_user.id, 'Respon Pengaduan', 'Pengaduan', f'Subjek: {pengaduan.subjek}')
            flash('Respon pengaduan berhasil disimpan', 'success')
            return redirect(url_for('admin.kelola_pengaduan'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/pengaduan/detail.html', pengaduan=pengaduan)

@admin_bp.route('/pengaduan/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_pengaduan(id):
    pengaduan = Pengaduan.query.get_or_404(id)
    try:
        db.session.delete(pengaduan)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus Pengaduan', 'Pengaduan', f'Subjek: {pengaduan.subjek}')
        flash('Pengaduan berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_pengaduan'))

# ============ ADMIN DATA PENDUDUK ROUTES =============

@admin_bp.route('/penduduk')
@login_required
def kelola_penduduk():
    page = request.args.get('page', 1, type=int)
    dusun = request.args.get('dusun', '')
    
    query = DataPenduduk.query
    if dusun:
        query = query.filter_by(dusun=dusun)
    
    data = query.order_by(DataPenduduk.nama).paginate(page=page, per_page=20)
    
    dusun_list = db.session.query(DataPenduduk.dusun).distinct().all()
    dusun_list = [d[0] for d in dusun_list if d[0]]
    
    return render_template('admin/penduduk/list.html', data=data, dusun_list=dusun_list, filter_dusun=dusun)

@admin_bp.route('/penduduk/tambah', methods=['GET', 'POST'])
@login_required
def tambah_penduduk():
    if request.method == 'POST':
        try:
            data = DataPenduduk(
                nik=request.form.get('nik'),
                nama=request.form.get('nama'),
                tempat_lahir=request.form.get('tempat_lahir'),
                tanggal_lahir=request.form.get('tanggal_lahir') if request.form.get('tanggal_lahir') else None,
                jenis_kelamin=request.form.get('jenis_kelamin'),
                agama=request.form.get('agama'),
                status_perkawinan=request.form.get('status_perkawinan'),
                pendidikan=request.form.get('pendidikan'),
                pekerjaan=request.form.get('pekerjaan'),
                alamat=request.form.get('alamat'),
                dusun=request.form.get('dusun'),
                rw=request.form.get('rw'),
                rt=request.form.get('rt')
            )
            
            db.session.add(data)
            db.session.commit()
            
            log_activity(current_user.id, 'Tambah Data Penduduk', 'Penduduk', f'NIK: {data.nik}')
            flash('Data penduduk berhasil ditambahkan', 'success')
            return redirect(url_for('admin.kelola_penduduk'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/penduduk/form.html', action='Tambah')

@admin_bp.route('/penduduk/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_penduduk(id):
    data = DataPenduduk.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            data.nik = request.form.get('nik')
            data.nama = request.form.get('nama')
            data.tempat_lahir = request.form.get('tempat_lahir')
            data.tanggal_lahir = request.form.get('tanggal_lahir') if request.form.get('tanggal_lahir') else None
            data.jenis_kelamin = request.form.get('jenis_kelamin')
            data.agama = request.form.get('agama')
            data.status_perkawinan = request.form.get('status_perkawinan')
            data.pendidikan = request.form.get('pendidikan')
            data.pekerjaan = request.form.get('pekerjaan')
            data.alamat = request.form.get('alamat')
            data.dusun = request.form.get('dusun')
            data.rw = request.form.get('rw')
            data.rt = request.form.get('rt')
            
            db.session.commit()
            
            log_activity(current_user.id, 'Edit Data Penduduk', 'Penduduk', f'NIK: {data.nik}')
            flash('Data penduduk berhasil diupdate', 'success')
            return redirect(url_for('admin.kelola_penduduk'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/penduduk/form.html', data=data, action='Edit')

@admin_bp.route('/penduduk/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_penduduk(id):
    data = DataPenduduk.query.get_or_404(id)
    try:
        db.session.delete(data)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus Data Penduduk', 'Penduduk', f'Nama: {data.nama}')
        flash('Data penduduk berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_penduduk'))

# ============ ADMIN APB DESA ROUTES =============

@admin_bp.route('/apb')
@login_required
def kelola_apb():
    tahun = request.args.get('tahun', datetime.now().year, type=int)
    
    tahun_list = db.session.query(ApbDes.tahun).distinct().order_by(ApbDes.tahun.desc()).all()
    tahun_list = [t[0] for t in tahun_list]
    
    apb = ApbDes.query.filter_by(tahun=tahun).order_by(ApbDes.kategori).all()
    
    return render_template('admin/apb/list.html', apb=apb, tahun=tahun, tahun_list=tahun_list)

@admin_bp.route('/apb/tambah', methods=['GET', 'POST'])
@login_required
def tambah_apb():
    if request.method == 'POST':
        try:
            apb = ApbDes(
                tahun=request.form.get('tahun', type=int),
                kategori=request.form.get('kategori'),
                sub_kategori=request.form.get('sub_kategori'),
                uraian=request.form.get('uraian'),
                anggaran=float(request.form.get('anggaran', 0)),
                realisasi=float(request.form.get('realisasi', 0)),
                status=request.form.get('status', 'Anggaran')
            )
            
            db.session.add(apb)
            db.session.commit()
            
            log_activity(current_user.id, 'Tambah APB', 'APB', f'Kategori: {apb.kategori}')
            flash('Data APB berhasil ditambahkan', 'success')
            return redirect(url_for('admin.kelola_apb'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/apb/form.html', action='Tambah')

@admin_bp.route('/apb/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_apb(id):
    apb = ApbDes.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            apb.kategori = request.form.get('kategori')
            apb.sub_kategori = request.form.get('sub_kategori')
            apb.uraian = request.form.get('uraian')
            apb.anggaran = float(request.form.get('anggaran', 0))
            apb.realisasi = float(request.form.get('realisasi', 0))
            apb.status = request.form.get('status', 'Anggaran')
            
            db.session.commit()
            
            log_activity(current_user.id, 'Edit APB', 'APB', f'Kategori: {apb.kategori}')
            flash('Data APB berhasil diupdate', 'success')
            return redirect(url_for('admin.kelola_apb', tahun=apb.tahun))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/apb/form.html', apb=apb, action='Edit')

@admin_bp.route('/apb/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_apb(id):
    apb = ApbDes.query.get_or_404(id)
    tahun = apb.tahun
    try:
        db.session.delete(apb)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus APB', 'APB', f'Kategori: {apb.kategori}')
        flash('Data APB berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_apb', tahun=tahun))

# ============ ADMIN APARATUR DESA ROUTES =============

@admin_bp.route('/aparatur')
@login_required
def kelola_aparatur():
    page = request.args.get('page', 1, type=int)
    aparatur = AparaturDesa.query.order_by(AparaturDesa.jabatan).paginate(page=page, per_page=10)
    return render_template('admin/aparatur/list.html', aparatur=aparatur)

@admin_bp.route('/aparatur/tambah', methods=['GET', 'POST'])
@login_required
def tambah_aparatur():
    if request.method == 'POST':
        try:
            nama = request.form.get('nama')
            jabatan = request.form.get('jabatan')
            tanggal_input = request.form.get('tanggal_mulai_jabatan')
            tanggal_mulai = None

            if not nama or not jabatan:
                flash('Nama dan jabatan wajib diisi.', 'danger')
                return render_template('admin/aparatur/form.html', action='Tambah', form_data=request.form)

            if tanggal_input:
                try:
                    tanggal_mulai = datetime.strptime(tanggal_input, '%Y-%m-%d').date()
                except ValueError:
                    flash('Format tanggal Mulai Jabatan tidak valid. Gunakan format YYYY-MM-DD.', 'danger')
                    return render_template('admin/aparatur/form.html', action='Tambah', form_data=request.form)

            aparatur = AparaturDesa(
                nama=nama,
                jabatan=jabatan,
                nomor_identitas=request.form.get('nomor_identitas'),
                alamat=request.form.get('alamat'),
                nomor_hp=request.form.get('nomor_hp'),
                email=request.form.get('email'),
                tanggal_mulai_jabatan=tanggal_mulai,
                keterangan=request.form.get('keterangan')
            )
            
            # Handle foto upload
            if 'foto' in request.files:
                file = request.files['foto']
                if file and file.filename:
                    if not allowed_file(file.filename):
                        flash('Format foto tidak diizinkan. Gunakan JPG/PNG.', 'danger')
                        return render_template('admin/aparatur/form.html', action='Tambah', form_data=request.form)

                    filename = secure_filename(f"aparatur_{datetime.now().timestamp()}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    aparatur.foto = filename
            
            db.session.add(aparatur)
            db.session.commit()
            
            log_activity(current_user.id, 'Tambah Aparatur', 'Aparatur', f'Nama: {aparatur.nama}')
            flash('Data aparatur berhasil ditambahkan', 'success')
            return redirect(url_for('admin.kelola_aparatur'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/aparatur/form.html', action='Tambah')

@admin_bp.route('/aparatur/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_aparatur(id):
    aparatur = AparaturDesa.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            nama = request.form.get('nama')
            jabatan = request.form.get('jabatan')
            tanggal_input = request.form.get('tanggal_mulai_jabatan')

            if not nama or not jabatan:
                flash('Nama dan jabatan wajib diisi.', 'danger')
                return render_template('admin/aparatur/form.html', aparatur=aparatur, action='Edit', form_data=request.form)

            tanggal_mulai = None
            if tanggal_input:
                try:
                    tanggal_mulai = datetime.strptime(tanggal_input, '%Y-%m-%d').date()
                except ValueError:
                    flash('Format tanggal Mulai Jabatan tidak valid. Gunakan format YYYY-MM-DD.', 'danger')
                    return render_template('admin/aparatur/form.html', aparatur=aparatur, action='Edit', form_data=request.form)

            aparatur.nama = nama
            aparatur.jabatan = jabatan
            aparatur.nomor_identitas = request.form.get('nomor_identitas')
            aparatur.alamat = request.form.get('alamat')
            aparatur.nomor_hp = request.form.get('nomor_hp')
            aparatur.email = request.form.get('email')
            aparatur.tanggal_mulai_jabatan = tanggal_mulai
            aparatur.keterangan = request.form.get('keterangan')
            
            # Handle foto upload
            if 'foto' in request.files:
                file = request.files['foto']
                if file and file.filename:
                    if not allowed_file(file.filename):
                        flash('Format foto tidak diizinkan. Gunakan JPG/PNG.', 'danger')
                        return render_template('admin/aparatur/form.html', aparatur=aparatur, action='Edit', form_data=request.form)

                    # Delete old foto
                    if aparatur.foto:
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], aparatur.foto)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    filename = secure_filename(f"aparatur_{datetime.now().timestamp()}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    aparatur.foto = filename
            
            db.session.commit()
            
            log_activity(current_user.id, 'Edit Aparatur', 'Aparatur', f'Nama: {aparatur.nama}')
            flash('Data aparatur berhasil diupdate', 'success')
            return redirect(url_for('admin.kelola_aparatur'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/aparatur/form.html', aparatur=aparatur, action='Edit')

@admin_bp.route('/aparatur/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_aparatur(id):
    aparatur = AparaturDesa.query.get_or_404(id)
    try:
        # Delete foto
        if aparatur.foto:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], aparatur.foto)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(aparatur)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus Aparatur', 'Aparatur', f'Nama: {aparatur.nama}')
        flash('Data aparatur berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_aparatur'))

# ============ ADMIN PROFIL DESA ROUTES =============

@admin_bp.route('/profil', methods=['GET', 'POST'])
@login_required
def edit_profil_desa():
    profil = ProfilDesa.query.first()
    if not profil:
        profil = ProfilDesa()
        db.session.add(profil)
        db.session.commit()
    
    if request.method == 'POST':
        try:
            profil.nama_desa = request.form.get('nama_desa')
            profil.kecamatan = request.form.get('kecamatan')
            profil.kabupaten = request.form.get('kabupaten')
            profil.provinsi = request.form.get('provinsi')
            profil.luas_desa = float(request.form.get('luas_desa', 0)) if request.form.get('luas_desa') else None
            profil.jumlah_penduduk = int(request.form.get('jumlah_penduduk', 0)) if request.form.get('jumlah_penduduk') else None
            profil.juml_keluarga = int(request.form.get('juml_keluarga', 0)) if request.form.get('juml_keluarga') else None
            profil.visi = request.form.get('visi')
            profil.misi = request.form.get('misi')
            profil.sejarah_desa = request.form.get('sejarah_desa')
            profil.kontak_kantor = request.form.get('kontak_kantor')
            profil.email_desa = request.form.get('email_desa')
            profil.alamat_kantor = request.form.get('alamat_kantor')
            profil.diupdate_pada = datetime.utcnow()
            
            # Handle logo upload
            if 'logo' in request.files:
                file = request.files['logo']
                if file and allowed_file(file.filename):
                    if profil.logo:
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], profil.logo)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    filename = secure_filename(f"logo_{datetime.now().timestamp()}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    profil.logo = filename
            
            db.session.commit()
            
            log_activity(current_user.id, 'Edit Profil Desa', 'Profil', 'Update profil desa')
            flash('Profil desa berhasil diupdate', 'success')
            return redirect(url_for('admin.edit_profil_desa'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/profil/edit.html', profil=profil)

# ============ ADMIN ACCOUNT ROUTES =============

@admin_bp.route('/pengaturan-akun')
@login_required
def pengaturan_akun():
    return render_template('admin/account/settings.html')

@admin_bp.route('/pengaturan-akun/update', methods=['POST'])
@login_required
def update_profil_akun():
    try:
        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        
        db.session.commit()
        
        log_activity(current_user.id, 'Update Profil Akun', 'Account', 'Update data profil')
        flash('Profil akun berhasil diupdate', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.pengaturan_akun'))

@admin_bp.route('/pengaturan-akun/password', methods=['POST'])
@login_required
def ubah_password():
    try:
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(old_password):
            flash('Password lama tidak sesuai', 'danger')
            return redirect(url_for('admin.pengaturan_akun'))
        
        if new_password != confirm_password:
            flash('Password baru tidak sesuai', 'danger')
            return redirect(url_for('admin.pengaturan_akun'))
        
        if len(new_password) < 6:
            flash('Password minimal 6 karakter', 'danger')
            return redirect(url_for('admin.pengaturan_akun'))
        
        current_user.set_password(new_password)
        db.session.commit()
        
        log_activity(current_user.id, 'Ubah Password', 'Account', 'Ubah password akun')
        flash('Password berhasil diubah', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.pengaturan_akun'))

# ============ ADMIN PENGGUNA ROUTES =============

@admin_bp.route('/pengguna')
@login_required
def kelola_pengguna():
    page = request.args.get('page', 1, type=int)
    pengguna = Admin.query.order_by(Admin.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/pengguna/list.html', pengguna=pengguna)

@admin_bp.route('/pengguna/tambah', methods=['GET', 'POST'])
@login_required
def tambah_pengguna():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            
            # Check if username exists
            if Admin.query.filter_by(username=username).first():
                flash('Username sudah terdaftar', 'danger')
                return redirect(url_for('admin.tambah_pengguna'))
            
            if Admin.query.filter_by(email=email).first():
                flash('Email sudah terdaftar', 'danger')
                return redirect(url_for('admin.tambah_pengguna'))
            
            admin = Admin(
                username=username,
                email=email,
                full_name=full_name,
                is_active=True
            )
            admin.set_password(password)
            
            db.session.add(admin)
            db.session.commit()
            
            log_activity(current_user.id, 'Tambah Pengguna', 'Pengguna', f'Username: {username}')
            flash('Pengguna berhasil ditambahkan', 'success')
            return redirect(url_for('admin.kelola_pengguna'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/pengguna/form.html', action='Tambah')

@admin_bp.route('/pengguna/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_pengguna(id):
    pengguna = Admin.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            pengguna.full_name = request.form.get('full_name')
            pengguna.email = request.form.get('email')
            pengguna.is_active = request.form.get('is_active') == 'on'
            
            db.session.commit()
            
            log_activity(current_user.id, 'Edit Pengguna', 'Pengguna', f'Username: {pengguna.username}')
            flash('Pengguna berhasil diupdate', 'success')
            return redirect(url_for('admin.kelola_pengguna'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/pengguna/form.html', pengguna=pengguna, action='Edit')

@admin_bp.route('/pengguna/<int:id>/hapus', methods=['POST'])
@login_required
def hapus_pengguna(id):
    pengguna = Admin.query.get_or_404(id)
    
    if pengguna.id == current_user.id:
        flash('Anda tidak bisa menghapus akun sendiri', 'danger')
        return redirect(url_for('admin.kelola_pengguna'))
    
    try:
        db.session.delete(pengguna)
        db.session.commit()
        
        log_activity(current_user.id, 'Hapus Pengguna', 'Pengguna', f'Username: {pengguna.username}')
        flash('Pengguna berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.kelola_pengguna'))

# ============ FILE DOWNLOAD ROUTES =============

@public_bp.route('/download/file/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        else:
            flash('File tidak ditemukan', 'danger')
            return redirect(request.referrer or url_for('public.index'))
    except Exception as e:
        flash(f'Terjadi kesalahan saat download: {str(e)}', 'danger')
        return redirect(request.referrer or url_for('public.index'))

@public_bp.route('/download/dokumen/<filename>')
def download_dokumen(filename):
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'documents', filename)
        if os.path.exists(file_path):
            return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], 'documents'), filename, as_attachment=True)
        else:
            flash('File tidak ditemukan', 'danger')
            return redirect(request.referrer or url_for('public.dokumen_publik'))
    except Exception as e:
        flash(f'Terjadi kesalahan saat download: {str(e)}', 'danger')
        return redirect(request.referrer or url_for('public.dokumen_publik'))
