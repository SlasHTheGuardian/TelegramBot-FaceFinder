import telebot
import os
from pathlib import Path
import soundfile as sf
import cv2

TOKEN = "TokenIsSecret"
bot = telebot.TeleBot(TOKEN)


#  Voice message handling
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    ID = message.from_user.id 
    filename = message.voice.file_id
    folder_path = Path(f'D:\mylab\database\Voices\{ID}')
    try:
        os.mkdir(folder_path)
    except:
        pass
    file_path = folder_path / f'{filename}.oga'
    downloaded_file = bot.download_file(file_info.file_path)
    file_path.write_bytes(downloaded_file)
    data, samplerate = sf.read(file_path)
    dirpath = os.listdir(f'D:\mylab\database\Voices\{ID}')
    number = 0
    for element in dirpath:
        number = number+1
    number_of_new_element = number + 1
    sf.write(f'audio_message_{number_of_new_element}.wav', data, sr=16000)  # Audio converting


# Finding faces on the photo
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):  
    file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    ID = message.from_user.id
    filename = message.photo[len(message.photo)-1].file_id
    folder_path = Path(f'D:\mylab\database\Images\{ID}')
    try:
        os.mkdir(folder_path)
    except:
        pass
    file_path = folder_path / f'{filename}.jpg'
    downloaded_file = bot.download_file(file_info.file_path)
    file_path.write_bytes(downloaded_file)
    face_cascade = cv2.CascadeClassifier('D:\mylab\haarcascade_frontalface_default.xml')
    image = cv2.imread(f'D:\mylab\database\Images\{ID}\{filename}.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))
    num_of_faces = format(len(faces))
    if num_of_faces == 0:
        phrase = 'Тут нет ни одного лица'
        bot.send_message(message.chat.id, phrase)
        os.remove(file_path)
    else:
        phrase = f'Количество лиц: {num_of_faces} '
        bot.send_message(message.chat.id, phrase)


bot.polling(timeout=60)
