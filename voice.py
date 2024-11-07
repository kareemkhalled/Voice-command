"""
ems_zeta_voice base module.

This is the principal module of the ems_zeta_voice project.
here we have our main classes and objects.

"""
import os
import io
import pyttsx3
import openai
from typing import Tuple, Union
from fastapi import UploadFile
from config import CommonConfigurator
import speech_recognition as sr



class VoiceHandler(object):


    class VoiceHandler(object):
     def __init__(self, mode: str = "original", language: str = None) -> None:
        self.language = language if language else "ar"
        self.engine = pyttsx3.init()
        self.mode = mode
        self.set_voice(self.language)  # تعيين الصوت الافتراضي عند التهيئة
        self.invoices_information_info = فواتير ,الفواتير ,invoices}

    def set_voice(self, language: str):
        if language == "ar":
            self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_arEG_Hoda')
        elif language == "en":
            self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enUS_Zira')  # مثال لصوت إنجليزي

    async def speech_to_text(self, audio_file: str) -> str:
        if self.mode == "original":
            return await self.speech_to_text_original(audio_file)
        else:
            text = await self.speech_to_text_openai(audio_file)
            # التحقق من السؤال المحدد
            if text.lower() == "what is your name?":
                self.set_voice("en")  # تغيير الصوت إلى إنجليزي
                response = "My name is Voice Assistant."
                return response
            else:
                self.set_voice("ar")  # استعادة الصوت العربي لبقية الأسئلة
                return text  # إرجاع النص باللغة الافتراضية (العربية)

    async def text_to_speech(self, text_data: str) -> Tuple[str, bytes]:
        audio_file = os.path.join(r"D:\WEB_APP\ems_voice_command\ems_zeta_voice\temp", f"{CommonConfigurator.generate_random_name()}.mp3")
        self.engine.save_to_file(text_data, audio_file)
        self.engine.runAndWait()
        # قراءة الملف الصوتي المحفوظ
        with open(audio_file, "rb") as file:
            audio_data = file.read()
        return audio_file, audio_data

    # باقي الدوال...




    def __init__(self, mode:str = "original", language:str = None) -> None:

        self.language = language if language else "ar"
        self.engine = pyttsx3.init()
        self.mode = mode
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_arEG_Hoda')
    async def speech_to_text(self, audio_file: str) -> str:
        if self.mode == "original":
            return await self.speech_to_text_original(audio_file)
        else:
            return await self.speech_to_text_openai(audio_file)

    async def text_to_speech(self, text_data: str) -> Tuple[str, bytes]:
        if self.mode == "original":
            return await self.text_to_speech_original(text_data)
        else:
            return await self.text_to_speech_openai(text_data)

    async def speech_to_text_original(self, audio_file:str) -> str:

        """
        Recognizes speech from an audio file using Google Web Speech API.

        Parameters:
        - audio_file (str): The path to the audio file to be recognized.

        Returns:
        - str: The recognized text extracted from the audio file.

        Raises:
        - sr.UnknownValueError: If the speech recognizer is unable to understand the audio.
        - sr.RequestError: If there is an error in accessing the Google Web Speech API.
        """
        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data, language=self.language)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError as e:
            return f"Error: {e}"
        
    
    async def text_to_speech_original(self, text_data:str):

        """
        Converts text to speech using pyttsx3 library.

        Parameters:
        - text_data (str): The text data to be converted to speech.

        Returns:
        - Tuple[str, bytes]: A tuple containing the filename of the saved audio file and the audio data in bytes.

        Notes:
        - This function requires the pyttsx3 library to be installed.
        """
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_arEG_Hoda')
        audio_file = os.path.join(r"D:\WEB_APP\ems_voice_command\ems_zeta_voice\temp", f"{CommonConfigurator.generate_random_name()}.mp3")
        self.engine.save_to_file(text_data, audio_file)
        self.engine.runAndWait()
        # Read the saved audio file
        with open(audio_file, "rb") as file:
            audio_data = file.read()
        return audio_file, audio_data
    
    async def speech_to_text_openai(self, audio_file: Union[str, os.PathLike, UploadFile]) -> str:
        try:
            # Handle SpooledTemporaryFile or UploadFile
            if hasattr(audio_file, 'read'):
                # Read file content
                audio_data = audio_file.read()
                # Ensure that the audio file is a supported format
                file_extension = audio_file.filename.split('.')[-1].lower()
                if file_extension not in ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']:
                    return f"Unsupported file format: {file_extension}"
            else:
                # Use standard open for synchronous file reading if audio_file is a path
                with open(audio_file, 'rb') as f:
                    audio_data = f.read()

            # Convert bytes to file-like object for API
            audio_file_like = io.BytesIO(audio_data)

            # Call OpenAI's API for transcription
            response = await openai.Audio.transcribe("whisper-1", file=audio_file_like, language=self.language)
            return response.get("text", "Could not transcribe the audio.")
        except Exception as e:
            return f"Error: {e}"
        
    async def text_to_speech_openai(self, text_data: str) -> Tuple[str, bytes]:
        """
        Converts text to speech using OpenAI API.

        Parameters:
        - text_data (str): The text data to be converted to speech.

        Returns:
        - Tuple[str, bytes]: A tuple containing the filename of the saved audio file and the audio data in bytes.
        """
        try:
            response = await openai.audio.speech.create(voice="ar", text=text_data)
            audio_data = response['audio']

            # Save the audio data to a file
            audio_file = f"{CommonConfigurator.generate_random_name()}.mp3"
            async with open(audio_file, 'wb') as f:
                await f.write(audio_data)

            return audio_file, audio_data
        except Exception as e:
            return f"Error: {e}", b""