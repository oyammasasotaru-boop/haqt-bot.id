import sqlite3
import os

# Lokasi penyimpanan permanen di Railway
DB_DIR = "/app/data"
DB_PATH = os.path.join(DB_DIR, "aqt_database.db")

def init_db():
    # Pastikan folder data ada
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    # Mengaktifkan mode WAL untuk mencegah database locked/corrupt
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    
    # Tabel Stats: Menyimpan saldo dan profit (untuk tampilan dashboard)
    c.execute('''CREATE TABLE IF NOT EXISTS stats 
                 (id INTEGER PRIMARY KEY, saldo REAL, daily_profit REAL, total_profit REAL)''')
    
    # Tabel Trades: Menyimpan riwayat eksekusi (untuk grafik/history)
    c.execute('''CREATE TABLE IF NOT EXISTS trades 
                 (id INTEGER PRIMARY KEY, symbol TEXT, type TEXT, price REAL, timestamp DATETIME)''')
    
    # Pastikan record stats ada (ID 1 adalah record utama untuk AQT)
    c.execute("INSERT OR IGNORE INTO stats (id, saldo, daily_profit, total_profit) VALUES (1, 1000.0, 0.0, 0.0)")
    
    conn.commit()
    conn.close()
    print("Database AQT: Inisialisasi selesai dan siap digunakan.")

if __name__ == "__main__":
    init_db()
