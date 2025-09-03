import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    extract_body_content
    )
from parse import parse_with_llama
from test import convert_to_dict

st.title("AI Web Scrapper")
# url = st.text_input("Enter the Website URL: ")
parse_description = st.text_input("Enter Product Name: ")
url = parse_description.replace(" ","%20")
final_url = "https://www.flipkart.com/search?q="+url
if st.button("Scrape Site"):
    if parse_description:
        print("ABCD")
        st.write("Scraping the website")
        result = scrape_website(final_url,parse_description)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content

        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
    else:
        print("AA")

if "dom_content" in st.session_state:
    # parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        # if parse_description:
        st.write("Parsing the Content")

        dom_chunks = split_dom_content(st.session_state.dom_content)
        result = parse_with_llama(dom_chunks, parse_description)
        # print(result)
        dict = convert_to_dict(result)
        for key,value in dict.items():
            st.write(key + " : " + value)