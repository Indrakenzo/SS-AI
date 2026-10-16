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

# System prompt untuk Rules of Engagement (RoE)
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

print("="*50)
print("  SS-AI: Ethical Pentest Assistant (CLI Mode)")
print("  Coded by: Indrayaza Z")
print("  Ketik 'exit' atau 'quit' untuk keluar.")
print("="*50)

while True:
    user_input = input("\n[User] > ")
    if user_input.lower() in ['exit', 'quit']:
        print("[*] Exiting SS-AI...")
        break
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
        "model": "google/gemini-2.5-flash-free",
        "messages": messages
    }

    try:
        print("[*] SS-AI sedang memproses...")
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
