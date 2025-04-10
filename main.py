# One time import of all necessary Python modules
!pip install -q google-genai
!pip install -q gTTS
!pip install -q PyPDF2

# Mounting the drive
from google.colab import drive
drive.mount('/content/drive')

# Checks all available Gemini models. Note this code is a one time assessment of available models.
genai.configure(api_key=" ") # personalize to connect to your Google Drive!

import google.generativeai as genai_modules
for m in genai_modules.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

# Once a Gemini model has been identified, this code can be commented.
# Model settings for factuality and prompt blocking for safety.
m_generation_config = {
  "temperature":0,
  "top_p":1,
  "top_k":1,
  "max_output_tokens":400,
}

# Configure the model with specific safety and privacy setting to avoid
# non-kids friendly language and content.
m_safety_settings = [
  {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold" : "BLOCK_NONE"
  },

  {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold" : "BLOCK_NONE"
  },

    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold" : "BLOCK_NONE"
  },

    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold" : "BLOCK_NONE"
  }
]

# From the installed modules importing Python Packages.
import google.generativeai as genai
import os
import os.path

from google.colab import drive
from google.colab import userdata
from gtts import gTTS
from PyPDF2 import PdfReader

# Authenticating to Google Cloud using Google API_KEY to access Gemini API.
google_api_key = userdata.get('API_KEY')
genai.configure(api_key=google_api_key)

# Choosing am available Gemini model gemini-1.5-pro.
model = genai.GenerativeModel('gemini-1.5-pro')


def create_text_from_pdf(pdf_location):
  # Funtion to read a pdf from pdf_location
    reader = PdfReader(pdf_location)
    page = reader.pages[0]
    pdf_text = page.extract_text()
    return pdf_text

def pdf_to_narration(model, prompt_story, prompt_narration, pdf_text):
  # Function to convert the pdf into a narration script
  character_prompt = ("You are an expert story teller. Tell the story of the text below. Use 3 characters to narrate the story in Hindi. Use the following names for characters, Merchant: Zayan, Genius: Djinn, Wise Man: Zain. Ignore * in your speech. Call Genius Djinn.")
  g_prompt = prompt_story + prompt_narration + character_prompt + pdf_text
  response = model.generate_content(g_prompt)
  return response.text


def text_to_speech(text, name_of_audio):
  # Function to convert text to audio using gTTS
  # lang = hi  for hindi, ur for urdu
  # tld='com.au' for australian accent can be added to gTTS parameters.
  speech = gTTS(text, lang='hi')
  speech_file = name_of_audio + ".mp3"
  speech.save('/content/drive/MyDrive/' + speech_file)
  return speech_file

# Using user provided input as a prompt the Gemini model
story_file = input('Please provide name of your storybook (pdf) in your drive: ')

# Checking to see if the file exists to proceed, else exit after a message.
if os.path.isfile('/content/drive/MyDrive/' + story_file):
  # Asking the user to type of narration (humor, horror, kid story etc)
  story_prompt = input('Provide a style for story book: ')
  # Asking the user the style of audio narration (screenplay, theatrical etc)
  screenplay_prompt = input('Provide how you want the audio to be narrated: ')
  # Asking the user name of the audio file.
  name_of_audio = input('Provide a name that you want to use to save your A/I generated audio file (mp3)  : ')
else:
  print('PDF file not found in location specified. Quitting, please retry.')
  os._exit(1)

# At this time all the necessary information has been collected. Calling functions to start generating audio.

# Parse the pdf and create a narration first using a pddf in users drive.
pdf_narration_text = create_text_from_pdf('/content/drive/MyDrive/' + story_file)

# Turn the narration to a style (screenplay, theater etc) of audio narration
narration_text = pdf_to_narration(model, story_prompt, screenplay_prompt, pdf_narration_text)
#print(narration_text)

# Convert the narration_text generated above to an mp3 audio.
text_to_speech(narration_text, name_of_audio)

# TODO, either using text to video or Audio to video APIs, convert the mp3 to a short movie.
