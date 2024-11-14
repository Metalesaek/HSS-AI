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