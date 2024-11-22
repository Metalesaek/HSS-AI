import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import base64
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
# 	nav_items = ["home","preamble", "schedule", "speakers", "login", "register",  LANGUAGE_SELECTOR_PLACEHOLDER]
# else:
# 	nav_items = ["home","preamble", "schedule", "speakers", "logout", LANGUAGE_SELECTOR_PLACEHOLDER]

nav_items = ["home","preamble", "schedule", "register",  LANGUAGE_SELECTOR_PLACEHOLDER]
# Translate all items except the language selector placeholder
translated_nav_items = [translate(item) if item != LANGUAGE_SELECTOR_PLACEHOLDER else item for item in nav_items]

# Use st_navbar with the translated items
page = st_navbar(translated_nav_items, selected=translate("preamble"))

# After st_navbar, replace the placeholder with the actual language selector
for i, item in enumerate(translated_nav_items):
	if item == LANGUAGE_SELECTOR_PLACEHOLDER:
		st.write("")  # Add some space
		language_selector()
		break

# Navigation logic
if page == translate("home"):
    st.switch_page("conference_app.py")
elif page == translate("schedule"):
	navigate_to("schedule")
# elif page == translate("speakers"):
# 	navigate_to("speakers")
elif page == translate("register"):
	navigate_to("register")
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
if st.session_state.language == "en":
    navigate_to("preamble")
if st.session_state.language == "ar":
    navigate_to("preamble")

st.markdown(f"<center><h5 style='color:rgb(226,135,67);'>{translate('preamble')}</h5></center>", unsafe_allow_html=True)
st.markdown(f"<center><h3>{translate('page_title')}</h3></center>", unsafe_allow_html=True)
st.markdown(f"<center><h4>{translate('rest_title')}</h4></center>", unsafe_allow_html=True)



st.markdown("""


L'Intelligence Artificielle (IA) représente l'un des défis les plus importants auxquels l'humanité est confrontée, s'étendant sur de nombreuses disciplines et progressant rapidement grâce à l'intégration de diverses méthodes de résolution de problèmes, incluant la logique, les mathématiques, les réseaux de neurones artificiels, les statistiques et les probabilités. L'IA s'inspire également de la psychologie, de la linguistique, de la philosophie, de l'économie et du droit, entre autres domaines.

Le fondement de la recherche en IA est né des tentatives de simuler l'intelligence humaine, suscitant des débats philosophiques sur les implications éthiques de la création d'êtres artificiels dotés de capacités semblables à celles des humains. Cela souligne le rôle essentiel des sciences humaines et sociales dans l'évolution de l'IA, en se concentrant particulièrement sur les aspects sociaux, culturels, comportementaux et cognitifs de l'interaction humaine avec la technologie.

Le défi central de la recherche en IA est de comprendre la relation dynamique entre les humains, la société et la technologie. En favorisant cette compréhension, les systèmes d'IA peuvent être conçus pour mieux servir les intérêts individuels et sociétaux. Ce discours est essentiel non seulement pour les développeurs techniques visant à affiner leurs objectifs, mais aussi pour les chercheurs en sciences humaines et sociales afin d'orienter leur travail vers la maximisation des avantages sociétaux de l'IA et l'examen de ses implications éthiques et juridiques. Bien que l'IA n'ait pas encore atteint les aspirations de ses pionniers, elle reste la création la plus complexe de l'humanité - une création dont l'avenir est plein de potentiel mais difficile à prédire.

Si l'objectif ultime de l'IA est de simuler les capacités humaines ou celles d'autres êtres vivants, nous pouvons comparer le matériel au corps physique et le logiciel, la logique et l'ingénierie au cerveau. Pendant ce temps, les sciences humaines et sociales peuvent être considérées comme l'élément "spirituel" qui anime ce domaine, veillant à ce que les progrès de l'IA s'alignent sur les valeurs humaines.

En comprenant les contributions interdisciplinaires - de la philosophie et de la psychologie aux mathématiques et aux neurosciences - nous pouvons voir que l'IA est un domaine multidisciplinaire prêt à poursuivre sa croissance et sa complexité. Cette conférence vise à souligner le rôle central de la recherche en sciences humaines et sociales dans la formation de l'avenir de l'IA, la résolution de problèmes complexes et la minimisation des risques potentiels dans divers domaines.

### Thèmes de la conférence

1. **Le rôle et l'importance de l'IA dans la société moderne**:

Cette section offre un aperçu de l'IA, de son développement historique, de sa nature interdisciplinaire, de ses domaines, branches, applications et exigences essentielles, visant à mettre en lumière l'interaction entre l'IA et les sciences humaines et sociales.

2. **Fondements philosophiques et historiques de l'IA**:

Ce thème explore les contextes philosophiques et historiques d'où est née l'IA. Il examine les questions philosophiques fondamentales entourant l'IA, y compris les théories sur l'esprit et la conscience, et les interrogations sur la possibilité que les machines puissent un jour posséder une conscience de soi. Cet axe souligne également le contexte historique pour comprendre comment le développement de l'IA affecte à la fois les individus et la société.

3. **Le rôle de la psychologie et de la sociologie dans l'interaction humain-IA**:

Cette section met en évidence comment la psychologie et la sociologie contribuent à la compréhension du comportement humain et des structures sociétales en relation avec les systèmes intelligents. Les connaissances issues de ces domaines sont essentielles pour développer des modèles d'IA qui améliorent l'interaction avec les utilisateurs et reflètent les besoins des individus et des sociétés, enrichissant ainsi l'expérience homme-IA.

4. **Linguistique, communication et études culturelles dans le traitement du langage naturel**:

La linguistique joue un rôle central dans l'établissement de la communication entre les humains et les machines. Cette section examine comment une compréhension du langage et des nuances culturelles peut améliorer la capacité de l'IA à interpréter les commandes et à interagir efficacement avec des populations diverses, abordant les défis uniques du traitement du langage naturel et de la communication interculturelle.

5. **Médias et communication pour sensibiliser à l'IA**:

Le rôle des médias dans l'information du public sur les avantages et les risques de l'IA est crucial pour favoriser la compréhension. Grâce à des reportages précis et impartiaux et à la diffusion des résultats de recherche, les études sur les médias et la communication encouragent des perspectives éclairées sur l'IA parmi les individus, les organisations et les décideurs politiques.

6. **Impacts économiques et développement durable**:

L'économie fournit des outils pour comprendre les implications économiques de l'IA et offre des orientations pour élaborer des politiques qui favorisent le développement durable et l'égalité des chances. Ce thème se concentre sur les stratégies d'intégration de l'IA dans l'économie numérique tout en encourageant l'innovation et l'équité.

7. **Considérations éthiques, juridiques et politiques dans le développement de l'IA**:

Cette section explore les questions éthiques, juridiques et politiques qui surgissent à mesure que l'IA progresse, soulignant l'importance d'établir des lignes directrices qui respectent les droits humains et les valeurs sociales. Elle préconise une approche équilibrée du développement de l'IA qui tient compte à la fois de ses avantages sociaux et de ses risques potentiels.

### Objectifs de la conférence

1. Souligner l'importance des sciences humaines et sociales dans la recherche en IA pour équilibrer les avantages et les risques de l'IA pour la société.
2. Explorer l'impact de l'IA sur les domaines sociaux, culturels, éthiques et juridiques pour guider un développement cohérent avec les besoins et les valeurs humains.
3. Renforcer la collaboration interdisciplinaire pour exploiter de manière responsable et durable le potentiel de l'IA.
4. Aborder les inégalités et les biais en comprenant les contextes sociaux et culturels dans lesquels les humains et les systèmes intelligents interagissent.
5. Favoriser la sensibilisation aux technologies modernes, en promouvant la compréhension du public et la résilience face à la désinformation et aux préjugés.

### Comité de supervision de la conférence
- **Président d'honneur de la conférence** : Pr. Bouziani Marahi / Directeur de l'Université Djilali Liabes (Sidi Bel Abbès)
- **Superviseur général de la conférence** : Pr. Al-Ahmar Qadah / Doyen de la Faculté des Sciences Humaines et Sociales
- **Coordinateur général de la conférence** : Dr. Merah Said
- **Présidente de la conférence** : Dr. Metales Aicha
- **Présidente du comité scientifique** : Dr. Lhadj Ahmad Karima
- **Président du comité d'organisation** : Dr. Omar Oussama
- **Date prévue pour la conférence** : 26-27 février 2025

""")

# Footer section
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2e2e2e; /* Neutral background for both modes */
            color: #ffffff; /* Text color for readability */
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
        .footer a {
            color: #ffcc00; /* Accent color for links */
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        <p>Contact us at: <a href="mailto:hssaiudl@gmail.com">hssaiudl@gmail.com</a> | Phone: +213 668 11 31 31</p>
    </div>
    """,
    unsafe_allow_html=True
)
