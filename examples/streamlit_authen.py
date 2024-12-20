import streamlit as st
import speech_recognition as sr
import tempfile

def audio_to_text(file_path):
    """Convert audio to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="vi-VN")
            return text
    except sr.UnknownValueError:
        return "Không thể nhận diện âm thanh."
    except sr.RequestError as e:
        return f"Lỗi kết nối: {e}"

# Streamlit UI
st.title("Ghi âm và chuyển âm thanh thành văn bản")

# Record audio using st.audio_input
audio_file = st.audio_input("Nhấn để ghi âm bằng micro:")

if audio_file:
    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_file.read())
        temp_file_path = temp_file.name

    # Play the recorded audio
    st.audio(temp_file_path, format="audio/wav")

    # Convert audio to text
    st.info("Đang xử lý âm thanh...")
    text_result = audio_to_text(temp_file_path)
    st.success("Hoàn tất chuyển đổi!")
    st.text_area("Văn bản từ giọng nói:", value=text_result, height=200)
