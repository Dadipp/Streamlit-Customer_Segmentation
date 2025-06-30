import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import pickle

@st.cache_data
def load_data():
    df = pd.read_csv("E:\VScode\HANDSON_32B\my_portfolio\Customer_Segmentation\data\superstore_2.csv", parse_dates=["order_date"])
    return df

df = load_data()
st.title("Customer Segmentation with Machine Learning")
st.dataframe(df.head())


st.subheader("Feature Engineering: RFM")

snapshot_date = df['order_date'].max() + pd.Timedelta(days=1)
rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'count',
    'sales': 'sum'
}).rename(columns={
    'order_date': 'Recency',
    'order_id': 'Frequency',
    'sales': 'Monetary'
}).reset_index()


st.dataframe(rfm.head())

st.subheader("Standardisasi Fitur")

features = ['Recency', 'Frequency', 'Monetary']
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[features])

st.subheader("Clustering dengan K-Means")

k = st.slider("Pilih jumlah klaster:", 2, 10, 4)
model = KMeans(n_clusters=k, random_state=42)
rfm['Cluster'] = model.fit_predict(rfm_scaled)
st.dataframe(rfm.head())

st.subheader("Visualisasi Klaster")

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='tab10', ax=ax)
st.pyplot(fig)

with open("E:\VScode\HANDSON_32B\my_portfolio\Customer_Segmentation\models\kmeans_model.pkl", "wb") as f:
    pickle.dump(model, f)