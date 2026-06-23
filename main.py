import asyncio
import ccxt.async_support as ccxt
import logging
import database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def detect_support_resistance(ohlc_data):
    """Logika SnR: Mendeteksi level berdasarkan High/Low lokal."""
    highs = [candle['high'] for candle in ohlc_data]
    lows = [candle['low'] for candle in ohlc_data]
    return {"support": min(lows), "resistance": max(highs)}

async def fetch_and_analyze(symbol):
    """Fungsi worker: Tarik data riil dan analisis paralel."""
    exchange = ccxt.binance()
    try:
        # Tarik data dari Binance
        ohlcv = await exchange.fetch_ohlcv(symbol, '1h', limit=50)
        await exchange.close()
        
        data = [{'high': c[2], 'low': c[3]} for c in ohlcv]
        snr = detect_support_resistance(data)
        
        # Money Management: 10% dari $100 modal
        modal = 100.0
        posisi = modal * 0.10
        
        # Logika Sederhana Hybrid Weapon V3 (Entry di Support)
        current_price = data[-1]['high'] 
        if current_price <= snr['support'] * 1.01: # Margin 1% dekat support
            logging.info(f"Robot AQT BUY SIGNAL: {symbol} | SnR: {snr['support']} | Size: ${posisi:.2f}")
        
        return symbol
    except Exception as e:
        logging.error(f"Error pada {symbol}: {e}")
        return None

async def main_loop():
    coins = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']
    while True:
        logging.info("Robot AQT: Memulai siklus analisis paralel...")
        tasks = [fetch_and_analyze(symbol) for symbol in coins]
        await asyncio.gather(*tasks)
        await asyncio.sleep(60) # Jeda antar siklus agar tidak kena limit API

if __name__ == "__main__":
    database.init_db()
    asyncio.run(main_loop())
