import keyboard
import pandas as pd

# Membaca data dari file CSV
dataByPlace = pd.read_excel('data/scrapetable_wisata.xlsx')
dfNew = pd.read_csv('data/filtered_byPlaceData.csv')

# Filter data yang tidak ada di dfByPlace berdasarkan kolom 'name'
unpickedData = dataByPlace[~dataByPlace['name'].str.lower().isin(dfNew['name'].str.lower())]

# Pastikan unpickedData tidak kosong
if unpickedData.empty:
    print("No rows to process in unpickedData.")
else:
    # Inisialisasi iterator untuk unpickedData
    row_iterator = unpickedData.iterrows()
    current_row = next(row_iterator, None)  # Mengambil baris pertama

    # Fungsi untuk menampilkan baris saat ini
    def print_current_row(row):
        if row is not None:
            index, data = row
            print(f"Current Row: {index}, Name: {data['name']}, Address: {data['full_address']}")
        else:
            print("No more rows to process.")

    # Fungsi untuk menambahkan baris ke dataByPlace
    def add_row_to_dfByPlace(row):
        global dfNew
        if row is not None:
            index, data = row
            # Menambahkan baris ke dataByPlace
            dfNew = pd.concat([dfNew, pd.DataFrame([data])], ignore_index=True)
            print(f"Added row: {data['name']} to dfNew")
            dfNew.to_csv('data/filtered_byPlaceData.csv')
        else:
            print("No row to add.")

    # Fungsi untuk pindah ke baris berikutnya
    def move_next():
        global current_row, row_iterator
        current_row = next(row_iterator, None)  # Ambil baris berikutnya
        if current_row is not None:
            print_current_row(current_row)
        else:
            print("Reached the end of unpickedData")

    # Event listener untuk tombol enter untuk menambahkan baris
    keyboard.add_hotkey('enter', lambda: [add_row_to_dfByPlace(current_row), move_next()])

    # Event listener untuk tombol spasi untuk melewati baris dan pindah ke berikutnya
    keyboard.add_hotkey('space', move_next)

    # Menampilkan baris pertama
    print_current_row(current_row)

    # Menjaga program tetap berjalan hingga tombol 'esc' ditekan untuk keluar
    print("Press 'enter' to add row to dataByPlace or 'space' to skip. Use 'esc' to exit.")
    keyboard.wait('esc')
