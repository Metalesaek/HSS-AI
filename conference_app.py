import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import base64
from flask import Flask, request, jsonify
import streamlit as st
import threading
import json
import stripe
from flask import Flask, jsonify, request, Response
from werkzeug.serving import make_server


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



# st.markdown(f"""
# <style>
#     body {{
#         font-family: 'Arial', sans-serif;
#         color: #333;
#         line-height: 1.6;
#         direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
#     }}
#     .main {{
#         max-width: 800px;
#         margin: 0 auto;
#         padding: 20px;
#         background-color: #fff;
#         box-shadow: 0 0 10px rgba(0,0,0,0.1);
#         border-radius: 8px;
#     }}
#     .title {{
#         color: #e28743;
#         font-size: 28px;
#         text-align: center;
#         margin-bottom: 10px;
#         direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
#     }}
#     .subtitle {{
#         color: #4a4a4a;
#         font-size: 22px;
#         text-align: center;
#         direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
#     }}
#     h3 {{
#         color: #e28743;
#         border-bottom: 2px solid #e28743;
#         padding-bottom: 10px;
#         direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
#     }}
#     .important-dates {{
#         background-color: #f9f9f9;
#         padding: 15px;
#         border-radius: 5px;
#         margin-top: 20px;
#     }}
#     .contact-info {{
#         background-color: #e28743;
#         color: white;
#         padding: 15px;
#         border-radius: 5px;
#         margin-top: 20px;
#     }}
#     table {{
#         width: 100%;
#         border-collapse: collapse;
#         margin-top: 20px;
#     }}
#     th, td {{
#         border: 1px solid #ddd;
#         padding: 8px;
#         text-align: {'right' if st.session_state.language == 'ar' else 'left'};
#         direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
#     }}
#     th {{
#         background-color: #e28743;
#         color: white;
#         direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
#     }}
#     tr:nth-child(even) {{
#         background-color: #f2f2f2;
#         direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
#     }}
# </style>
# """, unsafe_allow_html=True)
# # Main content

st.markdown(f"""
<style>
	body {{
		font-family: 'Arial', sans-serif;
		color: #333;
		line-height: 1.6;
		direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
	}}
	
	.title {{
		color: #e28743;
		font-size: 28px;
		text-align: center;
		margin-bottom: 10px;
		direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
	}}
	.subtitle {{
		color: #4a4a4a;
		font-size: 22px;
		text-align: center;
		direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
	}}
	h3 {{
		color: #e28743;
		border-bottom: 2px solid #e28743;
		padding-bottom: 10px;
		direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
	}}
	.important-dates {{
		background-color: #f9f9f9;
		padding: 15px;
		border-radius: 5px;
		margin-top: 20px;
	}}
	.contact-info {{
		background-color: #e28743;
		color: white;
		padding: 15px;
		border-radius: 5px;
		margin-top: 20px;
	}}
	table {{
		width: 100%;
		border-collapse: collapse;
		margin-top: 20px;
	}}
	th, td {{
		border: 1px solid #ddd;
		padding: 8px;
		text-align: {'right' if st.session_state.language == 'ar' else 'left'};
		direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
	}}
	th {{
		background-color: #e28743;
		color: white;
		direction: {'rtl' if st.session_state.language == 'ar' else 'ltr'};
	
</style>
""", unsafe_allow_html=True)
# Main content


st.markdown("""
<script>
function getColorScheme() {
	if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
		return 'dark';
	} else {
		return 'light';
	}
}
const scheme = getColorScheme();
const url = new URL(window.location);
url.searchParams.set('color_scheme', scheme);
window.history.replaceState(null, '', url.toString());
</script>
""", unsafe_allow_html=True)

# Get the color scheme from URL parameters
query_params = st.query_params
color_scheme = query_params.get('color_scheme', ['light'])[0]



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
# 	nav_items = ["home", "preamble", "schedule", "speakers", "login", "register",  LANGUAGE_SELECTOR_PLACEHOLDER]
# else:
# 	nav_items = ["home", "preamble", "schedule", "speakers", "logout", LANGUAGE_SELECTOR_PLACEHOLDER]

nav_items = ["home", "preamble", "schedule",  "register",  LANGUAGE_SELECTOR_PLACEHOLDER]
# Translate all items except the language selector placeholder
translated_nav_items = [translate(item) if item != LANGUAGE_SELECTOR_PLACEHOLDER else item for item in nav_items]

# Use st_navbar with the translated items
page = st_navbar(translated_nav_items, selected=translate("home"))

# After st_navbar, replace the placeholder with the actual language selector
for i, item in enumerate(translated_nav_items):
	if item == LANGUAGE_SELECTOR_PLACEHOLDER:
		st.write("")  # Add some space
		language_selector()
		break

# Navigation logic
if page == translate("preamble"):
	navigate_to("preamble")
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

#st.image("logo_aicha.jpeg", width=300)

def main():

	if st.session_state.language == "en":
		st.markdown('<div class="main">', unsafe_allow_html=True)
		#st.image("coloq_english.jpeg", width=300)
		st.markdown(f"<h1 class='title'>Invitation to Participate in the International Conference:</h1>", unsafe_allow_html=True)
		
		st.markdown(
		"""
		<div style="display: flex; justify-content: center;">
			<img src="data:image/png;base64,{}" width="300">
		</div>
		""".format(base64.b64encode(open("coloq_english.jpeg", "rb").read()).decode()),
		unsafe_allow_html=True
		)
		

		st.markdown(f"<h1 class='title'>{translate('page_title')}</h1>", unsafe_allow_html=True)
		st.markdown(f"<h2 class='subtitle'>{translate('rest_title')}</h2>", unsafe_allow_html=True)

		st.markdown("""
		The University of Djilali Liabes, Sidi Bel Abbes, Faculty of Humanities and Social Sciences, Department of Media and Communication, is pleased to invite you to participate in this international conference on February 26–27, 2025.
		### Conference Overview:
		This conference aims to emphasize the vital role of humanities and social sciences in shaping AI research in alignment with human values and sustainable development goals.
		
		### Conference Objectives:
		1. Highlight the importance of humanities and social sciences in AI research.
		2. Explore AI's impact on social, cultural, ethical, and legal dimensions.
		3. Encourage interdisciplinary collaboration.
		4. Address inequality and biases in AI development.
		5. Raise awareness about emerging technologies.
		
		### Important Dates:
		- Full paper submissions deadline: January 15, 2025
		- Responding to accepted papers: January 30, 2025
		- Final program announcement: February 10, 2025
		
		### Participation Guidelines:
		- Open to professors, doctoral students, and researchers.
		- Research topics should align with conference themes.
		- Submissions must be original and unpublished.
		- Individual and co-authored submissions welcome.
		- Papers may be in Arabic, English, or French.
		
		### Contact Information:
		- Phone: +213 668 11 31 31
		- Email: hssaiudl@gmail.com
		
		""")
		st.markdown("""

		## Scientific Committee

		| Name and Surname | Role | Specialty | Institution |
		|------------------|------|-----------|-------------|
		| Karima Lahj Ahmed | President | Media and Communication Sciences | University of Sidi Bel Abbes | 
		| Sid Ahmed Makhlouf | Member | Philosophy | University of Sidi Bel Abbes |
		| Zein El Abidin Maghrebi | Member | Philosophy | University of Sidi Bel Abbes | 
		| Nasreddine Bouziane | Member | Media and Communication Sciences | University of Constantine 3 |
		| Mourad Ahaddad | Member | Media and Communication Sciences | University of Algiers 2 |
		| Bouamama Al-Arabi | Member | Media and Communication Sciences | University of Mostaganem |
		| Yasref Haj | Member | Media and Communication Sciences | University of Sidi Bel Abbès |
		| Ibrahim Qasemi | Member | Media and Communication Sciences | University of Sidi Bel Abbès |
		| Jamal Ben Zerrouk | Member | Media and Communication Sciences | University of Skikda | 
		| Said Marah | Member | Media and Communication Sciences | University of Sidi Bel Abbes | 
		| Wassila Ben Amr | Member | Psychology | University of Biskra | 
		| Aisha Metales | Member | Media and Communication Sciences | University of Sidi Bel Abbes |
		| Amal Khalaf | Member | Media and Communication Sciences | University of Sidi Bel Abbes |
		| Mustafa Djelti | Member | Media and Communication Sciences | University of Sidi Bel Abbes |
		| Soumia Berrahil | Member | Media and Communication Sciences | University of Oran 2 | 
		| Mohammed Aghoulaiche | Member | Media and Communication Sciences | University of Sidi Bel Abbes | 
		| Mohammed Belhamiti | Member | Sociology | University of Sidi Bel Abbes |
		| Haj Chaib | Member | Library Science | University of Saida | 
		| Mokhtar Djlouli | Member | Media and Communication Sciences | University of Tiaret | 
		| Oussama Omar | Member | Media and Communication Sciences | University of Sidi Bel Abbes | 
		| Assma Regui | Member | Media and Communication Sciences | University of Sidi Bel Abbes | 
		| Nassima Djemil | Member | Media and Communication Sciences | University of Oran 2 | 
		| Wassila Oudjdi Damirji | Member | Media and Communication Sciences | University of Sidi Bel Abbes | 
		| Abdelkarim Rqiq | Member | Arts | University of Sidi Bel Abbes | siquou@yahoo.fr |
		| Nabil Houari | Member | Media and Communication Sciences | University of Skikda | soheilhoura89@gmail.com |
		| Souhila Bediaf | Member | Media and Communication Sciences | University of Skikda | 
		| Noor El Hoda Obada | Member | Media and Communication Sciences | University of Algiers 3 | 
		| Souad Lilia Ainsouya | Member | Media and Communication Sciences | University of Souk Ahras | 
		| Yassine Hebal | Member | Psychology | University of Sidi Bel Abbes | 
		| Imen Harfouch | Member | Media and Communication Sciences | University of Tlemcen | 
		| Amina Ait El Hadj | Member | Media and Communication Sciences | University of El Oued | 
		| Chahrazad Abbane | Member | Macroeconomics | University of Algiers 3 | 
		| Mohammed Rezine | Member | Media and Communication Sciences | University of Sidi Bel Abbes | 
		| Lobna Souigat | Member | Media and Communication Sciences | University of Ouargla | 
		| Djamal Eddine Medfouni | Member | Media and Communication Sciences | University of Oum El Bouaghi | 
		| Oussama Demouche | Member | Library Science | University of Sidi Bel Abbes | 
		| Nourine Achache | Member | Sociology | University of Sidi Bel Abbes | 
		| Samia Bouguera | Member | Media and Communication Sciences | University of Annaba | 
		| El Djellal Meghat | Member | Sociology | University of Sidi Bel Abbes | 
		| Amina Bessafa | Member | Media and Communication Sciences | University of Algiers 3 | 
		| Karim Chaadou | Member | Sociology | University of Sidi Bel Abbes | 
		| Mohammed Sahali | Member | Sociology | University of Sidi Bel Abbes | 
		| Salih Chelouach | Member | Media and Communication Sciences | University of Skikda |
		

		## Members of the Scientific Committee from Abroad

		| Name and Surname | Role | Specialty | Institution | 
		|------------------|------|-----------|-------------|
		| Prof. Nour El Din Hamed | Member | | Al-Jouf University, Saudi Arabia |
		| Prof. Mehmet Zeki Aydin | Member | Education Sciences | Selcuk University, Turkey | 
		| Prof. Rasha Abdel Fattah El-Didi | Member | Psychology | Ain Shams University, Egypt | 
		| Dr. Rahima Aissani | Member | Media and Communication Sciences | Al Ain University, UAE | 
		| Dr. Sami Abdel Karim Al-Azraq | Member | Sociology | Ajdabiya University, Libya | 
		| Dr. Khaled Harzib | Member | Mathematics | Paderborn University, Germany | 
		| Dr. Reda Abdel Wahid El-Amin | Member | Media and Communication Sciences | Al-Azhar University, Egypt | 
		| Dr. Amal Saad El-Motwali Osman | Member | Media and Communication Sciences | Mansoura University, Egypt |
		| Dr. Abdel Latif Bel-Tayeb | Member | Mathematics | Saudi Arabia | 
		""")

		# Close the main div
		st.markdown('</div>', unsafe_allow_html=True)

	elif st.session_state.language == "fr":
		st.markdown('<div class="main">', unsafe_allow_html=True)
		#st.image("coloq_english.jpeg", width=300)
		st.markdown(f"<h1 class='title'>Invitation à participer à la conférence internationale :</h1>", unsafe_allow_html=True)
		
		st.markdown(
		"""
		<div style="display: flex; justify-content: center;">
			<img src="data:image/png;base64,{}" width="300">
		</div>
		""".format(base64.b64encode(open("coloq_english.jpeg", "rb").read()).decode()),
		unsafe_allow_html=True
		)
		
		st.markdown(f"<h1 class='title'>{translate('page_title')}</h1>", unsafe_allow_html=True)
		st.markdown(f"<h2 class='subtitle'>{translate('rest_title')}</h2>", unsafe_allow_html=True)

		st.markdown(r"""
		L'Université Djilali Liabes de Sidi Bel Abbes, Faculté des Sciences Humaines et Sociales, Département des Sciences de l'Information et de la Communication, a le plaisir de vous inviter à participer à cette conférence internationale qui se tiendra les 26 et 27 février 2025.
		### Aperçu de la Conférence:
		Cette conférence vise à souligner le rôle vital des sciences humaines et sociales dans l'orientation de la recherche en IA en accord avec les valeurs humaines et les objectifs de développement durable.
		
		### Objectifs de la Conférence:
		1. Mettre en évidence l'importance des sciences humaines et sociales dans la recherche en IA.
		2. Explorer l'impact de l'IA sur les dimensions sociales, culturelles, éthiques et juridiques.
		3. Encourager la collaboration interdisciplinaire.
		4. Aborder les inégalités et les biais dans le développement de l'IA.
		5. Sensibiliser aux technologies émergentes.
		
		### Dates Importantes :
		- Date limite de soumission des articles complets : 15 janvier 2025
		- Réponse aux articles acceptés : 30 janvier 2025
		- Annonce du programme final : 10 février 2025
		
		### Directives de Participation :
		- Ouvert aux professeurs, doctorants et chercheurs.
		- Les sujets de recherche doivent s'aligner sur les thèmes de la conférence.
		- Les soumissions doivent être originales et non publiées.
		- Les soumissions individuelles et en co-auteur sont les bienvenues.
		- Les articles peuvent être en arabe, anglais ou français.
		
		### Informations de Contact :
		- Téléphone : +213 668 11 31 31
		- Email : hssaiudl@gmail.com
		""")	

		st.markdown("""
		

		## Comité Scientifique

		| Nom et Prénom | Rôle | Spécialité | Institution | 
		|---------------|------|-----------|-------------|
		| Lahaj Ahmed Karima | Président | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Makhlouf Sid Ahmed | Membre | Philosophie | Université de Sidi Bel Abbès | 
		| Maghreb Zine El Abidine | Membre | Philosophie | Université de Sidi Bel Abbès | 
		| Nasreddine Bouziane | Membre | Sciences de l'information et de la communication | Université Constantine 3 | 
		| Mourad Ahaddad | Membre | Sciences de l'information et de la communication | Université d'Alger 2 |
		| Bouamama Al-Arabi | Membre | Sciences de l'information et de la communication | Université de Mostaganem |
		| Yasref Haj | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès |
		| Ibrahim Qasemi | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Djemal Ben Zarouq | Membre | Sciences de l'information et de la communication | Université de Skikda | 
		| Merah Saïd | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Wassila Benamer | Membre | Psychologie | Université de Biskra | wassila.benameur@univ-biskra.dz |
		| Sadiki Abdelnour | Membre | Sociologie | Université de Sidi Bel Abbès | seddikinour@yahoo.fr |
		| Metales Aicha | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Khalf Amal | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Djelti Mostafa | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Berrahil Soumia | Membre | Sciences de l'information et de la communication | Université d'Oran 2 | 
		| Aghoulais Mohamed | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès |
		| Belhamiti Mohamed | Membre | Sociologie | Université de Sidi Bel Abbès | 
		| Chaïb Hadj | Membre | Sciences des bibliothèques | Université de Saïda | 
		| Djeloul Mokhtar | Membre | Sciences de l'information et de la communication | Université de Tiaret | 
		| Omar Oussama | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Rigui Asmaa | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès |
		| Djamil Nassima | Membre | Sciences de l'information et de la communication | Université d'Oran 2 | 
		| Ould Demerji Wassila | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | 
		| Reghigue Abdelkrim | Membre | Arts | Université de Sidi Bel Abbès | 
		| Houra Nabil | Membre | Sciences de l'information et de la communication | Université de Skikda | 
		| Bediaf Souhila | Membre | Sciences de l'information et de la communication | Université de Skikda | 
		| Abada Nour El Hoda | Membre | Sciences de l'information et de la communication | Université d'Alger 3 | 
		| Lilia Aïn Souya | Membre | Sciences de l'information et de la communication | Université de Souk Ahras | 
		| Hebbal Yacine | Membre | Psychologie | Université de Sidi Bel Abbès | 
		| Harfouche Imene | Membre | Sciences de l'information et de la communication | Université de Tlemcen | 
		| Amina Ait El Hadj | Membre | Sciences de l'information et de la communication | Université d'El Oued | 
		| Abane Chahrazad | Membre | Économie | Université d'Alger 3 | chahrazad.abbane@gmail.com |
		| Rezine Mohamed | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès |
		| Souigat Lobna | Membre | Sciences de l'information et de la communication | Université d'Ouargla | 
		| Madfouni Djamal Eddine | Membre | Sciences de l'information et de la communication | Université d'Oum El Bouaghi |
		| Demouche Oussama | Membre | Sciences des bibliothèques | Université de Sidi Bel Abbès |
		| Achache Nourine | Membre | Sociologie | Université de Sidi Bel Abbès | 
		| Bouguera Samia | Membre | Sciences de l'information et de la communication | Université d'Annaba | 
		| Maghtat El Ajjal | Membre | Sociologie | Université de Sidi Bel Abbès |
		| Bessafa Amina | Membre | Sciences de l'information et de la communication | Université d'Alger 3 |
		| Chadou Karim | Membre | Sociologie | Université de Sidi Bel Abbès |
		| Sahali Mohamed | Membre | Sociologie | Université de Sidi Bel Abbès | 
		| Chelouache Saliha | Membre | Sciences de l'information et de la communication | Université de Skikda |
		
		## Membres du Comité Scientifique Hors National

		| Nom et Prénom | Rôle | Université | Institution | 
		|---------------|------|-----------|-------------|
		| Prof. Nour El Dine Hamed | Membre | | Université Al Jouf, Arabie Saoudite | 
		| Prof. Mehmet Zeki Aydin | Membre | Sciences de l'éducation | Université Selçuk, Turquie | 
		| Prof. Rasha Abdel Fattah El-Didy | Membre | Psychologie | Université Ain Shams, Égypte | 
		| Dr. Rahima Aissani | Membre | Sciences de l'information et de la communication | Université Al Ain, Émirats Arabes Unis | 
		""")
		# Close the main div
		st.markdown('</div>', unsafe_allow_html=True)


	else:
		st.markdown('<div class="main">', unsafe_allow_html=True)
		#st.image("coloq_english.jpeg", width=300)
		st.markdown(f"<h1 class='title'>دعوة للمشاركة في الملتقى العلمي الدولي الموسوم:</h1>", unsafe_allow_html=True)
		
		st.markdown(
		"""
		<div style="display: flex; justify-content: center;">
			<img src="data:image/png;base64,{}" width="300">
		</div>
		""".format(base64.b64encode(open("coloq_arab.jpeg", "rb").read()).decode()),
		unsafe_allow_html=True
		)
		
		st.markdown(f"<h1 class='title'>{translate('page_title')}</h1>", unsafe_allow_html=True)
		st.markdown(f"<h2 class='subtitle'>{translate('rest_title')}</h2>", unsafe_allow_html=True)


		st.markdown("""

		### العلوم الإنسانية والاجتماعية وعلاقتها بأبحاث الذكاء الاصطناعي: نحو ذكاء اصطناعي مسؤول ومستدام

		يسر جامعة جيلالي ليابس، سيدي بلعباس، كلية العلوم الإنسانية والاجتماعية، قسم علوم الإعلام والاتصال، دعوتكم للمشاركة في الملتقى الدولي الموسوم ب "العلوم الإنسانية والاجتماعية وعلاقتها بأبحاث الذكاء الاصطناعي: نحو ذكاء اصطناعي مسؤول ومستدام"، الذي سيُعقد يومي 26 و27 فبراير 2025.

		يهدف هذا الملتقى إلى تسليط الضوء على الدور الحيوي لهذه العلوم في توجيه وتطوير أبحاث الذكاء الاصطناعي بما يتماشى مع القيم الإنسانية ويلبي متطلبات التنمية المستدامة، من خلال بناء جسور التعاون بين الباحثين والمتخصصين من جميع أنحاء العالم لتبادل الأفكار حول كيفية المساهمة في تطوير ذكاء اصطناعي بشكل يخدم المجتمع ويدعم الاستدامة.

		### أهداف الملتقى:

		1. التأكيد على أهمية العلوم الإنسانية والاجتماعية في تطوير أبحاث الذكاء الاصطناعي بما يحقق التوازن بين الفوائد والمخاطر على الأفراد والمجتمعات.
		2. فهم تأثير الذكاء الاصطناعي على الجوانب الاجتماعية والثقافية والأخلاقية والقانونية، وتوجيه تطويره بما يتوافق مع الاحتياجات والقيم الانسانية.
		3. تعزيز التعاون بين الباحثين من مختلف التخصصات لاستكشاف إمكانيات الذكاء الاصطناعي واستخدامها بشكل مسؤول ومستدام.
		4. التخفيف من حدة التفاوت والتحيزات من خلال الفهم العميق للبنى الاجتماعية والسياقات الثقافية التي تجري فيها التفاعلات بين الأفراد والأنظمة الذكية.
		5. تعزيز الفهم وزيادة وعي الأفراد والمجتمعات بالتقنيات الحديثة لمواكبة التطورات المتسارعة وذلك عبر تزويدهم بالمعلومات الموثوقة والدقيقة ومكافحة الأخبار الكاذبة والمضللة والتحيزات.

		### مواعيد هامة:

		- آخر أجل لإرسال المداخلات كاملة: 15/01/2025  
		- الرد على المداخلات المقبولة: 30/01/2025  
		- الإعلان عن البرنامج النهائي للملتقى: 10/02/2025

		### شروط المشاركة:

		- المشاركة مفتوحة لجميع الأساتذة وطلبة الدكتوراه والباحثين في الجامعات والمؤسسات الأكاديمية.
		- أن يدرج الموضوع ضمن أحد محاور الملتقى
		- أن لا يكون البحث قد سبق نشره أو المشاركة به.
		- تقبل المشاركات الفردية والثنائية.
		- تقبل المداخلات باللغات العربية والإنجليزية والفرنسية.
		

		### للتواصل والاستفسار:

		- رقم الهاتف: **213668113131+**
		- البريد الإلكتروني: hssaiudl@gmail.com
		
		
		نتطلع لاستقبال أبحاث مميزة تساهم في دعم أهداف الملتقى ودفع عجلة البحث العلمي في مجالات الذكاء الاصطناعي والمسؤولية الاجتماعية.
			""")
		st.markdown("""
		
		##  اللجنة العلمية

		| الاسم واللقب | الصفة | التخصص | المؤسسة |
		|-------------|------|---------|---------|
		| لحاج أحمد كريمة | رئيس | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| مخلوف سيد أحمد | عضو | فلسفة | جامعة سيدي بلعباس | 
		| مغربي زين العابدين | عضو | فلسفة | جامعة سيدي بلعباس | 
		| نصر الدين بوزيان | عضو | علوم الاعلام والاتصال | جامعة قسنطينة 3 | 
		| أحداد موراد | عضو | علوم الاعلام والاتصال | جامعة الجزائر 2 |
		| العربي بوعمامة | عضو | علوم الاعلام والاتصال | جامعة مستغانم |
		| حاج يصرف | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس |
		| قاسمي ابراهيم | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| جمال بن زروق | عضو | علوم الاعلام والاتصال | جامعة سكيكدة | 
		| مراح سعيد | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| وسيلة بن عامر | عضو | علم النفس | جامعة بسكرة | 
		| صديقي عبدالنور | عضو | علم الاجتماع | جامعة سيدي بلعباس | 
		| مطالس عائشة | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| خالف أمال | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| جلطي مصطفى | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| برحيل سمية | عضو | علوم الاعلام والاتصال | جامعة وهران 2 | 
		| أغولايش محمد | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| يلحميتي محمد | عضو | علم الاحتماع | جامعة سيدي بلعباس | 
		| شعيب حاج | عضو | علم المكتبات | جامعة سعيدة | 
		| جلولي مختار | عضو | علوم الاعلام والاتصال | جامعة تيارت | 
		| عمر أوسامة | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| ريغي أسماء | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| جميل نسيمة | عضو | علوم الاعلام والاتصال | جامعة وهران 2 | 
		| وجدي دمرجي وسيلة | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| رقيق عبد الكريم | عضو | فنون | جامعة سيدي بلعباس | 
		| حورة نبيل | عضو | علوم الاعلام والاتصال | جامعة سكيكدة | 
		| بضياف سوهيلة | عضو | علوم الاعلام والاتصال | جامعة سكيكدة | 
		| عبادة نور الهدى | عضو | علوم الاعلام والاتصال | جامعة الجزائر 3 | 
		| ليليا عين سوية | عضو | علوم الاعلام والاتصال | جامعة سوق أهراس | 
		| حبال ياسين | عضو | علم النفس | جامعة سيدي بلعباس | 
		| حرفوش إيمان | عضو | علوم الاعلام والاتصال | جامعة تلمسان | 
		| أمينة آيت الحاج | عضو | علوم الاعلام والاتصال | جامعة الوادي | 
		| عبان شهرزاد | عضو | اقتصاد كلي | جامعة الجزائر 3 | 
		| رزين محمد | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | 
		| سويقات لبنى | عضو | علوم الاعلام والاتصال | جامعة ورقلة | 
		| مدفوني جمال الدين | عضو | علوم الاعلام والاتصال | جامعة أم البواقي | 
		| دموش أسامة | عضو | علم المكتبات | جامعة سيدي بلعباس | 
		| عشاش نورين | | علم الاجتماع | جامعة سيدي بلعباس | 
		| بوقرة سامية | عضو | علوم الاعلام والاتصال | جامعة عنابة | 
		| مغتات العجال | عضو | علم الاجتماع | جامعة سيدي بلعباس | 
		| بصافة أمينة | عضو | علوم الاعلام والاتصال | جامعة الجزائر 3 | 
		| شعدو كريم | عضو | علم الاجتماع | جامعة سيدي بلعباس | 
		| سهالي محمد | عضو | علم الاجتماع | جامعة سيدي بلعباس | 
		| شلواش صليحة | عضو | علوم الاعلام والاتصال | جامعة سكيدة |
		

		## أعضاء اللجنة العلمية من خارج الوطن

		| الاسم واللقب | الصفة | الجامعة | المؤسسة | البريد الالكتروني |
		|-------------|------|---------|---------|-------------------|
		| أ.د/ نورالدين حامد | عضو | | جامعة الجوف المملكة العربية السعودية | 
		| أ.د/ محمت زكي ايدن | عضو | علوم التربية | جامعة سلجوق تركيا | 
		| أ.د / رشا عبد الفتاح الديدي | عضو | علم النفس | جامعة عين شمس - مصر | 
		| د/ رحيمة عيساني | عضو | علوم الاعلام والاتصال | جامعة العين الامارات العربية المتحدة | 
		| د/ سامي عبد الكريم الأزرق | عضو | علم الاجتماع | جامعة أجدابيا- ليبيا | 
		| د/ خالد حريز | عضو | الرياضيات | جامعة Pederbon ألمانيا | 
		| د/ رضا عبد الواجد الأمين | عضو | علوم الاعلام والاتصال | جامعة الأزهر - مصر | 
		| د/ أمال سعد المتولي عثمان | عضو | علوم الاعلام والاتصال | جامعة المنصورة - مصر | 
		| د/ عبد اللطيف بالطيب | عضو | الرياضيات | المملكة العربية السعودية | 
		""")
		# Close the main div
		st.markdown('</div>', unsafe_allow_html=True)


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


# Flask webhook server
class ServerThread(threading.Thread):
	def __init__(self, app):
		threading.Thread.__init__(self)
		self.server = make_server('0.0.0.0', 8501, app)
		self.ctx = app.app_context()
		self.ctx.push()

	def run(self):
		self.server.serve_forever()

	def shutdown(self):
		self.server.shutdown()

# Create Flask app for webhook
flask_app = Flask(__name__)

# Stripe API key setup
stripe.api_key = os.getenv("STRIPE_SECRET")  # Replace with your actual test key

# Webhook endpoint secret
endpoint_secret = os.getenv("ENDPOINT_SCRET_WEBHOOK")  # Replace with your actual endpoint secret

@flask_app.route('/webhook', methods=['POST'])
def webhook():
	event = None
	payload = request.data
	sig_header = request.headers.get('STRIPE_SIGNATURE')
	
	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, endpoint_secret
		)
	except ValueError as e:
		# Invalid payload
		return Response(status=400)
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		return Response(status=400)
	
	# Handle the event
	if event['type'] == 'payment_link.created':
		payment_link = event['data']['object']
		# Process payment_link.created
		print(f"Payment link created: {payment_link.get('id')}")
	elif event['type'] == 'payment_link.updated':
		payment_link = event['data']['object']
		# Process payment_link.updated
		print(f"Payment link updated: {payment_link.get('id')}")
	# ... handle other event types
	elif event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		print(f"Checkout completed for session: {session.get('id')}")
	# Add more event types as needed
	else:
		print(f'Unhandled event type {event["type"]}')
	
	return jsonify(success=True)

# Start Flask server in a thread
def run_flask():
	server = ServerThread(flask_app)
	server.start()
	return server

# Run the Streamlit app
if __name__ == "__main__":
	# Start the Flask server in a separate thread
	flask_thread = run_flask()
	
	# Run the Streamlit app
	main()