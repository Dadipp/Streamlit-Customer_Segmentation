import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
from sklearn.preprocessing import StandardScaler

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/superstore_2.csv", parse_dates=["order_date"])
    return df

# --- Load Model ---
@st.cache_resource
def load_model():
    with open("models/kmeans_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model


# Load data dan model
df = load_data()
model = load_model()

# --- Sidebar Navigasi ---
st.sidebar.header("Navigasi")
page = st.sidebar.radio("Pilih Halaman", [
    "Overview Data", "Analisis RFM", "Customer Clustering",
    "Demographic Segmentation", "Behavioral Segmentation"
])

# --- Sidebar Filter ---
st.sidebar.markdown("### Filter Data")
df['year'] = df['order_date'].dt.year
year_options = ['All'] + sorted(df['year'].unique().tolist())
selected_year = st.sidebar.selectbox("Pilih Tahun", year_options, index=0)
selected_region = st.sidebar.selectbox("Pilih Region", ['All'] + sorted(df['region'].unique()))

filtered_df = df.copy()
if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['year'] == selected_year]
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['region'] == selected_region]

# --- Hitung RFM ---
snapshot_date = filtered_df['order_date'].max() + pd.Timedelta(days=1)
rfm = filtered_df.groupby('customer_id').agg({
    'order_date': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'nunique',
    'sales': 'sum'
}).reset_index().rename(columns={
    'order_date': 'Recency',
    'order_id': 'Frequency',
    'sales': 'Monetary'
})

# --- Overview Data ---
if page == "Overview Data":
    st.title("📦 Overview Customer Order Data")
    st.markdown("Tinjauan umum terhadap data transaksi pelanggan.")

    st.dataframe(filtered_df.head(), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📟 Jumlah Transaksi", filtered_df['order_id'].nunique())
    with col2:
        st.metric("👥 Jumlah Pelanggan", filtered_df['customer_id'].nunique())
    with col3:
        st.metric("💰 Total Penjualan", f"${filtered_df['sales'].sum():,.2f}")

    sales_trend = filtered_df.groupby('order_date')['sales'].sum().reset_index()
    fig = px.line(sales_trend, x='order_date', y='sales',
                  title="📈 Tren Penjualan Harian",
                  labels={'sales': 'Total Penjualan', 'order_date': 'Tanggal'})
    st.plotly_chart(fig, use_container_width=True)

# --- Analisis RFM ---
elif page == "Analisis RFM":
    st.title("📊 RFM Analysis")
    st.markdown("Analisis pelanggan berdasarkan Recency, Frequency, dan Monetary.")

    st.dataframe(rfm.head(), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(px.histogram(rfm, x='Recency', nbins=30, title="Distribusi Recency"), use_container_width=True)
    with col2:
        st.plotly_chart(px.histogram(rfm, x='Frequency', nbins=30, title="Distribusi Frequency"), use_container_width=True)
    with col3:
        st.plotly_chart(px.histogram(rfm, x='Monetary', nbins=30, title="Distribusi Monetary"), use_container_width=True)

    st.markdown("### 🌟 Segmentasi Heuristik Berdasarkan Recency")
    rfm['Segment'] = pd.cut(
        rfm['Recency'],
        bins=[-1, 30, 90, 180, np.inf],
        labels=['Power User', 'Loyal User', 'New User', 'Churned User']
    )

    fig = px.box(rfm, x='Segment', y='Monetary', color='Segment',
                 title="Distribusi Monetary per Segment RFM")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 Insight Segmentasi RFM")
    st.markdown("""
        - **Churned User**: Pelanggan yang sudah lama tidak melakukan pembelian, kontribusi rendah.
        - **Power User**: Pelanggan baru yang melakukan pembelian besar dalam waktu dekat.
        - **Loyal User**: Pelanggan yang belanja secara konsisten dan kontributif.
        - **New User**: Pelanggan baru yang masih perlu dikembangkan loyalitasnya.
            """)



# --- Customer Clustering ---
elif page == "Customer Clustering":
    st.title("🧩 Customer Segmentation via K-Means Clustering")
    st.markdown("Cluster pelanggan berdasarkan nilai RFM.")

    features = ['Recency', 'Frequency', 'Monetary']
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[features])
    rfm['Cluster'] = model.predict(rfm_scaled)

    fig = px.scatter_3d(rfm, x='Recency', y='Frequency', z='Monetary',
                        color=rfm['Cluster'].astype(str),
                        title="📍 Visualisasi Klaster Pelanggan (3D)",
                        labels={'Cluster': 'Klaster'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📌 Statistik RFM per Klaster")
    st.dataframe(rfm.groupby('Cluster')[features].mean().round(1), use_container_width=True)

    # --- Insight Otomatis ---
    st.markdown("### 🔐 Insight Otomatis dari Klaster")
    cluster_stats = rfm.groupby('Cluster')[features].mean()
    best_cluster = cluster_stats['Monetary'].idxmax()
    low_recency_cluster = cluster_stats['Recency'].idxmin()

    st.success(f"💡 Cluster {best_cluster} memiliki nilai *Monetary* tertinggi (${cluster_stats.loc[best_cluster, 'Monetary']:.2f}).")
    st.info(f"📉 Cluster {low_recency_cluster} memiliki *Recency* terendah ({cluster_stats.loc[low_recency_cluster, 'Recency']:.0f} hari), menandakan pelanggan paling aktif.")

    # --- Download CSV ---
    csv = rfm.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📅 Download Hasil Klaster CSV",
        data=csv,
        file_name='customer_cluster_result.csv',
        mime='text/csv'
    )

# --- Demographic Segmentation ---
elif page == "Demographic Segmentation":
    st.title("🌍 Demographic Segmentation")
    st.markdown("Analisis berdasarkan atribut demografis pelanggan.")

    fig1 = px.pie(filtered_df, names='segment', title="Distribusi Tipe Pelanggan")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.treemap(filtered_df, path=['region', 'country'], values='sales',
                      title="Penjualan Berdasarkan Region dan Negara")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("### 🧠 Insight Demografi")
    st.markdown("""
    - Mayoritas pelanggan berasal dari segmen **Consumer**, menunjukkan dominasi pasar B2C (retail).
    - **Corporate** dan **Home Office** juga memberikan kontribusi signifikan, cocok untuk pendekatan B2B.
    - Region **West** dan **East** terlihat memiliki volume penjualan yang lebih tinggi dibandingkan region lainnya.
    - Segmentasi ini dapat dimanfaatkan untuk menyusun strategi pemasaran yang lebih relevan secara geografis maupun jenis pelanggan.
    """)



# --- Behavioral Segmentation ---
elif page == "Behavioral Segmentation":
    st.title("🧠 Behavioral Segmentation")
    st.markdown("Segmentasi berdasarkan perilaku transaksi pelanggan.")

    behavior = filtered_df.groupby('customer_id').agg({
        'order_id': 'nunique',
        'product_name': pd.Series.nunique
    }).rename(columns={
        'order_id': 'Total_Orders',
        'product_name': 'Unique_Products'
    }).reset_index()

    behavior['Behavior'] = pd.cut(
        behavior['Total_Orders'],
        bins=[-1, 2, 5, 10, np.inf],
        labels=['Single Purchase', 'Frequent Buyer', 'Loyal Buyer', 'Power Buyer']
    )

    st.dataframe(behavior.head(), use_container_width=True)

    fig = px.histogram(behavior, x='Behavior', color='Behavior',
                       title="Distribusi Perilaku Pelanggan",
                       labels={'Behavior': 'Kategori Perilaku'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("### 🧠 Insight Perilaku Pembelian")
    st.markdown("""
    - **Loyal Buyer** merupakan kelompok terbanyak, menunjukkan banyak pelanggan yang rutin melakukan pembelian.
    - **Frequent Buyer** menunjukkan potensi untuk dijadikan **Loyal Buyer** melalui retensi dan penawaran.
    - **Power Buyer** sedikit tapi berpotensi tinggi — bisa dijadikan target campaign eksklusif.
    - **Single Purchase** cukup besar jumlahnya, menandakan perlu pendekatan untuk meningkatkan retensi pelanggan ini.
    """)


