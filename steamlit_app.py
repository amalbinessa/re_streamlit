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

df = pandas.read_excel('Data/T_dataframe.xlsx')

# print whole  data
st.write(df) 



