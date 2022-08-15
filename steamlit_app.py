import streamlit as st
import pandas as pd
import numpy as np
# add app title
st.set_page_config(
    page_title="ماذا يقول عنك محرك البحث قوقل ",
    page_icon="✅",
    layout="wide",
)
df = pd.read_excel('T_dataframe.xlsx')


