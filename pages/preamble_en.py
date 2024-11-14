import streamlit as st
from streamlit_navigation_bar import st_navbar
import os

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

nav_items = ["home","preamble", "schedule",  "register",  LANGUAGE_SELECTOR_PLACEHOLDER]
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

if st.session_state.language == "fr":
    navigate_to("preamble")
if st.session_state.language == "ar":
    navigate_to("preamble")

st.markdown(f"<center><h5 style='color:rgb(226,135,67);'>{translate('preamble')}</h5></center>", unsafe_allow_html=True)
st.markdown(f"<center><h3>{translate('page_title')}</h3></center>", unsafe_allow_html=True)
st.markdown(f"<center><h4>{translate('rest_title')}</h4></center>", unsafe_allow_html=True)

st.markdown("""

Artificial Intelligence (AI) presents one of the most significant challenges humanity has faced, spanning numerous disciplines and advancing rapidly through the integration of diverse problem-solving methods, including logic, mathematics, artificial neural networks, statistics, and probability. AI also draws from psychology, linguistics, philosophy, economics, and law, among other fields.

The foundation of AI research emerged from attempts to simulate human intelligence, sparking philosophical debates about the ethical implications of creating artificial beings with human-like capabilities. This highlights the essential role of the humanities and social sciences in shaping AI’s evolution, particularly by focusing on the social, cultural, behavioral, and cognitive aspects of human interaction with technology.

The core challenge in AI research is understanding the dynamic relationship between humans, society, and technology. By fostering this understanding, AI systems can be designed to better serve individual and societal interests. This discourse is essential not only for technical developers aiming to refine their goals but also for researchers in the humanities and social sciences to direct their work toward maximizing AI’s societal benefits and addressing its ethical and legal implications. Although AI has yet to reach the aspirations of its pioneers, it remains humanity’s most complex creation—one whose future is full of potential yet difficult to predict.

If AI’s ultimate goal is to simulate human-like or other living beings' capabilities, we can compare the hardware to the physical body and software, logic, and engineering to the brain. Meanwhile, the humanities and social sciences can be seen as the "spiritual" element driving this field, ensuring that AI’s progress aligns with human values.

By understanding the interdisciplinary contributions—from philosophy and psychology to mathematics and neuroscience—we can see that AI is a multidisciplinary field poised for continued growth and complexity. This conference aims to underscore the pivotal role of humanities and social sciences research in shaping AI’s future, solving complex problems, and minimizing potential risks across diverse fields.

### Conference Topics:
1. **The Role and Significance of AI in Modern Society**:

This section provides an overview of AI, its historical development, interdisciplinary nature, fields, branches, applications, and essential requirements, aiming to showcase the interplay between AI and the humanities and social sciences.

2. **Philosophical and Historical Foundations of AI**:

This topic explores the philosophical and historical contexts from which AI emerged. It examines the core philosophical issues surrounding AI, including theories about mind and consciousness, and questions about whether machines could one day possess self-awareness. This axis also emphasizes the historical context to understand how AI’s development affects both individuals and society.

3. **Psychology and Sociology’s Role in Human-AI Interaction**:

This section highlights how psychology and sociology contribute to understanding human behavior and societal structures in relation to intelligent systems. Insights from these fields are instrumental in developing AI models that enhance user interaction and reflect the needs of individuals and societies, ultimately enriching the human-AI experience.

4. **Linguistics, Communication, and Cultural Studies in Natural Language Processing**:

Linguistics plays a central role in bridging communication between humans and machines. This section examines how an understanding of language and cultural nuances can improve AI's ability to interpret commands and interact effectively with diverse populations, addressing the unique challenges of natural language processing and intercultural communication.

5. **Media and Communication in Raising AI Awareness**:

The media’s role in informing the public about AI’s benefits and risks is crucial for fostering understanding. Through accurate, unbiased reporting and dissemination of research findings, media and communication studies encourage informed perspectives on AI among individuals, organizations, and policymakers.

6. **Economic Impacts and Sustainable Development**:

Economics provides tools to understand AI’s economic implications and offers guidance for crafting policies that promote sustainable development and equitable opportunity. This topic focuses on strategies for integrating AI within the digital economy while encouraging innovation and fairness.

7. **Ethical, Legal, and Political Considerations in AI Development**:

This section explores the ethical, legal, and political questions that arise as AI advances, underscoring the importance of establishing guidelines that respect human rights and social values. It advocates for a balanced approach to AI development that considers both its social benefits and potential risks.

### Conference Objectives:
1. Emphasize the importance of humanities and social sciences in AI research to balance AI’s benefits and risks for society.
2. Explore AI’s impact on social, cultural, ethical, and legal domains to guide development consistent with human needs and values.
3. Strengthen interdisciplinary collaboration to responsibly and sustainably harness AI’s potential.
4. Address inequality and bias by understanding the social and cultural contexts in which humans and intelligent systems interact.
5. Foster awareness of modern technologies, promoting public understanding and resilience against misinformation and biases.

""")
