import os
import requests
import json
from dotenv import load_dotenv

# Load konfigurasi dari file .env
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    print("[-] Error: OPENROUTER_API_KEY tidak ditemukan di file .env")
    exit(1)

# Default model
current_model = "google/gemini-2.5-flash-free"

system_prompt = {
    "role": "system",
    "content": "Anda adalah SS-AI, Asisten Penetration Testing yang dikembangkan oleh Indrayaza Z. "
               "Anda HARUS mematuhi Rules of Engagement (RoE): "
               "1. Hanya edukasi, metodologi, dan skrip untuk defensif/audit legal. "
               "2. Ingatkan perlunya otorisasi tertulis. "
               "3. Tolak peretasan target spesifik atau malware destruktif tanpa konteks edukasi. "
               "4. Fokus pada OWASP Top 10, MITRE ATT&CK, dan audit standar."
}

messages = [system_prompt]

print("="*55)
print("  SS-AI: Ethical Pentest Assistant (CLI Mode)")
print("  Coded by: Indrayaza Z")
print("="*55)
print(f"  [*] Model aktif : {current_model}")
print("  [*] Ketik '/model <nama_model>' untuk ganti model.")
print("  [*] Ketik 'exit' atau 'quit' untuk keluar.")
print("="*55)

while True:
    user_input = input("\n[User] > ")
    
    # Deteksi perintah keluar
    if user_input.lower() in ['exit', 'quit']:
        print("[*] Exiting SS-AI...")
        break
        
    # Deteksi perintah ganti model
    if user_input.lower().startswith('/model'):
        parts = user_input.split()
        if len(parts) > 1:
            current_model = parts[1]
            print(f"[+] Model berhasil diubah menjadi: {current_model}")
        else:
            print("[!] Daftar model gratis OpenRouter yang direkomendasikan:")
            print("    - google/gemini-2.5-flash-free")
            print("    - meta-llama/llama-3-8b-instruct:free")
            print("    - mistralai/mistral-7b-instruct:free")
            print("    - gryphe/mythomax-l2-13b:free")
            print("    Cara pakai: /model <nama_model>")
        continue

    if not user_input.strip():
        continue

    messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/indrayaza/SS-AI",
        "X-Title": "SS-AI Pentest Assistant"
    }

    payload = {
        "model": current_model,
        "messages": messages
    }

    try:
        print(f"[*] SS-AI ({current_model}) sedang memproses...")
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        
        if response.status_code == 200:
            ai_reply = response_data['choices'][0]['message']['content']
            print(f"\n[SS-AI]\n{ai_reply}")
            messages.append({"role": "assistant", "content": ai_reply})
        else:
            print(f"[-] API Error: {response_data}")
    except Exception as e:
        print(f"[-] Terjadi kesalahan: {e}")
