from streamlit_lottie import st_lottie
import streamlit as st
import requests

# Hàm tải file Lottie JSON từ URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Tải animation từ URL
lottie_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")

st.title("Streamlit Lottie Animation Demo")
st.write("Dưới đây là một animation được nhúng từ Lottie:")

# Hiển thị animation
st_lottie(
    lottie_animation,
    speed=1,          # Tốc độ phát
    reverse=False,    # Đảo ngược animation
    loop=True,        # Lặp lại animation
    quality="high",   # Chất lượng: 'low', 'medium', 'high'
    height=400,       # Chiều cao của animation
    width=400,        # Chiều rộng của animation
    key="example_lottie"  # Khóa để nhận diện animation này
)
