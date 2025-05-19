import streamlit as st
from PIL import Image
from gtts import gTTS
import tempfile
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pytesseract

# Set Tesseract cmd and tessdata path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# Section to update api key from streamlit UI
st.sidebar.header("Update Gemini API key")
with st.sidebar.form("update_api_key_form"):
    new_api_key = st.text_input("Enter new Gemini API key: ", type="password")
    submitted = st.form_submit_button("Update API key")
    if submitted:
        if new_api_key.strip():
            try:
                with open(".env", "w") as f:
                    f.write(f"GOOGLE_API_KEY={new_api_key.strip()}\n")
                load_dotenv(override=True)
                st.success("API key updated successfully")
            except Exception as e:
                st.error(f"Error while updating API key: {e}")
        else:
            st.warning("Please enter a valid API key")

# Sidebar: OCR and TTS Language Selection
st.sidebar.markdown("----")
ocr_lang_display = st.sidebar.selectbox("Select OCR Language", ["English", "Hindi", "Tamil", "Telugu"])
ocr_lang_map = {"English": "eng", "Hindi": "hin", "Tamil": "tam", "Telugu": "tel"}
ocr_lang = ocr_lang_map[ocr_lang_display]

tts_lang_display = st.sidebar.selectbox("Select TTS Language", ["English", "Hindi", "Tamil", "Telugu"])
tts_lang_map = {"English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te"}
tts_lang = tts_lang_map[tts_lang_display]

# Load environment and get the api key
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Title of the app
st.title("AI Vision Assist")
st.write("This app helps visually impaired people understand scenes from text and images.")

# File Uploader to upload an image
uploaded_file = st.file_uploader("Upload an Image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

# Display the image if its uploaded
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
else:
    image = None

# Button to extract text
if st.button("Extract text from Image"):
    if image is not None:
        with st.spinner("Extracting text..."):
            try:
                extracted_text = pytesseract.image_to_string(image, lang=ocr_lang)
                st.subheader("Extracted Text")
                st.text_area("Result", extracted_text, height=200)
                # Download text button
                st.download_button("Download text", extracted_text, file_name="extracted_text.txt")
            except Exception as e:
                st.error(f"Error during OCR: {e}")
    else:
        st.warning("Please upload an image first.")

# Text-to-Speech function using gTTS
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# Button for text to speech
if st.button("Read Text Aloud"):
    if image is not None:
        try:
            extracted_text = pytesseract.image_to_string(image, lang=ocr_lang)
            if extracted_text.strip():
                audio_path = text_to_speech(extracted_text, lang=tts_lang)
                st.audio(audio_path, format="audio/mp3")
                st.success("Speech generated!")
                with open(audio_path, "rb") as audio_file:
                    st.download_button("⬇️ Download Audio", audio_file, file_name="speech.mp3", mime="audio/mp3")
            else:
                st.warning("No text found to read.")
        except Exception as e:
            st.error(f"Error during OCR or TTS: {e}")
    else:
        st.warning("Please upload an image first.")

# Prepare Image for Gemini API
def prepare_image(image_file):
    bytes_data = image_file.getvalue()
    image_part = {
        "mime_type": image_file.type,
        "data": bytes_data,
    }
    return image_part

# Add a Function to Describe the Scene Using Gemini
def describe_scene(image_data):
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    input_prompt = """
    You are an AI assistant helping visually impaired individuals by describing the scene in the image. 
    Provide:
    1. List of objects/items in the image and their purpose.
    2. A short summary of what’s happening in the scene.
    3. Any suggestions or safety precautions if relevant.
    """
    response = model.generate_content([input_prompt,image_data])
    return response.text

# Dummy describe_scene function when Gemini API quota exceeds and you want to test the app
# def describe_scene(image_data):
#     return "This is a sample scene description while Gemini API quota is exceeded."

# Button to Trigger Gemini Scene Description
if st.button("Describe Scene with AI"):
    if uploaded_file:
        with st.spinner("Analyzing the image..."):
            image_part = prepare_image(uploaded_file)
            result = describe_scene(image_part)
            st.subheader("Scene Description")
            st.write(result)
    else:
        st.warning("Please upload an image first.")