import streamlit as st # data web app development
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
import matplotlib.pyplot as plt
import arabic_NER
from wordcloud import WordCloud
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import ClusterTransformer.ClusterTransformer as ctrans
import os

# to remove any warning coming on streamlit web app page
st.set_option('deprecation.showPyplotGlobalUse', False)
# add app title
st.set_page_config(
    page_title="ماذا يقول عنك محرك البحث قوقل",
    page_icon="✅",
    layout="wide",
)


st.title("ابحث عنك في قوقل")

query = st.sidebar.text_input('اضف/ـي  كلمات البحث ')

if query:
    query = query 
else :
    query = "شركة ثقة لخدمات الأعمال"
search = query.replace(' ', '+')

num_of_results = st.sidebar.text_input('حدد/ـي عدد النتائج التي ترغب في نمذجتها')
if query:
    num_of_results = num_of_results
else :
    num_of_results = 10



url = (f"https://www.google.com/search?q={search}&num={num_of_results}")

requests_results = requests.get(url)
soup_link = BeautifulSoup(requests_results.content, "html.parser")
links = soup_link.find_all("a")
title_link_list = []

for link in links:
    link_href = link.get('href')
    if "url?q=" in link_href and not "webcache" in link_href:
      title = link.find_all('h3')

      if len(title) > 0:
          title_list = []
          title_list.append(title[0].getText())
          title_list.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
          
          title_link_list.append(title_list)



# add result to dataframe
df = pd.DataFrame(title_link_list, columns =['title', 'link']) 

# extract information from title and link data  

def split_text(text):
  
  if ' - ' in text:
    return text.split('-',1)
  elif '/' in text:
    return text.rsplit('/',1)
  elif '|' in text:
    return text.rsplit('|',1)
  
  else:
    return [text,0]
# text preprocessing 
df['title'] = df['title'].str.replace('.', '')

df['title'].str.strip()

df['splited_title'] =[split_text(text) for text in df['title']]

df['sub_title'] = [splited_title[0] for splited_title in df['splited_title']]

df['source_name'] = [splited_title[-1] for splited_title in df['splited_title']]

# get source_site_name from link

df['sub_link'] = df['link'].str.split('/', 3)

def get_source_site_name(site_link):
  site_link[2].split('.')[-2]
  return site_link[2].split('.')[-2]

#df['source_site_name'] = [get_source_site_name(link) for link in df['sub_link']]

# text preprocessing :
def get_text_preprocessing(text):
  # text = str(text).strip()
  # text = text.lstrip()
  # " ".join(text.split())
  
  #clean non Arabic letters and spicial characters  

  text = re.sub('([@A-Za-z0-9_ـــــــــــــ]+)|[^\w\s]|#|http\S+', '', text) # cleaning up

  return " ".join(text.split())
df['cleaned_title'] = [get_text_preprocessing(text) for text in df['sub_title']]

# remove no values in cleaned_title

df['title_length'] = df.cleaned_title.str.len()

df = df[df.title_length > 1]

# dataframe filter
#df = df[df["cleaned_title"] == title_filter] 

# cleaned_text for 
def get_cleaned_text(text):
    return ' '.join(text.tolist())

cleaned_text = get_cleaned_text(df['cleaned_title'])
# drop unwanted columns
df =df.drop(columns=['splited_title', 'sub_link' , 'title_length' ])


##################################### NER ##################################


def text_to_ner_model_line(text):
  text = arabic_NER.get_ner(text)
  return get_entity_key_value(text)
def get_entity_key_value(text):
  key__value_list_outer = []
  for ner_ in text[0]:
    for key , value in ner_.items():
      if '-' in value:
        #key_value_list_inner = [key,value]
        key__value_list_outer.append(key)

  return key__value_list_outer

df['entity_list'] = [text_to_ner_model_line(text) for text in df['cleaned_title']]



############################################################################

# create  charts

st.header("")
st.markdown("Search Result Titles Chart")
fig1 = px.histogram(data_frame=df, x="cleaned_title", width=1000, height=800)
st.write(fig1)

st.header("")
st.markdown("Result Source Site Name Chart")
fig2 = px.histogram(data_frame=df[df['source_name'] != 0], x="source_name", width=1000, height=800)
st.write(fig2)
 
########################################################




# # remove stop words:
stopwords_list = stopwords.words('arabic')

# def remove_stopword_withtokenize(text):
#   text_tokens = word_tokenize(text)
#   tokens_without_sw = [word for word in text_tokens if not word in stopwords_list]
#   return ' '.join(tokens_without_sw)


# df['cleaned_title_without_stopword'] = [remove_stopword_withtokenize(text)for text in df['cleaned_title'] ] 
# text = df['cleaned_title_without_stopword']
# text = [''.join(sentence) for sentence in text]
# text = ' '.join(text)
# reshaped_text = arabic_reshaper.reshape(text)
# arabic_text = get_display(reshaped_text)
# wordcloud = WordCloud(font_path = 'arial.ttf',width=700, height=300, background_color="black").generate(arabic_text)
# st.image(wordcloud.to_array())





# stop TOKENIZERS_PARALLELISM

os.environ["TOKENIZERS_PARALLELISM"] = "false"
cr=ctrans.ClusterTransformer()
model_name='albert-base-v1'

#Creating an input list of sentences to be clustered

li_sentence = list(df['cleaned_title'])


#Declare hyperparameters
batch_size=2
max_seq_length=64
convert_to_numpy=False
normalize_embeddings=False
neighborhood_min_size=1
cutoff_threshold=0.83
kmeans_max_iter=100
kmeans_random_state=42
kmeans_no_clusters=6


#Declare the methods : model_inference,neighborhood_detection,kmeans_detection,convert_to_df and plot_cluster with associated hyperparameters
embeddings=cr.model_inference(li_sentence,batch_size,model_name,max_seq_length,normalize_embeddings,convert_to_numpy)
#output_dict=cr.neighborhood_detection(li_sentence,embeddings,cutoff_threshold,neighborhood_min_size)
output_kmeans_dict=cr.kmeans_detection(li_sentence,embeddings,kmeans_no_clusters,kmeans_max_iter,kmeans_random_state)
#neighborhood_detection_df=cr.convert_to_df(output_dict)
kmeans_df=cr.convert_to_df(output_kmeans_dict)






###################WC_FOR_CLUSTER#############################

def remove_stopword_withtokenize_for_clusters(text):
  text_tokens = word_tokenize(text)
  tokens_without_sw = [word for word in text_tokens if not word in stopwords_list]
  return ' '.join(tokens_without_sw)
def generate_wordcloud(df, cluster_num):

  df_grouped_by_cluster = df[df['Cluster'] == cluster_num]
  df_grouped_by_cluster['text_without_stopword'] = [remove_stopword_withtokenize_for_clusters(text) for text in df_grouped_by_cluster['Text'] ] 
  
  text = df_grouped_by_cluster['text_without_stopword']

  text = [''.join(sentence) for sentence in text]
  text = ' '.join(text)
  reshaped_text = arabic_reshaper.reshape(text)
  arabic_text = get_display(reshaped_text)
  wordcloud = WordCloud(font_path = 'arial.ttf',width=700, height=300, background_color="black").generate(arabic_text)
  return wordcloud

########################WC_FOR_CLUSTER###################################

# fined number of clusters
kmeans_clusters_list = kmeans_df.Cluster.unique()
#neighborhood_detection_clusters_list = neighborhood_detection_df.Cluster.unique()



# cluster result in kmeans

# nsert containers laid out as side-by-side columns.
col1, col2, col3 = st.columns(3)

for  index , cluster_num in enumerate(kmeans_clusters_list):
  # group df based on cluster filter :
  wordcloud_result =generate_wordcloud(kmeans_df,cluster_num)
  new_index = index + 1 
  if index == 1 :
    with col1:
        st.header(f'Topic {index+1} Words :\n ')
        st.image(wordcloud_result.to_array())
    
  if index == 2 :
    with col1:
        st.header(f'Topic {index+1} Words :\n ')
        st.image(wordcloud_result.to_array())
    
  if index == 3 :
    with col1:
        st.header(f'Topic {index+1} Words :\n ')
        st.image(wordcloud_result.to_array())
        

  
  

  











