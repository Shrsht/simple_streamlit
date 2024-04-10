import os
import pickle

import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2


import plotly.express as px
import plotly.graph_objects as go

from pdf2image import convert_from_bytes
from PIL import Image
from PyPDF2 import PdfReader

from keybert import KeyBERT


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'final_sample.csv'


# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
@st.cache_data
def get_data():
    # collect data frame of reviews and their sentiment
    
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df_portals = b2.get_df(REMOTE_DATA)


    
    return df_portals
        
# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'], 
        secret_key=os.environ['B2_APPKEY'])  

kb = KeyBERT()
# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 1 : Pull data
# ------------------------------

st.set_page_config(page_title = "Resume Uploader")

def on_text_area_change():
    st.session_state.page_text = st.session_state.my_text_area

st.write(
'''
# Welcome to your resume assistant
''')

### Get Job_Portal DataFrame
df_portals= get_data()

# ------------------------------------------------------
#                     RESUME UPLOAD
# ------------------------------------------------------



resume_file = st.file_uploader(label = "Please Upload your Resume (pdf files only)", type = 'pdf')

if resume_file:
    pdfReader = PdfReader(resume_file)
    page = pdfReader.pages[0] 
    page_text =  page.extract_text()

  # Convert the selected page to an image
    images = convert_from_bytes(resume_file.getvalue())
    page_image = images[0]

    # Create two columns to display the image and text
    col1, col2 = st.columns(2)

  # Display the image in the first column
    col1.image(page_image)
  
    col2.text_area("Page Text", height=800, value= page_text,
                  key="my_text_area", on_change=on_text_area_change)
    
    keywords = kb.extract_keywords(page_text, stop_words = 'english',
                               keyphrase_ngram_range = (1,3),
                               nr_candidates= 0.2*len(page_text),
                               use_mmr = True,
                               top_n = 20,
                               diversity = 0.8,)
    scores = []
    words = []
    
    for i in keywords:
        words.append(i[0])
        scores.append(i[1])

    
    st.write("Your Resume contains the following keywords:")

    st.write(words)



# ------------------------------
# PART 2 : Plot
# ------------------------------

st.write(
    '''
    ## Issues with the Model:

    Model is able to give us a breakdown of keywords in our inputted resume. 
    However it is still unable to recognize strings like '__________'. We need ot work on cleaning the resumes as they are uploaded
    The model still can't recognize which entities represent what keywords 
    i.e We want to know if a specific keyword is a 'Job Description' or a 'Skill' , etc.
        

   ##  Way Forward:

    We need to improve our model using NER (Named Entity Recognition) models that can recognize the exact label of a given resume. We can then match these
    named-entities with job descriptions in our dataframe. 

    Such NER models are available and can be included in the model.py file. 
    Furthermore we need to include a section where we clean the resume text and remove values like '______'.
    Our app can also have better visualisations in terms of the graphs and keywords we collect. 

    ''')

st.write(
'''
## Visualize
Plotting the frequency of Job Portals in our Dataset
'''
)



# fig = fig = go.Figure(data=[go.Bar(x=df_portals['Job Portal'].value_counts().index, 
#                                    y= df_portals['Job Portal'].value_counts().values)])

fig = fig = go.Figure(data=[go.Bar(x = words, 
                                    y = scores)])

st.plotly_chart(fig)


