import pandas as pd
import keyboard
dataByPlace = 'data/byPlaceData.csv'
dfByPlace = pd.read_csv(dataByPlace)

# Tentukan range data yang ingin diiterasi (misal: setengah dari total data)
total_rows = len(dfByPlace)
half_range =  10  # Mengambil setengah dari total datatotal_rows // 2

# Ambil subset dari DataFrame berdasarkan range yang diinginkan
df_subset = dfByPlace.iloc[:half_range]  # Mengambil baris dari indeks 0 hingga half_range


# List untuk menyimpan indeks baris yang dipilih untuk dipertahankan
rows_to_keep = []

print("Mulai iterasi melalui setiap baris. Tekan Enter untuk mempertahankan, Backspace untuk menghapus.")

# Iterasi melalui setiap baris dalam subset DataFrame
for index, row in df_subset.iterrows():
    print(f"Nama: {row['name']}")

    # Menunggu input dari keyboard
    while True:
        if keyboard.read_event().event_type == 'down':  # Menunggu tombol ditekan
            if keyboard.is_pressed('enter'):
                print("Dipertahankan.")
                rows_to_keep.append(index)  # Menyimpan indeks baris yang dipertahankan
                break  # Keluar dari loop dan lanjutkan ke baris berikutnya

            elif keyboard.is_pressed('backspace'):
                print("Dihapus.")
                break  # Keluar dari loop dan lanjutkan ke baris berikutnya

# Memfilter DataFrame berdasarkan baris yang dipertahankan
dfFiltered = dfByPlace.loc[rows_to_keep]
dfFiltered.to_csv('data/coba1.csv')
