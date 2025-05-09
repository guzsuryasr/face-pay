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

facepay/
│
├── user_frontend.py # GUI untuk pengguna (registrasi, bayar, top up)
├── admin_dashboard.py # Dashboard admin
├── user_db.py # Logika backend pengguna & admin
├── init_db.py # Setup database SQLite awal
├── embeddings_db.npy # Embedding wajah
├── users.json # Metadata pengguna
├── requirements.txt # Dependensi
├── README.md
│
├── assets/ # Foto wajah pengguna
├── logs/ # (Opsional) Log file eksternal
└── .streamlit/
└── config.toml # Konfigurasi Streamlit Cloud


---

## ⚙️ Instalasi & Setup Lokal

1. **Clone repo:**
   ```bash
   git clone https://github.com/username/facepay.git
   cd facepay

pip install -r requirements.txt

python init_db.py

streamlit run user_frontend.py

streamlit run admin_dashboard.py

🔒 Autentikasi
Default admin:

Username: admin

Password: admin123

Ganti password setelah deploy!

☁️ Deploy ke Streamlit Cloud
Buat repo GitHub

Upload semua file

Di Streamlit Cloud, klik "New App"

Pilih repo, set user_frontend.py atau admin_dashboard.py sebagai entrypoint

Jalankan dan uji!

📸 Teknologi yang Digunakan
Streamlit

OpenCV

MTCNN (deteksi wajah)

FaceNet (embedding wajah)

SQLite + bcrypt (keamanan)

NumPy + Pandas

