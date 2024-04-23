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


st.write(

    '''
    ### This App is designed to give you a breakdown of the various keywords in your resume as well as give you a recommendation of a few jobs you would be a good fit for.

    ## To learn about your Resume, please upload it below:

    '''

)

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
  
    col2.text_area("Page Text",height=800, value= page_text,
                  key="my_text_area", on_change=on_text_area_change)

    st.write(
        '''
        ## Thank you for uploading your resume! The most relevant keywords we found in your resume are as follows:

        '''
    )

    page_text = page_text.replace("_","")
    pat = r'[^a-zA-z.,!?/:_;\"\'\s]'
    page_text = re.sub(pat,'', page_text)

   
    st.write (
        '''
        ### One-Letter Keywords:
        ''' )
    
    keywords_1 = kb.extract_keywords(page_text, stop_words = 'english',
                               keyphrase_ngram_range = (1,1),
                               nr_candidates= 0.2*len(page_text),
                               use_mmr = True,
                               top_n = 20,
                               diversity = 0.8)
    for tup in keywords_1[0:5]:
        st.caption(tup[0]) 


    st.write (
        '''
        ### Two-Letter Keywords:
        ''' )

    keywords_2 = kb.extract_keywords(page_text, stop_words = 'english',
                               keyphrase_ngram_range = (1,2),
                               nr_candidates= 0.2*len(page_text),
                               use_mmr = True,
                               top_n = 20,
                               diversity = 0.8)
    
    for tup in keywords_2[0:5]:
        st.caption(tup[0]) 


    st.write (
        '''
        ### Three-Letter Keywords:
        ''' )

    keywords_3 = kb.extract_keywords(page_text, stop_words = 'english',
                               keyphrase_ngram_range = (1,3),
                               nr_candidates= 0.2*len(page_text),
                               use_mmr = True,
                               top_n = 20,
                               diversity = 0.8)
    
    for tup in keywords_2[0:5]:
        st.caption(tup[0]) 



# ------------------------------
# PART 2 : Plot
# ------------------------------


    st.write(
    '''
    ## Given your keywords, let us have a look at what jobs match your resume: 
    '''
    )





    #fig = go.Figure(data=[go.Bar(x = words, y = scores)])

    #st.plotly_chart(fig)


