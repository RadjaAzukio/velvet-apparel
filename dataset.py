import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Konfigurasi Random Seed
np.random.seed(42)

# ==========================================
# KONFIGURASI 1 TAHUN (ANNUAL)
# ==========================================
# Kita naikkan jadi 5000 baris agar data padat sepanjang tahun
n_rows = 5000  

start_date = datetime(2025, 1, 1)  # Awal Tahun
end_date = datetime(2025, 12, 31)  # Akhir Tahun
# ==========================================

platforms = ['Instagram Ads', 'TikTok Ads', 'Google Ads']
categories = ['T-Shirt', 'Hoodie/Jacket', 'Pants', 'Accessories']

data = []

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

print(f"🔄 Sedang men-generate {n_rows} data transaksi untuk periode 1 Tahun (Jan-Des)...")

for _ in range(n_rows):
    # Buat Tanggal & Jam Acak
    date_time = random_date(start_date, end_date)
    date_only = date_time.date()
    time_only = date_time.strftime("%H:%M:%S")
    
    platform = random.choice(platforms)
    category = random.choice(categories)
    
    # Logika Angka
    if platform == 'TikTok Ads':
        impressions = np.random.randint(5000, 25000)
        cpc = np.random.uniform(500, 1200)
    elif platform == 'Google Ads':
        impressions = np.random.randint(1000, 8000)
        cpc = np.random.uniform(2500, 6000)
    else: 
        impressions = np.random.randint(3000, 18000)
        cpc = np.random.uniform(1500, 3500)
        
    ctr_rate = np.random.uniform(0.005, 0.040)
    clicks = int(impressions * ctr_rate)
    if clicks == 0: clicks = 1
        
    cost = int(clicks * cpc)
    
    cvr_rate = np.random.uniform(0.01, 0.08)
    conversions = int(clicks * cvr_rate)
    
    # Revenue
    if category == 'Hoodie/Jacket': price = 250000
    elif category == 'Pants': price = 180000
    elif category == 'T-Shirt': price = 95000
    else: price = 45000
        
    revenue = conversions * price

    data.append([date_only, time_only, platform, category, impressions, clicks, cost, conversions, revenue])

# Buat DataFrame & Shuffle
df = pd.DataFrame(data, columns=['Date', 'Time', 'Platform', 'Category', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'Revenue'])
df = df.sample(frac=1).reset_index(drop=True)

# Simpan ke file (menimpa yang lama)
filename = 'velvet_apparel_ads_data.csv'
df.to_csv(filename, index=False)

print(f"✅ SUKSES! Dataset 1 Tahun ({n_rows} baris) tersimpan sebagai: {filename}")