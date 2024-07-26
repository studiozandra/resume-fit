# Cell 1: Setup
import streamlit as st
from openai import OpenAI
import os
# import the pdf convert script (https://pypdf2.readthedocs.io/en/latest/index.html)
import PyPDF2
import secrets
from io import StringIO


# Get your OpenAI API key from environment variables

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)




# Cell 2: Title & Description
st.title('🤖 AI Resume Fixer')
st.markdown('I was made to suggest fixes to resumes. This app demonstrates how to use OpenAI GPT-3.5 to answer data-related interview questions in a deployed envionment. Remember, always verify AI-generated responses.')

# Cell 3: Upload
st.markdown('Please upload your PDF resume.')

uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)






# Cell 4: Streamlit UI
if uploaded_file:
    
    with uploaded_file as file:

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize a string to hold the resume text
        resume_text = ""
        
        # Iterate over the pages of the PDF
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
            # print(resume_text)
            # Extract the text from
    user_input = st.text_area("Paste in job qualifications", "start typing here")
    # Open the PDF file in read-binary mode

    job_description = user_input

# Cell 3: Function to analyze text using OpenAI
def analyze_text(job_description, resume_text):
  """
  This function sends a text prompt to the OpenAI API using the GPT-3.5 model.

  Args:
      text (str): The tech interview question to be answered.

  Returns:
      str: The response generated by the GPT-3.5 model.
  """

  # Ensure your API_KEY is set as an environment variable
  if not os.environ.get("OPENAI_API_KEY"):
      st.error("OpenAI API key is not set. Please set it in your environment variables.")
      return

  # send your resume text to GPT-3 and receive the analysis (handling errors):
  try:
      completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": F"Give a strict comparison of the {job_description} to the {resume_text}. Do not use more than 3 sentences." },
          {"role": "user", "content": "Give a strict comparison of the job_description to the resume text. Do not use more than 3 sentences."}
      ],
      temperature=0.4,            
      )
  except Exception as e:
      print("Error sending request to GPT-3:", e)
      exit()


    # Check if the response object has a "text" field
  print(completion.choices[0].message.content)
  if "content" in str(completion.choices[0]):
    # Extract the text field from the response
      response = completion.choices[0].message.content
      return response
    
  else:
      print("Error: response does not have a 'text' field")

# st.write("Hello, *World!* :sunglasses:")

if st.button('Analyze Resume Qualifications'):
    with st.spinner('Analyzing...'):
        result = analyze_text(job_description, resume_text)
        st.write(result)