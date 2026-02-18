import google.generativeai as genai

# Your API Key
API_KEY = "AIzaSyCIJjV6wVstDJkjkNzN4t2tpzs1tnLZGiw"

# Configure
genai.configure(api_key=API_KEY)

# List all available models
print("Available Gemini Models:")
print("=" * 50)
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Methods: {model.supported_generation_methods}")
        print("-" * 50)
