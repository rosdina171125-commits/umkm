import streamlit as st
import pandas as pd
import pydeck as pdk

# ============================================================
# KONFIGURASI APLIKASI
# ============================================================
st.set_page_config(page_title="Peta UMKM Sulawesi Barat", layout="wide")

st.title("🗺️ Aplikasi Peta UMKM Sulawesi Barat")
st.write("Peta ini menampilkan lokasi UMKM di Sulawesi Barat.")

# ============================================================
# DATA UMKM (TANPA KONTAK)
# ============================================================
data_umkm = [
    ["UMKM Kopi Lembang", "Kuliner", "Mamasa", "Lembang, Mamasa", -2.9435, 119.3670],
    ["UMKM Sarabba Polewali", "Minuman", "Polewali Mandar", "Polewali", -3.4325, 119.3439],
    ["UMKM Kerajinan Anyaman", "Kerajinan", "Majene", "Banggae, Majene", -3.5400, 118.9700],
    ["UMKM Ikan Asap Tande", "Kuliner", "Mamuju", "Tande, Mamuju", -2.6800, 118.8900],
    ["UMKM Kue Kering Sande", "Kuliner", "Mamuju", "Simboro, Mamuju", -2.6500, 118.9000],
    ["UMKM Tenun Tradisional", "Kerajinan", "Polewali Mandar", "Binuang, Polman", -3.4820, 119.2920],
    ["UMKM Oleh-oleh Majene", "Oleh-oleh", "Majene", "Pusat Kota Majene", -3.5420, 118.9730],
    ["UMKM Rumput Laut Pasangkayu", "Pertanian & Perikanan", "Pasangkayu", "Pasangkayu", -1.1960, 119.3630],
    ["UMKM Keripik Pisang Topoyo", "Snack", "Mamuju Tengah", "Topoyo, Mateng", -2.1190, 119.3610],
    ["UMKM Kopi Tapalang", "Minuman", "Mamuju", "Tapalang, Mamuju", -2.7590, 118.7990]
]

columns = ["nama", "kategori", "kabupaten", "alamat", "latitude", "longitude"]
df = pd.DataFrame(data_umkm, columns=columns)

# ============================================================
# SIDEBAR FILTER
# ============================================================
st.sidebar.header("🔍 Filter UMKM")

kabupaten_list = ["Semua"] + sorted(df["kabupaten"].unique())
kategori_list = ["Semua"] + sorted(df["kategori"].unique())

pilih_kabupaten = st.sidebar.selectbox("Pilih Kabupaten:", kabupaten_list)
pilih_kategori = st.sidebar.selectbox("Pilih Kategori Usaha:", kategori_list)
keyword = st.sidebar.text_input("Cari Nama UMKM:")

df_filtered = df.copy()

if pilih_kabupaten != "Semua":
    df_filtered = df_filtered[df_filtered["kabupaten"] == pilih_kabupaten]

if pilih_kategori != "Semua":
    df_filtered = df_filtered[df_filtered["kategori"] == pilih_kategori]

if keyword:
    df_filtered = df_filtered[df_filtered["nama"].str.contains(keyword, case=False)]

# ============================================================
# METRIK
# ============================================================
col1, col2, col3 = st.columns(3)
col1.metric("Total UMKM", len(df))
col2.metric("UMKM Terfilter", len(df_filtered))
col3.metric("Jumlah Kabupaten", df["kabupaten"].nunique())

st.write("---")

# ============================================================
# PETA MENGGUNAKAN PYDECK (TIDAK PERLU INSTALL)
# ============================================================
st.subheader("📍 Peta Lokasi UMKM")

if not df_filtered.empty:
    view_state = pdk.ViewState(
        latitude=df_filtered["latitude"].mean(),
        longitude=df_filtered["longitude"].mean(),
        zoom=7,
        pitch=0
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        df_filtered,
        get_position='[longitude, latitude]',
        get_radius=4000,
        get_fill_color=[0, 100, 255, 180],
        pickable=True
    )

    tooltip = {
        "html": "<b>{nama}</b><br/>Kategori: {kategori}<br/>Kabupaten: {kabupaten}<br/>Alamat: {alamat}",
        "style": {"color": "white"}
    }

    map_render = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )

    st.pydeck_chart(map_render)
else:
    st.warning("Tidak ada data UMKM sesuai filter.")

# ============================================================
# TABEL DATA
# ============================================================
st.subheader("📄 Data UMKM")
st.dataframe(df_filtered.reset_index(drop=True))



