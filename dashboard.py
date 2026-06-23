import streamlit as st
import sqlite3
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Robot AQT", layout="wide")

# Header & Branding
st.title("🤖 Robot Action Quant Trade")
st.markdown("### Sistem Trading Spot - AQT")

# Path Database
DB_PATH = "/app/data/aqt_database.db"

def load_data():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM stats", conn)
        conn.close()
        return df
    return None

# Menampilkan Data
data = load_data()
if data is not None:
    st.metric("Saldo Virtual (USDT)", f"{data['saldo'][0]:.2f}")
    st.metric("Profit Akumulasi", f"{data['total_profit'][0]:.2f}")
else:
    st.warning("Data AQT belum terbaca. Bot sedang inisialisasi...")

st.sidebar.info("Status: Online 24/7 - AQT Active")
