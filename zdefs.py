import subprocess
from time import sleep
from datetime import datetime
import datetime
from moviepy.editor import VideoFileClip
import re

from hype_filter import hype_filter_upper, hype_filter_lower


def record_stream(streamer, live_url, start_time, retreat, advance, duration, ordem):
    """This function do a subprocess using streamlink with the link, time and duration of the stream"""

    folder_path = "C:/Users/picha/Desktop/Automation Project/refused clip/"
    
    if ordem == 0:
        with open("video_number.txt", 'r') as file: #Pegar o numero de arquivo
            number = file.readline()
            number = int(number)
        number += 1
        with open('video_number.txt', 'w') as file: #Escrever o numero no arquivo
            number = str(number)
            file.write(number)
            ordem = number

    record_time = duration + retreat + advance
    start_time = start_time.replace("_", ":")
    time_obj = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
    new_time_obj = datetime.datetime.combine(datetime.date.today(), time_obj) - datetime.timedelta(seconds=retreat)
    start_time = new_time_obj.time().strftime("%H:%M:%S")

    stream_number = live_url.replace("https://www.twitch.tv/videos/", "")
    file_start_time = start_time.replace(":", "_")
    file_name = f"{ordem}-{streamer}-{stream_number}-{file_start_time}.mp4"
    
    cmd = f"streamlink {live_url} best --hls-segment-threads 8 --retry-max 100 --hls-live-edge 5 -o \"{folder_path}{file_name}\" --hls-duration {record_time} --hls-start-offset {start_time} --retry-streams 10 --force"
    subprocess.call(cmd, shell=True)
    
    #Copiar o video para outro folder para deixar em um formato mais aceitavel pro ffmpeg
    sleep(1)
    path = "refused clip/" + file_name
    path2 = "evaluete clip/" + file_name
    video = VideoFileClip(path)
    duration = int(video.duration)
    c = segundos_para_hms(duration)
    d = segundos_para_hms(1)
    
    try:
        subprocess.call(['ffmpeg', '-y', '-i', path, '-ss', d, '-t', c, '-c', 'copy', path2])
    except Exception as e:
        print("Ocorreu um erro ao cortar o vídeo:", str(e))
    
def check_url(live_url):
    """This def check if the url is in the file 'url_done.txt'

    If it is, returns False.

    Else, returns True and put the url in the file"""

    with open("url_done.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        if live_url in line:
            return False
    lines.append(live_url + '\n')
    with open("url_done.txt", "w") as file:
        for line in lines:
            file.write(line)
    return True

def formatar_tempo(tempo):
    """This def formats the time of the stream
    00:01:00 --> 1:00
    00:52:10 --> 52:10
    03:12:12 --> 03:12:12"""

    tempo1 = re.compile('0[1-9]:[0-9][0-9]:[0-9][0-9]')
    tempo2 = re.compile('00:0[0-9]:[0-9][0-9]')
    tempo3 = re.compile('00:[1-9][0-9]:[0-9][0-9]')
    tempo4 = re.compile('[1-9][0-9]:[0-9][0-9]:[0-9][0-9]')
    if re.fullmatch(tempo1, tempo):
        return tempo[1:]
    if re.fullmatch(tempo2, tempo):
        return tempo[4:]
    if re.fullmatch(tempo3, tempo):
        return tempo[3:]
    if re.fullmatch(tempo4, tempo):
        return tempo

def evaluete_hype(text_message):
    """This function evaluete the hype of a message, quantifiying by the numbers of 'k' or by the commun messages 
    of a hype spyke. If it doesn't match any of them, returns -2."""

    random_all = r"(.*[kswhj]){4,}.*"
    if "K" in text_message or "k" in text_message:
        if text_message.count("k") == 3 or text_message.count("k") == 2:
            hyper = 1
        elif text_message.count("k") == 4 or text_message.count("k") == 5:
            hyper = 2
        elif text_message.count("k") > 5:
            hyper = 3
        elif text_message.count("K") == 3 or text_message.count("K") == 2:
            hyper = 2
        elif text_message.count("K") == 4 or text_message.count("K") == 5:
            hyper = 3
        elif text_message.count("K") > 5:
            hyper = 4
    elif re.fullmatch(random_all, text_message, re.IGNORECASE) and text_message.count(" ") < 2:
        hyper = 3
    elif text_message in hype_filter_upper:
        hyper = 4
    elif text_message in hype_filter_lower:
        hyper = 3
    else:   
        hyper = -2
    return round(hyper, 2)

def screen_go(sm, screen, nome):
    """Function used in the kivy application to change the screens of a screen manager"""

    sm.switch_to(screen(name=f"{nome}"))

def reduce_time(start_time, retreat):
    """Remove time in seconds of a time in a string format (00:00:00)"""

    time_obj = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
    new_time_obj = datetime.datetime.combine(datetime.date.today(), time_obj) - datetime.timedelta(seconds=retreat)
    start_time = new_time_obj.time().strftime("%H:%M:%S")
    return start_time

def add_time(start_time, advance):
    """Add time in seconds of a time in a string format (00:00:00)"""

    time_obj = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
    new_time_obj = datetime.datetime.combine(datetime.date.today(), time_obj) + datetime.timedelta(seconds=advance)
    start_time = new_time_obj.time().strftime("%H:%M:%S")
    return start_time

def segundos_para_hms(segundos):
    """Transform seconds to a string format (00:00:00)"""

    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def predict_post(time):
    """A def to calculate time that the video might be posted by how many time between it"""

    # Obter a data e hora atual
    data_atual = datetime.datetime.now()

    # Converter a string de tempo em um objeto timedelta
    tempo_delta = datetime.timedelta(hours=int(time[:2]),
                            minutes=int(time[3:5]),
                            seconds=int(time[6:]))

    # Somar a data atual com o timedelta
    data_atualizada = data_atual + tempo_delta
    horario_atualizado = data_atualizada.strftime("%H:%M:%S")

    data_atualizada2 = data_atual + tempo_delta + tempo_delta
    horario_atualizado2 = data_atualizada2.strftime("%H:%M:%S")

    data_atualizada3 = data_atual + tempo_delta + tempo_delta + tempo_delta
    horario_atualizado3 = data_atualizada3.strftime("%H:%M:%S")
    
    return (horario_atualizado + "\n" + horario_atualizado2 + "\n" + horario_atualizado3)
