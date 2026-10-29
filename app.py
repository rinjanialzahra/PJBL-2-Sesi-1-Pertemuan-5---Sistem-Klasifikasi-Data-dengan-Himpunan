
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sistem Klasifikasi Himpunan",
    page_icon="📊",
    layout="wide"
)

# =====================================
# 1. DATASET MAHASISWA
# =====================================
data = [
    {"ID": "M01", "Nama": "Andi",  "Nilai": 85, "Organisasi": "Ya",   "Kepanitiaan": "Tidak"},
    {"ID": "M02", "Nama": "Bunga", "Nilai": 75, "Organisasi": "Ya",   "Kepanitiaan": "Ya"},
    {"ID": "M03", "Nama": "Citra", "Nilai": 90, "Organisasi": "Tidak", "Kepanitiaan": "Ya"},
    {"ID": "M04", "Nama": "Dimas", "Nilai": 65, "Organisasi": "Tidak", "Kepanitiaan": "Tidak"},
    {"ID": "M05", "Nama": "Eka",   "Nilai": 88, "Organisasi": "Ya",   "Kepanitiaan": "Ya"},
    {"ID": "M06", "Nama": "Fajar", "Nilai": 72, "Organisasi": "Tidak", "Kepanitiaan": "Tidak"},
    {"ID": "M07", "Nama": "Gina",  "Nilai": 80, "Organisasi": "Ya",   "Kepanitiaan": "Tidak"},
    {"ID": "M08", "Nama": "Hadi",  "Nilai": 92, "Organisasi": "Tidak", "Kepanitiaan": "Ya"},
    {"ID": "M09", "Nama": "Intan", "Nilai": 78, "Organisasi": "Ya",   "Kepanitiaan": "Tidak"},
    {"ID": "M10", "Nama": "Joko",  "Nilai": 68, "Organisasi": "Tidak", "Kepanitiaan": "Ya"},
]

df = pd.DataFrame(data)

# =====================================
# 2. MEMBENTUK HIMPUNAN
# =====================================
U = set(df["ID"])

A = set(df.loc[df["Nilai"] >= 80, "ID"])
B = set(df.loc[df["Organisasi"] == "Ya", "ID"])
C = set(df.loc[df["Kepanitiaan"] == "Ya", "ID"])

himpunan = {
    "A": A,
    "B": B,
    "C": C
}

nama_himpunan = {
    "A": "Nilai minimal 80",
    "B": "Aktif organisasi",
    "C": "Ikut kepanitiaan"
}

# =====================================
# 3. JUDUL DAN PENJELASAN
# =====================================
st.title("📊 Sistem Klasifikasi Data dengan Himpunan")
st.write(
    "Aplikasi PJBL-2 untuk mengelompokkan data mahasiswa "
    "dan menjalankan operasi himpunan."
)

st.info(
    "A = Nilai minimal 80 | "
    "B = Aktif organisasi | "
    "C = Ikut kepanitiaan"
)

# =====================================
# 4. MENAMPILKAN DATASET
# =====================================
st.header("1. Dataset Mahasiswa")
st.dataframe(df, use_container_width=True)

# Tombol mengunduh dataset
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Unduh Dataset CSV",
    data=csv,
    file_name="mahasiswa.csv",
    mime="text/csv"
)

# =====================================
# 5. MENAMPILKAN ANGGOTA HIMPUNAN
# =====================================
st.header("2. Daftar Anggota Himpunan")

kolom = st.columns(3)

for i, kode in enumerate(["A", "B", "C"]):
    anggota = sorted(himpunan[kode])

    with kolom[i]:
        st.subheader(f"Himpunan {kode}")
        st.caption(nama_himpunan[kode])
        st.write(", ".join(anggota) if anggota else "Tidak ada anggota")
        st.metric("Jumlah anggota", len(anggota))

# =====================================
# 6. MEMILIH OPERASI HIMPUNAN
# =====================================
st.header("3. Operasi Himpunan")

operasi = st.selectbox(
    "Pilih operasi:",
    [
        "Union (Gabungan)",
        "Intersection (Irisan)",
        "Difference (Selisih)",
        "Complement (Komplemen)"
    ]
)

hasil = set()
penjelasan = ""

if operasi == "Complement (Komplemen)":
    pilihan = st.selectbox(
        "Pilih himpunan yang akan dicari komplemennya:",
        ["A", "B", "C"]
    )

    hasil = U - himpunan[pilihan]
    penjelasan = f"{pilihan}ᶜ = U - {pilihan}"

else:
    pilihan1 = st.selectbox(
        "Pilih himpunan pertama:",
        ["A", "B", "C"],
        key="himpunan1"
    )

    pilihan2 = st.selectbox(
        "Pilih himpunan kedua:",
        ["A", "B", "C"],
        index=1,
        key="himpunan2"
    )

    if operasi == "Union (Gabungan)":
        hasil = himpunan[pilihan1] | himpunan[pilihan2]
        penjelasan = f"{pilihan1} ∪ {pilihan2}"

    elif operasi == "Intersection (Irisan)":
        hasil = himpunan[pilihan1] & himpunan[pilihan2]
        penjelasan = f"{pilihan1} ∩ {pilihan2}"

    elif operasi == "Difference (Selisih)":
        hasil = himpunan[pilihan1] - himpunan[pilihan2]
        penjelasan = f"{pilihan1} - {pilihan2}"

# =====================================
# 7. MENAMPILKAN HASIL OPERASI
# =====================================
st.header("4. Hasil Operasi")

if st.button("Proses Operasi", type="primary"):
    hasil_urut = sorted(hasil)

    st.subheader(f"Hasil: {penjelasan}")
    st.write("Anggota himpunan hasil:")

    if hasil_urut:
        hasil_df = df[df["ID"].isin(hasil_urut)].copy()
        hasil_df = hasil_df.sort_values("ID")

        st.dataframe(hasil_df, use_container_width=True)
    else:
        st.warning("Hasil operasi tidak memiliki anggota.")

    st.metric("Jumlah anggota hasil", len(hasil))

    st.success("Operasi himpunan berhasil diproses.")

# =====================================
# 8. RINGKASAN
# =====================================
st.header("5. Ringkasan Dataset")

c1, c2, c3 = st.columns(3)

c1.metric("Himpunan semesta (U)", len(U))
c2.metric("Total data mahasiswa", len(df))
c3.metric("Kategori himpunan", 3)

st.caption(
    "PJBL-2 | Sistem Klasifikasi Data dengan Himpunan | Python"
)
