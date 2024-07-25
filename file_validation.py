import streamlit as st
import pandas as pd
import emoji
import openpyxl
from streamlit_js_eval import streamlit_js_eval

def val(template, real_file):
    try:
        df_template = pd.read_excel(template)
        st.write(df_template)
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown("<h1 style='text-align: center;'>File Validation App</h1>", unsafe_allow_html=True)

template = st.file_uploader("Upload Template File", type=["xlsx"])
real_file = st.file_uploader("Upload Real File", type=["xlsx"])

if st.button("Validate"):
    if template is None:
        st.write("Please upload a valid template file.")
    elif real_file is None:
        st.write("Please upload a valid real file.")
    else:
        val(template, real_file)
           
if st.button("Home"):
    # Use Streamlit's rerun functionality to reset app state
    st.experimental_rerun()
