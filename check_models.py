import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyDTADt0bP6Hv5h7AHm_kAJiwgHNVkkG1Ec")

# List all available models
print("Available Gemini Models:")
print("=" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Methods: {model.supported_generation_methods}")
        print()
