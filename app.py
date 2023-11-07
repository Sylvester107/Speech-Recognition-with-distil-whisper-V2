from tempfile import NamedTemporaryFile
from transformers import pipeline
import streamlit as st
from st_audiorec import st_audiorec 
#load and cache speech recoginition model
@st.cache_resource
def load_model():
    pipe=pipeline("automatic-speech-recognition","distil-whisper/distil-large-v2")
    return pipe

speech_to_text_model=load_model()

def make_text(audio):
    global speech_to_text_model
    text= speech_to_text_model(audio)
    extract_text=text['text']
    return extract_text

st.title('speech recognition, is it worth it!')
st.write('Click start recording to record an audio in English, afterwards click stop, click on convert text once and wait')
# Create columns to be used to separate file upload and audio recording interfaces
col1,col2=st.columns(2)

with col1:
    with st.form(key='record audio'):
        
        #Record an Audio
        wave_audio_data=st_audiorec()
        
        #submit
        button=st.form_submit_button(label='Convert to Text,click once and wait')
        #if the submit button is pressed 
        if button:
            st.success('audio submitted, processing is slow give us some few seconds')
            try:
                #check if audio file
                if wave_audio_data is not None:
                    #do the conversion
                    text=make_text(wave_audio_data)

                    st.write(text)
            except:
                st.write("we can't process your request at this time")
        else:
            st.success('No Audio data yet')

with col2:
    with st.form(key='file upload '):
         #or upload an audio file
        st.write('Or you can upload an audio file')

        upload=st.file_uploader(label='Upload audio file')

        #submit
        button=st.form_submit_button(label='Convert to Tex. Click once and wait')
        #if the submit button is pressed 
        if button:
            st.success('audio submitted, processing is slow give us some few seconds')
            try:
                if upload is not None:
                     with NamedTemporaryFile() as temp:
                        temp.write(upload.getvalue())
                        temp.seek(0)
                        text = make_text(temp.name)
                        
                     st.write(text)
            except:
                st.write("we can't process your request at the moment")
        else:
            st.success('No Audio data yet')


