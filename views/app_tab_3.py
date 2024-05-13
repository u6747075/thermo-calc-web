import streamlit as st
import pandas as pd

# Sample data initialization


def delete_row(index):
    """ Function to delete a row based on index """
    st.session_state['data'] = st.session_state['data'].drop(index).reset_index(drop=True)

# Display the DataFrame with a delete button for each row
def display_table_with_delete(df):
    # for index, row in df.iterrows():
    #     cols = st.columns([0.2, 1, 1, 1, 1, 1, 1, 1])
    #     delete_button = cols[0].button("D", key=f"delete_{index}")
    #     if delete_button:
    #         delete_row(index)
    #         st.experimental_rerun()
    #     cols[1].write(row['title'])
    #     cols[2].write(row['max_temp'])
    #     cols[3].write(row['min_temp'])
    #     cols[4].write(row['selected_average'])
    #     cols[5].write(row['n_regions'])
    #     cols[6].write(row['note'])
    csv = convert_df_to_csv(st.session_state['data'])
    col1, col2 = st.columns(2)
    with col2:
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='data.csv',
            mime='text/csv',
            
        )
    with col1:
        
        edit= st.toggle("Edit mode",key="edit",value=False)

    if edit:
       edited_df= st.data_editor(df,num_rows="dynamic")
       st.session_state['data'] =edited_df
    else:
        st.data_editor(df)
        
def convert_df_to_csv(df):
    # Convert DataFrame to CSV, index=False means don't write row names (index)
    return df.to_csv(index=False)


def render_objects():
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame({
                "title": [],
                "max_temp": [],
                "min_temp": [],
                "selected_average": [],
                "n_regions": [],
                "filename": []
            }).astype({
                "title": "string",
                "max_temp": "float",
                "min_temp": "float",
                "selected_average": "float",
                "n_regions": "int",
                "filename": "string"
            })
  

    display_table_with_delete( st.session_state['data'] )


