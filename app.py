import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
from edukasi import waste_info

# Konfigurasi Streamlit
st.set_page_config(page_title="WasteTrack", layout="centered")
menu = st.sidebar.selectbox("Navigasi", ["Home", "Deteksi Sampah", "Jenis Sampah", "Tentang Kami"])

# Load model hanya sekali
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("garbage_classifier_model.h5")

model = load_model()
class_names = list(waste_info.keys())  # 12 kelas

# Fungsi prediksi
def predict(image):
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    max_prob = float(np.max(prediction))
    predicted_index = np.argmax(prediction)

    if max_prob < 0.6:
        return "Tidak Terdeteksi", max_prob
    else:
        return class_names[predicted_index], max_prob

# Halaman Home
if menu == "Home":
    st.title("♻️ WasteTrack: Deteksi & Edukasi Sampah")
    st.markdown("""
    Aplikasi edukatif untuk mengenali dan mengelola jenis sampah.  
    ## 🌟 Fitur
    - Deteksi gambar menjadi salah satu dari 12 jenis sampah
    - Edukasi: apakah bisa didaur ulang, kategori, dan tips pengelolaan

    ## 📸 Cara Menggunakan
    1. Masuk ke menu **Deteksi Sampah**
    2. Upload atau ambil gambar
    3. Klik **Deteksi**
    4. Dapatkan hasil dan informasi edukatif
    """)

# Halaman Deteksi
elif menu == "Deteksi Sampah":
    st.title("📰 Deteksi Jenis Sampah")

    uploaded = st.file_uploader("Upload gambar sampah", type=["jpg", "jpeg", "png"])
    camera = st.camera_input("Atau ambil gambar langsung")

    image = None
    if uploaded:
        image = Image.open(uploaded)
    elif camera:
        image = Image.open(camera)

    if image:
        st.image(image, caption="Gambar yang Anda unggah", use_column_width=True)
        if st.button("Deteksi"):
            label, confidence = predict(image)
            if label == "Tidak Terdeteksi":
                st.warning("⚠️ Sampah tidak dapat dikenali dengan cukup percaya diri.")
            else:
                st.success(f"🔍 Jenis sampah: **{label.upper()}** ({confidence*100:.2f}%)")
                info = waste_info.get(label, {})
                st.markdown(f"**♻️ Kategori**: {info.get('kategori', '-')}")
                st.markdown(f"**🔁 Daur Ulang**: {info.get('daur_ulang', '-')}")
                st.markdown(f"**📘 Edukasi**: {info.get('edukasi', '-')}")
        else:
            st.info("Klik tombol 'Deteksi' untuk memulai.")

# Halaman Jenis Sampah
elif menu == "Jenis Sampah":
    st.title("📚 Jenis Sampah & Edukasi")
    for jenis, detail in waste_info.items():
        st.subheader(jenis.capitalize())
        st.markdown(f"**Kategori**: {detail['kategori']}")
        st.markdown(f"**Daur Ulang**: {detail['daur_ulang']}")
        st.markdown(f"**Tips/Edukasi**: {detail['edukasi']}")
        st.markdown("---")

# Halaman Tentang Kami
else:
    st.title("👥 Tentang Kami")
    st.markdown("""
    Kami adalah tim mahasiswa yang peduli terhadap lingkungan dan ingin meningkatkan kesadaran masyarakat tentang pengelolaan sampah.

    **Anggota Kelompok:**
    - 🌱 Amelia Kurnia Fitri  
    - 🌱 Helvy Tiana Rosa Nabila  
    - 🌱 Ratna Maulidah Wulandari  
    - 🌱 Riska Aisyah Widyaningsari

    Terima kasih telah menggunakan WasteTrack!
    """)
