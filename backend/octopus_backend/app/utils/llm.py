
import google.generativeai as genai

genai.configure(api_key="-")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

