# face-pay
face pay sistem 

# 💳 FacePay - Sistem Pembayaran dengan Pengenalan Wajah

**FacePay** adalah sistem pembayaran berbasis pengenalan wajah (facial recognition) yang dibangun menggunakan Python, Streamlit, MTCNN, dan FaceNet. Sistem ini menyediakan antarmuka pengguna untuk registrasi wajah, pembayaran, dan top-up saldo, serta dashboard admin untuk mengelola log, pengguna, dan autentikasi admin.

---

## 🚀 Fitur Utama

### 🔐 User
- Registrasi pengguna baru dengan wajah + PIN fallback (6 digit)
- Simpan embedding wajah menggunakan FaceNet
- Proses pembayaran dengan wajah
- Fallback ke verifikasi PIN jika wajah tidak dikenali
- Top-up saldo
- Penyimpanan data pengguna di `users.json` dan `embeddings_db.npy`
- Simpan foto wajah di folder `assets/`

### 🛠️ Admin
- Login admin menggunakan username & password (disimpan di SQLite)
- Reset PIN pengguna
- Dashboard log aktivitas:
  - Transaksi (top up, pembayaran)
  - Login admin
- Ekspor log ke CSV
- Filter nama pengguna dan rentang tanggal
- Validasi autentikasi berbasis sesi
- Sistem lock PIN setelah 3x gagal

---

## 🗂️ Struktur Folder

<pre> 📁 <b>facepay/</b> ├── <b>user_frontend.py</b> # Antarmuka pengguna (registrasi, top up, bayar) ├── <b>admin_dashboard.py</b> # Dashboard admin (log, reset PIN, autentikasi) ├── <b>user_db.py</b> # Backend logika (pengguna, transaksi, PIN) ├── <b>init_db.py</b> # Inisialisasi database SQLite ├── <b>users.json</b> # Data pengguna (nama, PIN hash, saldo) ├── <b>embeddings_db.npy</b> # Embedding wajah pengguna (FaceNet) ├── <b>requirements.txt</b> # Daftar dependensi Python ├── <b>README.md</b> # Dokumentasi proyek │ ├── 📁 <b>assets/</b> # Foto wajah pengguna │ └── user_id_123.jpg │ ├── 📁 <b>logs/</b> # File log eksternal (jika ada) │ └── activity_2025-05-09.csv │ └── 📁 <b>.streamlit/</b> # Konfigurasi untuk Streamlit Cloud └── config.toml </pre>


---

## 🧠 Arsitektur Sistem FacePay
Sistem ini dibagi menjadi dua peran utama: User dan Admin, dengan proses yang saling terhubung menggunakan pengenalan wajah, verifikasi PIN, dan manajemen log berbasis SQLite.

┌──────────────────────┐
│    📷 Webcam Input    │
└────────┬─────────────┘
         ▼
┌────────────────────────────┐
│ 🎯 MTCNN - Deteksi Wajah   │
└────────┬───────────────────┘
         ▼
┌────────────────────────────┐
│ 🔍 FaceNet - Ekstrak       │
│     Embedding Wajah        │
└────────┬───────────────────┘
         ▼
┌────────────────────────────┐
│ 🔐 Pencocokan Embedding    │◄──────────────┐
│ atau Verifikasi PIN (6 digit)            │
└────────┬───────────────────┘             │
         ▼                                 │
┌────────────────────────────┐             │
│ 💳 Proses Pembayaran / Top Up │             │
└────────┬───────────────────┘             │
         ▼                                 │
┌────────────────────────────┐             │
│ 📝 Logging ke SQLite + CSV │             │
└────────┬────────────┬──────┘             │
         ▼            ▼                    │
   User Frontend   Admin Dashboard         │
   (Streamlit UI)  (Streamlit UI)          │
         │            │                    │
         ▼            ▼                    │
 [Registrasi]    [Lihat Log, Reset PIN]────┘

------------------------------------------------------------

## ⚙️ Instalasi & Setup Lokal

1. **Clone repo:**
   ```bash
   git clone https://github.com/username/facepay.git
   cd facepay

pip install -r requirements.txt

python init_db.py

streamlit run user_frontend.py

streamlit run admin_dashboard.py

## 🔒 Autentikasi
Default admin:

Username: admin

Password: admin123

Ganti password setelah deploy!

## 📸 Teknologi yang Digunakan
Streamlit

OpenCV

MTCNN (deteksi wajah)

FaceNet (embedding wajah)

SQLite + bcrypt (keamanan)

NumPy + Pandas

