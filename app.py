import os
import pickle

import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2


import plotly.express as px
import plotly.graph_objects as go



# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'final_sample.csv'


# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'], 
        secret_key=os.environ['B2_APPKEY'])  


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
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 1 : Pull data
# ------------------------------
st.write(
'''
# What are the different Job Portals in our Data:
We pull data from our Backblaze storage bucket, and render it in Streamlit.
''')


df_portals= get_data()


# ------------------------------
# PART 2 : Plot
# ------------------------------

st.write(
'''
## Visualize
Plotting the frequency of Job Portals in our Dataset
'''
)



fig = fig = go.Figure(data=[go.Bar(x=df_portals['Job Portal'].value_counts().index, 
                                   y= df_portals['Job Portal'].value_counts().values)])

st.plotly_chart(fig)

