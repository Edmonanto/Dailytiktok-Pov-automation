#!/usr/bin/env python3
import os, sys, json, datetime, urllib.request, urllib.error

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1").strip()
TELEGRAM_LIMIT = 4096

def fail(msg):
    print(f"ERREUR: {msg}", file=sys.stderr); sys.exit(1)

def check_env():
    missing = [n for n, v in [("OPENAI_API_KEY", OPENAI_API_KEY),
        ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)] if not v]
    if missing: fail("Secrets manquants: " + ", ".join(missing))

def http_post_json(url, payload, headers, timeout=120):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code} sur {url}: {e.read().decode('utf-8', errors='replace')}")
    except urllib.error.URLError as e:
        fail(f"Connexion echouee sur {url}: {e}")
    return {}

def build_prompt():
    today = datetime.date.today().isoformat()
    return f"""Nous sommes le {today}.
Tu produis un PACK DE CONTENU TIKTOK QUOTIDIEN, entierement EN FRANCAIS, pour un
createur qui fait des videos POV face camera sur les opportunites business.
Niches: DROPSHIPPING / e-commerce et ENTREPRENEURIAT / side hustles.

ETAPE 1 - Utilise la recherche web pour trouver UNE video courte reellement
virale/tendance maintenant (TikTok, Reels ou Shorts) liee a une vraie opportunite
business dans ces niches. Le LIEN DOIT ETRE REEL et venir de la recherche web -
n'invente JAMAIS d'URL. Varie le sujet chaque jour.

ETAPE 2 - Redige le pack dans ce format (texte simple, emojis, SANS markdown):

🎥 LA VIDEO A REFAIRE AUJOURD'HUI
<titre> — <lien reel>
<1 ligne: pourquoi elle est virale>

💡 L'OPPORTUNITE BUSINESS
- <puce 1>
- <puce 2>
- <puce 3>

🎬 TON SCRIPT POV (~35 sec)
HOOK (0-3s): "<phrase choc>" [texte a l'ecran: ...]
CORPS: "<opportunite + 1-2 etapes concretes>" [texte a l'ecran: ...]
CTA: "<appel a s'abonner / commenter>" [texte a l'ecran: ...]

#️⃣ HASHTAGS
<5 a 7 hashtags>

📌 ASTUCE DE PUBLICATION
<un conseil rapide>

Reponds UNIQUEMENT avec le pack, rien d'autre."""

def generate_pack():
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": OPENAI_MODEL, "tools": [{"type": "web_search_preview"}], "input": build_prompt()}
    result = http_post_json("https://api.openai.com/v1/responses", payload, headers)
    text = result.get("output_text")
    if isinstance(text, str) and text.strip(): return text.strip()
    chunks = []
    for item in result.get("output", []) or []:
        if item.get("type") == "message":
            for c in item.get("content", []) or []:
                if c.get("type") in ("output_text", "text") and isinstance(c.get("text"), str):
                    chunks.append(c["text"])
    if chunks: return "\n".join(chunks).strip()
    fail("Reponse OpenAI inattendue: " + json.dumps(result)[:1500])

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}
    parts = [text[i:i+TELEGRAM_LIMIT] for i in range(0, len(text), TELEGRAM_LIMIT)] or [text]
    for part in parts:
        resp = http_post_json(url, {"chat_id": TELEGRAM_CHAT_ID, "text": part,
            "disable_web_page_preview": False}, headers, timeout=30)
        if not resp.get("ok"): fail("Envoi Telegram echoue: " + json.dumps(resp)[:1000])
    print("Pack envoye sur Telegram OK")

def main():
    check_env()
    pack = generate_pack()
    print(pack)
    send_telegram(pack)

if __name__ == "__main__":
    main()
