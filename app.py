import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Property Analysis Tool",
    page_icon="🏠",
    layout="centered"
)

# Main title and description
st.title("🏠 Property Analysis Tool")
st.markdown("""
Welcome to the Property Analysis Tool! This application helps you analyze and evaluate properties.
Choose one of the following tools to get started:
""")

# Create two columns for the buttons
col1, col2 = st.columns(2)

# Evaluator button
with col1:
    st.markdown("### Property Evaluator")
    st.markdown("Evaluate properties based on various criteria and get detailed analysis.")
    if st.button("Go to Evaluator", key="evaluator"):
        st.switch_page("pages/evaluator.py")

# Price Check button
with col2:
    st.markdown("### Price Check")
    st.markdown("Check and compare property prices in different areas.")
    if st.button("Go to Price Check", key="price_check"):
        st.switch_page("pages/price_check.py")

# Add some spacing
st.markdown("### Website Showcase")
st.video("https://youtu.be/RwTPFqlw184")

st.markdown("""
<sub>
You can view our profiles and projects on GitHub and LinkedIn:
</sub><br>

[![GitHub](https://img.shields.io/badge/GitHub-gdevdar-181717?logo=github&style=flat-square)](https://github.com/gdevdar)
[![GitHub](https://img.shields.io/badge/GitHub-MalkhazBirtvelishvili-181717?logo=github&style=flat-square)](https://github.com/MalkhazBirtvelishvili)<br>
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Giorgi%20Devdariani-0A66C2?logo=linkedin&style=flat-square)](https://www.linkedin.com/in/giorgi-devdariani/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Malkhaz%20Birtvelishvili-0A66C2?logo=linkedin&style=flat-square)](https://www.linkedin.com/in/malkhaz-birtvelishvili-463850285/)
""", unsafe_allow_html=True)


