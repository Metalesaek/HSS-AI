import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import base64

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

if st.session_state.language == "en":
	st.markdown(f"<center><h5 style='color:rgb(226,135,67);'>Invitation to Participate in the International Conference:</h5></center>", unsafe_allow_html=True)
	
	st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{}" width="300">
    </div>
    """.format(base64.b64encode(open("coloq_english.jpeg", "rb").read()).decode()),
    unsafe_allow_html=True
	)
	
	st.markdown(f"<center><h3>{translate('page_title')}</h3></center>", unsafe_allow_html=True)
	st.markdown(f"<center><h4>{translate('rest_title')}</h4></center>", unsafe_allow_html=True)

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
	- Abstract submissions deadline: January 1, 2025
	- Accepted abstracts notification: January 10, 2025
	- Full paper submissions deadline: January 30, 2025
	- Final program announcement: February 10, 2025
	
	### Participation Guidelines:
	- Open to professors, doctoral students, and researchers.
	- Research topics should align with conference themes.
	- Submissions must be original and unpublished.
	- Individual and co-authored submissions welcome.
	- Papers may be in Arabic, English, or French.
	
	### Contact Information:
	- Phone: +213541531962
	- Email: hssai2024@gmail.com
	""")
	st.markdown("""
	## Personal Information

	|  |  |
	|-------------|-------|
	| Name and Surname | Aisha Metales |
	| Rank | Assistant Professor |
	| Position | Professor |
	| Email | metales.sic@gmail.com |
	| Phone | 541531962 |

	## Part 3: Organizing Committee

	| Name and Surname | Role | Institution | Email | Phone |
	|------------------|------|-------------|-------|-------|
	| Dr. Oussama Omar | President | University of Sidi Bel Abbes | oussama_sic@yahoo.fr | 676494906 |
	| Aisha Metales | Member | University of Sidi Bel Abbes | metalesch12@gmail.com | 541531962 |
	| Mustafa Djelti | Member | University of Sidi Bel Abbes | djelti.mostafa@yahoo.com | 675332071 |
	| Said Marah | Member | University of Sidi Bel Abbes | said_telm13@gmail.fr | 668113131 |
	| Karima Lahj Ahmed | Member | University of Sidi Bel Abbes | hadjahmedkarima@yahoo.fr | 659535111 |

	### Doctoral Students

	| Name and Surname | University | Email | Phone |
	|------------------|------------|-------|-------|
	| Ahmed Ben Aisha | University of Sidi Bel Abbes | benadoudie@gmail.com | 793178258 |
	| Fatima Benafla | University of Sidi Bel Abbes | benaflawafaa@gmail.com | 697857039 |
	| Rahima Bousheta | University of Sidi Bel Abbes | bouchetarahma@gmail.com | 555943688 |
	| Amal Si Mohammed | University of Sidi Bel Abbes | simohammed0690@gmail.com | 540172749 |

	## Part 4: Scientific Committee

	| Name and Surname | Role | Specialty | Institution | Email |
	|------------------|------|-----------|-------------|-------|
	| Karima Lahj Ahmed | President | Media and Communication Sciences | University of Sidi Bel Abbes | hadjahmedkarima@yahoo.fr |
	| Sid Ahmed Makhlouf | Member | Philosophy | University of Sidi Bel Abbes | makphilos@yahoo.fr |
	| Zein El Abidin Maghrebi | Member | Philosophy | University of Sidi Bel Abbes | logiquezino@yahoo.fr |
	| Nasreddine Bouziane | Member | Media and Communication Sciences | University of Constantine 3 | nasreddine.bouziane@univ-constantine3.dz |
	| Jamal Ben Zerrouk | Member | Media and Communication Sciences | University of Skikda | benzeroukd@yahoo.fr |
	| Said Marah | Member | Media and Communication Sciences | University of Sidi Bel Abbes | said_telm13@hotmail.fr |
	| Wassila Ben Amr | Member | Psychology | University of Biskra | wassila.benameur@univ-biskra.dz |
	| Abdenour Seddiki | Member | Sociology | University of Sidi Bel Abbes | seddikinour@yahoo.fr |
	| Aisha Metales | Member | Media and Communication Sciences | University of Sidi Bel Abbes | metalesch12@gmail.com |
	| Amal Khalaf | Member | Media and Communication Sciences | University of Sidi Bel Abbes | bdfamal1519@gmail.com |
	| Mustafa Djelti | Member | Media and Communication Sciences | University of Sidi Bel Abbes | djelti.mostafa@yahoo.com |
	| Soumia Berrahil | Member | Media and Communication Sciences | University of Oran 2 | soumia.berrahil@yahoo.fr |
	| Mohammed Aghoulaiche | Member | Media and Communication Sciences | University of Sidi Bel Abbes | aghoulaiche.transfer@gmail.com |
	| Mohammed Belhamiti | Member | Sociology | University of Sidi Bel Abbes | belhamiti@live.com |
	| Haj Chaib | Member | Library Science | University of Saida | biblio.doc2001@gmail.com |
	| Mokhtar Djlouli | Member | Media and Communication Sciences | University of Tiaret | mokhtardjl20@gmail.com |
	| Oussama Omar | Member | Media and Communication Sciences | University of Sidi Bel Abbes | oussama_sic@yahoo.fr |
	| Assma Regui | Member | Media and Communication Sciences | University of Sidi Bel Abbes | assoum_doctorat@hotmail.fr |
	| Nassima Djemil | Member | Media and Communication Sciences | University of Oran 2 | djemilnassima@hotmail.com |
	| Wassila Oudjdi Damirji | Member | Media and Communication Sciences | University of Sidi Bel Abbes | odw1987@gmail.com |
	| Abdelkarim Rqiq | Member | Arts | University of Sidi Bel Abbes | siquou@yahoo.fr |
	| Nabil Houari | Member | Media and Communication Sciences | University of Skikda | soheilhoura89@gmail.com |
	| Souhila Bediaf | Member | Media and Communication Sciences | University of Skikda | bediafsouhila@gmail.com |
	| Noor El Hoda Obada | Member | Media and Communication Sciences | University of Algiers 3 | n.nour74@yahoo.fr |
	| Souad Lilia Ainsouya | Member | Media and Communication Sciences | University of Souk Ahras | lilia.ainsouya@yahoo.fr |
	| Yassine Hebal | Member | Psychology | University of Sidi Bel Abbes | yacine_22000@hotmail.com |
	| Imen Harfouch | Member | Media and Communication Sciences | University of Tlemcen | dr.imene.harfouche@gmail.com |
	| Amina Ait El Hadj | Member | Media and Communication Sciences | University of El Oued | Aminaaitelhadj2020@gmail.com |
	| Chahrazad Abbane | Member | Macroeconomics | University of Algiers 3 | chahrazad.abbane@gmail.com |
	| Mohammed Rezine | Member | Media and Communication Sciences | University of Sidi Bel Abbes | rezine.mohammed@yahoo.com |
	| Lobna Souigat | Member | Media and Communication Sciences | University of Ouargla | l.souigat@gmail.com |
	| Djamal Eddine Medfouni | Member | Media and Communication Sciences | University of Oum El Bouaghi | djimyhome@hotmail.com |
	| Oussama Demouche | Member | Library Science | University of Sidi Bel Abbes | demouche31@hotmail.fr |
	| Nourine Achache | Member | Sociology | University of Sidi Bel Abbes | nourine.achache@gmail.com |
	| Samia Bouguera | Member | Media and Communication Sciences | University of Annaba | samyoub@gmail.com |
	| El Djellal Meghat | Member | Sociology | University of Sidi Bel Abbes | essalam-1@hotmail.fr |
	| Amina Bessafa | Member | Media and Communication Sciences | University of Algiers 3 | bessafa.amina@gmail.com |
	| Karim Chaadou | Member | Sociology | University of Sidi Bel Abbes | chadou.karim@gmail.com |
	| Mohammed Sahali | Member | Sociology | University of Sidi Bel Abbes | sahali22mohammed@gmail.com |
	| Salih Chelouach | Member | Media and Communication Sciences | University of Skikda | chelouachesaly2011@gmail.com |

	## Members of the Scientific Committee from Abroad

	| Name and Surname | Role | Specialty | Institution | Email |
	|------------------|------|-----------|-------------|-------|
	| Prof. Nour El Din Hamed | Member | | Al-Jouf University, Saudi Arabia | nhamed@ju.edu.sa |
	| Prof. Mehmet Zeki Aydin | Member | Education Sciences | Selcuk University, Turkey | mehmetezeki.aydin@selcuk.edu.tr |
	| Prof. Rasha Abdel Fattah El-Didi | Member | Psychology | Ain Shams University, Egypt | rrashaeldidy@gmail.com |
	| Dr. Rahima Aissani | Member | Media and Communication Sciences | Al Ain University, UAE | rahima.aissani@aau.ac.ae |
	| Dr. Sami Abdel Karim Al-Azraq | Member | Sociology | Ajdabiya University, Libya | sk_top_new@yahoo.com |
	| Dr. Khaled Harzib | Member | Mathematics | Paderborn University, Germany | khaled.harzib@gmail.com |
	| Dr. Reda Abdel Wahid El-Amin | Member | Media and Communication Sciences | Al-Azhar University, Egypt | redaabdelwage.amine@gmail.com |
	| Dr. Amal Saad El-Motwali Osman | Member | Media and Communication Sciences | Mansoura University, Egypt | amalsaadmetwaly@gmail.com |
	| Dr. Abdel Latif Bel-Tayeb | Member | Mathematics | Saudi Arabia | abdellatif.bettayab@gmail.com |
	""")



elif st.session_state.language == "fr":
	st.markdown(f"<center><h5 style='color:rgb(226,135,67);'>Invitation à participer à la conférence internationale :</h5></center>", unsafe_allow_html=True)
	
	st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{}" width="300">
    </div>
    """.format(base64.b64encode(open("coloq_english.jpeg", "rb").read()).decode()),
    unsafe_allow_html=True
	)
	
	st.markdown(f"<center><h3>{translate('page_title')}</h3></center>", unsafe_allow_html=True)
	st.markdown(f"<center><h4>{translate('rest_title')}</h4></center>", unsafe_allow_html=True)
	st.markdown("""
    L'Université Djilali Liabes de Sidi Bel Abbes, Faculté des Sciences Humaines et Sociales, Département des Sciences de l'Information et de la Communication, a le plaisir de vous inviter à participer à cette conférence internationale qui se tiendra les 26 et 27 février 2025.

    ### Aperçu de la Conférence :
    Cette conférence vise à souligner le rôle vital des sciences humaines et sociales dans l'orientation de la recherche en IA en accord avec les valeurs humaines et les objectifs de développement durable.

    ### Objectifs de la Conférence :
    1. Mettre en évidence l'importance des sciences humaines et sociales dans la recherche en IA.
    2. Explorer l'impact de l'IA sur les dimensions sociales, culturelles, éthiques et juridiques.
    3. Encourager la collaboration interdisciplinaire.
    4. Aborder les inégalités et les biais dans le développement de l'IA.
    5. Sensibiliser aux technologies émergentes.

    ### Dates Importantes :
    - Date limite de soumission des résumés : 1er janvier 2025
    - Notification des résumés acceptés : 10 janvier 2025
    - Date limite de soumission des articles complets : 30 janvier 2025
    - Annonce du programme final : 10 février 2025

    ### Directives de Participation :
    - Ouvert aux professeurs, doctorants et chercheurs.
    - Les sujets de recherche doivent s'aligner sur les thèmes de la conférence.
    - Les soumissions doivent être originales et non publiées.
    - Les soumissions individuelles et en co-auteur sont les bienvenues.
    - Les articles peuvent être en arabe, anglais ou français.

    ### Informations de Contact :
    - Téléphone : +213541531962
    - Email : hssai2024@gmail.com
    """)
	st.markdown("""
	## Informations Personnelles

	| |  |
	|-------------|--------|
	| Nom et Prénom | Metales Aicha |
	| Rang | Assistant Professeur |
	| Fonction | Professeur |
	| Email | metales.sic@gmail.com |
	| Téléphone | 541531962 |

	## Partie 3: Comité d'Organisation

	| Nom et Prénom | Rôle | Institution | Email | Téléphone |
	|---------------|------|-------------|-------|-----------|
	| Dr. Omar Oussama | Président | Université de Sidi Bel Abbès | oussama_sic@yahoo.fr | 676494906 |
	| Metales Aicha | Membre | Université de Sidi Bel Abbès | metalesch12@gmail.com | 541531962 |
	| Djelti Mostafa | Membre | Université de Sidi Bel Abbès | djelti.mostafa@yahoo.com | 675332071 |
	| Merah Saïd | Membre | Université de Sidi Bel Abbès | said_telm13@gmail.fr | 668113131 |
	| Lahaj Ahmed Karima | Membre | Université de Sidi Bel Abbès | hadjahmedkarima@yahoo.fr | 659535111 |

	### Doctorants

	| Nom et Prénom | Université | Email | Téléphone |
	|---------------|------------|-------|-----------|
	| Ben Aïcha Ahmed | Université de Sidi Bel Abbès | benadoudie@gmail.com | 793178258 |
	| Benafla Fatiha | Université de Sidi Bel Abbès | benaflawafaa@gmail.com | 697857039 |
	| Boucheta Rahima | Université de Sidi Bel Abbès | bouchetarahma@gmail.com | 555943688 |
	| Si Mohammed Amal | Université de Sidi Bel Abbès | simohammed0690@gmail.com | 540172749 |

	## Partie 4: Comité Scientifique

	| Nom et Prénom | Rôle | Spécialité | Institution | Email |
	|---------------|------|-----------|-------------|-------|
	| Lahaj Ahmed Karima | Président | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | hadjahmedkarima@yahoo.fr |
	| Makhlouf Sid Ahmed | Membre | Philosophie | Université de Sidi Bel Abbès | makphilos@yahoo.fr |
	| Maghreb Zine El Abidine | Membre | Philosophie | Université de Sidi Bel Abbès | logiquezino@yahoo.fr |
	| Nasreddine Bouziane | Membre | Sciences de l'information et de la communication | Université Constantine 3 | nasreddine.bouziane@univ-constantine3.dz |
	| Djemal Ben Zarouq | Membre | Sciences de l'information et de la communication | Université de Skikda | benzeroukd@yahoo.fr |
	| Merah Saïd | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | said_telm13@hotmail.fr |
	| Wassila Benamer | Membre | Psychologie | Université de Biskra | wassila.benameur@univ-biskra.dz |
	| Sadiki Abdelnour | Membre | Sociologie | Université de Sidi Bel Abbès | seddikinour@yahoo.fr |
	| Metales Aicha | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | metalesch12@gmail.com |
	| Khalf Amal | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | bdfamal1519@gmail.com |
	| Djelti Mostafa | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | djelti.mostafa@yahoo.com |
	| Berrahil Soumia | Membre | Sciences de l'information et de la communication | Université d'Oran 2 | soumia.berrahil@yahoo.fr |
	| Aghoulais Mohamed | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | aghoulaiche.transfer@gmail.com |
	| Belhamiti Mohamed | Membre | Sociologie | Université de Sidi Bel Abbès | belhamiti@live.com |
	| Chaïb Hadj | Membre | Sciences des bibliothèques | Université de Saïda | biblio.doc2001@gmail.com |
	| Djeloul Mokhtar | Membre | Sciences de l'information et de la communication | Université de Tiaret | mokhtardjl20@gmail.com |
	| Omar Oussama | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | oussama_sic@yahoo.fr |
	| Rigui Asmaa | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | assoum_doctorat@hotmail.fr |
	| Djamil Nassima | Membre | Sciences de l'information et de la communication | Université d'Oran 2 | djemilnassima@hotmail.com |
	| Ould Demerji Wassila | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | odw1987@gmail.com |
	| Reghigue Abdelkrim | Membre | Arts | Université de Sidi Bel Abbès | siquou@yahoo.fr |
	| Houra Nabil | Membre | Sciences de l'information et de la communication | Université de Skikda | soheilhoura89@gmail.com |
	| Bediaf Souhila | Membre | Sciences de l'information et de la communication | Université de Skikda | bediafsouhila@gmail.com |
	| Abada Nour El Hoda | Membre | Sciences de l'information et de la communication | Université d'Alger 3 | n.nour74@yahoo.fr |
	| Lilia Aïn Souya | Membre | Sciences de l'information et de la communication | Université de Souk Ahras | lilia.ainsouya@yahoo.fr |
	| Hebbal Yacine | Membre | Psychologie | Université de Sidi Bel Abbès | yacine_22000@hotmail.com |
	| Harfouche Imene | Membre | Sciences de l'information et de la communication | Université de Tlemcen | dr.imene.harfouche@gmail.com |
	| Amina Ait El Hadj | Membre | Sciences de l'information et de la communication | Université d'El Oued | Aminaaitelhadj2020@gmail.com |
	| Abane Chahrazad | Membre | Économie | Université d'Alger 3 | chahrazad.abbane@gmail.com |
	| Rezine Mohamed | Membre | Sciences de l'information et de la communication | Université de Sidi Bel Abbès | rezine.mohammed@yahoo.com |
	| Souigat Lobna | Membre | Sciences de l'information et de la communication | Université d'Ouargla | l.souigat@gmail.com |
	| Madfouni Djamal Eddine | Membre | Sciences de l'information et de la communication | Université d'Oum El Bouaghi | djimyhome@hotmail.com |
	| Demouche Oussama | Membre | Sciences des bibliothèques | Université de Sidi Bel Abbès | demouche31@hotmail.fr |
	| Achache Nourine | Membre | Sociologie | Université de Sidi Bel Abbès | nourine.achache@gmail.com |
	| Bouguera Samia | Membre | Sciences de l'information et de la communication | Université d'Annaba | samyoub@gmail.com |
	| Maghtat El Ajjal | Membre | Sociologie | Université de Sidi Bel Abbès | essalam-1@hotmail.fr |
	| Bessafa Amina | Membre | Sciences de l'information et de la communication | Université d'Alger 3 | bessafa.amina@gmail.com |
	| Chadou Karim | Membre | Sociologie | Université de Sidi Bel Abbès | chadou.karim@gmail.com |
	| Sahali Mohamed | Membre | Sociologie | Université de Sidi Bel Abbès | sahali22mohammed@gmail.com |
	| Chelouache Saliha | Membre | Sciences de l'information et de la communication | Université de Skikda | chelouachesaly2011@gmail.com |

	## Membres du Comité Scientifique Hors National

	| Nom et Prénom | Rôle | Université | Institution | Email |
	|---------------|------|-----------|-------------|-------|
	| Prof. Nour El Dine Hamed | Membre | | Université Al Jouf, Arabie Saoudite | nhamed@ju.edu.sa |
	| Prof. Mehmet Zeki Aydin | Membre | Sciences de l'éducation | Université Selçuk, Turquie | mehmetezeki.aydin@selcuk.edu.tr |
	| Prof. Rasha Abdel Fattah El-Didy | Membre | Psychologie | Université Ain Shams, Égypte | rrashaeldidy@gmail.com |
	| Dr. Rahima Aissani | Membre | Sciences de l'information et de la communication | Université Al Ain, Émirats Arabes Unis | rahima.aissani@ua.ac.ae |
	""")


else:
	st.markdown(f"<center><h5 style='color:rgb(226,135,67);'>دعوة للمشاركة في الملتقى العلمي الدولي الموسوم:</h5></center>", unsafe_allow_html=True)
	
	st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{}" width="300">
    </div>
    """.format(base64.b64encode(open("coloq_arab.jpeg", "rb").read()).decode()),
    unsafe_allow_html=True
	)
	
	st.markdown(f"<center><h3>{translate('page_title')}</h3></center>", unsafe_allow_html=True)
	st.markdown(f"<center><h4>{translate('rest_title')}</h4></center>", unsafe_allow_html=True)
	st.markdown("""

	## العلوم الإنسانية والاجتماعية وعلاقتها بأبحاث الذكاء الاصطناعي: نحو ذكاء اصطناعي مسؤول ومستدام

	يسر جامعة جيلالي ليابس، سيدي بلعباس، كلية العلوم الإنسانية والاجتماعية، قسم علوم الإعلام والاتصال، دعوتكم للمشاركة في الملتقى الدولي الموسوم ب "العلوم الإنسانية والاجتماعية وعلاقتها بأبحاث الذكاء الاصطناعي: نحو ذكاء اصطناعي مسؤول ومستدام"، الذي سيُعقد يومي 26 و27 فبراير 2025.

	يهدف هذا الملتقى إلى تسليط الضوء على الدور الحيوي لهذه العلوم في توجيه وتطوير أبحاث الذكاء الاصطناعي بما يتماشى مع القيم الإنسانية ويلبي متطلبات التنمية المستدامة، من خلال بناء جسور التعاون بين الباحثين والمتخصصين من جميع أنحاء العالم لتبادل الأفكار حول كيفية المساهمة في تطوير ذكاء اصطناعي بشكل يخدم المجتمع ويدعم الاستدامة.

	## أهداف الملتقى:

	1. التأكيد على أهمية العلوم الإنسانية والاجتماعية في تطوير أبحاث الذكاء الاصطناعي بما يحقق التوازن بين الفوائد والمخاطر على الأفراد والمجتمعات.
	2. فهم تأثير الذكاء الاصطناعي على الجوانب الاجتماعية والثقافية والأخلاقية والقانونية، وتوجيه تطويره بما يتوافق مع الاحتياجات والقيم الانسانية.
	3. تعزيز التعاون بين الباحثين من مختلف التخصصات لاستكشاف إمكانيات الذكاء الاصطناعي واستخدامها بشكل مسؤول ومستدام.
	4. التخفيف من حدة التفاوت والتحيزات من خلال الفهم العميق للبنى الاجتماعية والسياقات الثقافية التي تجري فيها التفاعلات بين الأفراد والأنظمة الذكية.
	5. تعزيز الفهم وزيادة وعي الأفراد والمجتمعات بالتقنيات الحديثة لمواكبة التطورات المتسارعة وذلك عبر تزويدهم بالمعلومات الموثوقة والدقيقة ومكافحة الأخبار الكاذبة والمضللة والتحيزات.

	## مواعيد هامة:

	- آخر أجل لإرسال الملخصات: 1/01/2025
	- الرد على الملخصات المقبولة: 10/ 01/ 2025
	- آخر أجل لإرسال المداخلات كاملة: 30/01/2025   
	- الإعلان عن البرنامج النهائي للملتقى: 10/02/2025

	## شروط المشاركة:

	- المشاركة مفتوحة لجميع الأساتذة وطلبة الدكتوراه والباحثين في الجامعات والمؤسسات الأكاديمية.
	- أن يدرج الموضوع ضمن أحد محاور الملتقى
	- أن لا يكون البحث قد سبق نشره أو المشاركة به.
	- تقبل المشاركات الفردية والثنائية.
	- تقبل المداخلات باللغات العربية والإنجليزية والفرنسية.

	للتسجيل يرجى زيارة الموقع التالي: 
	https:// 

	## للتواصل والاستفسار:

	- رقم الهاتف: +213541531962
	- البريد الإلكتروني: hssai2024@gmail.com

	نتطلع لاستقبال أبحاث مميزة تساهم في دعم أهداف الملتقى ودفع عجلة البحث العلمي في مجالات الذكاء الاصطناعي والمسؤولية الاجتماعية.
		""")
	st.markdown("""
	## معلومات شخصية

	|  |  |
	|-------|-------|
	| الاسم واللقب | مطالس عائشة |
	| الرتبة | أستاذ مساعد |
	| الوظيفة | أستاذ |
	| البريد الالكتروني | metales.sic@gmail.com |
	| الهاتف | 541531962 |

	## الجزء 3: اللجنة التنظيمية

	| الاسم واللقب | الصفة | المؤسسة | البريد الالكتروني | الهاتف |
	|-------------|------|---------|-------------------|--------|
	| د.عمر أوسامة | رئيس | جامعة سيدي بلعباس | oussama_sic@yahoo.fr | 676494906 |
	| مطالس عائشة | عضو | جامعة سيدي بلعباس | metalesch12@gmail.com | 541531962 |
	| جلطي مصطفى | عضو | جامعة سيدي بلعباس | djelti.mostafa@yahoo.com | 675332071 |
	| مراح سعيد | عضو | جامعة سيدي بلعباس | said_telm13@gmail.fr | 668113131 |
	| لحاج أحمد كريمة | عضو | جامعة سيدي بلعباس | hadjahmedkarima@yahoo.fr | 659535111 |

	### طلبة الدكتوراه

	| الاسم واللقب | الجامعة | البريد الالكتروني | الهاتف |
	|-------------|--------|-------------------|--------|
	| بن عائشة أحمد | جامعة سيدي بلعباس | benadoudie@gmail.com | 793178258 |
	| بنافلة فتيحة | جامعة سيدي بلعباس | benaflawafaa@gmail.com | 697857039 |
	| بوشتة رحيمة | جامعة سيدي بلعباس | bouchetarahma@gmail.com | 555943688 |
	| سي محمد أمال | جامعة سيدي بلعباس | simohammed0690@gmail.com | 540172749 |

	## الجزء 4: اللجنة العلمية

	| الاسم واللقب | الصفة | التخصص | المؤسسة | البريد الالكتروني |
	|-------------|------|---------|---------|-------------------|
	| لحاج أحمد كريمة | رئيس | علوم الاعلام والاتصال | جامعة سيدي بلعباس | hadjahmedkarima@yahoo.fr |
	| مخلوف سيد أحمد | عضو | فلسفة | جامعة سيدي بلعباس | makphilos@yahoo.fr |
	| مغربي زين العابدين | عضو | فلسفة | جامعة سيدي بلعباس | logiquezino@yahoo.fr |
	| نصر الدين بوزيان | عضو | علوم الاعلام والاتصال | جامعة قسنطينة 3 | nasreddine.bouziane@univ-constantine3.dz |
	| جمال بن زروق | عضو | علوم الاعلام والاتصال | جامعة سكيكدة | benzeroukd@yahoo.fr |
	| مراح سعيد | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | said_telm13@hotmail.fr |
	| وسيلة بن عامر | عضو | علم النفس | جامعة بسكرة | wassila.benameur@univ-bisakra.dz |
	| صديقي عبدالنور | عضو | علم الاجتماع | جامعة سيدي بلعباس | seddikinour@yahoo.fr |
	| مطالس عائشة | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | metalesch12@gmail.com |
	| خالف أمال | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | bdfamal1519@gmail.com |
	| جلطي مصطفى | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | djelti.mostafa@yahoo.com |
	| برحيل سمية | عضو | علوم الاعلام والاتصال | جامعة وهران 2 | soumia.berrahil@yahoo.fr |
	| أغولايش محمد | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | aghoulaiche.transfer@gmail.com |
	| يلحميتي محمد | عضو | علم الاحتماع | جامعة سيدي بلعباس | belhamiti@live.com |
	| شعيب حاج | عضو | علم المكتبات | جامعة سعيدة | biblio.doc2001@gmail.com |
	| جلولي مختار | عضو | علوم الاعلام والاتصال | جامعة تيارت | mokhtardjl20@gmail.com |
	| عمر أوسامة | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | oussama_sic@yahoo.fr |
	| ريغي أسماء | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | assoum_doctorat@hotmail.fr |
	| جميل نسيمة | عضو | علوم الاعلام والاتصال | جامعة وهران 2 | djemilnassima@hotmail.com |
	| وجدي دمرجي وسيلة | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | odw1987@gmail.com |
	| رقيق عبد الكريم | عضو | فنون | جامعة سيدي بلعباس | siquou@yahoo.fr |
	| حورة نبيل | عضو | علوم الاعلام والاتصال | جامعة سكيكدة | soheilhoura89@gmail.com |
	| بضياف سوهيلة | عضو | علوم الاعلام والاتصال | جامعة سكيكدة | bediafsouhila@gmail.com |
	| عبادة نور الهدى | عضو | علوم الاعلام والاتصال | جامعة الجزائر 3 | n.nour74@yahoo.fr |
	| ليليا عين سوية | عضو | علوم الاعلام والاتصال | جامعة سوق أهراس | lilia.ainsouya@yahoo.fr |
	| حبال ياسين | عضو | علم النفس | جامعة سيدي بلعباس | yacine_22000@hotmail.com |
	| حرفوش إيمان | عضو | علوم الاعلام والاتصال | جامعة تلمسان | dr.imene.harfouche@gmail.com |
	| أمينة آيت الحاج | عضو | علوم الاعلام والاتصال | جامعة الوادي | Aminaaitelhadj2020@gmail.com |
	| عبان شهرزاد | عضو | اقتصاد كلي | جامعة الجزائر 3 | chahrazad.abbane@gmail.com |
	| رزين محمد | عضو | علوم الاعلام والاتصال | جامعة سيدي بلعباس | rezine.mohammed@yahoo.com |
	| سويقات لبنى | عضو | علوم الاعلام والاتصال | جامعة ورقلة | l.souigat@gmail.com |
	| مدفوني جمال الدين | عضو | علوم الاعلام والاتصال | جامعة أم البواقي | djimyhome@hotmail.com |
	| دموش أسامة | عضو | علم المكتبات | جامعة سيدي بلعباس | demouche31@hotmail.fr |
	| عشاش نورين | | علم الاجتماع | جامعة سيدي بلعباس | nourine.achache@gmail.com |
	| بوقرة سامية | عضو | علوم الاعلام والاتصال | جامعة عنابة | samyoub@gmail.com |
	| مغتات العجال | عضو | علم الاجتماع | جامعة سيدي بلعباس | essalam-1@hotmail.fr |
	| بصافة أمينة | عضو | علوم الاعلام والاتصال | جامعة الجزائر 3 | bessafa.amina@gmail.com |
	| شعدو كريم | عضو | علم الاجتماع | جامعة سيدي بلعباس | chadou.karim@gmail.com |
	| سهالي محمد | عضو | علم الاجتماع | جامعة سيدي بلعباس | sahali22mohammed@gmail.com |
	| شلواش صليحة | عضو | علوم الاعلام والاتصال | جامعة سكيدة | chelouachesaly2011@gmail.com |

	## أعضاء اللجنة العلمية من خارج الوطن

	| الاسم واللقب | الصفة | الجامعة | المؤسسة | البريد الالكتروني |
	|-------------|------|---------|---------|-------------------|
	| أ.د/ نورالدين حامد | عضو | | جامعة الجوف المملكة العربية السعودية | nhamed@ju.edu.sa |
	| أ.د/ محمت زكي ايدن | عضو | علوم التربية | جامعة سلجوق تركيا | mehmetezeki.aydin@selcuk.edu.tr |
	| أ.د / رشا عبد الفتاح الديدي | عضو | علم النفس | جامعة عين شمس - مصر | rrashaeldidy@gmail.com |
	| د/ رحيمة عيساني | عضو | علوم الاعلام والاتصال | جامعة العين الامارات العربية المتحدة | rahima.aissani@aau.ac.ae |
	| د/ سامي عبد الكريم الأزرق | عضو | علم الاجتماع | جامعة أجدابيا- ليبيا | sk_top_new@yahoo.com |
	| د/ خالد حريز | عضو | الرياضيات | جامعة Pederbon ألمانيا | khaled.harzib@gmail.com |
	| د/ رضا عبد الواجد الأمين | عضو | علوم الاعلام والاتصال | جامعة الأزهر - مصر | redaabdelwage.amine@gmail.com |
	| د/ أمال سعد المتولي عثمان | عضو | علوم الاعلام والاتصال | جامعة المنصورة - مصر | amalsaadmetwaly@gmail.com |
	| د/ عبد اللطيف بالطيب | عضو | الرياضيات | المملكة العربية السعودية | abdellatif.bettayab@gmail.com |
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
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
        }
    </style>
    <div class="footer">
        <p>Contact us at: <a href="mailto:hssaiudl@gmail.com">hssaiudl@gmail.com</a> | Phone: +213541531962</p>
    </div>
    """,
    unsafe_allow_html=True
)
