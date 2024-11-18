import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
import base64
import time
from dotenv import load_dotenv


load_dotenv()

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

st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{}" width="70">
    </div>
    """.format(base64.b64encode(open("logo_univ.png", "rb").read()).decode()),
    unsafe_allow_html=True
	)

if st.session_state.language == "fr":
    navigate_to("register")
if st.session_state.language == "ar":
    navigate_to("register")

st.markdown(f"<h5 style='color:rgb(226,135,67);'>Register for the Conference</h5>", unsafe_allow_html=True)



# def send_email(to_email, subject, body, attachment=None):
#     # Email configuration
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_username = st.secrets["email"]["username"]
#     smtp_password = st.secrets["email"]["password"]

#     msg = MIMEMultipart()
#     msg['From'] = smtp_username
#     msg['To'] = to_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     if attachment:
#         with open(attachment, "rb") as file:
#             part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
#         part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
#         msg.attach(part)

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.send_message(msg)
#         return True
#     except Exception as e:
#         st.error("An error occurred while sending the email, try again, if the problem persist contact as")
#         return False

def send_email(to_email, subject, body, attachment=None):
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.getenv("USERNAME")
    smtp_password = os.getenv("PASSWORD")
    # smtp_username = st.secrets["email"]["username"]
    # smtp_password = st.secrets["email"]["password"]

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment:
        part = MIMEApplication(attachment.getvalue(), Name=attachment.name)
        part['Content-Disposition'] = f'attachment; filename="{attachment.name}"'
        msg.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error("An error occurred while sending the email. Please try again. If the problem persists, please contact us.")
        return False


# Main Streamlit app
st.title("Conference Registration Form")

full_name = st.text_input("Full Name (As it appears on official documents)")
academic_degree = st.selectbox("Academic Degree", ["Ph.D.", "Master's", "Bachelor's", "Other"])
specialization = st.text_input("Field of Specialization")
current_position = st.text_input("Current Position")
institution = st.text_input("Affiliated Institution")
country = st.text_input("Country of Residence")
nationality = st.text_input("Nationality")
email = st.text_input("Email Address")
confirm_email = st.text_input("Confirm Email Address")
phone = st.text_input("Phone Number (Include country code)")
paper_title = st.text_input("Title of the Submitted Paper")
keywords = st.text_input("Keywords (up to 5, separated by commas)")
conference_theme = st.selectbox("Conference Theme", ["Theme 1: The Role and Significance of AI in Modern Society", 
                                "Theme 2: Philosophical and Historical Foundations of AI",
                                "Theme 3: Psychology and Sociology’s Role in Human-AI Interaction",
                             "Theme 4: Linguistics, Communication, and Cultural Studies in Natural Language Processing", 
                             "Theme 5: Media and Communication in Raising AI Awareness",
                             "Theme 6: Economic Impacts and Sustainable Development", 
                             "Theme 7: Ethical, Legal, and Political Considerations in AI Development"])

abstract_file = st.file_uploader("Upload Abstract (PDF, DOCX, or DOC file, 100-150 words)", type=["pdf", "docx", "doc"])

if st.button("Register"):
    if email != confirm_email:
        st.error("Email addresses do not match. Please check and try again.")
    elif full_name and academic_degree and specialization and current_position and institution and country and nationality and email and confirm_email and phone and paper_title and keywords and conference_theme and abstract_file:
        # Save the uploaded file
        #abstract_path = os.path.join("uploads", abstract_file.name)
        with st.spinner("Uploading your information..."):
            #with open(abstract_path, "wb") as f:
            #   f.write(abstract_file.getbuffer())
            # Prepare email content
            email_body = f"""
            New Conference Registration:

            Full Name: {full_name}
            Academic Degree: {academic_degree}
            Field of Specialization: {specialization}
            Current Position: {current_position}
            Affiliated Institution: {institution}
            Country of Residence: {country}
            Nationality: {nationality}
            Email Address: {email}
            Phone Number: {phone}
            Paper Title: {paper_title}
            Keywords: {keywords}
            Conference Theme: {conference_theme}

            Abstract file is attached.
            """

            # Send email
            if send_email("hssaiudl@gmail.com", "New Conference Registration", email_body, abstract_file):
                st.success(f"""
                Thank you for registering, {full_name}!,  We have successfully received your information and abstract.
                If the email address you provided is correct, you will receive a confirmation email shortly. 
                If you have any questions or need to make any changes, please feel free to contact us directly at hssaiudl@gmail.com or by phone at +213 541 531 962.
                """)
                body = f"""
                Dear {full_name},

                Thank you for submitting your information and abstract for the {translate('page_title')} scheduled to take place on 26-27 Fabruary 2025 at Djillali Liabes University, Sid Bel Abbes. We are excited to have you as part of this event!

                Submission Details:
                We have successfully received your submission, which includes:
                
                Title of Paper: {paper_title}

                Next Step:
                Our review committee will evaluate all submissions, and we will notify you of the acceptance status by January 10, 2025. If accepted, you will be provided with further details regarding presentation guidelines and registration.

                If you have any questions or require further information, please do not hesitate to reach out to us at hssaiudl@gmail.com or +213 541 531 962.

                Thank you once again for your contribution. We look forward to a successful conference and appreciate your participation!

                Best regards,

                DR. Metales Aicha
                Conference Chair
                """
                time.sleep(10)
                send_email(email, "Confirmation of Your Conference Submission", body)

            else:
                st.error("There was an error processing your registration. Please try again later.")

            # # Clean up the uploaded file
            # os.remove(abstract_path)
    else:
        st.error("Please fill in all fields and upload your abstract.")

# Footer section
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
        }
    </style>
    <div class="footer">
        <p>Contact us at: <a href="mailto:hssaiudl@gmail.com">hssaiudl@gmail.com</a> | Phone: +213 668 11 31 31</p>
    </div>
    """,
    unsafe_allow_html=True
)