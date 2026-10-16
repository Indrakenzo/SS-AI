import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    print("[-] Error: OPENROUTER_API_KEY tidak ditemukan di file .env")
    exit(1)

current_model = "nvidia/nemotron-3.5-lightning:free"

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
    
    if user_input.lower() in ['exit', 'quit']:
        print("[*] Exiting SS-AI...")
        break
        
    if user_input.lower().startswith('/model'):
        parts = user_input.split()
        if len(parts) > 1:
            current_model = parts[1]
            print(f"[+] Model berhasil diubah menjadi: {current_model}")
        else:
            print("[!] Daftar model gratis OpenRouter yang tersedia:")
            print("    - nvidia/nemotron-3.5-lightning:free")
            print("    - openrouter/free")
            print("    - poolside/laguna-s-2.1:free")
            print("    - dots-studio/dots-3-note-preview:free")
            print("    - nvidia/nemotron-3-super-120b-a12b:free")
            print("    - apodex/apodex-1.1-mini:free")
            print("    - thinkingmachines/inkling:free")
            print("    - cohere/north-mini-code:free")
            print("    - thinkingmachines/inkling-small:free")
            print("    - poolside/laguna-xs-2.1:free")
            print("    - nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free")
            print("    - inception/mercury-decide:free")
            print("    - liquid/lfm-2.5-2.6b:free")
            print("    - nvidia/llama-nemotron-rerank-vl-1b-v2:free")
            print("    - nvidia/nemotron-3.5-content-safety:free")
            print("    - nvidia/nemotron-3-embed-1b:free")
            print("    - google/gemma-4-26b-a4b-it:free")
            print("    - nvidia/llama-nemotron-embed-vl-1b-v2:free")
            print("    - google/gemma-4-31b-it:free")
            print("    - respan/span-01-lite:free")
            print("    - liquid/lfm-2.5-embedding-350m:free")
            print("    - fish-audio/s2.1-pro-free:free")
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
