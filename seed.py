#!/usr/bin/env python
"""
Script untuk menambahkan sample data ke database Desa Way Ilahan
Jalankan: python seed.py
"""

import os
import sys
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    Admin, Berita, Galeri, DokumenPublik, Pengaduan,
    DataPenduduk, ApbDes, AparaturDesa, ProfilDesa, ActivityLog
)

def seed_database():
    """Seed database dengan sample data"""
    
    app = create_app()
    with app.app_context():
        # Clear existing data (optional)
        # db.drop_all()
        # db.create_all()
        
        print("Menambahkan data ke database...")
        
        # 1. Update Profile Desa
        profil = ProfilDesa.query.first()
        if not profil:
            profil = ProfilDesa(
                nama_desa="Way Ilahan",
                kecamatan="Pulau Panggung",
                kabupaten="Tanggamus",
                provinsi="Lampung",
                luas_desa=2500,
                jumlah_penduduk=3450,
                juml_keluarga=780,
                visi="Terwujudnya Desa Way Ilahan yang maju, mandiri, dan sejahtera dengan nilai-nilai budaya lokal",
                misi="1. Meningkatkan kualitas sumber daya manusia\n2. Mengembangkan ekonomi lokal\n3. Memperkuat kelembagaan desa\n4. Menjaga kelestarian lingkungan",
                sejarah_desa="Desa Way Ilahan merupakan salah satu desa di Kecamatan Pulau Panggung, Kabupaten Tanggamus, Provinsi Lampung. Desa ini memiliki sejarah panjang sebagai kawasan pertanian dan perkebunan yang berkembang pesat.",
                kontak_kantor="(0728) XXXXXX",
                email_desa="desa.wayilahan@gmail.com",
                alamat_kantor="Jl. Raya Way Ilahan, Desa Way Ilahan, Kec. Pulau Panggung"
            )
            db.session.add(profil)
        
        # 2. Add Aparatur (Village Officials)
        aparatur_list = [
            AparaturDesa(
                nama="Budi Santoso",
                jabatan="Kepala Desa",
                nomor_identitas="1234567890123456",
                alamat="Jl. Raya Way Ilahan",
                nomor_hp="081234567890",
                email="budi@desa.local",
                tanggal_mulai_jabatan=datetime(2020, 1, 1)
            ),
            AparaturDesa(
                nama="Siti Mariani",
                jabatan="Sekretaris Desa",
                nomor_identitas="1234567890123457",
                alamat="Jl. Pendidikan",
                nomor_hp="081234567891",
                email="siti@desa.local",
                tanggal_mulai_jabatan=datetime(2020, 1, 1)
            ),
            AparaturDesa(
                nama="Ahmad Wijaya",
                jabatan="Bendahara Desa",
                nomor_identitas="1234567890123458",
                alamat="Jl. Kesehatan",
                nomor_hp="081234567892",
                email="ahmad@desa.local",
                tanggal_mulai_jabatan=datetime(2021, 6, 15)
            ),
        ]
        for aparatur in aparatur_list:
            existing = AparaturDesa.query.filter_by(nama=aparatur.nama).first()
            if not existing:
                db.session.add(aparatur)
        
        # 3. Add News (Berita)
        berita_list = [
            Berita(
                judul="Pembukaan Pasar Tradisional Way Ilahan",
                konten="<p>Pemerintah Desa Way Ilahan dengan bangga membuka kembali Pasar Tradisional Way Ilahan yang telah direnovasi. Pasar ini menjadi pusat ekonomi masyarakat lokal dengan lebih dari 50 pedagang yang berjualan berbagai kebutuhan sehari-hari.</p>",
                slug="pembukaan-pasar-tradisional-way-ilahan",
                penulis="Admin",
                tanggal_publikasi=datetime.now() - timedelta(days=5),
                is_published=True,
                views=45
            ),
            Berita(
                judul="Program Vaksinasi Anak di Desa Way Ilahan",
                konten="<p>Klinik kesehatan desa menyelenggarakan program vaksinasi gratis untuk anak-anak usia 0-2 tahun. Program ini didukung oleh Dinas Kesehatan Kabupaten Tanggamus dan diikuti oleh lebih dari 100 orang tua dengan anak-anak mereka.</p>",
                slug="program-vaksinasi-anak-desa-way-ilahan",
                penulis="Admin",
                tanggal_publikasi=datetime.now() - timedelta(days=3),
                is_published=True,
                views=28
            ),
            Berita(
                judul="Musyawarah Rencana Pembangunan Desa 2024",
                konten="<p>Desa Way Ilahan mengadakan Musyawarah Rencana Pembangunan (Musbang) untuk tahun 2024. Dalam acara ini, kepala desa dan masyarakat merumuskan program-program prioritas pembangunan yang akan dilaksanakan sepanjang tahun 2024.</p>",
                slug="musyawarah-rencana-pembangunan-desa-2024",
                penulis="Admin",
                tanggal_publikasi=datetime.now() - timedelta(days=1),
                is_published=True,
                views=12
            ),
        ]
        for berita in berita_list:
            existing = Berita.query.filter_by(slug=berita.slug).first()
            if not existing:
                db.session.add(berita)
        
        # 4. Add Population Data (Sample)
        penduduk_list = [
            DataPenduduk(
                nik="1234567890123456",
                nama="Rudi Hermawan",
                tempat_lahir="Bandar Lampung",
                tanggal_lahir=datetime(1985, 5, 15),
                jenis_kelamin="Laki-laki",
                agama="Islam",
                status_perkawinan="Kawin",
                pendidikan="SMA",
                pekerjaan="Petani",
                alamat="Jl. Raya Way Ilahan No. 10",
                dusun="Dusun Utama",
                rw="01",
                rt="01"
            ),
            DataPenduduk(
                nik="1234567890123457",
                nama="Sinta Wijaya",
                tempat_lahir="Way Ilahan",
                tanggal_lahir=datetime(1990, 3, 20),
                jenis_kelamin="Perempuan",
                agama="Islam",
                status_perkawinan="Kawin",
                pendidikan="SMA",
                pekerjaan="Pedagang",
                alamat="Jl. Pendidikan No. 5",
                dusun="Dusun Utama",
                rw="01",
                rt="02"
            ),
            DataPenduduk(
                nik="1234567890123458",
                nama="Ahmad Yusuf",
                tempat_lahir="Metro",
                tanggal_lahir=datetime(1988, 7, 10),
                jenis_kelamin="Laki-laki",
                agama="Islam",
                status_perkawinan="Kawin",
                pendidikan="Diploma",
                pekerjaan="Guru",
                alamat="Jl. Kesehatan No. 3",
                dusun="Dusun Karya",
                rw="02",
                rt="01"
            ),
        ]
        for penduduk in penduduk_list:
            existing = DataPenduduk.query.filter_by(nik=penduduk.nik).first()
            if not existing:
                db.session.add(penduduk)
        
        # 5. Add APB (Budget) Data
        apb_list = [
            ApbDes(
                tahun=2024,
                kategori="Operasional",
                sub_kategori="Gaji dan Tunjangan",
                uraian="Gaji PNS Desa",
                anggaran=150000000,
                realisasi=145000000,
                status="Terealisasi"
            ),
            ApbDes(
                tahun=2024,
                kategori="Pembangunan",
                sub_kategori="Infrastruktur",
                uraian="Perbaikan Jalan Desa",
                anggaran=300000000,
                realisasi=250000000,
                status="Terealisasi Sebagian"
            ),
            ApbDes(
                tahun=2024,
                kategori="Pemberdayaan",
                sub_kategori="Pendidikan",
                uraian="Beasiswa Siswa Berprestasi",
                anggaran=50000000,
                realisasi=0,
                status="Belum Terealisasi"
            ),
        ]
        for apb in apb_list:
            existing = ApbDes.query.filter_by(
                tahun=apb.tahun,
                uraian=apb.uraian
            ).first()
            if not existing:
                db.session.add(apb)
        
        # 6. Add Sample Complaint
        pengaduan = Pengaduan(
            nama_pelapor="Contoh Masyarakat",
            email_pelapor="masyarakat@example.com",
            nomor_hp="081234567890",
            kategori="Saran",
            subjek="Saran Perbaikan Jalan Desa",
            isi="Jalan di dusun utama perlu segera diperbaiki karena banyak lubang.",
            status="Ditanggapi",
            respon_admin="Terima kasih atas masukan. Tim desa akan melakukan survey dan perencanaan perbaikan jalan segera."
        )
        existing_pengaduan = Pengaduan.query.filter_by(
            email_pelapor=pengaduan.email_pelapor
        ).first()
        if not existing_pengaduan:
            db.session.add(pengaduan)
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Sample data berhasil ditambahkan!")
        print("\nData yang ditambahkan:")
        print("- 1 Profil Desa")
        print("- 3 Pejabat Desa")
        print("- 3 Berita")
        print("- 3 Data Penduduk")
        print("- 3 APB Entry")
        print("- 1 Pengaduan Contoh")
        print("\nSilakan login ke admin dengan:")
        print("  Username: admin")
        print("  Password: admin123")

if __name__ == '__main__':
    seed_database()
