import ctypes
import os
import re
import google.generativeai as genai

# Incarcam libraria compilata pe Mac M1
lib_path = os.path.abspath('./libcrypto.dylib')
crypto_lib = ctypes.CDLL(lib_path)
crypto_lib.encrypt_data.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

MASTER_KEY = b"math_secret_key_2026"
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Te rog seteaza GEMINI_API_KEY in terminal! (ex: export GEMINI_API_KEY='cheia_ta')")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.5-flash')

def secure_pipeline(prompt):
    secrets = re.findall(r'\[(.*?)\]', prompt)
    masked_prompt = prompt
    
    for idx, secret in enumerate(secrets):
        input_bytes = secret.encode('utf-8')
        output_buffer = ctypes.create_string_buffer(len(input_bytes) + 1)
        
        crypto_lib.encrypt_data(input_bytes, output_buffer, MASTER_KEY)
        
        placeholder = f"{{ENCRYPTED_DATA_BLOCK_{idx}}}"
        masked_prompt = masked_prompt.replace(f"[{secret}]", placeholder)
        
    return masked_prompt

def ask_agent(prompt):
    safe_prompt = secure_pipeline(prompt)
    response = model.generate_content(safe_prompt)
    return safe_prompt, response.text