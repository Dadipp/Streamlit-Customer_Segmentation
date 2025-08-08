# 🧠 Customer Segmentation Dashboard

An interactive **Streamlit** application for analyzing and segmenting customers based on transaction data.  
This dashboard provides insights through **RFM Analysis**, **K-Means Clustering**, and segmentation by **Demographics** and **Behavior**.

---

## 📌 Link Streamlit
🔗 [Open Streamlit App](https://app-customer-segmentation.streamlit.app)

---

## 📖 Project Overview

**Objective:**  
To help businesses understand their customers better by segmenting them into meaningful groups.  
This segmentation enables more targeted marketing strategies, improved customer retention, and better resource allocation.

**Main Features:**
- **Overview Data**: Summary of transactions, customers, and sales trends.
- **RFM Analysis**: Segmentation based on Recency, Frequency, and Monetary value.
- **Customer Clustering**: K-Means clustering with interactive 3D visualization.
- **Demographic Segmentation**: Insights based on customer type, region, and country.
- **Behavioral Segmentation**: Classification based on purchase frequency and diversity.

---

## 📂 Dataset

- **File**: `superstore_2.csv`  
- **Size**: ~999 rows (example)  
- **Key Columns**:
  - `order_date`
  - `region`
  - `country`
  - `customer_id`
  - `segment`
  - `sales`
  - `order_id`
  - `product_name`

---

## 📊 Features in Detail

### 1. Overview Data
- Table preview of transaction data.
- KPIs: Total Transactions, Number of Customers, Total Sales.
- Daily sales trend chart.

### 2. RFM Analysis
- Calculation of **Recency**, **Frequency**, **Monetary**.
- Histograms for each RFM metric.
- Segmentation into: `Power User`, `Loyal User`, `New User`, `Churned User`.
- Boxplot to compare segments.

### 3. Customer Clustering
- Standardization of RFM features.
- K-Means clustering model (pre-trained `kmeans_model.pkl`).
- 3D scatter plot visualization.
- Downloadable clustering results.

### 4. Demographic Segmentation
- Pie chart of customer types.
- Treemap of sales by region and country.
- Geographic and segment insights.

### 5. Behavioral Segmentation
- Classification: `Single Purchase`, `Frequent Buyer`, `Loyal Buyer`, `Power Buyer`.
- Histogram of behavioral categories.

---

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **Pandas**, **NumPy**
- **Plotly**
- **scikit-learn**
- **Pickle**
