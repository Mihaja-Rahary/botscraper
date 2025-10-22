# config.py

# -----------------------------
# Token Telegram
# -----------------------------
# Récupéré depuis @BotFather
BOT_TOKEN = "8096060900:AAGpN9DL9fsBK6mTYfNlOElgzrfz4McJSX0"  # <- remplace par ton token

# -----------------------------
# Login Instagram pour le scraping
# -----------------------------
INSTAGRAM_USERNAME = "luzyponty"   # compte Instagram pour le scraping
INSTAGRAM_PASSWORD = "0TSxzVgyeubeyhlr"

# -----------------------------
# Paramètres du scraper
# -----------------------------
HEADLESS = True            # True = navigateur invisible
MAX_POSTS = 15             # Nombre maximum de posts à récupérer
SLEEP_AFTER_NAV = 2        # Secondes d'attente après navigation

# -----------------------------
# Paramètres optionnels
# -----------------------------
NAV_TIMEOUT = 60000        # Temps max pour navigation (ms)
OUTPUT_CSV = "results_instagram.csv"   # si tu veux sauvegarder localement les résultats
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
