"""
API Routes untuk GitHub Pages Frontend
Menyediakan data dalam format JSON
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import (
    db, Berita, Galeri, DokumenPublik, Pengaduan, DataPenduduk, 
    ApbDes, AparaturDesa, ProfilDesa
)

api_bp = Blueprint('api', __name__, url_prefix='/api')

def serialize_datetime(dt):
    """Convert datetime to ISO format string"""
    if dt:
        return dt.isoformat()
    return None

# ============ PROFIL DESA API =============

@api_bp.route('/profil', methods=['GET'])
def get_profil():
    """Get village profile"""
    profil = ProfilDesa.query.first()
    if not profil:
        return jsonify({'error': 'Profil tidak ditemukan'}), 404
    
    return jsonify({
        'id': profil.id,
        'nama_desa': profil.nama_desa,
        'visi': profil.visi,
        'misi': profil.misi,
        'logo': profil.logo,
        'sejarah': profil.sejarah,
    })

@api_bp.route('/aparatur', methods=['GET'])
def get_aparatur():
    """Get village officials/aparatur"""
    aparatur = AparaturDesa.query.all()
    return jsonify({
        'total': len(aparatur),
        'data': [{
            'id': a.id,
            'nama': a.nama,
            'jabatan': a.jabatan,
            'periode': a.periode,
            'foto': a.foto
        } for a in aparatur]
    })

# ============ BERITA API =============

@api_bp.route('/berita', methods=['GET'])
def get_berita_list():
    """Get list of published news"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    berita = Berita.query.filter_by(is_published=True).order_by(
        Berita.tanggal_publikasi.desc()
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': berita.total,
        'pages': berita.pages,
        'current_page': page,
        'data': [{
            'id': b.id,
            'judul': b.judul,
            'slug': b.slug,
            'konten': b.konten[:200] + '...' if len(b.konten) > 200 else b.konten,
            'thumbnail': b.thumbnail,
            'penulis': b.penulis,
            'tanggal_publikasi': serialize_datetime(b.tanggal_publikasi),
            'views': b.views
        } for b in berita.items]
    })

@api_bp.route('/berita/<string:slug>', methods=['GET'])
def get_berita_detail(slug):
    """Get detailed news by slug"""
    berita = Berita.query.filter_by(slug=slug).first()
    if not berita:
        return jsonify({'error': 'Berita tidak ditemukan'}), 404
    
    # Update views
    berita.views += 1
    db.session.commit()
    
    # Get related news
    berita_terkait = Berita.query.filter_by(is_published=True).filter(
        Berita.id != berita.id
    ).order_by(Berita.tanggal_publikasi.desc()).limit(3).all()
    
    return jsonify({
        'id': berita.id,
        'judul': berita.judul,
        'slug': berita.slug,
        'konten': berita.konten,
        'thumbnail': berita.thumbnail,
        'penulis': berita.penulis,
        'tanggal_publikasi': serialize_datetime(berita.tanggal_publikasi),
        'views': berita.views,
        'berita_terkait': [{
            'id': b.id,
            'judul': b.judul,
            'slug': b.slug,
            'thumbnail': b.thumbnail,
            'tanggal_publikasi': serialize_datetime(b.tanggal_publikasi)
        } for b in berita_terkait]
    })

# ============ GALERI API =============

@api_bp.route('/galeri', methods=['GET'])
def get_galeri_list():
    """Get gallery items"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    kategori = request.args.get('kategori', '')
    
    query = Galeri.query
    if kategori:
        query = query.filter_by(kategori=kategori)
    
    galeri = query.order_by(Galeri.tanggal_upload.desc()).paginate(page=page, per_page=per_page)
    
    # Get all categories
    kategori_list = db.session.query(Galeri.kategori).distinct().all()
    kategori_list = [k[0] for k in kategori_list if k[0]]
    
    return jsonify({
        'total': galeri.total,
        'pages': galeri.pages,
        'current_page': page,
        'kategori_list': kategori_list,
        'data': [{
            'id': g.id,
            'judul': g.judul,
            'deskripsi': g.deskripsi,
            'file_path': g.file_path,
            'file_type': g.file_type,
            'kategori': g.kategori,
            'tanggal_upload': serialize_datetime(g.tanggal_upload)
        } for g in galeri.items]
    })

# ============ DOKUMEN PUBLIK API =============

@api_bp.route('/dokumen', methods=['GET'])
def get_dokumen_list():
    """Get public documents"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    jenis = request.args.get('jenis', '')
    
    query = DokumenPublik.query
    if jenis:
        query = query.filter_by(jenis_dokumen=jenis)
    
    dokumen = query.order_by(DokumenPublik.tanggal_upload.desc()).paginate(page=page, per_page=per_page)
    
    # Get all document types
    jenis_list = db.session.query(DokumenPublik.jenis_dokumen).distinct().all()
    jenis_list = [j[0] for j in jenis_list if j[0]]
    
    return jsonify({
        'total': dokumen.total,
        'pages': dokumen.pages,
        'current_page': page,
        'jenis_list': jenis_list,
        'data': [{
            'id': d.id,
            'judul': d.judul,
            'deskripsi': d.deskripsi,
            'file_path': d.file_path,
            'jenis_dokumen': d.jenis_dokumen,
            'tanggal_upload': serialize_datetime(d.tanggal_upload),
            'uploader': d.uploader
        } for d in dokumen.items]
    })

# ============ APB DESA API =============

@api_bp.route('/apb', methods=['GET'])
def get_apb():
    """Get APB (budget) data"""
    tahun = request.args.get('tahun', datetime.now().year, type=int)
    
    # Get list of years
    tahun_list = db.session.query(ApbDes.tahun).distinct().order_by(ApbDes.tahun.desc()).all()
    tahun_list = [t[0] for t in tahun_list]
    
    anggaran = ApbDes.query.filter_by(tahun=tahun, status='Anggaran').all()
    realisasi = ApbDes.query.filter_by(tahun=tahun, status='Realisasi').all()
    
    total_anggaran = sum(a.anggaran for a in anggaran)
    total_realisasi = sum(r.realisasi for r in realisasi)
    
    return jsonify({
        'tahun': tahun,
        'tahun_list': tahun_list,
        'total_anggaran': total_anggaran,
        'total_realisasi': total_realisasi,
        'anggaran': [{
            'id': a.id,
            'keterangan': a.keterangan,
            'anggaran': a.anggaran,
            'persentase': round((a.anggaran / total_anggaran * 100) if total_anggaran > 0 else 0, 2)
        } for a in anggaran],
        'realisasi': [{
            'id': r.id,
            'keterangan': r.keterangan,
            'realisasi': r.realisasi,
            'persentase': round((r.realisasi / total_realisasi * 100) if total_realisasi > 0 else 0, 2)
        } for r in realisasi]
    })

# ============ DATA PENDUDUK API =============

@api_bp.route('/penduduk', methods=['GET'])
def get_data_penduduk():
    """Get population data"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    dusun = request.args.get('dusun', '')
    
    query = DataPenduduk.query
    if dusun:
        query = query.filter_by(dusun=dusun)
    
    data = query.order_by(DataPenduduk.nama).paginate(page=page, per_page=per_page)
    
    # Get all hamlets
    dusun_list = db.session.query(DataPenduduk.dusun).distinct().all()
    dusun_list = [d[0] for d in dusun_list if d[0]]
    
    # Calculate statistics
    total_penduduk = DataPenduduk.query.count()
    
    return jsonify({
        'total': data.total,
        'pages': data.pages,
        'current_page': page,
        'total_penduduk': total_penduduk,
        'dusun_list': dusun_list,
        'data': [{
            'id': p.id,
            'nik': p.nik,
            'nama': p.nama,
            'tempat_lahir': p.tempat_lahir,
            'tanggal_lahir': p.tanggal_lahir.isoformat() if p.tanggal_lahir else None,
            'jenis_kelamin': p.jenis_kelamin,
            'agama': p.agama,
            'status_perkawinan': p.status_perkawinan,
            'pendidikan': p.pendidikan,
            'pekerjaan': p.pekerjaan,
            'alamat': p.alamat,
            'dusun': p.dusun
        } for p in data.items]
    })

# ============ PENGADUAN API =============

@api_bp.route('/pengaduan', methods=['GET', 'POST'])
def handle_pengaduan():
    """Get or submit complaints"""
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pengaduan = Pengaduan.query.filter_by(status='Selesai').order_by(
            Pengaduan.tanggal_dibuat.desc()
        ).paginate(page=page, per_page=10)
        
        return jsonify({
            'total': pengaduan.total,
            'pages': pengaduan.pages,
            'current_page': page,
            'data': [{
                'id': p.id,
                'nama_pelapor': p.nama_pelapor,
                'subjek': p.subjek,
                'kategori': p.kategori,
                'status': p.status,
                'tanggal_dibuat': serialize_datetime(p.tanggal_dibuat),
                'respon_admin': p.respon_admin
            } for p in pengaduan.items]
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            pengaduan = Pengaduan(
                nama_pelapor=data.get('nama_pelapor'),
                email_pelapor=data.get('email_pelapor'),
                nomor_hp=data.get('nomor_hp'),
                kategori=data.get('kategori'),
                subjek=data.get('subjek'),
                isi=data.get('isi'),
                status='Baru'
            )
            
            db.session.add(pengaduan)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Pengaduan berhasil dikirim',
                'id': pengaduan.id
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

# ============ STATISTICS API =============

@api_bp.route('/stats', methods=['GET'])
def get_statistics():
    """Get overall statistics"""
    total_berita = Berita.query.count()
    total_pengaduan = Pengaduan.query.count()
    total_penduduk = DataPenduduk.query.count()
    total_galeri = Galeri.query.count()
    
    pengaduan_baru = Pengaduan.query.filter_by(status='Baru').count()
    
    # Latest news
    berita_terbaru = Berita.query.filter_by(is_published=True).order_by(
        Berita.tanggal_publikasi.desc()
    ).limit(6).all()
    
    return jsonify({
        'total_berita': total_berita,
        'total_pengaduan': total_pengaduan,
        'total_penduduk': total_penduduk,
        'total_galeri': total_galeri,
        'pengaduan_baru': pengaduan_baru,
        'berita_terbaru': [{
            'id': b.id,
            'judul': b.judul,
            'slug': b.slug,
            'thumbnail': b.thumbnail,
            'tanggal_publikasi': serialize_datetime(b.tanggal_publikasi)
        } for b in berita_terbaru]
    })
