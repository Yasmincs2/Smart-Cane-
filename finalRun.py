import sounddevice as sd  
import soundfile as sf  
import openai  
import requests  
import re  
from colorama import Fore, Style, init  
from gtts import gTTS  
import os  
from transformers import ViltProcessor, ViltForQuestionAnswering  
import torch  
import cv2  
from PIL import Image  
import speech_recognition as sr  

# Initialize colorama for colored terminal output
init()

def open_file(filepath):
    """Reads the contents of a file and returns the text."""
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read().strip()

# Read API keys from text files
api_key = open_file('openaiapikey2.txt')

# Set the OpenAI API key
openai.api_key = api_key

# Initialize conversation and chatbot data
conversation1 = []
chatbot1 = open_file('chatbot1.txt')

# Load the pre-trained VQA model and processor from Hugging Face
model_name = "dandelin/vilt-b32-finetuned-vqa"
processor = ViltProcessor.from_pretrained(model_name)
model = ViltForQuestionAnswering.from_pretrained(model_name)

# Create a VideoCapture object to capture video
cap = cv2.VideoCapture(0)

def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    """Interacts with the ChatGPT API to get a response based on the conversation and chatbot context."""
    conversation.append({"role": "user", "content": user_input})
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input
    )
    chat_response = completion['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": chat_response})
    return chat_response

def text_to_speech(text):
    """Converts text to speech and plays the audio."""
    tts = gTTS(text=text, lang='ar')
    tts.save("output.mp3")
    
    # Use os.system to play the sound file
    if os.name == 'nt':  # For Windows
        os.system("start output.mp3")

def print_colored(agent, text):
    """Prints text with a specific color based on the agent."""
    agent_colors = {
        "Nour:": Fore.YELLOW,
    }
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")

def record_and_transcribe(duration=8, fs=44100):
    """Records audio for a specified duration, saves it as a WAV file, and transcribes it using OpenAI's Whisper model."""
    print('Recording...')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    print('Recording complete.')
    filename = 'myrecording.wav'
    sf.write(filename, myrecording, fs)
    with open(filename, "rb") as file:
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=file
        )
    transcription = response['text']
    return transcription

def process_visual_question(user_message, frame):
    """Processes a visual question using the VILT model and provides an answer."""
    # Convert the frame to PIL Image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)

    # Process the image and question using VILT
    inputs = processor(frame, user_message, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    answer_idx = logits.argmax(-1).item()
    answer = model.config.id2label[answer_idx]

    print(f"Question: {user_message}")
    print(f"Answer: {answer}")
    text_to_speech(answer)

def handle_location_questions(user_message):
    """Handles location-based questions and provides answers."""
    if "أين أنا" in user_message or "ما حولي" in user_message:
        print_colored("Nour:", "أنت في أكاديمية طويق")
    elif "أقرب قهوة" in user_message:
        print_colored("Nour:", "Dunkin's,  2 دقيقة (180 متر)")
    elif "أقرب مطعم" in user_message:
        print_colored("Nour:", "Quizness, 2 دقيقة (170 متر)")
    elif "أقرب مول" in user_message:
        print_colored("Nour:", "Park Avenue, 2 ساعة 33 دقيقة (10.5 كيلومتر)")
    elif "أقرب مستشفى" in user_message:
        print_colored("Nour:", "مستشفى جامعة الملك عبد الله, 57 دقيقة (4.2 كيلومتر)")
    elif "أقرب محطة قطار" in user_message:
        print_colored("Nour:", "محطة القطار S1, 4 دقيقة (300 متر)")

# Initialize speech recognition
r = sr.Recognizer()

def recognize_speech_from_audio_file(audio_file):
    """Recognizes speech from an audio file using Google Speech-to-Text."""
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
    try:
        question = r.recognize_google(audio_data, language='ar-AR')
        print(f"Recognized question: {question}")
        return question
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from speech recognition service; {e}")
        return None

def record_audio():
    """Records audio from the microphone."""
    # Record audio from the microphone
    print('Recording...')
    myrecording = sd.rec(int(8 * 44100), samplerate=44100, channels=2)
    sd.wait()
    print('Recording complete.')
    return myrecording, 44100

def save_audio(audio, fs, audio_file):
    """Saves audio data to a WAV file."""
    sf.write(audio_file, audio, fs)

while True:
    try:
        # Capture a frame from the camera
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # Flip horizontally for a mirror-like view

        # Record audio from the microphone
        audio, fs = record_audio()

        # Save the recorded audio as a WAV file
        audio_file = "question.wav"
        save_audio(audio, fs, audio_file)

        # Recognize speech from the recorded audio file
        question = recognize_speech_from_audio_file(audio_file)

        # Check if the user wants to exit
        if question.lower() == "stop":
            print("Thank you! Exiting the model.")
            break

        # Process the visual question
        process_visual_question(question, frame)

    except Exception as e:
        print(f"An error occurred: {e}")

# Release resources
cap.release()
cv2.destroyAllWindows()