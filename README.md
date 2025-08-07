# 🧠 Customer Segmentation Dashboard

## 📌 Overview

Aplikasi ini adalah dashboard interaktif berbasis **Streamlit** untuk melakukan **segmentasi pelanggan** menggunakan pendekatan **RFM (Recency, Frequency, Monetary)** dan **K-Means Clustering**. Aplikasi ini membantu tim marketing dan manajemen untuk memahami perilaku pelanggan dan membuat strategi yang lebih terfokus.

Dashboard mencakup:
- Tinjauan data transaksi pelanggan
- Analisis RFM
- Segmentasi pelanggan otomatis dengan K-Means
- Segmentasi berdasarkan demografi (region, country, segment)
- Segmentasi berdasarkan perilaku pembelian (jumlah transaksi, variasi produk)

📂 Dataset: `superstore_2.csv`  
👉 [**Buka Aplikasi**](https://app-customer-segmentation.streamlit.app)

---

## 📊 Fitur Dashboard

- **Overview Data**  
  - Jumlah transaksi, pelanggan, penjualan total  
  - Tren penjualan harian

- **RFM Analysis**  
  - Distribusi nilai *recency*, *frequency*, dan *monetary*  
  - Segmentasi heuristik berbasis skor RFM

- **Customer Clustering**  
  - Segmentasi otomatis menggunakan K-Means berdasarkan fitur RFM  
  - Visualisasi klaster dan interpretasi profil masing-masing klaster

- **Demographic Segmentation**  
  - Analisis pelanggan berdasarkan region, negara, dan segmen bisnis

- **Behavioral Segmentation**  
  - Kategori pembeli berdasarkan jumlah transaksi & jumlah produk unik

- **Export Data**  
  - Unduh hasil segmentasi pelanggan dalam format CSV

---

## 💡 Insight

Dashboard ini memberikan berbagai insight yang dapat digunakan untuk meningkatkan efektivitas strategi pemasaran dan retensi pelanggan, seperti:

- **Klaster pelanggan aktif**: pelanggan dengan *recency* rendah dan *frequency* tinggi, cocok untuk program loyalitas.
- **Power buyers**: pelanggan dengan *monetary* tinggi yang berpotensi dijadikan brand ambassador atau VIP customer.
- **One-time buyers**: pelanggan dengan hanya satu transaksi—perlu pendekatan retargeting atau promosi khusus.
- **Segmentasi regional**: membantu melihat performa penjualan di tiap negara/region dan menyesuaikan pendekatan lokal.
- **Analisis variasi produk**: mengidentifikasi pelanggan yang suka beragam produk vs pelanggan yang hanya beli satu jenis produk.

Insight-insight ini dapat digunakan untuk:
- Menentukan target campaign yang lebih tepat sasaran  
- Menyesuaikan penawaran produk/layanan berdasarkan profil pelanggan  
- Meningkatkan customer lifetime value (CLV)

---

## ✍️ Author

Created by **Dimas Adi Prasetyo**  
Bootcamp Project – **Customer Analytics and Segmentation**
