import streamlit as st
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Image Processing with RGB Sliders and Histogram")

# Sidebar untuk memilih fitur
feature = st.sidebar.selectbox(
    "Choose a feature",
    ("Upload Image", "Grayscale", "Edge Detection", "RGB Adjustment")
)

# Fungsi untuk meng-upload gambar
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Menampilkan gambar yang di-upload
    image = Image.open(uploaded_file)
    image_array = np.array(image)

    # Fungsi untuk menampilkan histogram
    def plot_histogram(image, title="Histogram"):
        fig, ax = plt.subplots()
        if len(image.shape) == 2:  # Grayscale
            ax.hist(image.ravel(), bins=256, color='gray')
        else:  # RGB
            colors = ('r', 'g', 'b')
            for i, color in enumerate(colors):
                ax.hist(image[:, :, i].ravel(), bins=256, color=color, alpha=0.5)
        ax.set_title(title)
        ax.set_xlabel("Pixel Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    # Layout kolom untuk gambar asli dan hasil pengolahan
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, caption="Original Image", use_column_width=True)
        st.write("Histogram of Original Image")
        plot_histogram(image_array, "Histogram - Original Image")

    # Fitur berdasarkan pilihan pengguna
    if feature == "Grayscale":
        # Konversi ke grayscale
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        with col2:
            st.image(gray_image, caption="Grayscale Image", use_column_width=True)
            st.write("Histogram of Grayscale Image")
            plot_histogram(gray_image, "Histogram - Grayscale")

    elif feature == "Edge Detection":
        # Slider untuk threshold deteksi tepi Canny
        threshold1 = st.sidebar.slider("Threshold 1", min_value=0, max_value=255, value=100)
        threshold2 = st.sidebar.slider("Threshold 2", min_value=0, max_value=255, value=200)

        # Konversi ke grayscale sebelum deteksi tepi
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

        # Deteksi tepi
        edges = cv2.Canny(gray_image, threshold1=threshold1, threshold2=threshold2)
        with col2:
            st.image(edges, caption="Edge Detection", use_column_width=True)
            st.write("Histogram of Edge Detection")
            plot_histogram(edges, "Histogram - Edge Detection")

    elif feature == "RGB Adjustment":
        # Slider untuk mengatur intensitas masing-masing kanal RGB
        r_factor = st.sidebar.slider("Red Intensity", min_value=0, max_value=255, value=255)
        g_factor = st.sidebar.slider("Green Intensity", min_value=0, max_value=255, value=255)
        b_factor = st.sidebar.slider("Blue Intensity", min_value=0, max_value=255, value=255)

        # Mengubah intensitas kanal warna
        adjusted_image = image_array.copy()
        adjusted_image[:, :, 0] = np.clip(adjusted_image[:, :, 0] * (r_factor / 255), 0, 255)
        adjusted_image[:, :, 1] = np.clip(adjusted_image[:, :, 1] * (g_factor / 255), 0, 255)
        adjusted_image[:, :, 2] = np.clip(adjusted_image[:, :, 2] * (b_factor / 255), 0, 255)

        with col2:
            st.image(adjusted_image.astype(np.uint8), caption="RGB Adjusted Image", use_column_width=True)
            st.write("Histogram of RGB Adjusted Image")
            plot_histogram(adjusted_image, "Histogram - RGB Adjusted Image")
