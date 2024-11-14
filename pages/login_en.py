import streamlit as st

st.title("Login")

email = st.text_input("Email Address")
password = st.text_input("Password", type="password")

if st.button("Login"):
    # Here you would typically verify the user credentials
    st.success("Login successful!")