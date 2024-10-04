import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Fungsi-fungsi utama yang digunakan
def get_total_count_by_hour_df(hour_df):
    return hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})

def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dteday").agg({"registered": "sum"})
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dteday").agg({"casual": "sum"})
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

def sum_order(hour_df):
    return hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()

def macem_season(day_df): 
    return day_df.groupby(by="season").count_cr.sum().reset_index()

# Membaca file CSV
days_df = pd.read_csv("day_clean.csv")
hours_df = pd.read_csv("hour_clean.csv")

# Mengonversi kolom datetime
days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

# Mengurutkan data
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)
hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

# Rentang tanggal
min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()
min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

# Sidebar untuk memilih rentang waktu
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )
  
# Filter data berdasarkan rentang tanggal
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & (hours_df["dteday"] <= str(end_date))]

# Memanggil fungsi untuk mendapatkan data yang diperlukan
hour_count_df = get_total_count_by_hour_df(main_df_hour)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')
st.header('Come if You Need a Bike')

col1, col2, col3 = st.columns(3)
 
# Menghitung total orders secara langsung dari main_df_days
with col1:
    total_orders = main_df_days["count_cr"].sum()
    st.metric("Total Sharing Bike", value=total_orders)

# Menggunakan data dari reg_df untuk total registered
with col2:
    total_sum = reg_df["register_sum"].sum()
    st.metric("Total Registered", value=total_sum)

# Menggunakan data dari cas_df untuk total casual
with col3:
    total_sum = cas_df["casual_sum"].sum()
    st.metric("Total Casual", value=total_sum)

# Visualisasi jam penyewaan sepeda
st.subheader("Pada jam berapa sepeda paling banyak disewa dan paling sedikit disewa?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Barplot untuk jam dengan banyak penyewaan sepeda
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
# Barplot untuk jam dengan sedikit penyewaan sepeda
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.caption('Berikut adalah hasil analysys data menunjukan bahwa sepeda paling banyak disewa pukul 17.00 dan paling sedikit pukul 4')

# Visualisasi penyewaan per musim
st.subheader("pada musim apa sepeda paling banyak disewa orang?")
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="count_cr", 
    x="season",
    data=season_df.sort_values(by="season", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.caption('Berikut adalah daftar pada musim apa orang banyak menyewa sepeda, pada musim fall dengan jumlah penyewa mencapai 1061129')
