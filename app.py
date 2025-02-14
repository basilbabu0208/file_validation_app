import streamlit as st
import validation 
import testing
import emoji
from streamlit_js_eval import streamlit_js_eval


st.write("Hello")

st.markdown("<h1 style='text-align: center;'>File Validation App</h1>", unsafe_allow_html=True)


template = st.file_uploader("Upload Template File")
real_file = st.file_uploader("Upload Real File")

if st.button("Validate"):
      if template is None:
           st.write("Please upload a valid template file.")
      elif real_file is None:
           st.write("Please upload a valid real file.")
      elif template and real_file:
           #validation.val(template, real_file)
            testing.val(template, real_file)
           
if st.button("Home"):
   # Reset session state and rerun the app

   #validation.reset_app()
   streamlit_js_eval(js_expressions = "parent.window.location.reload()")


