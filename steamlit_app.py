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


dataset_url = "./Data/T_dataframe.xlsx"

# read csv from a URL

def get_data() -> pd.DataFrame:
    return pd.read_excel(dataset_url)

df = get_data()

st.write(df) 



