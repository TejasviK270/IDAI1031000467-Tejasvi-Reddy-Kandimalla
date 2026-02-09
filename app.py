import google.generativeai as genai

genai.configure(api_key="AIzaSyBWWER_Il5ZAwAvnVz4sznagXXVx0xfI7k")

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
