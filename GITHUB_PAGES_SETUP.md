# 🌐 GitHub Pages Setup Guide

Panduan lengkap untuk setup GitHub Pages untuk aplikasi Desa Way Ilahan.

## ✅ Prerequisites

- Repository di GitHub
- Access ke GitHub repository settings
- Admin panel di backend (untuk manage data)

---

## 📝 Step-by-Step Setup

### Step 1: Verify `/docs` Folder

```bash
# Pastikan struktur sudah ada
ls -la docs/
# Output:
# -rw-r--r-- index.html
# drwxr-xr-x css/
# drwxr-xr-x js/
# -rw-r--r-- .nojekyll
```

### Step 2: Push ke GitHub

```bash
# Add changes
git add .
git commit -m "Setup GitHub Pages with static frontend"
git push origin main
```

### Step 3: Enable GitHub Pages

1. Buka **GitHub Repository**
2. Klik **Settings** (di tab repository)
3. Di sidebar, klik **Pages**
4. Isi form:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` / `docs`
   - **Folder**: `/docs`
5. Klik **Save**

### Step 4: Wait for Deployment

GitHub akan mulai deploy. Status bisa dilihat di:
- **Settings** → **Pages** (lihat status)
- Atau **Actions** tab untuk detail CI/CD

Biasanya selesai dalam 1-2 menit.

### Step 5: Verify Live

```bash
# URL akan terlihat seperti:
https://USERNAME.github.io/REPO_NAME/

# Contoh:
https://rizkisyamsulh354-svg.github.io/datadesa1/
```

Klik link dan verifikasi website loading.

---

## 🔧 Configuration Options

### A. Custom Domain (Optional)

Jika punya domain sendiri:

1. Di **Settings** → **Pages** → **Custom domain**
2. Masukkan domain Anda (contoh: `desa.example.com`)
3. Klik **Save**
4. Setup DNS records:

```
CNAME record:
Name: www (atau subdomain)
Value: USERNAME.github.io
```

5. Tunggu DNS propagation (5-48 jam)

### B. HTTPS (Automatic)

GitHub Pages otomatis setup HTTPS dengan Let's Encrypt.

- ✅ Enforce HTTPS: **Settings** → **Pages** → Check "Enforce HTTPS"

### C. Custom 404 Page (Optional)

Buat file `docs/404.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>404 - Halaman Tidak Ditemukan</title>
</head>
<body>
  <h1>Halaman Tidak Ditemukan</h1>
  <p><a href="/">← Kembali ke halaman utama</a></p>
</body>
</html>
```

---

## 📊 GitHub Pages Settings

### Recommended Settings

```
Source: Deploy from a branch
Branch: main
Folder: /docs
Enforce HTTPS: ✓ (Yes)
Restrict editing: ✓ (Optional)
```

### Build & Deployment (Advanced)

Jika ingin custom build:

1. **Settings** → **Pages** → **Build and deployment**
2. Setup GitHub Actions workflow (sudah ada di `.github/workflows/deploy.yml`)

---

## 🔍 Monitoring & Troubleshooting

### Check Deployment Status

1. **Settings** → **Pages**
   - Green checkmark = Success ✅
   - Red X = Failed ❌

2. **Actions** tab
   - Lihat detail CI/CD logs
   - Debug build errors

### Common Issues

#### Issue 1: "404 - Page Not Found"

**Solusi:**
```bash
# Pastikan file ada di /docs folder
ls -la docs/index.html

# Pastikan .nojekyll ada
ls -la docs/.nojekyll

# Push ulang
git add . && git commit -m "Fix" && git push origin main
```

#### Issue 2: "Your site is published at..."

Berarti sudah berhasil ✅

#### Issue 3: CSS/JS tidak loading

**Solusi:**
1. Cek path di HTML (harus relative path)
   ```html
   <!-- ✅ Correct -->
   <link rel="stylesheet" href="css/style.css">
   <script src="js/app.js"></script>
   
   <!-- ❌ Wrong -->
   <link rel="stylesheet" href="/css/style.css">
   ```

2. Verify file permissions:
   ```bash
   ls -la docs/css/style.css
   # Harus readable (r--) untuk semua
   ```

#### Issue 4: API tidak connect

**Solusi:**
1. Edit `docs/js/app.js` baris 3:
   ```javascript
   // Ubah dari:
   const API_BASE_URL = 'http://localhost:5000/api';
   
   // Menjadi:
   const API_BASE_URL = 'https://your-backend-url.com/api';
   ```

2. Commit & push:
   ```bash
   git add docs/js/app.js
   git commit -m "Update API URL"
   git push origin main
   ```

---

## 📈 Site Analytics

### View Traffic

**Settings** → **Pages** → Lihat traffic statistics

### Setup Analytics (Optional)

Tambah Google Analytics ke `docs/index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

Replace `GA_MEASUREMENT_ID` dengan Google Analytics ID Anda.

---

## 🚀 Deployment Pipeline

### Automatic Deployment

```
GitHub Push
    ↓
.github/workflows/deploy.yml
    ↓
Build static files
    ↓
Deploy to GitHub Pages
    ↓
Live! 🎉
```

### Manual Update

```bash
# Edit files locally
vim docs/index.html

# Commit & push
git add docs/
git commit -m "Update homepage"
git push origin main

# Auto deploy dalam 1-2 menit
```

---

## 🔐 Security Best Practices

### 1. Never Commit Secrets

```bash
# ❌ DON'T
echo "API_KEY=secret-key-123" >> docs/js/app.js

# ✅ DO
# Store secrets di backend environment variables
# Frontend hanya fetch data dari API
```

### 2. Validate Input

Frontend sudah validate, tapi selalu double-check di backend.

### 3. HTTPS Always

- ✅ GitHub Pages HTTPS (automatic)
- ✅ Backend HTTPS (jika Render/Railway)
- ✅ API CORS (terbatas ke frontend URL)

### 4. Rate Limiting

Backend sebaiknya setup rate limiting:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/pengaduan', methods=['POST'])
@limiter.limit("5 per hour")
def submit_complaint():
    # ...
```

---

## 📊 GitHub Pages Limits

| Item | Limit |
|------|-------|
| Repo size | 100 GB |
| Published size | 1 GB |
| Build time | 10 minutes |
| Bandwidth | Unlimited |
| Deployments/month | Unlimited |

---

## 🎨 Customization

### Change Theme/Style

Edit `docs/css/style.css` atau ganti dengan Bootstrap:

```html
<!-- Add Bootstrap CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

### Add Favicon

```html
<!-- Di docs/index.html <head> -->
<link rel="icon" href="favicon.ico">
```

### Add Meta Tags (SEO)

```html
<!-- Di docs/index.html <head> -->
<meta name="description" content="Portal Transparansi Desa Way Ilahan">
<meta name="keywords" content="desa, transparansi, keuangan, data">
<meta name="author" content="Desa Way Ilahan">
```

---

## 📱 Mobile Optimization

Aplikasi sudah responsive, tapi verify:

```bash
# 1. Open di mobile device
# 2. Test semua pages
# 3. Check performance: https://pagespeed.web.dev/
```

---

## 🔄 Updates & Maintenance

### Update Frontend

```bash
# Edit di docs/
vim docs/index.html

# Test locally
cd docs && python -m http.server 8000

# Commit & push
git add docs/
git commit -m "Update frontend"
git push origin main

# Live dalam 1-2 menit!
```

### Update Backend

```bash
# Edit di app/
vim app/api.py

# Test locally
python run.py

# Commit & push
git add app/
git commit -m "Update API"
git push origin main

# Render otomatis redeploy!
```

---

## 📞 Support & Resources

- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **GitHub Pages Status**: https://www.githubstatus.com
- **Community Help**: https://github.community

---

## ✅ Checklist

- [ ] Repository created di GitHub
- [ ] `/docs` folder dengan `index.html`
- [ ] `.nojekyll` file ada
- [ ] GitHub Pages enabled di settings
- [ ] Custom domain setup (jika perlu)
- [ ] HTTPS enforced
- [ ] API URL updated di `docs/js/app.js`
- [ ] Backend deployed & running
- [ ] Test frontend loading
- [ ] Test API connectivity
- [ ] Verify CORS working
- [ ] Setup custom domain DNS (jika perlu)
- [ ] Monitor deployment status
- [ ] Setup analytics (opsional)

---

## 🎉 Success!

Jika semua checkmarks hijau ✅, aplikasi Anda sudah live di GitHub Pages!

**Share URL**: `https://USERNAME.github.io/REPO_NAME/`

---

**Last Updated:** 2024-06-09  
**Status:** ✅ Production Ready
