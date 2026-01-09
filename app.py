import streamlit as st
import pandas as pd
import plotly.express as px
import os # Library untuk membaca lokasi file sistem

# ==========================================
# 1. KONFIGURASI HALAMAN (PAGE CONFIG)
# ==========================================
st.set_page_config(
    page_title="Dashboard Marketing - Velvet Apparel",
    page_icon="👕",
    layout="wide"
)

# ==========================================
# 2. LOAD DATASET (DENGAN PERBAIKAN PATH)
# ==========================================
@st.cache_data
def get_data():
    try:
        # Mencari lokasi absolut di mana file app.py ini berada
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Menggabungkan lokasi folder dengan nama file CSV
        # Ini memastikan file tetap ketemu meskipun dijalankan dari terminal yang berbeda
        file_path = os.path.join(current_dir, 'velvet_apparel_ads_data.csv')
        
        # Membaca file CSV
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return None

# Panggil fungsi load data
df = get_data()

# Validasi jika file tidak ditemukan
if df is None:
    st.error("⚠️ File 'velvet_apparel_ads_data.csv' tidak ditemukan!")
    st.info("Pastikan file CSV berada di dalam folder yang sama dengan app.py")
    st.stop()

# ==========================================
# 3. SIDEBAR (FILTER DATA)
# ==========================================
st.sidebar.header("🎛️ Filter Dashboard")

# A. Filter Platform
platform_list = df['Platform'].unique().tolist()
selected_platform = st.sidebar.multiselect(
    "Pilih Platform:",
    options=platform_list,
    default=platform_list
)

# B. Filter Kategori
category_list = df['Category'].unique().tolist()
selected_category = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=category_list,
    default=category_list
)

# C. Filter Rentang Tanggal
min_date = df['Date'].min()
max_date = df['Date'].max()
start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu:",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# --- LOGIKA FILTERING ---
df_selection = df.query(
    "Platform == @selected_platform & Category == @selected_category & Date >= @start_date & Date <= @end_date"
)

# Cek jika data kosong setelah difilter
if df_selection.empty:
    st.warning("Data tidak ditemukan dengan filter yang Anda pilih. Silakan atur ulang filter.")
    st.stop()

# ==========================================
# 4. DASHBOARD UTAMA (MAIN PAGE)
# ==========================================
st.title("👕 Executive Dashboard: Velvet Apparel")
st.markdown("Laporan Kinerja Digital Marketing Tahunan (Annual Report 2025)")
st.markdown("---")

# --- BAGIAN A: KPI CARDS (METRIK UTAMA) ---
st.subheader("📌 Key Performance Indicators (KPI)")

# Perhitungan Metrik Total
total_cost = df_selection['Cost'].sum()
total_revenue = df_selection['Revenue'].sum()
total_conversions = df_selection['Conversions'].sum()
total_clicks = df_selection['Clicks'].sum()

# Menghindari pembagian dengan nol (Zero Division Error)
roi = ((total_revenue - total_cost) / total_cost) * 100 if total_cost > 0 else 0
avg_cpc = total_cost / total_clicks if total_clicks > 0 else 0

# Tampilan 5 Kolom KPI
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Biaya Iklan", f"Rp {total_cost:,.0f}")
col2.metric("Total Pendapatan", f"Rp {total_revenue:,.0f}")
col3.metric("Keuntungan Bersih", f"Rp {total_revenue - total_cost:,.0f}")
col4.metric("ROI Marketing", f"{roi:.1f}%")
col5.metric("Avg. CPC", f"Rp {avg_cpc:,.0f}")

st.markdown("---")

# --- BAGIAN B: GRAFIK VISUALISASI (BARIS 1) ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Tren Pendapatan vs Biaya (Harian)")
    # Grouping data per hari
    daily_trend = df_selection.groupby('Date')[['Cost', 'Revenue']].sum().reset_index()
    
    fig_trend = px.line(
        daily_trend, 
        x='Date', 
        y=['Revenue', 'Cost'],
        markers=True,
        color_discrete_map={'Revenue': '#2ecc71', 'Cost': '#e74c3c'}, # Hijau & Merah
        labels={'value': 'Rupiah', 'variable': 'Metrik'}
    )
    st.plotly_chart(fig_trend, width="stretch")

with col_right:
    st.subheader("📊 Efisiensi Platform Iklan")
    # Grouping data per platform
    platform_perf = df_selection.groupby('Platform')[['Cost', 'Revenue']].sum().reset_index()
    platform_melt = platform_perf.melt(id_vars='Platform', value_vars=['Cost', 'Revenue'], var_name='Metric', value_name='Amount')
    
    fig_bar = px.bar(
        platform_melt, 
        x='Platform', 
        y='Amount', 
        color='Metric', 
        barmode='group',
        text_auto='.2s',
        color_discrete_map={'Revenue': '#2ecc71', 'Cost': '#e74c3c'}
    )
    st.plotly_chart(fig_bar, width="stretch")

# --- BAGIAN C: GRAFIK VISUALISASI (BARIS 2) ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("🥧 Kontribusi Pendapatan per Kategori")
    fig_pie = px.pie(
        df_selection, 
        values='Revenue', 
        names='Category', 
        hole=0.4, # Donut Chart
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_pie, width="stretch")

with col4:
    st.subheader("📋 10 Transaksi Terakhir")
    
    # Ambil 10 data terbaru berdasarkan Tanggal dan Jam
    df_display = df_selection.sort_values(by=['Date', 'Time'], ascending=False).head(10).copy()
    
    # Ubah format kolom Date agar jam 00:00:00 hilang (hanya tanggal)
    df_display['Date'] = df_display['Date'].dt.date
    
    # Tampilkan tabel tanpa index
    st.dataframe(
        df_display,
        hide_index=True,
        use_container_width=True
    )

# ==========================================
# 5. FOOTER & DOWNLOAD
# ==========================================
st.markdown("---")
st.caption("Dashboard dikembangkan oleh Kelompok Digital Marketing TI.22.A.AI.1 - Studi Kasus: Velvet Apparel")

# Tombol Download Data
csv = df_selection.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Laporan Lengkap (CSV)",
    data=csv,
    file_name='Laporan_Annual_Velvet_Apparel_2025.csv',
    mime='text/csv',
)