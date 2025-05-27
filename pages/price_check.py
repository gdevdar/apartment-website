import streamlit as st

st.set_page_config(
    page_title="Apartment Price Checker",
    page_icon="🏠",
    layout="centered"
)

st.title("Apartment Price Checker")
st.write("Enter a MyHome.ge apartment listing URL to check its estimated price.")

# URL input field
url = st.text_input(
    "Enter MyHome.ge URL",
    placeholder="https://www.myhome.ge/pr/..."
)

from link_scrape import data_collector
from data_extract import row_creator
from data_extract import data_load

# Submit button
if st.button("Check Price"):
    if url:
        if "myhome.ge" in url.lower():
            st.write("Processing URL...")
            data = data_collector(url)
            mapping = data_load("mapping.json")
            row = row_creator(data,mapping)
            # Your scraper code will go here
            # For now, just showing a placeholder
            st.write(f"{row}")
            st.info("URL received and ready for processing!")
        else:
            st.error("Please enter a valid MyHome.ge URL")
    else:
        st.warning("Please enter a URL first")



# Location where a url will be inputted

# Code that will scrape

# Code that will pick out the data that is needed

# creating an array similar to evaluator.py

# predicting using our model