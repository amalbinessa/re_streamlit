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

df = pd.read_csv(dataset_url,lineterminator='\n')
st.write(df) 
