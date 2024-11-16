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
if st.session_state.language == "fr":
    navigate_to("register")

st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{}" width="70">
    </div>
    """.format(base64.b64encode(open("logo_univ.png", "rb").read()).decode()),
    unsafe_allow_html=True
	)

st.markdown(f"<h5 style='color:rgb(226,135,67);'>التسجيل في الملتقى</h5>", unsafe_allow_html=True)



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
        st.error("حدث خطأ أثناء إرسال البريد الإلكتروني، حاول مرة أخرى. إذا استمرت المشكلة، اتصل بنا.")
        return False

# Main Streamlit app
st.title(" استمارة التسجيل في الملتقى")

full_name = st.text_input("الاسم الكامل (كما يظهر في الوثائق الرسمية)")
academic_degree = st.selectbox("الدرجة الأكاديمية", ["دكتوراه", "ماجستير", "بكالوريوس", "أخرى"])
specialization = st.text_input("مجال التخصص")
current_position = st.text_input("المسمى الوظيفي الحالي")
institution = st.text_input("المؤسسة المنتمي إليها")
country = st.text_input("دولة الإقامة")
nationality = st.text_input("الجنسية")
email = st.text_input("عنوان البريد الإلكتروني")
confirm_email = st.text_input("تأكيد عنوان البريد الإلكتروني")
phone = st.text_input("رقم الهاتف (يشمل رمز الدولة)")
paper_title = st.text_input("عنوان البحث المقدم")
keywords = st.text_input("الكلمات المفتاحية (حتى 5، مفصولة بفواصل)")
conference_theme = st.selectbox("محور الملتقى", ["المحور 1: مدخل للذكاء الاصطناعي وأهميته في المجتمع الحديث", 
                                                   "المحور 2: الخلفية الفلسفية والتاريخية لتطور أبحاث الذكاء الاصطناعي",
                                                   "المحور 3: إسهامات علم النفس وعلم الاجتماع في فهم التفاعل بين الانسان والنظم الذكية",
                                                   "المحور 4: دور اللغويات والتواصل والدراسات الثقافية في فهم ومعالجة اللغات الطبيعية وضمان التواصل الفعال بين الإنسان والآلة", 
                                                   "المحور 5: اسهامات الاعلام والاتصال في تطوير الذكاء الاصطناعي والتوعية بفوائده ومخاطره",
                                                   "المحور 6: اسهامات علم الاقتصاد في فهم التأثيرات الاقتصادية للذكاء الاصطناعي واستكشاف كيفية استخدامه لتحقيق التنمية المستدامة", 
                                                   "المحور 7: القضايا الفقهية، الأخلاقية، القانونية والسياسية المرتبطة بتطور واستخدام الذكاء الاصطناعي"])
abstract_file = st.file_uploader("تحميل الملخص (ملف PDF أو DOCX أو DOC، 100-150 كلمة)", type=["pdf", "docx", "doc"])


if st.button("التسجيل"):
    if email != confirm_email:
        st.error("عناوين البريد الإلكتروني لا تتطابق. يرجى التحقق والمحاولة مرة أخرى.")
    elif full_name and academic_degree and specialization and current_position and institution and country and nationality and email and confirm_email and phone and paper_title and keywords and conference_theme and abstract_file:
        # Save the uploaded file
        #abstract_path = os.path.join("uploads", abstract_file.name)
        with st.spinner("تحميل معلوماتك..."):
            # with open(abstract_path, "wb") as f:
            #     f.write(abstract_file.getbuffer())
            # تحضير محتوى البريد الإلكتروني
            email_body = f"""
            تسجيل جديد في الملتقى:

            الاسم الكامل: {full_name}
            الدرجة الأكاديمية: {academic_degree}
            مجال التخصص: {specialization}
            الوظيفة الحالية: {current_position}
            المؤسسة التابعة: {institution}
            الدولة: {country}
            الجنسية: {nationality}
            عنوان البريد الإلكتروني: {email}
            رقم الهاتف: {phone}
            عنوان البحث: {paper_title}
            الكلمات المفتاحية: {keywords}
            محور الملتقى: {conference_theme}

            تم إرفاق ملف الملخص.
            """


            # Send email
            # if send_email("hssaiudl@gmail.com", "تسجيل جديد في الملتقى", email_body, abstract_file):
            #     st.success(f"شكرًا لتسجيلك، {full_name}! لقد تلقينا معلوماتك وملخص البحث.")
            # else:
            #     st.error("حدث خطأ أثناء معالجة تسجيلك. يرجى المحاولة مرة أخرى لاحقًا.")
            if send_email("hssaiudl@gmail.com", "New Conference Registration", email_body, abstract_file):
                st.success(f"""
                شكرًا لتسجيلك، {full_name}!
                لقد استلمنا بنجاح معلوماتك والملخص الخاص بك.
                إذا كان عنوان البريد الإلكتروني الذي قدمته صحيحًا، فستتلقى رسالة تأكيد قريبًا.
                إذا كانت لديك أي أسئلة أو تحتاج إلى إجراء أي تغييرات، فلا تتردد في الاتصال بنا مباشرة على hssaiudl@gmail.com أو عبر الهاتف على +213 541 531 962.
                """)
                body = f"""
                عزيزي {full_name}،

                شكرًا لتقديم معلوماتك والملخص الخاص بك لـ {translate('page_title')} المقرر عقده في 26-27 فبراير 2025 في جامعة جيلالي ليابس، سيدي بلعباس. نحن متحمسون لمشاركتك في هذا الحدث!

                تفاصيل التقديم:
                لقد استلمنا بنجاح مشاركتك، والتي تتضمن:

                عنوان الورقة: {paper_title}

                الخطوات التالية
                ستقوم لجنة المراجعة بتقييم جميع المشاركات، وسنخطرك بحالة القبول بحلول 10 يناير 2025. إذا تم قبول مشاركتك، سيتم تزويدك بمزيد من التفاصيل حول إرشادات العرض والتسجيل.

                إذا كانت لديك أي أسئلة أو تحتاج إلى مزيد من المعلومات، فلا تتردد في التواصل معنا على hssaiudl@gmail.com أو +213 541 531 962.

                شكرًا لك مرة أخرى على مساهمتك. نتطلع إلى مؤتمر ناجح ونقدر مشاركتك!

                مع أطيب التحيات،

                د. مطالس عائشة
                رئيسة الملتقى
                
                """
                time.sleep(10)
                send_email(email, "تأكيد تقديم مشاركتك في المؤتمر", body)

            else:
                st.error("حدث خطأ أثناء معالجة تسجيلك. يرجى المحاولة مرة أخرى لاحقًا.")

            # Clean up the uploaded file
            # os.remove(abstract_path)
    else:
        st.error("يرجى ملء جميع الحقول وتحميل الملخص الخاص بك.")

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