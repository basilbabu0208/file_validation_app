import streamlit as st
import pandas as pd
import emoji
import openpyxl
from streamlit_js_eval import streamlit_js_eval






def reset_app():
    st.experimental_rerun()

def validate_file_name(template , real_file):
    file_name_temp = template.name
    file_name_real = real_file.name
    
    a = int(file_name_temp.find("_PARAM_"))
    b = int(file_name_real.find("_PARAM_"))
    file_tem_format = file_name_temp[0:a]
    #balance =file_name_temp[a+8:]
    file_real_format = file_name_real[0:b]
    if (file_tem_format != file_real_format ):
        
        return "Expected Pattern: "+file_tem_format + "%" 
def header_name_validation(template , real_file):
    df_temp = pd.read_excel(template)
    df_real = pd.read_excel(real_file)

    column_name_temp = pd.DataFrame(df_temp.columns, columns=["Column Name"])
    column_name_real = pd.DataFrame(df_real.columns, columns=["Column Name"])
    data_type_temp = pd.DataFrame(df_temp.dtypes, columns=["Data Type"] ). reset_index(drop=True)
    data_type_real = pd.DataFrame(df_real.dtypes, columns=["Data Type"]). reset_index(drop=True)

    temp_dataframe = pd.concat([column_name_temp, data_type_temp], axis=1)
    temp_dataframe['File Type'] = "Template"
    real_dataframe = pd.concat([column_name_real, data_type_real], axis=1)
    real_dataframe['File Type'] = "Real"

    row_wise_comparison = temp_dataframe.eq(real_dataframe)
    comparison_columns = [f'{col}_match' for col in temp_dataframe.columns]
    row_wise_comparison.columns = comparison_columns

# Concatenate the original DataFrame with the comparison results
    combined_df = pd.concat([temp_dataframe, row_wise_comparison], axis=1)

    inner_join_df = pd.merge( real_dataframe,temp_dataframe, on='Column Name', how='left')
    column_positions = {col_name: idx for idx, col_name in enumerate(df_real.columns)}
    column_position_df = pd.DataFrame(list(column_positions.items()), columns=['Column Name', 'Column Index'])

    final_df = pd.merge( inner_join_df,column_position_df, on='Column Name', how='inner')










    
   # st.write(final_df)

    filtered_df = final_df[final_df['File Type_y'] .isna()| (final_df['Data Type_x'] != final_df['Data Type_y'])]

    filtered_df.columns = ["Column Name", "Current Datatype", "File Type1","Expected Datatype", "File Type2", "Column Position"]
    filtered_df['File Type'] = filtered_df['File Type1'] + '/' + filtered_df['File Type2']



    filtered_df['File Type'] = filtered_df['File Type'].fillna('Real')
    filtered_df['File Type'] = filtered_df['File Type'].fillna('Real')
    filtered_df['Expected Datatype'] = filtered_df['Expected Datatype'].fillna('N/A')

    filtered_df['Comment'] = filtered_df['File Type'] .apply(lambda x: 'Data Type Error' if x == 'Real/Template' else 'Header Error')

    selected_columns = ['Column Name', 'File Type','Current Datatype', 'Expected Datatype', 'Comment', 'Column Position']
    filtered_df= filtered_df[selected_columns]
    if not filtered_df.empty:
        return filtered_df
 


def empty_row(real_file):
    df_real = pd.read_excel(real_file)
    rows_with_all_empty_or_spaces = df_real[df_real.applymap(lambda x: isinstance(x, str) and x.strip() == '').all(axis=1) | df_real.isnull().all(axis=1)]
    rows_with_all_empty_or_spaces = pd.DataFrame(rows_with_all_empty_or_spaces)
    if rows_with_all_empty_or_spaces is not None:
        row_indices_list = rows_with_all_empty_or_spaces.index.tolist()
        row_indices_str = ','.join(map(str, row_indices_list))
        return row_indices_str


# if not rows_with_all_empty_or_spaces.empty:
    return None
    
        







def val(template , real_file):
    file_name_result = validate_file_name(template , real_file)
    validated_df = header_name_validation(template , real_file)
    empty_rws = empty_row(real_file)



    if file_name_result:
        st.write('File naming mismatch!')
        st.write(file_name_result)

    if validated_df is not None:
        st.write('Column Issues :')
        st.write(validated_df)

    if  empty_rws is not None:
        st.write( 'Empty or NULL row found at: '+empty_rws)

    if file_name_result is None and validated_df is  None and empty_rws.empty:
        st.write("File Format Matching.")




st.markdown("<h1 style='text-align: center;'>File Validation App</h1>", unsafe_allow_html=True)


template = st.file_uploader("Upload Template File")
real_file = st.file_uploader("Upload Real File")

if st.button("Validate"):
      if template is None:
           st.write("Please upload a valid template file.")
      elif real_file is None:
           st.write("Please upload a valid real file.")
      elif template and real_file:
           val(template, real_file)
           
if st.button("Home"):
   # Reset session state and rerun the app

   #validation.reset_app()
   streamlit_js_eval(js_expressions = "parent.window.location.reload()")




