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

dataset_url ="https://github.com/amalbinessa/re_streamlit/blob/main/T_dataframe.xlsx"


# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_excel(dataset_url, encoding='utf8')

df = get_data()

st.write(df) 
