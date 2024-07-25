import streamlit as st
import pandas as pd
import emoji
import openpyxl
from streamlit_js_eval import streamlit_js_eval






def empty_row(real_file):
    df_real = pd.read_excel(real_file)
    rows_with_all_empty_or_spaces = df_real[df_real.applymap(lambda x: isinstance(x, str) and x.strip() == '').all(axis=1) | df_real.isnull().all(axis=1)]
    rows_with_all_empty_or_spaces = pd.DataFrame(rows_with_all_empty_or_spaces)
    if rows_with_all_empty_or_spaces is not None:
        row_indices_list = rows_with_all_empty_or_spaces.index.tolist()
        row_indices_str = ','.join(map(str, row_indices_list))
        st.write( "empty" + row_indices_str == '')

st.markdown("<h1 style='text-align: center;'>File Validation App</h1>", unsafe_allow_html=True)


template = st.file_uploader("Upload Template File")
real_file = st.file_uploader("Upload Real File")

if st.button("Validate"):
      if template is None:
           st.write("Please upload a valid template file.")
      elif real_file is None:
           st.write("Please upload a valid real file.")
      elif template and real_file:
           empty_row( real_file)
           
if st.button("Home"):
   # Reset session state and rerun the app

   #validation.reset_app()
   streamlit_js_eval(js_expressions = "parent.window.location.reload()")
