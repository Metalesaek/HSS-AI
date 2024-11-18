import streamlit as st

st.title("Featured Speakers")

col1, col2 = st.columns(2)

with col1:
    st.subheader("John Doe")
    st.image("https://placekitten.com/200/200")
    st.write("AI Researcher at Tech Corp")

with col2:
    st.subheader("Jane Smith")
    st.image("https://placekitten.com/201/201")
    st.write("Data Science Lead at Data Inc")


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