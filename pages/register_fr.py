import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd


st.set_page_config(initial_sidebar_state="collapsed")

# Language settings
languages = {
	"en": "English",
	"ar": "Arabic",
	"fr": "French"
}


# Initialize session state variables
if 'logged_in' not in st.session_state:
	st.session_state.logged_in = False
if 'page' not in st.session_state:
	st.session_state.page = "home"
# Initialize language in session state
if 'language' not in st.session_state:
	st.session_state.language = 'en'

def get_page_path(page_name):
	return f"pages/{page_name}_{st.session_state.language}.py"

# Navigation function
def navigate_to(page_name):
	page_path = get_page_path(page_name)
	if os.path.exists(page_path):
		st.switch_page(page_path)
	else:
		st.error(f"Page {page_name} not found for the selected language.")


translations = {
    "en": {
        "welcome": "Welcome to:",
        "about": "About the Conference",
        "date_location": "Date and Location",
        "date_location_info": "April 23-25, 2025 | Virtual Conference",
        "schedule": "Conference Schedule",
        "speakers": "Participants",
        "register": "Register for the Conference",
		"preamble": "Conference Preamble",
        "full_name": "Full Name",
        "email": "Email Address",
        
        "affiliation": "Affiliation",
        "register_button": "Register",
        "abstract": "Abstract",
        "file_upload": "Upload Your Paper",
        "submit": "Submit Registration",
        "home": "Home",
        "language": "Language",
		"page_title":"Humanities and Social Sciences in Relation to Artificial Intelligence Research:",
		"rest_title": "Towards Responsible and Sustainable Artificial Intelligence" 
    },
    "ar": {

        "welcome": ":مرحبًا بكم",
        "about": "حول الملتقى",
        "date_location": "التاريخ والموقع",
        "date_location_info": "23-25 أبريل 2025 | مؤتمر افتراضي",
        "schedule": "جدول الملتقى",
        "speakers": "المشاركون",
        "register": "التسجيل في الملتقى",
        
		"preamble": "مقدمة الملتقى",
        "full_name": "الاسم الكامل",
        "email": "عنوان البريد الإلكتروني",
        
        "affiliation": "الانتماء",
        "abstract": "الملخص",
        "file_upload": "تحميل ورقتك البحثية",
        "submit": "إرسال التسجيل",
        "home": "الرئيسية",
        "language": "اللغة",
		"page_title": "العلوم الإنسانية والاجتماعية وعلاقتها بأبحاث الذكاء الاصطناعي:",
		"rest_title": "نحو ذكاء اصطناعي مسؤول ومستدام"
    },
    "fr": {
        
        "welcome": "Bienvenue à:",
        "about": "À propos de la conférence",
        "date_location": "Date et lieu",
        "date_location_info": "23-25 avril 2025 | Conférence virtuelle",
        "schedule": "Programme de la conférence",
        "speakers": "Conférenciers",
        "register": "Inscrivez-vous à la conférence",
        "preamble": "Préambule de la Conférence",
        "full_name": "Nom complet",
        "email": "Adresse e-mail",
        
        "affiliation": "Affiliation",
        "abstract": "Résumé",
        "file_upload": "Téléchargez votre article",
        "submit": "Soumettre l'inscription",
        "home": "Accueil",
        "language": "Langue",
		"page_title": "Sciences humaines et sociales et leur relation avec la recherche en intelligence artificielle:",
		"rest_title": "vers une intelligence artificielle responsable et durable"
    }
}

st.markdown(
    """
    <style>
    body {
        direction: """ + ('rtl' if st.session_state.language == 'ar' else 'ltr') + """;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def cycle_language():
	current_lang = st.session_state.language
	lang_codes = list(languages.keys())
	current_index = lang_codes.index(current_lang)
	next_index = (current_index + 1) % len(lang_codes)
	new_lang = lang_codes[next_index]
	
	# Clear all variables in st.session_state
	for key in list(st.session_state.keys()):
		del st.session_state[key]

	# Set the new language
	st.session_state.language = new_lang
	st.rerun()

def language_selector():
	# Create a button with a fixed width and height
	button_label = st.session_state.language.upper()  # Convert to uppercase for better visibility
	button = st.button(button_label, key="lang_button", help="Click to change language", 
					   use_container_width=False)

	if button:
		cycle_language()

# Your existing translation function
def translate(key):
	return translations[st.session_state.language].get(key, key)





# def generate_confirmation_link(email):
# 	# In a real application, use a more secure method to generate this link
# 	return f"http://yourapp.com/confirm?email={email}&token={hashlib.md5(email.encode()).hexdigest()}"






# Create a placeholder for the language selector
LANGUAGE_SELECTOR_PLACEHOLDER = ""

# Your existing navigation setup
# if not st.session_state.get('logged_in', False):
# 	nav_items = ["home", "schedule", "speakers", "login", "register",  LANGUAGE_SELECTOR_PLACEHOLDER]
# else:
# 	nav_items = ["home", "schedule", "speakers", "logout", LANGUAGE_SELECTOR_PLACEHOLDER]

nav_items = ["home","preamble", "schedule",  "register",  LANGUAGE_SELECTOR_PLACEHOLDER]
# Translate all items except the language selector placeholder
translated_nav_items = [translate(item) if item != LANGUAGE_SELECTOR_PLACEHOLDER else item for item in nav_items]

# Use st_navbar with the translated items
page = st_navbar(translated_nav_items, selected=translate("register"))

# After st_navbar, replace the placeholder with the actual language selector
for i, item in enumerate(translated_nav_items):
	if item == LANGUAGE_SELECTOR_PLACEHOLDER:
		st.write("")  # Add some space
		language_selector()
		break

# Navigation logic
if page == translate("home"):
    st.switch_page("conference_app.py")
elif page == translate("preamble"):
	navigate_to("preamble")
# elif page == translate("speakers"):
# 	navigate_to("speakers")
elif page == translate("schedule"):
	navigate_to("schedule")
# elif page == translate("login"):
# 	navigate_to("login")
# elif page == translate("logout"):
# 	navigate_to("logout")

if st.session_state.language == "en":
    navigate_to("register")
if st.session_state.language == "ar":
    navigate_to("register")

st.markdown(f"<h5 style='color:rgb(226,135,67);'>Inscrivez-vous à la conférence</h5>", unsafe_allow_html=True)



def send_email(to_email, subject, body, attachment=None):
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = st.secrets["email"]["username"]
    smtp_password = st.secrets["email"]["password"]

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment:
        with open(attachment, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
        msg.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error("Une erreur est survenue lors de l'envoi de l'e-mail, veuillez réessayer. Si le problème persiste, contactez-nous.")
        return False

# Main Streamlit app
st.title("Formulaire d'inscription à la conférence")

full_name = st.text_input("Nom complet (tel qu'il apparaît sur les documents officiels)")
academic_degree = st.selectbox("Diplôme académique", ["Doctorat", "Master", "Licence", "Autre"])
specialization = st.text_input("Domaine de spécialisation")
current_position = st.text_input("Poste actuel")
institution = st.text_input("Institution affiliée")
country = st.text_input("Pays de résidence")
nationality = st.text_input("Nationalité")
email = st.text_input("Adresse e-mail")
confirm_email = st.text_input("Confirmer l'adresse e-mail")
phone = st.text_input("Numéro de téléphone (inclure l'indicatif du pays)")
paper_title = st.text_input("Titre de l'article soumis")
keywords = st.text_input("Mots-clés (jusqu'à 5, séparés par des virgules)")
conference_theme = st.selectbox("Thème de la conférence", ["Thème 1 : Le rôle et l'importance de l'IA dans la société moderne", 
                                                       "Thème 2 : Fondements philosophiques et historiques de l'IA",
                                                       "Thème 3 : Le rôle de la psychologie et de la sociologie dans l'interaction humain-IA",
                                                       "Thème 4 : Linguistique, communication et études culturelles dans le traitement du langage naturel", 
                                                       "Thème 5 : Médias et communication pour sensibiliser à l'IA",
                                                       "Thème 6 : Impacts économiques et développement durable", 
                                                       "Thème 7 : Considérations éthiques, juridiques et politiques dans le développement de l'IA"])
abstract_file = st.file_uploader("Télécharger le résumé (fichier PDF, DOCX ou DOC, 100-150 mots)", type=["pdf", "docx", "doc"])

if st.button("S'inscrire"):
    if email != confirm_email:
        st.error("Les adresses e-mail ne correspondent pas. Veuillez vérifier et réessayer.")
    elif full_name and academic_degree and specialization and current_position and institution and country and nationality and email and confirm_email and phone and paper_title and keywords and conference_theme and abstract_file:
        # Save the uploaded file
        abstract_path = os.path.join("uploads", abstract_file.name)
        with st.spinner("Téléchargement de vos informations..."):
            with open(abstract_path, "wb") as f:
                f.write(abstract_file.getbuffer())
            # Préparer le contenu de l'email
            email_body = f"""
            Nouvelle inscription à la conférence :

            Nom complet : {full_name}
            Diplôme académique : {academic_degree}
            Domaine de spécialisation : {specialization}
            Poste actuel : {current_position}
            Institution affiliée : {institution}
            Pays de résidence : {country}
            Nationalité : {nationality}
            Adresse e-mail : {email}
            Numéro de téléphone : {phone}
            Titre de la communication : {paper_title}
            Mots-clés : {keywords}
            Thème de la conférence : {conference_theme}

            Le fichier du résumé est ci-joint.
            """


            # Envoyer l'email
            if send_email("metalesaek@yahoo.fr", "Nouvelle inscription à la conférence", email_body, abstract_path):
                st.success(f"Merci pour votre inscription, {full_name} ! Nous avons bien reçu vos informations et votre résumé.")
            else:
                st.error("Une erreur s'est produite lors du traitement de votre inscription. Veuillez réessayer plus tard.")


            # Clean up the uploaded file
            os.remove(abstract_path)
    else:
        st.error("Veuillez remplir tous les champs et télécharger votre résumé.")

