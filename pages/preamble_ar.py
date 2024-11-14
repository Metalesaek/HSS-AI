import streamlit as st
from streamlit_navigation_bar import st_navbar
import os

import pandas as pd
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

st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{}" width="70">
    </div>
    """.format(base64.b64encode(open("logo_univ.png", "rb").read()).decode()),
    unsafe_allow_html=True
	)

if st.session_state.language == "fr":
    navigate_to("preamble")
if st.session_state.language == "en":
    navigate_to("preamble")

st.markdown(f"<center><h5 style='color:rgb(226,135,67);'>{translate('preamble')}</h5></center>", unsafe_allow_html=True)
st.markdown(f"<center><h3>{translate('page_title')}</h3></center>", unsafe_allow_html=True)
st.markdown(f"<center><h4>{translate('rest_title')}</h4></center>", unsafe_allow_html=True)

st.markdown("""

يعتبر الذكاء الاصطناعي واحدًا من أهم التحديات التي لم تواجه البشرية مثلها من قبل، حيث يمتد إلى مجالات متعددة ويشمل مختلف التخصصات، وقد تطور الذكاء الاصطناعي في السنوات الأخيرة بسرعة كبيرة، بفضل تكييف ودمج مجموعة واسعة من تقنيات حل المشكلات، بما في ذلك المنطق والرياضيات والشبكات العصبونية الاصطناعية والأساليب القائمة على الإحصاء والاحتمالات، كما يستفيد الذكاء الاصطناعي أيضا من علم النفس واللغويات والفلسفة والاقتصاد والقانون والعديد من المجالات الأخرى. والنواة الأساسية لانطلاق الأبحاث في هذا المجال بدأت من محاولات محاكاة البشر وقد أثار ذلك الأمر حججاً فلسفية حول العواقب الأخلاقية لخلق كائنات اصطناعية مزودة بذكاء يشبه البشر؛ وهنا تتجلى أهمية العلوم الإنسانية والاجتماعية التي تلعب دورًا هامًا في تحسين المنتجات الحالية للذكاء الاصطناعي، والتنبؤ بالتطورات المستقبلية له من خلال التركيز على دراسة الجوانب الاجتماعية والثقافية والسلوكية والإدراكية للإنسان.

فالقضية الرئيسية في تطوير أبحاث الذكاء الاصطناعي تتمحور حول فهم تفاعل الإنسان والمجتمع مع التكنولوجيا، ومن خلال هذا الفهم يمكن تحسين تصميم النظم الذكية وتطويرها بما يخدم مصلحة الأفراد والمجتمعات، والنقاشات في هذا المجال مهمة للتقنيين والمطورين لتحديد أهدافهم التقنية، كما هي مهمة للباحثين في العلوم الإنسانية والاجتماعية لتوجيه مسارات بحثهم في الاتجاهات التي تخدم مصالح البشرية في تحقيق الاستفادة القصوى من تطور الذكاء الاصطناعي، وكذلك لمواجهة التحديات الأخلاقية والقانونية الحالية والمستقبلية التي يمكن أن تصاحب هذه التطورات، فعلى الرغم من حقيقة أن الذكاء الاصطناعي لا يزال في بداياته ولم يصل بعد إلى مستوى تطلعات القائمين عليه مقارنة بالذكاء الفطري، إلا أنه أكثر إبداعات البشرية تعقيدًا وإذهالًا حتى الآن، وأكثرها غموضا من ناحية عدم القدرة على التنبؤ بكل الاحتمالات التي من الممكن أن يسفر عنها هذا التطور في المستقبل.

فإذا كان الهدف من الذكاء الاصطناعي هو محاكاة الانسان أو أي كائن حي آخر، فيمكن عندئذ أن نشبه العتاد والمكونات المادية لهذه التكنولوجيا بجسد هذا الكائن أو الانسان، في حين تحتل البرمجيات والإحصاء والمنطق الرياضي وهندسة الحاسوب مكانة الدماغ والعمليات العقلية، وتمثل العلوم الإنسانية والاجتماعية الجانب الروحي لهذا العلم والمحرك الأساسي لهذا الجسد، فلقد أثبت لنا السياق التاريخي لتطور هذا المجال والأبحاث الحالية أن إسهامات الفلسفة بفروعها وعلم النفس واللغويات والفنون وغيرها من التخصصات في مجالات العلوم الإنسانية لا تقل أهمية عن الرياضيات والإحصاء وهندسة الحاسوب ولغات البرمجة وعلم الأعصاب، وذلك من منطلق حقيقة مفادها أن الذكاء الاصطناعي هو مجال بحثي ضخم ومتعدد التخصصات وسريع التطور والنمو.

وهو ما يسعى له هذا الملتقى من خلال تسليط الضوء على الدور الحيوي الذي لعبته الأبحاث والدراسات في مجال العلوم الإنسانية والاجتماعية في تطوير هذا المجال، من خلال حل العديد من المشكلات المتعلقة بتطوير ذكاء اصطناعي فعال والحد من المخاطر المحتملة التي قد تنجم عنه في مختلف المجالات.


### محاور الملتقى:

1. **مدخل للذكاء الاصطناعي وأهميته في المجتمع الحديث**:

يقدم هذا المحور نظرة عامة على مجال الذكاء الاصطناعي، وتطوره التاريخي، وطبيعته متعددة التخصصات، ومجالاته وفروعه وتطبيقاته، ومتطلباته الرئيسية بهدف توفير فهم شامل للتداخل بين هذا المجال والعلوم الإنسانية والاجتماعية.

2. **الخلفية الفلسفية والتاريخية لتطور أبحاث الذكاء الاصطناعي**:

يسعى هذا المحور إلى إبراز أهمية الجانب الفلسفي والتاريخي في فهم السياق الذي نشأت فيه هذه التكنولوجيا المتقدمة، وتتبع تطور الأفكار والمفاهيم المرتبطة بها، من خلال التطرق لأهم القضايا الفلسفية المرتبطة بالمناقشات الحالية والمستقبلية لهذا الحقل، وفحص النظريات المختلفة حول العقل والوعي وتأثيراتها على البحوث في هذا المجال، ويتناول مسألة ما إذا كانت الآلات قادرة على امتلاك الحالات العقلية والتجارب الشخصية، وأهمية  المنهج التاريخي لتتبع مسار هذه التطورات والتغيرات وانعكاساتها وتأثيراتها على الفرد والمجتمع.

3. **إسهامات علم النفس وعلم الاجتماع في فهم التفاعل بين الانسان والنظم الذكية**:

يلعب كل من علم الاجتماع وعلم النفس دورا محوريا بارزا في مجالات تطوير أبحاث الذكاء الاصطناعي، وخاصة في مجالات تقنيات التعلم الآلي والتعلم العميق والتفاعل مع الروبوتات، حيث يتجلى دور علم النفس في فهم سلوك البشر وطبيعة تفاعلهم مع التكنولوجيا والذكاء الاصطناعي، والتفاعل البشري-آلي بشكل أعمق، ويوفر الإطار النظري والأسس العلمية لفهم سلوك الأفراد وتحليله، في حين يساعد علم الاجتماع على فهم البنى الاجتماعية وأشكال التفاعل بين الأفراد والجماعات الأمر الذي يساعد على تطوير نماذج وأنظمة ذكاء اصطناعي تتفاعل بشكل أفضل مع المستخدمين وتلبي احتياجاتهم الفعلية، بطرق تعزز تجربة المستخدم وتعزز تفاعله بشكل طبيعي، بما يتوافق مع احتياجات الأفراد والمجتمعات ويساهم في فهم التأثيرات الناجمة عن الأنظمة الذكية.

4. **دور اللغويات والتواصل والدراسات الثقافية في فهم ومعالجة اللغات الطبيعية وضمان التواصل الفعال بين الإنسان والآلة**:

تلعب اللغويات دورًا حيويًا في تحسين التفاعل بين الإنسان والذكاء الاصطناعي من خلال تطوير نظم التحدث والفهم اللغوي، لأن فهم بنية اللغة والثقافة يمكن أن يساهم في تطوير أنظمة أكثر فاعلية وفهمًا دقيقًا للأوامر والتفسيرات البشرية، وتراعي الفروقات الثقافية والتنوع، لذلك يستعرض هذا المحور الدور الفعال للغويات والدراسات الثقافية في مواجهة أهم التحديات للذكاء الاصطناعي، المتعلقة بمعالجة اللغة الطبيعية وضمان تحقيق التواصل الفعال بين الإنسان والآلة، ومدى قدرة أجهزة الحاسب على تحليل وفهم وتوليد اللغة البشرية ، بما في ذلك الكلام وبطريقة تراعي السياق والتنوع الثقافي وأهم التطورات الحاصلة في هذا المجال.

5. **اسهامات الاعلام والاتصال في تطوير الذكاء الاصطناعي والتوعية بفوائده ومخاطره**:

حيث تتجلى أهمية الاعلام والاتصال في نشر الوعي وتزويد الجماهير بالمعلومات الكافية والحديثة حول أساسيات ومتطلبات الذكاء الاصطناعي، وفوائده ومخاطره، من خلال التغطية الإعلامية الموضوعية للقضايا الأكثر أهمية وتأثيرا على الفرد والمجتمع، ونشر نتائج الأبحاث والابتكارات الحالية، مما قد يساهم في تعزيز الفهم وتوعية الأفراد والمؤسسات الحكومية والخاصة بضرورة الاستثمار في هذا المجال وخلق بيئة آمنة للتواصل بين الباحثين والمختصين وصناع القرار عبر مختلف قنوات الاتصال.

6. **اسهامات علم الاقتصاد في فهم التأثيرات الاقتصادية للذكاء الاصطناعي واستكشاف كيفية استخدامه لتحقيق التنمية المستدامة**:

يسعى هذا المحور إلى ابراز الدور الفعال لعلم الاقتصاد في فهم التأثيرات الاقتصادية للذكاء الاصطناعي كونه يمتلك الأدوات والآليات اللازمة لتحليل هذه التأثيرات وتوجيهها بما يضمن تحقيق التنمية المستدامة والتوزيع العادل للفرص، ووضع السياسات الاقتصادية المناسبة لتطوير الأبحاث في هذا المجال خاصة مع تنامي الاقتصاد الرقمي والاقتصاد القائم على المعرفة وتشجيع الابتكار. 

7. **القضايا الفقهية، الأخلاقية، القانونية والسياسية المرتبطة بتطور واستخدام الذكاء الاصطناعي**:

يسعى هذا المحور إلى إبراز دور العلوم الإنسانية والاجتماعية في تحديد المبادئ الأخلاقية والقيم الإنسانية المتعلقة بتطوير واستخدام الذكاء الاصطناعي، ووضع التشريعات والسياسات الحالية والمستقبلية لتنظيمه، فمن خلال فهم تأثير التكنولوجيا على الفرد والمجتمع يمكن توجيه تطوير الذكاء الاصطناعي بطرق تحافظ على القيم الأخلاقية وتحمي حقوق الأفراد والمجتمعات، من أجل ضمان تحقيق التوازن بين الفوائد والمخاطر في تأثيراته الاقتصادية والاجتماعية.

### أهداف الملتقى

1. التأكيد على أهمية العلوم الإنسانية والاجتماعية في تطوير أبحاث الذكاء الاصطناعي بما يحقق التوازن بين الفوائد والمخاطر على الأفراد والمجتمعات.
2. فهم تأثير الذكاء الاصطناعي على الجوانب الاجتماعية والثقافية والأخلاقية والقانونية، وتوجيه تطويره بما يتوافق مع الاحتياجات والقيم الانسانية.
3. تعزيز التعاون بين الباحثين من مختلف التخصصات لاستكشاف إمكانيات الذكاء الاصطناعي واستخدامها بشكل مسؤول ومستدام.
4. التخفيف من حدة التفاوت والتحيزات من خلال الفهم العميق للبنى الاجتماعية والسياقات الثقافية التي تجري فيها التفاعلات بين الأفراد والأنظمة الذكية.
5. تعزيز الفهم وزيادة وعي الأفراد والمجتمعات بالتقنيات الحديثة لمواكبة التطورات المتسارعة وذلك عبر تزويدهم بالمعلومات الموثوقة والدقيقة ومكافحة الأخبار الكاذبة والمضللة والتحيزات.



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
        <p>Contact us at: <a href="mailto:hssai2024@gmail.com">hssai2024@gmail.com</a> | Phone: +213541531962</p>
    </div>
    """,
    unsafe_allow_html=True
)