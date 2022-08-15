import streamlit as st
import pandas as pd
import numpy as np
# add app title
st.set_page_config(
    page_title="ماذا يقول عنك محرك البحث قوقل",
    page_icon="✅",
    layout="wide",
)


dataset_url = "T_dataframe.xlsx"

# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_excel(dataset_url)

df = get_data()
st.title("ماذا يقول عنك محرك البحث قوقل")


