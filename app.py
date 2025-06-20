# app.py

import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Chargement de la clé API OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration de la page
st.set_page_config(page_title="DALL·E CyberWar Generator", layout="centered")

# CSS personnalisé
with open("assets/style.css") as f:
    css = f"<style>{f.read()}</style>"
    st.markdown(css, unsafe_allow_html=True)

# ❄️ Neige de fond
st.snow()

# 🎵 Audio ambiant / Intro hacker theme
st.markdown("### 🎧 Ambiance sonore cyberpunk")
audio_file = open("assets/Deep Secrets.mp3", "rb")  # ← mets ta musique dans ce fichier
st.audio(audio_file.read(), format="audio/mp3")

# Titre glitch
st.markdown("<h1 class='title glitch-effect'>⚔️ DALL·E 3 - Cyberwar Image Generator</h1>", unsafe_allow_html=True)
st.toast("⚡ FCK Israhell", icon="👾")
st.markdown(":rainbow[Stop the war!!]")

# 🎙️ Entrée audio optionnelle
# st.markdown("#### 🗣️ Enregistrer une idée vocale pour l’inspiration (optionnel)")
# audio = st.audio(st.audio_input("Enregistre ton idée"), format="audio/wav")

# 📸 Choix utilisateur
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

# 🔮 Prompt final
prompt = f"""
A powerful {style} in the theme of {theme}, featuring an anonymous hacker character, military elements,
neon digital codes, graffiti slogans saying: '{message}'.
Dark background, green/black/red contrast, matrix style, digital anarchy.
{'Add signature: ' + signature if signature else ''}
"""

# 🚀 Lancement de génération
if st.button("🚀 Générer l’image avec DALL·E 3"):
    with st.spinner("🧠 Génération cyberpunk en cours..."):
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

            # 🎉 Animation après succès
            st.balloons()

        except Exception as e:
            st.error(f"💥 Erreur lors de la génération : {e}")
