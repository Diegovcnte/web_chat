from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from pathlib import Path

class AsistenteOpenAi:
    def __init__(self):
          load_dotenv()
          self.api_key = os.getenv("OPENAI_API_KEY")
          self.client = OpenAI(api_key=self.api_key)

    def audio_to_text(self,audio_path="./audio/recibido/audio.mp3"):
         with open(audio_path, "rb") as audio_file:
              transcription = self.client.audio.transcriptions.create(
                   model="whisper-1",
                   file = audio_file
              )
              return transcription.text
         
    def generate_answer(self, texto):
         completion = self.client.chat.completions.create(
              model = "gpt-3.5-turbo",
              temperature = random.randrange(0,11)/10,
              messages=[
                {"role": "system", "content": "Eres un asistente virtual que ayudará a los profesores de la Universidad San Sebastían de Chile en su labor."},
                {"role": "user", "content": texto}
              ]
         )

         return completion.choices[0].message.content
    
    def generate_audio(self, audio_content, file_path="./audio/enviado/respuesta.mp3"):
         with self.client.audio.speech.with_streaming_response.create(
              model='tts-1',
              voice='nova',
              input=audio_content
         ) as response:
              response.stream_to_file(file_path)


asistente = AsistenteOpenAi()  

transcripcion = asistente.audio_to_text()  
chat = asistente.generate_answer(transcripcion)  
asistente.generate_audio(chat)  




