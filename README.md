# AI Vision Assist

**AI Vision Assist** is a multi-language assistive app for visually impaired individuals that extracts text from images, reads it aloud, and describes scenes using Google Gemini AI.

---

## Features

- Upload image
- Optical Character Recognition (OCR) in English, Hindi, Tamil, Telugu
- Text-to-Speech in multiple languages (English, Hindi, Tamil, Telugu)
- Scene description powered by Gemini AI
- Download extracted text and audio
- Streamlit web interface

---

## Tech Stack

- Streamlit
- PyTesseract (OCR)
- gTTS (TTS)
- Google Generative AI (Gemini)
- Python Dotenv

---

## How to Run

```bash
git clone https://github.com/shailylitoriya/ai_vision_assist.git
cd ai_vision_assist
pip install -r requirements.txt
```

**Set your Gemini API key in .env:**
GOOGLE_API_KEY=your_api_key_here

**Then run the app:**
streamlit run ai_vision_assist.py

---

## Deployment
You can deploy this app for free on Streamlit Cloud. Make sure to set your GOOGLE_API_KEY as a secret in the cloud settings.

---

## Author
Made with ❤️ by Shaily Litoriya
[GitHub](https://github.com/shailylitoriya) [LinkedIn](www.linkedin.com/in/shailylitoriya)