import speech_recognition as sr
from moviepy import AudioFileClip
import os
import sys
import io

#converting to utf-8 for passing terminal error
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def process_mp4_to_form(mp4_file_path):
    #converting to temporary .wav file 
    wav_file_path = "temp_audio.wav"
    
    #checking file path
    if not os.path.exists(mp4_file_path):
        print(f"File is not in the path: {mp4_file_path}")
        return

    print(f"Video file is processing: {mp4_file_path}")
    try:
        #loading as audio
        audio = AudioFileClip(mp4_file_path)
        audio.write_audiofile(wav_file_path, logger=None) 
        audio.close()
    except Exception as e:
        print(f"Error in processing audio: {e}")
        return

    #text extraction from audio
    recognizer = sr.Recognizer()
    form_data = {"নাম": "পাওয়া যায়নি", "ইমেইল": "পাওয়া যায়নি", "ঠিকানা": "পাওয়া যায়নি"}

    if os.path.exists(wav_file_path):
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)
            try:
                #google speech recognition
                text = recognizer.recognize_google(audio_data, language='bn-BD') #setting to bangla
                print(f"\nIn the audio: {text}")

                name_keywords = ["নাম", "পরিচয়", "বলা হয়"]
                email_keywords = ["ইমেইল", "মেইল", "ই-মেইল"]
                address_keywords = ["ঠিকানা", "বাসা", "বাড়ি", "ঘর", "গ্রাম"]

                #name extraction
                for kw in name_keywords:
                    if kw in text:
                        form_data["নাম"] = text.split(kw)[-1].strip().split()[0]
                        break 

                #address
                for kw in address_keywords:
                    if kw in text:
                        after_kw = text.split(kw)[-1].strip()
                        for e_kw in email_keywords:
                            if e_kw in after_kw:
                                after_kw = after_kw.split(e_kw)[0].strip()
                        form_data["ঠিকানা"] = after_kw
                        break  

                #email
                for kw in email_keywords:
                    if kw in text:
                        email_content = text.split(kw)[-1].strip()
                        garbage_words = ["শেষ", "ধন্যবাদ", "থ্যাঙ্ক ইউ"]
                        for g_word in garbage_words:
                            if g_word in email_content:
                                email_content = email_content.split(g_word)[0].strip()
                        form_data["ইমেইল"] = email_content.replace(" ", "").replace("এটদারেট", "@").replace("ডট", ".")
                        break

            except sr.UnknownValueError:
                print("Audio is not clear")
            except sr.RequestError:
                print("Internet connection or Server error.")

        #remove the temporary file created
        os.remove(wav_file_path)

    print("\n--- সংগৃহীত ফর্ম ডেটা ---")
    for key, value in form_data.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    my_video = r"D:\Python\Machine Learning Practice\Speech Recognition\test.mp4" 
    process_mp4_to_form(my_video)