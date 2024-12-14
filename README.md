# Grootopia: Growing Roots, Optimized Tech for Perfect Yields  

Grootopia adalah aplikasi manajemen kebun yang dirancang untuk mempermudah pengelolaan informasi tanaman, catatan perkembangan, jadwal perawatan, dan pemberitahuan perawatan tanaman. 
Aplikasi ini bertujuan untuk membantu pengguna dalam meningkatkan efisiensi dan produktivitas pengelolaan kebun.  

# Fitur Utama   
1. Pengelolaan Daftar Tanaman
2. Catatan Perkembangan Tanaman
3. Pengelolaan Jadwal Perawatan
4. Pemberitahuan Perawatan

# Teknologi yang Digunakan   
• Bahasa Pemrograman: Python  
• Framework GUI: PyQt  
• Database: SQLite  
• Sistem Operasi: Windows (platform utama pengembangan)  

# Cara Instalasi  
Persyaratan Sistem:
• Python versi 3.7 atau lebih baru  
• PyQt5  
• SQLite    



## Project Structure
```
IF2150-2024-K01-G04-Grootopia/
├── src/                    # Source code
│   ├── frontend/          # Frontend components
│   │   ├── components/    # Reusable UI components
│   │   └── pages/        # Application pages
│   └── backend/           # Backend logic
├── img/                   # Image assets
├── tests/                 # Test files
├── docs/                  # Documentation
└── requirements.txt       # Python dependencies
```


## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/IF2150-2024-K01-G04-Grootopia.git
cd IF2150-2024-K01-G04-Grootopia
```

### 2. Set Up Virtual Environment
For Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

For Unix/MacOS:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python src/main.py
```
###DATABASE OVERVIEW
Database: SQLite
Nama File: grootopia.db

Terdiri dari 3 tabel utama yang saling berelasi:
- Tanaman (Menyimpan informasi dasar tanaman)
- Jadwal Perawatan (Menyimpan jadwal perawatan untuk setiap tanaman) 
- Catatan Perkembangan (Mencatat riwayat perkembangan tanaman)

================================================================================
TABLE SCHEMAS
================================================================================

1. TANAMAN
--------------------------------------------------------------------------------
CREATE TABLE tanaman (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nama            TEXT NOT NULL,           -- Nama tanaman
    waktu_tanam     DATETIME NOT NULL        -- Waktu tanaman ditanam
);

2. JADWAL PERAWATAN 
--------------------------------------------------------------------------------
CREATE TABLE jadwal_perawatan (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    deskripsi               TEXT NOT NULL,    -- Deskripsi perawatan
    waktu                   DATETIME NOT NULL, -- Waktu perawatan
    tanaman_id              INTEGER NOT NULL,  -- Foreign key ke tabel tanaman
    jenis_perawatan         TEXT NOT NULL DEFAULT 'Pemupukan',    -- Jenis perawatan
    perulangan_perawatan    TEXT NOT NULL DEFAULT 'Harian',  -- Frekuensi perawatan
    FOREIGN KEY (tanaman_id) REFERENCES tanaman(id)
);

3. CATATAN PERKEMBANGAN
--------------------------------------------------------------------------------
CREATE TABLE catatan_perkembangan (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    tanaman_id              INTEGER NOT NULL,  -- Foreign key ke tabel tanaman
    judul_catatan           TEXT NOT NULL,     -- Judul catatan
    tanggal_perkembangan    DATETIME NOT NULL, -- Tanggal pencatatan
    tinggi                  INTEGER NOT NULL,  -- Tinggi tanaman (cm)
    kondisi                 TEXT NOT NULL,     -- Kondisi tanaman
    catatan                 TEXT NOT NULL,     -- Detail catatan
    FOREIGN KEY (tanaman_id) REFERENCES tanaman(id)
);

================================================================================
RELASI ANTAR TABEL
================================================================================
- Tabel jadwal_perawatan dan catatan_perkembangan memiliki foreign key tanaman_id 
  yang merujuk ke id pada tabel tanaman
- Penghapusan data di tabel tanaman akan mempengaruhi data terkait di 
  tabel jadwal_perawatan dan catatan_perkembangan

================================================================================
FORMAT DATA
================================================================================
- Semua field DATETIME menggunakan format: 'YYYY-MM-DD HH:MM:SS'
- Jenis perawatan default: 'Pemupukan'
- Perulangan perawatan default: 'Harian'

================================================================================
DATABASE CONSTRAINTS
================================================================================
- Semua field yang ditandai NOT NULL wajib diisi
- Foreign key constraints diaktifkan untuk menjaga integritas data
- ID di semua tabel bersifat auto-increment



# Kontributor   
• Muhammad Alfansya (13523005)  
• Muhammad Raihan Nazhim Oktana (13523021)  
• Faqih Muhammad Syuhada (13523057)  
• Dzaky Aurellia Fawwaz (13523065)  
• Adinda Putri (13523071) 
