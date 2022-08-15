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



import csv

with open('dataset_url') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')

st.write(df) 
