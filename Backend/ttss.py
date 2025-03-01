import os
import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import io
import pdfplumber  # Alternative PDF text extraction

# Azure subscription key and region
subscription_key = "4dWeuj5JRjZCLfnXFaSqiO7qsv6dYzMK1klZaNVb6lCe72LyyqcOJQQJ99BBACGhslBXJ3w3AAAYACOG1pJE"
region = "centralindia"

# Set up the speech configuration
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

# Streamlit app title and introduction
st.title("Text-to-Speech with Azure - PDF Reader")
st.write("Upload a PDF file, extract the text, and listen to it being spoken by the AI!")

# Mode selection
mode = st.radio("Choose mode", ("PDF to Speech", "Text to Speech"))

# Voice selection
voice_options = [
    "en-IN-AaravNeural",  # Male voice
    "en-IN-NeerjaNeural",  # Female voice
]
selected_voice = st.selectbox("Select voice", voice_options)

# Set the selected voice for speech synthesis
speech_config.speech_synthesis_voice_name = selected_voice

if mode == "PDF to Speech":
    # File upload feature
    uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")

    # If a PDF is uploaded, extract the text
    if uploaded_pdf is not None:
        # Extract text using pdfplumber
        with pdfplumber.open(uploaded_pdf) as pdf:
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()
        
        # Display the extracted text (optional)
        st.text_area("Extracted Text", pdf_text, height=300)
        
        # Create an audio stream and synthesizer
        audio_stream = io.BytesIO()

        if st.button("Play Audio"):
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            result = synthesizer.speak_text_async(pdf_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                st.success("Speech synthesized successfully!")
                
                # Get the audio and write it to the stream
                audio_data = result.audio_data
                audio_stream.write(audio_data)
                audio_stream.seek(0)
                
                # Play the audio
                st.audio(audio_stream, format="audio/wav")
            else:
                cancellation_details = result.cancellation_details
                st.error(f"Speech synthesis failed: {cancellation_details.error_details}")
    else:
        st.write("Please upload a PDF file to extract text and convert to speech.")
else:
    # Add a text input box for normal text-to-speech
    st.write("Enter text below for text-to-speech:")
    input_text = st.text_area("Enter text here")

    if st.button("Convert Text to Speech"):
        if input_text:
            # Create an audio stream and synthesizer
            audio_stream = io.BytesIO()
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            result = synthesizer.speak_text_async(input_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                st.success("Speech synthesized successfully!")
                
                # Get the audio and write it to the stream
                audio_data = result.audio_data
                audio_stream.write(audio_data)
                audio_stream.seek(0)
                
                # Play the audio
                st.audio(audio_stream, format="audio/wav")
            else:
                cancellation_details = result.cancellation_details
                st.error(f"Speech synthesis failed: {cancellation_details.error_details}")
        else:
            st.error("Please enter some text for conversion.")