from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "HAQT Bot is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 1. Tentukan modal awal virtual kamu
virtual_balance_usdt = 1000.0  # Misal modal awal $1000
virtual_asset_amount = 0.0      # Jumlah koin yang dimiliki (awal 0)

def simulate_trade(side, price, quantity):
    global virtual_balance_usdt, virtual_asset_amount
    
    if side == "BUY":
        cost = price * quantity
        if virtual_balance_usdt >= cost:
            virtual_balance_usdt -= cost
            virtual_asset_amount += quantity
            print(f"--- SIMULASI BUY: Beli {quantity} di harga {price} ---")
            print(f"Saldo sekarang: {virtual_balance_usdt} USDT")
        else:
            print("Saldo tidak cukup untuk beli!")

    elif side == "SELL":
        if virtual_asset_amount >= quantity:
            revenue = price * quantity
            virtual_balance_usdt += revenue
            virtual_asset_amount -= quantity
            print(f"--- SIMULASI SELL: Jual {quantity} di harga {price} ---")
            print(f"Saldo sekarang: {virtual_balance_usdt} USDT")
        else:
            print("Tidak punya aset untuk dijual!")
          # --- Tes simulasi ---
# Kita coba panggil fungsi buat beli 0.1 BTC di harga $60000
simulate_trade("BUY", 60000.0, 0.1) 

# Kita coba panggil fungsi buat jual 0.05 BTC di harga $65000
simulate_trade("SELL", 65000.0, 0.05)  
