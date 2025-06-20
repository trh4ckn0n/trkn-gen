import os
import sqlite3
import openai
import streamlit as st
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime

# --- Initialisation ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_FILE = "app_data.db"
ph = PasswordHasher()

# Connexion DB (création si pas existante)
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Création tables si pas existantes
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    created_at TEXT NOT NULL
);
""")
conn.commit()

# Création user admin (à lancer une fois)
def create_admin_user():
    username = "admin"
    password = os.getenv("ADMIN_PASSWORD")
    if not password:
        raise ValueError("ADMIN_PASSWORD manquant dans le fichier .env")
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone() is None:
        password_hash = ph.hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        print(f"Admin user '{username}' créé avec le mot de passe issu de .env")

create_admin_user()

# --- Fonctions ---

def verify_password(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if row:
        try:
            ph.verify(row[0], password)
            return True
        except VerifyMismatchError:
            return False
    return False

def save_image(url):
    now = datetime.utcnow().isoformat()
    cursor.execute("INSERT INTO images (url, created_at) VALUES (?, ?)", (url, now))
    conn.commit()

def get_all_images():
    cursor.execute("SELECT id, url, created_at FROM images ORDER BY id DESC")
    return cursor.fetchall()

def delete_image(image_id):
    cursor.execute("DELETE FROM images WHERE id=?", (image_id,))
    conn.commit()

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Streamlit App ---

st.set_page_config(page_title="DALL·E Trhacknon Generator", layout="centered")

page = st.sidebar.selectbox("Navigation", ["Générateur", "Admin"])

if page == "Admin":
    st.title("🔐 Page Admin - Images générées")

    if not st.session_state.logged_in:
        with st.form("login_form"):
            username = st.text_input("Login")
            password = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter")
            if submitted:
                if verify_password(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Bienvenue {username} !")
                    st.experimental_rerun()
                else:
                    st.error("Login ou mot de passe incorrect.")
    else:
        st.write(f"Connecté en tant que : {st.session_state.username}")
        if st.button("Se déconnecter"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

        images = get_all_images()
        if images:
            for img_id, url, created_at in images:
                st.image(url, caption=f"Image #{img_id} générée le {created_at}", use_container_width=True)
                st.markdown(f"[Lien direct]({url})")
                if st.button(f"Supprimer l'image #{img_id}"):
                    delete_image(img_id)
                    st.success(f"Image #{img_id} supprimée")
                    st.experimental_rerun()
        else:
            st.info("Aucune image générée pour le moment.")

if page == "Générateur":
    # --- Ton code actuel, inchangé ---
    if os.path.exists("assets/style.css"):
        with open("assets/style.css") as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)

    st.snow()
    spinner_html = """
    <div class="spinner-anonymous">
      <img src="https://github.com/trh4ckn0n/trkn-gen/raw/refs/heads/main/assets/68747470733a2f2f74476a3552794b2e706e67.png" alt="Anonymous">
    </div>
    """
    st.markdown(spinner_html, unsafe_allow_html=True)
    audio_html = """
    <audio autoplay loop>
      <source src="https://h.top4top.io/m_3457nnrbo0.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
    st.markdown("<h1 class='title glitch-effect'>⚔️ DALL·E 3 - Trhacknon Image Generator</h1>", unsafe_allow_html=True)
    st.toast("⚡ FCK Israhell", icon="👾")
    st.markdown(":rainbow[Stop the war!!]")

    theme = st.selectbox("🎯 Thème principal", [
        "Cyberwar & Anonymous", "Street Art contre Fake News", "Surveillance & Résistance", "Désinformation Iranienne", "Autre"
    ])

    if theme == "Autre":
        theme = st.text_input("Tape ton propre thème")

    style = st.selectbox("🎨 Style visuel", [
        "Graffiti fluo sur fond sombre",
        "Illustration dystopique",
        "Style comics cyberpunk",
        "Photomontage réaliste",
        "Pixel art"
    ])

    message = st.text_input("🧠 Message ou slogan à afficher", value="La vraie menace, c’est l’ignorance programmée.")
    signature = st.text_input("✍️ Signature dans l’image (ex: trhacknon)", value="trhacknon")

    prompt = f"""
    A powerful {style} in the theme of {theme}, featuring an anonymous hacker character, military elements,
    neon digital codes, graffiti slogans saying: '{message}'.
    Dark background, green/black/red contrast, matrix style, digital anarchy.
    {'Add signature: ' + signature if signature else ''}
    """

    if st.button("🚀 Générer l’image avec DALL·E 3"):
        with st.spinner("😈 Génération image en cours..."):
            st.markdown(spinner_html, unsafe_allow_html=True)
            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                    response_format="url"
                )
                image_url = response.data[0].url
                st.image(image_url, caption="🖼️ Image générée par DALL·E 3", use_container_width=True)
                st.markdown(f"[💾 Télécharger l'image]({image_url})")

                save_image(image_url)

                st.balloons()

            except Exception as e:
                st.error(f"💥 Erreur lors de la génération : {e}")
