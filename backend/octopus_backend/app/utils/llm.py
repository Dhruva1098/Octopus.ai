import os

import google.generativeai as genai

genai.configure(api_key="AIzaSyBGBFTfLWLUbaC0lMwzGauTVqdADb6VczE")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

