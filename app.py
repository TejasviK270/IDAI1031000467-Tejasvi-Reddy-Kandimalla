import google.generativeai as genai

genai.configure(api_key="AIzaSyBlJ0FSupoYW8NrsxXsZQyDehDLzbwV-N4")

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
