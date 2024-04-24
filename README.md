# Resume Assistant App

https://localtest.streamlit.app/

## Overview

This app is designed as a resume analyzing assistant for students and aspiring jobb applicants that are looking to improve and modify their resume to suit a job description. 
The app takes in a resume and analyzes it using HuggingFace's KeyBERT() Keyword Recognition Model. It then returns graphical visualisations of the most important keywords in the user's resume as well as a list of jobs fron the database that match the keywords.

## Data Description 

The dataset used in this project was obtained from Kaggle and contained a list of 4000 job descriptions for a variety of different roles. The dataset included information about the company, location, base-pay as well as about techinical skills, experience and education. 

## Algorithm Description

KeyBERT is a minimal and easy-to-use keyword extraction technique that leverages BERT embeddings to create keywords and keyphrases that are most similar to a document.

It is a model that is very widely used in industry to find our keywords in a document and makes use of HuggingFace's BERT Transformer architecture to take into account token across an entire document. This allows it to outperform most other Keyword recognition models available on the internet. 


## Tools Used:

- Python
- KeyBERT()
- Backblaze
- NLTK
- Regex


## Ethical concerns:

Since users are uploading their personal resumes to the app, keeping thierr data private is extremely important to prevent loss of privacy and personal information. Furthermore, we must also be aware of ethical concerns regarding users misusing the app to lie about their skills and changing their reusme information to suit a particular job that they are not qualified for 

