import os
import json
import openai
import streamlit as st
from dotenv import load_dotenv

# Chargement de la clé API OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fichier stockage images générées
IMAGES_DB = "generated_images.json"

# Fonction pour charger la liste des images
def load_images():
    if os.path.exists(IMAGES_DB):
        with open(IMAGES_DB, "r") as f:
            return json.load(f)
    return []

# Fonction pour sauvegarder une nouvelle image
def save_image(url):
    images = load_images()
    images.append(url)
    with open(IMAGES_DB, "w") as f:
        json.dump(images, f)

# --- Configuration de la page ---
st.set_page_config(page_title="DALL·E Trhacknon Generator", layout="centered")

# Barre latérale menu
page = st.sidebar.selectbox("Navigation", ["Générateur", "Admin"])

# === PAGE ADMIN ===
if page == "Admin":
    st.title("🔐 Page Admin - Images générées")

    # Simple login (pour exemple)
    login = st.text_input("Login", value="", key="login")
    password = st.text_input("Mot de passe", type="password", key="password")

    # Hardcoded credentials (à changer en prod!)
    ADMIN_LOGIN = "admin"
    ADMIN_PASSWORD = "trhacknon123"

    if st.button("Se connecter"):
        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            st.success("Connexion réussie ! Voici toutes les images générées :")

            images = load_images()
            if images:
                for i, url in enumerate(images, 1):
                    st.image(url, caption=f"Image #{i}", use_container_width=True)
                    st.markdown(f"[Lien direct]({url})")
            else:
                st.info("Aucune image générée pour le moment.")
        else:
            st.error("Login ou mot de passe incorrect.")

# === PAGE GENERATEUR ===
if page == "Générateur":
    # ... Ton code actuel sans rien changer ...

    # CSS personnalisé
    with open("assets/style.css") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

    # ❄️ Neige de fond
    st.snow()
    spinner_html = """
    <div class="spinner-anonymous">
      <img src="https://github.com/trh4ckn0n/trkn-gen/raw/refs/heads/main/assets/68747470733a2f2f74476a3552794b2e706e67.png" alt="Anonymous">
    </div>
    """
    st.markdown(spinner_html, unsafe_allow_html=True)
    # Audio ambiant
    audio_html = """
    <audio autoplay loop>
      <source src="https://h.top4top.io/m_3457nnrbo0.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
    # Titre glitch
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

                # Sauvegarde dans le fichier JSON
                save_image(image_url)

                st.balloons()

            except Exception as e:
                st.error(f"💥 Erreur lors de la génération : {e}")
