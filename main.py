import time
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- SETTING STRATEGI ---
DANA_PER_LAYER = 15.0
saldo_virtual = 50.0
posisi_aktif = []

def cek_sinyal(df_m5, df_m15, df_h4):
    """Fungsi otak strategi kamu"""
    harga_live = float(df_m5['Close'].iloc[-1])
    candle_a = df_m5.iloc[-2]
    
    # Logika Rejection (Hybrid Weapon V3)
    body_size = abs(float(candle_a['Close']) - float(candle_a['Open']))
    lower_shadow = min(float(candle_a['Open']), float(candle_a['Close'])) - float(candle_a['Low'])
    is_rejection = lower_shadow >= (1.0 * body_size)
    
    # Contoh Sinyal (Sederhanakan logika fibo/bb kamu di sini)
    # Jika sinyal valid, return "BUY"
    if is_rejection:
        return "BUY"
    return None

def main():
    global saldo_virtual
    print("🚀 BOT HYBRID V3: LIVE MODE STARTED")
    
    while True:
        try:
            # 1. Fetch data singkat (5 menit terakhir)
            df = yf.download("BTC-USD", period="1d", interval="5m", progress=False)
            
            # 2. Cek Sinyal
            sinyal = cek_sinyal(df, df, df) # Sesuaikan data frame-mu
            
            # 3. Eksekusi
            if sinyal == "BUY" and len(posisi_aktif) < 2:
                jumlah_koin = DANA_PER_LAYER / float(df['Close'].iloc[-1])
                posisi_aktif.append({'harga': float(df['Close'].iloc[-1]), 'volume': jumlah_koin})
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ ENTRY: ${df['Close'].iloc[-1]:.2f}")
            
            # 4. Cek Profit (Exit)
            for p in posisi_aktif[:]:
                if float(df['Close'].iloc[-1]) > p['harga'] * 1.005: # Take Profit 0.5%
                    profit = (float(df['Close'].iloc[-1]) - p['harga']) * p['volume']
                    saldo_virtual += (p['volume'] * float(df['Close'].iloc[-1]))
                    posisi_aktif.remove(p)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 💰 EXIT PROFIT: ${profit:.4f} | Saldo: ${saldo_virtual:.2f}")

        except Exception as e:
            print(f"⚠️ Error: {e}")
        
        time.sleep(300) # Cek tiap 5 menit

if __name__ == "__main__":
    main()
