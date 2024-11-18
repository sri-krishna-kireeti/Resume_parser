import streamlit as st
import base64
import os
import base64
from urllib.parse import urlparse
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from dotenv import load_dotenv
# import spacy
from typing import Union
import google.generativeai as genai
import json

load_dotenv()

adi_api_key = os.getenv('adi_api_key')
adi_endpoint = os.getenv('adi_endpoint')
genai.configure(api_key=os.getenv('gemini_api_key'))


#AZURE DOCUMENT INTELLIGENCE PART
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def client():
  client = DocumentIntelligenceClient(endpoint=adi_endpoint, credential = AzureKeyCredential(adi_api_key))
  return client

def load_file(file_input):
    data = file_input.read()  # Read the file data from the uploaded file
    base64_data = base64.b64encode(data).decode('utf-8')  # Convert to base64
    return base64_data

# def lemmatization(resume_content):
#   nlp = spacy.load("en_core_web_sm")
#   doc = nlp(resume_content)
#   lemmatized_tokens = [token.lemma_ for token in doc]
#   lemmatized_text = ' '.join(lemmatized_tokens)
#   return lemmatized_text

def document_content(doc):
    model = "prebuilt-layout"
    document_intelligence_client = client()
    
    poller = document_intelligence_client.begin_analyze_document(
        model, {"base64Source": doc}
    )
    result = poller.result()
    # return lemmatization(result['content'])
    return result['content']
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




#GEMINI AI CODE
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def document_analysis(resume_content, job_description) -> dict:
  model = genai.GenerativeModel('gemini-1.5-flash-8b')
  prompt = '''I will provide you a resume and a job description. Please analyze both and output the results in the following JSON format:
  {
    "student_name": name,
    "key_skill": skill,
  "relevant_to_job_description": 0, // Score out of 5
  "creativity": 0, // Score out of 5 based on projects
  "achievements": 0 // Score out of 5 including extracurricular activities
}
Make sure to assess how well the resume aligns with the job description, skill relavant to job description, evaluate the creativity demonstrated in the projects listed, and consider any relevant achievements or extracurricular activities when assigning scores.
  Resume Content:
  ''' + resume_content + '''
  Job Description:
  ''' + job_description


  response = model.generate_content(prompt).text.strip()
  try:
    response = response.replace("json","")
    response = response.replace("```","")
  except Exception as e:
    print(e)
  front_dict={}
  try:
      front_dict = json.loads(response)
      print(front_dict)
  except json.JSONDecodeError as e:
      print(f"Error converting JSON string to dict: {e}")
  return front_dict
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



#Streamlit Code
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def client_method(pdf):
    resume_content = document_content(pdf)
    document_analytics = document_analysis(resume_content, job_description)
    return document_analytics

st.title("Resume Parser Using ADI and GEMINI")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
job_description = st.text_area("Enter Job Description")

if st.button("Submit"):
    if uploaded_file and job_description is not None:
        pdf = load_file(uploaded_file)
        processed_text = client_method(pdf)
        st.subheader("Processed Text from Client Method")
        st.text(processed_text)