# 📡 API Documentation

Base URL: `{API_BASE_URL}/api`

## Endpoints Overview

### Public Endpoints (Tidak perlu autentikasi)

#### Statistics
- **GET** `/stats` - Get overall statistics

#### Profile
- **GET** `/profil` - Get village profile
- **GET** `/aparatur` - Get village officials

#### News/Berita
- **GET** `/berita` - Get news list (paginated)
- **GET** `/berita/<slug>` - Get news detail by slug

#### Gallery
- **GET** `/galeri` - Get gallery items (paginated)

#### Documents
- **GET** `/dokumen` - Get public documents (paginated)

#### Budget/APB
- **GET** `/apb` - Get budget data by year

#### Population
- **GET** `/penduduk` - Get population data (paginated)

#### Complaints
- **GET** `/pengaduan` - Get complaints
- **POST** `/pengaduan` - Submit new complaint

---

## Detailed Endpoints

### 1. GET `/stats` - Statistik Keseluruhan

**Description:** Get overall statistics of the village

**Parameters:** None

**Response:**
```json
{
  "total_berita": 15,
  "total_pengaduan": 24,
  "total_penduduk": 3500,
  "total_galeri": 45,
  "pengaduan_baru": 3,
  "berita_terbaru": [
    {
      "id": 1,
      "judul": "Pembersihan Lingkungan Desa",
      "slug": "pembersihan-lingkungan-desa",
      "thumbnail": "path/to/image.jpg",
      "tanggal_publikasi": "2024-01-15T10:30:00"
    }
  ]
}
```

---

### 2. GET `/profil` - Profil Desa

**Description:** Get village profile information

**Response:**
```json
{
  "id": 1,
  "nama_desa": "Desa Way Ilahan",
  "visi": "Menjadi desa yang maju, sejahtera, dan berkelanjutan",
  "misi": "Meningkatkan kesejahteraan masyarakat...",
  "logo": "logo-desa.png",
  "sejarah": "Desa Way Ilahan didirikan tahun..."
}
```

---

### 3. GET `/aparatur` - Data Aparatur Desa

**Description:** Get list of village officials

**Response:**
```json
{
  "total": 5,
  "data": [
    {
      "id": 1,
      "nama": "Supardi",
      "jabatan": "Kepala Desa",
      "periode": "2020-2026",
      "foto": "foto-supardi.jpg"
    }
  ]
}
```

---

### 4. GET `/berita?page=1&per_page=10` - Daftar Berita

**Description:** Get paginated list of published news

**Parameters:**
- `page` (int, default: 1) - Page number
- `per_page` (int, default: 10) - Items per page

**Response:**
```json
{
  "total": 15,
  "pages": 2,
  "current_page": 1,
  "data": [
    {
      "id": 1,
      "judul": "Pembersihan Lingkungan",
      "slug": "pembersihan-lingkungan-desa",
      "konten": "Kegiatan pembersihan lingkungan...",
      "thumbnail": "berita_123.jpg",
      "penulis": "Admin",
      "tanggal_publikasi": "2024-01-15T10:30:00",
      "views": 150
    }
  ]
}
```

---

### 5. GET `/berita/<slug>` - Detail Berita

**Description:** Get detailed news by slug

**Parameters:**
- `slug` (string) - News slug

**Response:**
```json
{
  "id": 1,
  "judul": "Pembersihan Lingkungan",
  "slug": "pembersihan-lingkungan-desa",
  "konten": "Lorem ipsum dolor sit amet...",
  "thumbnail": "berita_123.jpg",
  "penulis": "Admin",
  "tanggal_publikasi": "2024-01-15T10:30:00",
  "views": 150,
  "berita_terkait": [
    {
      "id": 2,
      "judul": "Program Sehat Desa",
      "slug": "program-sehat-desa",
      "thumbnail": "berita_124.jpg",
      "tanggal_publikasi": "2024-01-14T09:00:00"
    }
  ]
}
```

---

### 6. GET `/galeri?page=1&per_page=12&kategori=` - Galeri

**Description:** Get gallery items with optional category filter

**Parameters:**
- `page` (int, default: 1) - Page number
- `per_page` (int, default: 12) - Items per page
- `kategori` (string, optional) - Filter by category

**Response:**
```json
{
  "total": 45,
  "pages": 4,
  "current_page": 1,
  "kategori_list": ["Kegiatan Desa", "Acara Rakyat", "Pembangunan"],
  "data": [
    {
      "id": 1,
      "judul": "Pembersihan Sampah",
      "deskripsi": "Kegiatan bersih-bersih lingkungan",
      "file_path": "galeri_123.jpg",
      "file_type": "photo",
      "kategori": "Kegiatan Desa",
      "tanggal_upload": "2024-01-15T10:30:00"
    }
  ]
}
```

---

### 7. GET `/dokumen?page=1&per_page=10&jenis=` - Dokumen Publik

**Description:** Get public documents with optional type filter

**Parameters:**
- `page` (int, default: 1) - Page number
- `per_page` (int, default: 10) - Items per page
- `jenis` (string, optional) - Filter by document type

**Response:**
```json
{
  "total": 25,
  "pages": 3,
  "current_page": 1,
  "jenis_list": ["SK", "Berita Acara", "Laporan", "Perdes"],
  "data": [
    {
      "id": 1,
      "judul": "SK Pembentukan Panitia",
      "deskripsi": "Surat keputusan pembentukan panitia",
      "file_path": "dokumen_123.pdf",
      "jenis_dokumen": "SK",
      "tanggal_upload": "2024-01-15T10:30:00",
      "uploader": "Admin"
    }
  ]
}
```

---

### 8. GET `/apb?tahun=2024` - Data APB

**Description:** Get budget data for specific year

**Parameters:**
- `tahun` (int, default: current year) - Year

**Response:**
```json
{
  "tahun": 2024,
  "tahun_list": [2024, 2023, 2022],
  "total_anggaran": 500000000,
  "total_realisasi": 450000000,
  "anggaran": [
    {
      "id": 1,
      "keterangan": "Gaji PNS",
      "anggaran": 150000000,
      "persentase": 30.0
    }
  ],
  "realisasi": [
    {
      "id": 1,
      "keterangan": "Gaji PNS",
      "realisasi": 150000000,
      "persentase": 33.33
    }
  ]
}
```

---

### 9. GET `/penduduk?page=1&per_page=20&dusun=` - Data Penduduk

**Description:** Get population data with optional hamlet filter

**Parameters:**
- `page` (int, default: 1) - Page number
- `per_page` (int, default: 20) - Items per page
- `dusun` (string, optional) - Filter by hamlet

**Response:**
```json
{
  "total": 3500,
  "pages": 175,
  "current_page": 1,
  "total_penduduk": 3500,
  "dusun_list": ["Dusun A", "Dusun B", "Dusun C"],
  "data": [
    {
      "id": 1,
      "nik": "1234567890123456",
      "nama": "Budi Santoso",
      "tempat_lahir": "Bandar Lampung",
      "tanggal_lahir": "1990-05-15",
      "jenis_kelamin": "Laki-laki",
      "agama": "Islam",
      "status_perkawinan": "Menikah",
      "pendidikan": "SMA",
      "pekerjaan": "Petani",
      "alamat": "Jl. Merdeka No. 123",
      "dusun": "Dusun A"
    }
  ]
}
```

---

### 10. GET `/pengaduan?page=1` - Daftar Pengaduan

**Description:** Get list of resolved complaints

**Parameters:**
- `page` (int, default: 1) - Page number

**Response:**
```json
{
  "total": 24,
  "pages": 3,
  "current_page": 1,
  "data": [
    {
      "id": 1,
      "nama_pelapor": "Siti Nurhaliza",
      "subjek": "Jalan Rusak di Dusun A",
      "kategori": "Pengaduan",
      "status": "Selesai",
      "tanggal_dibuat": "2024-01-10T15:30:00",
      "respon_admin": "Tim akan perbaiki jalan dalam 2 minggu"
    }
  ]
}
```

---

### 11. POST `/pengaduan` - Submit Pengaduan

**Description:** Submit new complaint

**Request Body:**
```json
{
  "nama_pelapor": "Siti Nurhaliza",
  "email_pelapor": "siti@example.com",
  "nomor_hp": "082123456789",
  "kategori": "Pengaduan",
  "subjek": "Jalan Rusak di Dusun A",
  "isi": "Jalan di depan rumah sangat rusak dan berbahaya..."
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Pengaduan berhasil dikirim",
  "id": 25
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Error message details"
}
```

---

## Error Responses

### 404 Not Found
```json
{
  "error": "Halaman tidak ditemukan"
}
```

### 500 Internal Server Error
```json
{
  "error": "Terjadi kesalahan pada server"
}
```

---

## Rate Limiting

No rate limiting on public endpoints (for now).

---

## CORS Headers

All API endpoints return:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Example Usage with JavaScript

```javascript
// Get statistics
const stats = await fetch('http://api.example.com/api/stats')
  .then(r => r.json());

// Get news with pagination
const berita = await fetch('http://api.example.com/api/berita?page=1&per_page=10')
  .then(r => r.json());

// Submit complaint
await fetch('http://api.example.com/api/pengaduan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nama_pelapor: 'John Doe',
    email_pelapor: 'john@example.com',
    subjek: 'Complaint subject',
    isi: 'Complaint details'
  })
});
```

---

## Example Usage with cURL

```bash
# Get statistics
curl https://api.example.com/api/stats

# Get news
curl 'https://api.example.com/api/berita?page=1&per_page=10'

# Get specific news
curl https://api.example.com/api/berita/pembersihan-lingkungan-desa

# Submit complaint
curl -X POST https://api.example.com/api/pengaduan \
  -H 'Content-Type: application/json' \
  -d '{
    "nama_pelapor": "John Doe",
    "email_pelapor": "john@example.com",
    "subjek": "My complaint",
    "isi": "Details here"
  }'
```

---

## Development Notes

- All timestamps are in ISO 8601 format (UTC)
- All responses are JSON
- File paths are relative to `/uploads/` directory
- Pagination uses offset/limit pattern
- No authentication required for public endpoints

---

**Last Updated:** 2024
**API Version:** 1.0
