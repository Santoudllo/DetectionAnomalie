import json
import boto3
import streamlit as st
import os
from datetime import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, InvalidRegionError

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_REGION_NAME = os.getenv('S3_REGION_NAME')

# Initialisation du client S3 avec boto3.client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION_NAME
)

def upload_feedback_to_s3(username, feedback):
    """
    Envoie le feedback de l'utilisateur à un bucket S3.
    """
    try:
        # Créez un nom de fichier basé sur le nom d'utilisateur et la date
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'{username}_{timestamp}.txt'

        content = f"Nom d'utilisateur: {username}\nFeedback: {feedback}"

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=content,
            ContentType='text/plain'
        )

        st.success('Feedback envoyé avec succès !')
    except NoCredentialsError:
        st.error("Aucune information d'identification AWS fournie.")
    except PartialCredentialsError:
        st.error("Informations d'identification AWS partielles fournies.")
    except InvalidRegionError:
        st.error(f"Nom de région invalide : {S3_REGION_NAME}")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

def show_feedback():
    """
    Affiche un formulaire pour envoyer des commentaires.
    """

    st.title("💬 Feedback des Utilisateurs")
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Vous pouvez envoyer vos commentaire via ce formulaire.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Formulaire de feedback avec bordures personnalisées
    name = st.text_input("Votre nom")
    feedback = st.text_area("Vos commentaires / suggestions")


    if st.button("Envoyer le Feedback"):
        if name and feedback:
            upload_feedback_to_s3(name, feedback)
        else:
            st.error("Veuillez remplir tous les champs avant de soumettre.")

    st.image("https://cdn-icons-png.flaticon.com/512/1256/1256650.png", width=100, caption="Feedback Utilisateurs")

