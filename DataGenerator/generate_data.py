import pandas as pd
import random
from datetime import datetime, timedelta



# Daftar cabang
cabang = ['Cafe Mall Kokas', 'Cafe Perumahan Cijantung', 'Cafe Kantor SCBD', 'Cafe Perumahan Tebet']
# Daftar produk
produk = ['Kopi Susu Gula Aren', 'Americano', 'Cappuccino', 'Cafe Latte', 'Milk Tea']
# Harga produk (Anda bisa sesuaikan)
harga = [25000, 20000, 22000, 23000, 21000]

# Buat dataframe kosong
data = []

# Generate data sebanyak 5000 baris
for _ in range(5000):
    tanggal = '2023-11-20'  # Ganti dengan tanggal yang diinginkan
    cabang_random = random.choice(cabang)
    produk_random = random.choice(produk)
    harga_random = harga[produk.index(produk_random)]
    jumlah_terjual = random.randint(10, 100)
    data.append([tanggal, cabang_random, produk_random, harga_random, jumlah_terjual])

# Buat dataframe Pandas
df = pd.DataFrame(data, columns=['Tanggal', 'Cabang', 'Nama Produk', 'Harga per Produk', 'Jumlah Terjual'])


def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date
# Tentukan rentang tanggal (misal, 2 bulan terakhir)
end_date = datetime.now().date()
start_date = end_date - timedelta(days=60)

# Terapkan fungsi pada akolom 'Tanggal'
df['Tanggal'] = df.apply(lambda row: generate_random_date(start_date, end_date), axis=1)

def is_weekday(date):
    date_str = date.strftime('%Y-%m-%d')
    return datetime.strptime(date_str, '%Y-%m-%d').weekday() < 5

# Tambahkan kolom 'Hari'
df['is_weekday'] = df['Tanggal'].apply(is_weekday)

# Tingkatkan penjualan di Cafe Mall Kokas dan Cafe Kantor SCBD pada weekday
df.loc[(df['Cabang'] == 'Cafe Mall Kokas') & (df['is_weekday']), 'Jumlah Terjual'] *= 3
df.loc[(df['Cabang'] == 'Cafe Kantor SCBD') & (df['is_weekday']), 'Jumlah Terjual'] *= 3

df.loc[(df['Cabang'] == 'Cafe Perumahan Cijantung') & (df['is_weekday']==False), 'Jumlah Terjual'] *= 2
df.loc[(df['Cabang'] == 'Cafe Perumahan Tebet') & (df['is_weekday']==False), 'Jumlah Terjual'] *= 2


print(df.head())


# Simpan data ke file CSV
df.to_csv('data_penjualan_kopi.csv', index=False)