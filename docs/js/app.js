/**
 * Main Application JavaScript
 * Menghandle data dari file JSON lokal
 */

const DATA_BASE_URL = './data';

const cache = {};

const API = {
  async fetch(fileName) {
    const url = `${DATA_BASE_URL}/${fileName}.json`;
    if (cache[url]) {
      return cache[url];
    }

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`File error: ${response.status} ${url}`);
    }

    const data = await response.json();
    cache[url] = data;
    return data;
  }
};

const DOM = {
  get(selector) {
    return document.querySelector(selector);
  },
  getAll(selector) {
    return document.querySelectorAll(selector);
  },
  show(selector) {
    const el = typeof selector === 'string' ? this.get(selector) : selector;
    if (el) el.style.display = 'block';
  },
  hide(selector) {
    const el = typeof selector === 'string' ? this.get(selector) : selector;
    if (el) el.style.display = 'none';
  }
};

function createPagination(pageData) {
  const totalPages = pageData.pages;
  const currentPage = pageData.current_page;
  if (totalPages <= 1) return '';

  let html = '<div class="pagination">';

  if (currentPage > 1) {
    html += `<a onclick="window.loadPage(${currentPage - 1})">← Sebelumnya</a>`;
  }

  for (let i = 1; i <= totalPages; i++) {
    if (i === currentPage) {
      html += `<span class="active">${i}</span>`;
    } else {
      html += `<a onclick="window.loadPage(${i})">${i}</a>`;
    }
  }

  if (currentPage < totalPages) {
    html += `<a onclick="window.loadPage(${currentPage + 1})">Selanjutnya →</a>`;
  }

  html += '</div>';
  return html;
}

function getLocalPengaduan() {
  try {
    const stored = localStorage.getItem('pengaduan_entries');
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    return [];
  }
}

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

function formatCurrency(value) {
  if (typeof value !== 'number') return 'Rp 0';
  return 'Rp ' + value.toLocaleString('id-ID');
}

function paginate(items, page = 1, per_page = 10) {
  const total = items.length;
  const pages = Math.max(1, Math.ceil(total / per_page));
  const current_page = Math.min(Math.max(page, 1), pages);
  const start = (current_page - 1) * per_page;
  const end = start + per_page;

  return {
    total,
    pages,
    current_page,
    per_page,
    data: items.slice(start, end)
  };
}

const router = {
  currentPage: 'home',

  setActiveMenu(page) {
    DOM.getAll('[data-page]').forEach(link => {
      if (link.dataset.page === page) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  },

  parseRoute() {
    const rawHash = window.location.hash.slice(1).trim();
    if (!rawHash) return { page: 'home' };
    if (rawHash.startsWith('berita-detail/')) {
      return { page: 'berita-detail', slug: rawHash.replace('berita-detail/', '') };
    }
    return { page: rawHash };
  },

  async handleRoute() {
    const route = this.parseRoute();
    if (route.page === 'berita-detail') {
      await this.showBeritaDetail(route.slug, false);
      return;
    }
    await this.navigate(route.page, false);
  },

  async navigate(page, updateHash = true) {
    this.currentPage = page;
    this.setActiveMenu(page === 'berita-detail' ? 'berita' : page);

    if (updateHash) {
      const targetHash = page === 'home' ? '#home' : `#${page}`;
      if (window.location.hash !== targetHash) {
        window.location.hash = targetHash;
      }
    }

    DOM.getAll('.page').forEach(el => DOM.hide(el));
    const pageElement = DOM.get(`#${page}`);
    if (!pageElement) return;
    DOM.show(pageElement);

    if (page === 'home') await this.loadHome();
    if (page === 'profil') await this.loadProfil();
    if (page === 'berita') await this.loadBerita();
    if (page === 'galeri') await this.loadGaleri();
    if (page === 'dokumen') await this.loadDokumen();
    if (page === 'apb') await this.loadAPB();
    if (page === 'penduduk') await this.loadPenduduk();
    if (page === 'pengaduan') await this.loadPengaduan();
  },

  async loadHome() {
    try {
      const stats = await API.fetch('stats');
      const container = DOM.get('#home .stats-section');
      if (container) {
        container.innerHTML = `
          <div class="row">
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-number">${stats.total_penduduk}</div>
              <p>Total Penduduk</p>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📰</div>
              <div class="stat-number">${stats.total_berita}</div>
              <p>Berita</p>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📸</div>
              <div class="stat-number">${stats.total_galeri}</div>
              <p>Galeri</p>
            </div>
            <div class="stat-card">
              <div class="stat-icon">💬</div>
              <div class="stat-number">${stats.total_pengaduan}</div>
              <p>Pengaduan</p>
            </div>
          </div>
        `;
      }

      const beritaContainer = DOM.get('#home .berita-terbaru');
      if (beritaContainer && stats.berita_terbaru.length) {
        beritaContainer.innerHTML = stats.berita_terbaru.map(b => `
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">${b.judul}</h5>
              <p class="text-muted">${formatDate(b.tanggal_publikasi)}</p>
              <a href="#" onclick="router.showBeritaDetail('${b.slug}')" class="btn btn-sm btn-primary">Baca Selengkapnya</a>
            </div>
          </div>
        `).join('');
      }
    } catch (error) {
      this.showError('Gagal memuat data statistik.');
    }
  },

  async loadProfil() {
    try {
      const profil = await API.fetch('profil');
      const aparatur = await API.fetch('aparatur');
      const container = DOM.get('#profil .profil-content');
      if (!container) return;

      container.innerHTML = `
        <div style="margin-bottom: 2rem;">
          <h3>${profil.nama_desa}</h3>
          <h5>Visi</h5>
          <p>${profil.visi}</p>
          <h5>Misi</h5>
          <p>${profil.misi}</p>
          <h5>Sejarah</h5>
          <p>${profil.sejarah}</p>
        </div>
        <h3>Aparatur Desa</h3>
        <div class="row">
          ${aparatur.data.map(a => `
            <div class="col-md-4">
              <div class="card text-center">
                <div class="card-body">
                  <h6 class="card-title">${a.nama}</h6>
                  <p class="text-muted">${a.jabatan}</p>
                  <p class="small">Periode: ${a.periode}</p>
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    } catch (error) {
      this.showError('Gagal memuat profil desa.');
    }
  },

  async loadBerita(page = 1) {
    try {
      const raw = await API.fetch('berita');
      const paged = paginate(raw.data, page, 10);
      const container = DOM.get('#berita .berita-list');
      if (!container) return;

      container.innerHTML = paged.data.map(b => `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">${b.judul}</h5>
            <p class="text-muted small">${formatDate(b.tanggal_publikasi)} • ${b.views} views</p>
            <p class="card-text">${b.konten}</p>
            <a href="#" onclick="router.showBeritaDetail('${b.slug}')" class="btn btn-sm btn-primary">Baca Selengkapnya</a>
          </div>
        </div>
      `).join('');

      const paginationContainer = DOM.get('#berita .pagination-container');
      if (paginationContainer) {
        paginationContainer.innerHTML = createPagination(paged);
      }
    } catch (error) {
      this.showError('Gagal memuat berita.');
    }
  },

  async loadGaleri(page = 1) {
    try {
      const raw = await API.fetch('galeri');
      const paged = paginate(raw.data, page, 12);
      const container = DOM.get('#galeri .galeri-list');
      if (!container) return;

      container.innerHTML = paged.data.map(g => `
        <div class="card">
          <div class="card-body">
            <h6 class="card-title">${g.judul}</h6>
            <p class="text-muted small">${g.kategori}</p>
            <p class="card-text small">${g.deskripsi}</p>
          </div>
        </div>
      `).join('');

      const paginationContainer = DOM.get('#galeri .pagination-container');
      if (paginationContainer) {
        paginationContainer.innerHTML = createPagination(paged);
      }
    } catch (error) {
      this.showError('Gagal memuat galeri.');
    }
  },

  async loadDokumen(page = 1) {
    try {
      const raw = await API.fetch('dokumen');
      const paged = paginate(raw.data, page, 10);
      const container = DOM.get('#dokumen .dokumen-list');
      if (!container) return;

      container.innerHTML = paged.data.map(d => `
        <div class="row" style="display: flex; align-items: center; border-bottom: 1px solid #eee; padding: 1rem 0;">
          <div style="flex: 1;">
            <h6>${d.judul}</h6>
            <p class="text-muted small">${d.jenis_dokumen} • ${formatDate(d.tanggal_upload)}</p>
            <p class="text-muted small">${d.deskripsi}</p>
          </div>
          <button class="btn btn-sm btn-primary" disabled>Download</button>
        </div>
      `).join('');

      const paginationContainer = DOM.get('#dokumen .pagination-container');
      if (paginationContainer) {
        paginationContainer.innerHTML = createPagination(paged);
      }
    } catch (error) {
      this.showError('Gagal memuat dokumen publik.');
    }
  },

  async loadAPB() {
    try {
      const data = await API.fetch('apb');
      const container = DOM.get('#apb .apb-content');
      if (!container) return;

      container.innerHTML = `
        <h4>Anggaran ${data.tahun}: ${formatCurrency(data.total_anggaran)}</h4>
        <div class="row">
          ${data.anggaran.map(a => `
            <div class="col-md-4">
              <div class="card">
                <div class="card-body">
                  <p class="small">${a.keterangan}</p>
                  <p style="font-weight: bold; color: var(--primary);">${formatCurrency(a.anggaran)}</p>
                  <div style="background: #eee; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: var(--primary); height: 100%; width: ${a.persentase}%;"></div>
                  </div>
                  <p class="text-muted small" style="margin-top: 0.5rem;">${a.persentase}%</p>
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    } catch (error) {
      this.showError('Gagal memuat data APB.');
    }
  },

  async loadPenduduk(page = 1) {
    try {
      const raw = await API.fetch('penduduk');
      const paged = paginate(raw.data, page, 20);
      const container = DOM.get('#penduduk .penduduk-list');
      if (!container) return;

      container.innerHTML = paged.data.map(p => `
        <div style="border-bottom: 1px solid #eee; padding: 1rem 0;">
          <strong>${p.nama}</strong><br>
          <small class="text-muted">
            NIK: ${p.nik} | ${p.jenis_kelamin} | ${p.pekerjaan}<br>
            Dusun: ${p.dusun} | Alamat: ${p.alamat}
          </small>
        </div>
      `).join('');

      const paginationContainer = DOM.get('#penduduk .pagination-container');
      if (paginationContainer) {
        paginationContainer.innerHTML = createPagination(paged);
      }
    } catch (error) {
      this.showError('Gagal memuat data penduduk.');
    }
  },

  async loadPengaduan(page = 1) {
    try {
      const raw = await API.fetch('pengaduan');
      const localPengaduan = getLocalPengaduan();
      const mergedData = [...localPengaduan, ...raw.data];
      const paged = paginate(mergedData, page, 10);
      const container = DOM.get('#pengaduan .pengaduan-list');
      if (!container) return;

      container.innerHTML = paged.data.map(p => `
        <div class="card mb-3">
          <div class="card-body">
            <h6 class="card-title">${p.subjek}</h6>
            <p class="text-muted small">${p.nama_pelapor} • ${formatDate(p.tanggal_dibuat)}</p>
            <p class="card-text">${p.isi || p.respon_admin || 'Belum ada respon'}</p>
            <span class="badge" style="background-color: ${p.status === 'Selesai' ? 'var(--success)' : 'var(--warning)'}; color: white; padding: 0.25rem 0.5rem;">${p.status}</span>
          </div>
        </div>
      `).join('');

      const paginationContainer = DOM.get('#pengaduan .pagination-container');
      if (paginationContainer) {
        paginationContainer.innerHTML = createPagination(paged);
      }
    } catch (error) {
      this.showError('Gagal memuat pengaduan.');
    }
  },

  async showBeritaDetail(slug, updateHash = true) {
    try {
      const raw = await API.fetch('berita');
      const berita = raw.data.find(b => b.slug === slug);
      if (!berita) {
        return this.showError('Berita tidak ditemukan.');
      }

      if (updateHash) {
        window.location.hash = `#berita-detail/${slug}`;
      }

      this.currentPage = 'berita-detail';
      this.setActiveMenu('berita');
      DOM.getAll('.page').forEach(el => DOM.hide(el));
      const pageElement = DOM.get('#berita-detail');
      if (!pageElement) return;
      DOM.show(pageElement);

      const container = DOM.get('#berita-detail .berita-detail-content');
      if (!container) return;

      container.innerHTML = `
        <article>
          <h2>${berita.judul}</h2>
          <p class="text-muted">${formatDate(berita.tanggal_publikasi)} • ${berita.views} views</p>
          <hr>
          <div>${berita.konten}</div>
        </article>
        <button onclick="router.navigate('berita')" class="btn btn-outline-primary" style="margin-top: 2rem;">← Kembali ke Berita</button>
      `;
      window.scrollTo(0, 0);
    } catch (error) {
      this.showError('Gagal memuat detail berita.');
    }
  },

  showError(message) {
    alert(message);
  }
};

window.loadPage = (page) => {
  if (router.currentPage === 'berita') return router.loadBerita(page);
  if (router.currentPage === 'galeri') return router.loadGaleri(page);
  if (router.currentPage === 'dokumen') return router.loadDokumen(page);
  if (router.currentPage === 'penduduk') return router.loadPenduduk(page);
  if (router.currentPage === 'pengaduan') return router.loadPengaduan(page);
  return null;
};

document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('[data-page]');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const page = link.dataset.page;
      router.navigate(page);
    });
  });

  window.addEventListener('hashchange', () => router.handleRoute());
  router.handleRoute();
});
