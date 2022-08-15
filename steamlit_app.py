import streamlit as st
import pandas as pd
import numpy as np
# add app title
st.set_page_config(
    page_title="ماذا يقول عنك محرك البحث قوقل",
    page_icon="✅",
    layout="wide",
)

st.title("ابحث عنك في قوقل")

dataset_url ="https://github.com/amalbinessa/re_streamlit/blob/main/Data/T_dataframe.csv"


# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url , chunksize=Chunk_Size, 
             error_bad_lines=False,
             warn_bad_lines=True)

df = get_data()

st.write(df) 
