import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Mendapatkan direktori kerja saat ini
currentDir = os.getcwd()

# Membuat jalur absolut menggunakan os.path.join
file_path = os.path.join(currentDir, 'data', 'fixedData.csv')

# Membaca file fixedData.csv menggunakan jalur absolut yang sudah dibentuk
fixedDf = pd.read_csv(file_path)

# Ambil nilai unik dari kolom 'types' dan drop NaN
unique_types = fixedDf['types'].dropna().unique()

# Menggunakan TF-IDF untuk merepresentasikan teks sebagai vektor
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(unique_types)

# Menggunakan KMeans untuk mengelompokkan nilai-nilai yang mirip
num_clusters = 20  # Anda bisa menyesuaikan jumlah cluster
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(tfidf_matrix)

# Membuat DataFrame untuk menyimpan hasil cluster
clustered_df = pd.DataFrame({'type': unique_types, 'cluster': kmeans.labels_})

# Membuat dictionary untuk setiap cluster
cluster_representatives = {}

# Pilih perwakilan dari setiap cluster (nilai yang paling umum/representatif dalam cluster)
for i in range(num_clusters):
    cluster_types = clustered_df[clustered_df['cluster'] == i]['type'].values
    cluster_representatives[i] = cluster_types[0]  # Misal, pilih item pertama sebagai representatif

# Tampilkan perwakilan setiap cluster
print("Cluster Representatives:")
for cluster, representative in cluster_representatives.items():
    print(f"Cluster {cluster}: {representative}")

# Membuat TF-IDF untuk kolom lain (misalnya 'name' atau 'address') sebagai fitur untuk baris NaN
def get_closest_cluster(row, cluster_representatives):
    # Vectorize nilai 'name' atau kolom lain untuk mencari kemiripan
    if pd.isna(row['types']):
        text = row['name']  # Anda bisa juga menggunakan 'address' atau kombinasi
        vector = tfidf.transform([text])  # Konversi teks ke vektor menggunakan TF-IDF
        similarities = kmeans.transform(vector)  # Menghitung jarak ke setiap cluster
        closest_cluster = np.argmin(similarities)  # Cluster terdekat
        return cluster_representatives[closest_cluster]  # Return perwakilan cluster terdekat
    else:
        return row['types']

# Simpan semua baris yang memiliki NaN di kolom 'types' sebelum pengisian
nan_rows_before = fixedDf[fixedDf['types'].isna()].copy()

# Terapkan fungsi ke dataframe untuk mengisi nilai NaN pada kolom 'types'
fixedDf['types'] = fixedDf.apply(lambda row: get_closest_cluster(row, cluster_representatives), axis=1)

# Buat DataFrame baru untuk validasi, berisi hanya data yang semula memiliki NaN
validation_df = nan_rows_before.copy()
validation_df['types_filled'] = validation_df.apply(lambda row: get_closest_cluster(row, cluster_representatives), axis=1)

# Simpan DataFrame validasi ke dalam CSV
# validation_file_path = os.path.join(currentDir, 'data', 'validation_filled_types.csv')
# validation_df.to_csv(validation_file_path, index=False)

# Simpan hasil akhir ke file yang sama (menimpa file asli)
fixedDf.to_csv(file_path, index=False)

# Tampilkan beberapa baris hasil untuk verifikasi
print("Validation DataFrame (only rows with NaN previously):")
print(validation_df[['name', 'types_filled']].head())
