import subprocess
import shutil
import threading
import os
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.image import Image
from moviepy.editor import VideoFileClip
from zdefs import record_stream, add_time, segundos_para_hms, predict_post
from selenium_upload import selenium_upload
from google_API_upload import google_API_upload
from streaming import streaming
from streaming import threads_ativas

#KIVY SECTION
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1500')
Config.set('graphics', 'height', '740')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'borderless', False)
Config.set('kivy', 'exit_on_escape', False)

#Streams que vão ser monitoradas
Streams = ["pijack11","dududuelista","guiven","yulla","kennzy","ayellol","minerva","thehydrogen","nicklink",
           "brtt","courtesy","aiye","absoluttlol","pimpimenta","titiltei"]

#Importei depois pq tava bugando com o config.set
from kivy.uix.textinput import TextInput

class VideoScreen(Screen):
    try:
        def __init__(self, **kw):
            super(VideoScreen, self).__init__(**kw)    
            #Imagem de fundo
            background_image = Image(source = "images/VideoBack.png", size_hint = (1,1), allow_stretch = True)
            self.add_widget(background_image)
            
            #VideoPlayer
            self.layout = BoxLayout(orientation='vertical', pos_hint={"x": 0.2, "y": 0.2}, size_hint=(0.8, 0.8))
            self.player = VideoPlayer(source="", options={'eos': 'loop'})
            self.player.state = "stop"
            
            self.player.allow_stretch = False
            self.layout.add_widget(self.player)
            self.add_widget(self.layout)

            #ScrollView
            scroll_layout = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None)
            scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
            clips_scroll = ScrollView(pos_hint={"x": 0, "y": 0.2}, size_hint=(0.2, 0.8))
            for clip in os.listdir('evaluete clip'):
                clip = clip.replace(".mp4", "")
                clip_button = Button(text=f"{clip}",
                                color = (1,1,1,1),
                                size_hint_y=None,
                                size_hint_x= 1,
                                font_size = 15,
                                height= 40,
                                halign='left')
                clip_button.bind(on_release = self.change_video)
                scroll_layout.add_widget(clip_button)
            clips_scroll.add_widget(scroll_layout)
            self.add_widget(clips_scroll)
        
            #PAGE BUTTONS
            button_go_posting_page = Button(text=f"Posting Page",
                                color = (1,1,1,1),
                                size_hint = (0.045,0.1),
                                pos_hint = {"x": 0.022, "y": 0.085},
                                font_size = 20,
                                opacity = 0)
            button_go_posting_page.bind(on_release=self.go_to_posting)
            self.add_widget(button_go_posting_page)

            button_go_streaming_page = Button(text=f"Streaming Page",
                                color = (1,1,1,1),
                                size_hint = (0.054,0.1),
                                pos_hint = {"x": 0.1265, "y": 0.085},
                                font_size = 20,
                                opacity = 0)
            button_go_streaming_page.bind(on_release= self.go_to_streaming)
            self.add_widget(button_go_streaming_page)

            button_go_video_page = Button(text=f"Video page",
                                color = (1,1,1,1),
                                size_hint = (0.056,0.1),
                                pos_hint = {"x": 0.069, "y": 0.015},
                                font_size = 20,
                                opacity = 0)
            button_go_video_page.bind(on_release= self.go_to_video)
            self.add_widget(button_go_video_page)

            button_go_trash_page = Button(text=f"Trash Page",
                                color = (1,1,1,1),
                                size_hint = (0.02,0.07),
                                pos_hint = {"x": 0.01, "y": 0.01},
                                font_size = 20,
                                opacity = 0)
            button_go_trash_page.bind(on_release= self.go_to_trash)
            self.add_widget(button_go_trash_page)
            
            accept_button = Button(size_hint = (0.07,0.11),
                                pos_hint = {"x": 0.86, "y": 0.023},
                                opacity = 0)
            accept_button.bind(on_release= self.accept_clip)
            self.add_widget(accept_button)

            refuse_button = Button(size_hint = (0.07,0.13),
                                pos_hint = {"x": 0.27, "y": 0.015},
                                opacity = 0)
            refuse_button.bind(on_release= self.refuse_clip)
            self.add_widget(refuse_button)

            retreat_button = Button(size_hint = (0.04 ,0.1),
                                pos_hint = {"x": 0.375, "y": 0.01},
                                opacity = 0)
            retreat_button.bind(on_release= self.retreat_clip)
            self.add_widget(retreat_button)

            advance_button = Button(size_hint = (0.04 ,0.1),
                                pos_hint = {"x": 0.79, "y": 0.01},
                                opacity = 0)
            advance_button.bind(on_release= self.advance_clip)
            self.add_widget(advance_button)

            cut_button = Button(size_hint = (0.049 ,0.1),
                                pos_hint = {"x": 0.575, "y": 0.02},
                                opacity = 0)
            
            cut_button.bind(on_release= self.cut_clip)
            self.add_widget(cut_button)
            
            
            self.cut_start_input = TextInput(size_hint = (0.05, 0.052),
                                pos_hint = {"x": 0.5, "y": 0.03},
                                font_size = 30,
                                multiline=False)

            self.add_widget(self.cut_start_input)
            
            self.cut_end_input = TextInput(size_hint = (0.05, 0.052),
                                pos_hint = {"x": 0.655, "y": 0.03},
                                font_size = 30,
                                multiline=False)
            
            self.add_widget(self.cut_end_input)

            self.File_name_label = Label(text = "",
                                    size_hint = (0.3, 0.1),
                                    pos_hint = {"x": 0.28, "y": 0.1},
                                    font_size = 35,
                                    padding = (10,10,10,10))
            self.add_widget(self.File_name_label)

            self.File_name_input = TextInput(size_hint = (0.3, 0.05),
                                    pos_hint = {"x": 0.55, "y": 0.12},
                                    font_size = 25,
                                    padding = (5,5,5,5))
            self.add_widget(self.File_name_input)

        def go_to_video(self, kw):
            sm.switch_to(VideoScreen(name="video"))  
        
        def go_to_streaming(self, kw):
            sm.switch_to(StreamingScreen(name="streaming"))
        
        def go_to_posting(self, kw):
            sm.switch_to(PostingScreen(name="posting")) 
        
        def go_to_trash(self, kw):
            sm.switch_to(TrashScreen(name="trash"))       
        
        def accept_clip(self, kw):
            video_path = self.player.source
            nick = video_path.split("-")[1]
            self.player.source = ""
            #Achar o channel referente ao video
            if nick in Streams:
                channel = "queen ashe clips"

            if self.File_name_input.text != "":
                try:
                    new_video_path = channel + "/" + self.File_name_input.text + ".mp4"
                    saved_clips_path = "C:/Users/picha/Desktop/Things of the project/Clips postados/" + self.File_name_input + ".mp4"
                    shutil.copy(video_path, new_video_path)
                    shutil.move(video_path, saved_clips_path)
                except:
                    print("ERRO, nome invalido ou esqueceu de colocar o canal")
                    None

            self.__init__() 
        
        def refuse_clip(self, kw):
            video_path = self.player.source
            self.player.source = ""
            new_video_path = "refused clip/" + video_path.replace("evaluete clip/", "")
            shutil.move(video_path, new_video_path)
        
            self.__init__()   
        
        def retreat_clip(self, kw): #Adicionar remoção de clip depois do retreat
            try:
                self.player.state = "stop"
                file_video = self.player.source
                self.__init__()
                video = file_video.replace("evaluete clip/", "").replace(".mp4", "")
                number_video = video.split("-")[0]
                nick = video.split("-")[1]
                video_id = video.split('-')[2]
                stream_url = "https://www.twitch.tv/videos/" + video_id
                text_currently_time = video.split("-")[3]
                splited_text_currently_time = text_currently_time.replace("_", ":")
                clip = VideoFileClip(file_video)
                duracao_segundos = int(clip.duration)
                
                try:
                    record_stream(nick, stream_url, splited_text_currently_time, 30, 0, duracao_segundos, number_video)
                except:
                    print("Aconteceu algum erro na regravação!")

                fvideo = f"{number_video}-{nick}-{video_id}-{text_currently_time}.mp4"
                self.player.source = "evaluete clip/" + fvideo
                #A falha de mudança:
                #new_video_path = "refused clip/" + file_video.replace("evaluete clip/", "")
                #shutil.move(file_video, new_video_path)
                self.__init__()

            except Exception as e:
                print("Ocorreu um erro:", str(e))  
        
        def advance_clip(self, kw): #Adicionar remoção de clip depois do advance
            try:
                file_video = self.player.source
                self.player.source = ""
                self.__init__()
                video = file_video.replace("evaluete clip/", "").replace(".mp4", "")
                number_video = video.split("-")[0]
                nick = video.split("-")[1]
                video_id = video.split('-')[2]
                stream_url = "https://www.twitch.tv/videos/" + video_id
                text_currently_time = video.split("-")[3]
                splited_text_currently_time = text_currently_time.replace("_", ":")
                clip = VideoFileClip(file_video)
                duracao_segundos = int(clip.duration)
                
                try:
                    record_stream(nick, stream_url, splited_text_currently_time, 0, 30, duracao_segundos, number_video)
                except:
                    print("Aconteceu algum erro na regravação!")

                fvideo = f"{number_video}-{nick}-{video_id}-{text_currently_time}.mp4"
                self.player.source = "evaluete clip/" + fvideo

                #new_video_path = "refused clip/" + file_video.replace("evaluete clip/", "")
                #shutil.move(file_video, new_video_path)
                self.__init__()
            except Exception as e:
                print("Ocorreu um erro:", str(e))  
        
        def cut_clip(self, kw): #Adicionar remoção de clip depois do Cut
            #Criar output video
            name_video = self.player.source
            self.player.source = ""
            video = name_video.replace("evaluete clip/", "").replace(".mp4", "")
            number_video = video.split("-")[0]
            nick = video.split("-")[1]
            video_id = video.split('-')[2]
            #Start Time e End Time
            start_time = int(self.cut_start_input.text)
            if start_time == 0:
                start_time = 1
            end_time = int(self.cut_end_input.text)
            text_currently_time = video.split("-")[3]
            text_curremtly_time = text_currently_time.replace("_", ":")
            file_start_time = add_time(text_curremtly_time, start_time)
            file_start_time = file_start_time.replace(":", "_")
            start_time = segundos_para_hms(start_time)
            end_time = segundos_para_hms(end_time)
            
            output_video = f"evaluete clip/{number_video}-{nick}-{video_id}-{file_start_time}.mp4"
            
            try:
                subprocess.call(['ffmpeg', '-i', name_video, '-ss', start_time, '-to', end_time, '-c', 'copy', output_video])
                print("Vídeo cortado com sucesso!")
            except Exception as e:
                print("Ocorreu um erro ao cortar o vídeo:", str(e))

            fvideo = f"{number_video}-{nick}-{video_id}-{text_currently_time}.mp4"
            self.player.source = "evaluete clip/" + fvideo
            self.cut_start_input.text = ""
            self.cut_end_input.text = ""
            new_video_path = "refused clip/" + name_video.replace("evaluete clip/", "")
            shutil.move(name_video, new_video_path)
            self.__init__()           
        
        def change_video(self, button):
            self.player.state = "stop"
            file_video = "evaluete clip/" + button.text + ".mp4"
            #Video Duration
            clip = VideoFileClip(file_video)
            duracao_segundos = int(clip.duration)
            duracao_segundos = str(duracao_segundos)
            #Video Number e Video Streamer
            video_number = button.text.split("-")[0]
            video_streamer = button.text.split("-")[1]
            self.File_name_label.text = video_number + " - " + video_streamer + ": " + duracao_segundos + "s"
            self.player.source = file_video
            self.player.state = "play"
    except Exception as e:
        print("ERRO FATAL:", str(e)) 
        None    


#Variables to the posting screen class
delete_count = 0
delete_text_button = ""
running = False

class PostingScreen(Screen):
    def __init__(self, **kw):
        global running
        super(PostingScreen, self).__init__(**kw)
        
        #Background
        background_image = Image(source = "images/UploadBack.png", size_hint = (1,1), allow_stretch = True)
        self.add_widget(background_image)
        
        #UPLOAD PAGE
        #Lista de videos que vão ser postados periodicamente
        layout_vertical = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, size_hint_x=1)
        layout_vertical.bind(minimum_height=layout_vertical.setter('height'))
        stream_scroll = ScrollView(pos_hint={"x":0.05, "y":0.4}, size_hint= (0.3, 0.5))
        accepted_clips = os.listdir("queen ashe clips/")

        for clip in accepted_clips:
            clip_button = Button(text= f"{clip}",
                                 color = (1,1,1,1),
                                size_hint_y= None,
                                size_hint_x= 1,
                                font_size = 25)
            layout_vertical.add_widget(clip_button)
            clip_button.bind(on_release = self.delete_video)
        stream_scroll.add_widget(layout_vertical)
        self.add_widget(stream_scroll)

        #Botão Postar Agora, chama a função post_now dependendo das config
        Post_now = Button(text=f"Post Now",
                            color = (1,1,1,1),
                            size_hint = (0.12,0.06),
                            pos_hint = {"x": 0.06, "y": 0.3},
                            font_size = 20)
        
        Post_now.bind(on_release= lambda instance: self.post_now(1))
        self.add_widget(Post_now)
        
        #Botão Ativar Postar Periodico
        self.Period_post_button = Button(text=f"Period Post",
                            color = (1,1,1,1),
                            size_hint = (0.12,0.06),
                            background_color = (1,0,0,1),
                            pos_hint = {"x": 0.21, "y": 0.3},
                            font_size = 20)
        
        #Esse botão, não faz mais nda ele era usado na versão em que o selenium fazia o upload
        self.Period_post_button.bind(on_release= self.turn_on_period_post) 
        self.add_widget(self.Period_post_button)
        

        #Label Proxima Postagem
        self.Period_post_label = Label(text ="",
                            color = (1,1,1,1),
                            size_hint = (0.12,0.05),
                            pos_hint = {"x": 0.21, "y": 0.22},
                            font_size = 20)        
        self.add_widget(self.Period_post_label)
        
        #PAGE BUTTONS
        button_go_posting_page = Button(text=f"Posting Page",
                            color = (1,1,1,1),
                            size_hint = (0.045,0.1),
                            pos_hint = {"x": 0.022, "y": 0.085},
                            font_size = 20,
                            opacity = 0)
        button_go_posting_page.bind(on_release=self.go_to_posting)
        self.add_widget(button_go_posting_page)

        button_go_streaming_page = Button(text=f"Streaming Page",
                            color = (1,1,1,1),
                            size_hint = (0.054,0.1),
                            pos_hint = {"x": 0.1265, "y": 0.085},
                            font_size = 20,
                            opacity = 0)
        button_go_streaming_page.bind(on_release= self.go_to_streaming)
        self.add_widget(button_go_streaming_page)

        button_go_video_page = Button(text=f"Video page",
                            color = (1,1,1,1),
                            size_hint = (0.056,0.1),
                            pos_hint = {"x": 0.069, "y": 0.015},
                            font_size = 20,
                            opacity = 0)
        button_go_video_page.bind(on_release= self.go_to_video)
        self.add_widget(button_go_video_page)

        button_go_trash_page = Button(text=f"Trash Page",
                            color = (1,1,1,1),
                            size_hint = (0.02,0.07),
                            pos_hint = {"x": 0.01, "y": 0.01},
                            font_size = 20,
                            opacity = 0)
        button_go_trash_page.bind(on_release= self.go_to_trash)
        self.add_widget(button_go_trash_page)

    def turn_on_period_post(self, button):
        None

    def delete_video(self, button):
        global delete_count, delete_text_button
        if delete_text_button != button.text:
            delete_text_button = button.text
            delete_count = 0
        delete_count += 1
        if delete_count == 3:
            delete_count = 0
            de = "queen ashe clips/" + button.text
            para = "refused clip/" + button.text
            shutil.move(de, para)
            self.__init__()
    
    def post_now(self, config):
        """Normaly only Opens a Folder Pack of where is the video, but can be changed to configs 1, 2 or 3\n
        1 --> Open the folder to get the videos\n
        2 --> Use the selenium with the google chrome beta to upload\n
        3 --> Use the Google's API to upload (Recommended)"""
        
        if config == 1:
            folder_path = "C:/Users/picha/Desktop/Git Done/Automation Project/queen ashe clips"
            subprocess.run(["explorer", folder_path])
        
        if config == 2:
            videos_folder = os.listdir("C:/Users/picha/Desktop/Git Done/Automation Project/queen ashe clips")
            
            selenium_upload(videos_folder[0], "Queen Ashe Clips")

        if config == 3:
            videos_folder = os.listdir("")
            video_path = "" + videos_folder[0]
            google_API_upload(video_path, videos_folder[0])

    def go_to_video(self, kw):
        sm.switch_to(VideoScreen(name="video"))    

    def go_to_streaming(self, kw):
        sm.switch_to(StreamingScreen(name="streaming"))

    def go_to_posting(self, kw):
        sm.switch_to(PostingScreen(name="posting"))    


    def go_to_trash(self, kw):
        sm.switch_to(TrashScreen(name="trash"))

class StreamingScreen(Screen):
    def __init__(self, **kw):
        super(StreamingScreen, self).__init__(**kw)
        
        #Background
        background_image = Image(source = "images/StreamingBack.png", size_hint = (1,1), allow_stretch = True)
        self.add_widget(background_image)

        #PAGE BUTTONS
        button_go_posting_page = Button(text=f"Posting Page",
                            color = (1,1,1,1),
                            size_hint = (0.045,0.1),
                            pos_hint = {"x": 0.022, "y": 0.085},
                            font_size = 20,
                            opacity = 0)
        button_go_posting_page.bind(on_release=self.go_to_posting)
        self.add_widget(button_go_posting_page)

        button_go_streaming_page = Button(text=f"Streaming Page",
                            color = (1,1,1,1),
                            size_hint = (0.054,0.1),
                            pos_hint = {"x": 0.1265, "y": 0.085},
                            font_size = 20,
                            opacity = 0)
        button_go_streaming_page.bind(on_release= self.go_to_streaming)
        self.add_widget(button_go_streaming_page)

        button_go_video_page = Button(text=f"Video page",
                            color = (1,1,1,1),
                            size_hint = (0.056,0.1),
                            pos_hint = {"x": 0.069, "y": 0.015},
                            font_size = 20,
                            opacity = 0)
        button_go_video_page.bind(on_release= self.go_to_video)
        self.add_widget(button_go_video_page)

        button_go_trash_page = Button(text=f"Trash Page",
                            color = (1,1,1,1),
                            size_hint = (0.02,0.07),
                            pos_hint = {"x": 0.01, "y": 0.01},
                            font_size = 20,
                            opacity = 0)
        button_go_trash_page.bind(on_release= self.go_to_trash)
        self.add_widget(button_go_trash_page)
        
        layout_vertical = BoxLayout(orientation='vertical', spacing=50, size_hint_y=None, size_hint_x=1, padding=(20, 0, 20, 0))
        layout_vertical.bind(minimum_height=layout_vertical.setter('height'))
        layout_horizontal= BoxLayout(orientation='horizontal', spacing=50, size_hint_y=None, size_hint_x=1)
        stream_scroll = ScrollView(pos_hint={"x":0, "y":0.2}, size_hint= (1, 0.7))

        count = 0
        for stream in Streams:
            count += 1
            stream_button = Button(text=f"{stream}",
                            color = (1,1,1,1),
                            size_hint_y= 1,
                            size_hint_x= 1,
                            font_size = 40)
            if stream in threads_ativas:
                stream_button.background_color = (0,1,0,1)

            stream_button.bind(on_release = self.start_streaming)
            layout_horizontal.add_widget(stream_button)

            if count == 4:
                layout_vertical.add_widget(layout_horizontal)
                layout_horizontal = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=None, size_hint_x=1)
                count = 0

        layout_vertical.add_widget(layout_horizontal)        
        stream_scroll.add_widget(layout_vertical)
        self.add_widget(stream_scroll)
    
    def start_streaming(self, refer_button): #Abrir threading com streming
        threading.Thread(target=streaming, daemon=False, args=(refer_button,)).start()
        
    def go_to_video(self, kw):
        sm.switch_to(VideoScreen(name="video"))    
    
    def go_to_streaming(self, kw):
        sm.switch_to(StreamingScreen(name="streaming"))
    
    def go_to_posting(self, kw):
        sm.switch_to(PostingScreen(name="posting"))  
    
    def go_to_trash(self, kw):
        sm.switch_to(TrashScreen(name="trash"))

class TrashScreen(Screen):
    def __init__(self, **kw):
        super(TrashScreen, self).__init__(**kw)
        
        #Background
        background_image = Image(source = "images/TrashBack.png", size_hint = (1,1), allow_stretch = True)
        self.add_widget(background_image)

        #ScrollView
        scroll_layout = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        clips_scroll = ScrollView(pos_hint={"x": 0, "y": 0.2}, size_hint=(1, 0.8))
        for clip in os.listdir('refused clip'):
            clip = clip.replace(".mp4", "")
            clip_button = Button(text=f"{clip}",
                            color = (1,1,1,1),
                            size_hint_y=None,
                            size_hint_x= 1,
                            font_size = 15,
                            height= 40,
                            halign='left')
            scroll_layout.add_widget(clip_button)
        clips_scroll.add_widget(scroll_layout)
        self.add_widget(clips_scroll)

        #Deletar todos
        delete_all = Button(text = "Delete All",
                            background_color = (1,0,0,1),
                            size_hint = (0.3, 0.1),
                            pos_hint = {"x": 0.45, "y": 0.05})
        delete_all.bind(on_release = self.delete_all)
        self.add_widget(delete_all)
        
        #PAGE BUTTONS
        button_go_posting_page = Button(text=f"Posting Page",
                            color = (1,1,1,1),
                            size_hint = (0.045,0.1),
                            pos_hint = {"x": 0.022, "y": 0.085},
                            font_size = 20,
                            opacity = 0)
        button_go_posting_page.bind(on_release=self.go_to_posting)
        self.add_widget(button_go_posting_page)

        button_go_streaming_page = Button(text=f"Streaming Page",
                            color = (1,1,1,1),
                            size_hint = (0.054,0.1),
                            pos_hint = {"x": 0.1265, "y": 0.085},
                            font_size = 20,
                            opacity = 0)
        button_go_streaming_page.bind(on_release= self.go_to_streaming)
        self.add_widget(button_go_streaming_page)

        button_go_video_page = Button(text=f"Video page",
                            color = (1,1,1,1),
                            size_hint = (0.056,0.1),
                            pos_hint = {"x": 0.069, "y": 0.015},
                            font_size = 20,
                            opacity = 0)
        button_go_video_page.bind(on_release= self.go_to_video)
        self.add_widget(button_go_video_page)

        button_go_trash_page = Button(text=f"Trash Page",
                            color = (1,1,1,1),
                            size_hint = (0.02,0.07),
                            pos_hint = {"x": 0.01, "y": 0.01},
                            font_size = 20,
                            opacity = 0)
        button_go_trash_page.bind(on_release= self.go_to_trash)
        self.add_widget(button_go_trash_page)
    
    def delete_all(self, *kw):
        for video in os.listdir("refused clip/"):
            videos = "refused clip/" + video
            os.remove(videos)
        self.__init__()

    def go_to_video(self, *kw):
        sm.switch_to(VideoScreen(name="video")) 
    
    def go_to_streaming(self, *kw):
        sm.switch_to(StreamingScreen(name="streaming"))
    
    def go_to_posting(self, *kw):
        sm.switch_to(PostingScreen(name="posting"))   
    
    def go_to_trash(self, *kw):
        sm.switch_to(TrashScreen(name="trash"))

class WindowManager(ScreenManager):
    pass

sm = WindowManager(transition=NoTransition())
screens = [VideoScreen(name="video"), PostingScreen(name="posting"), StreamingScreen(name="streaming"), TrashScreen(name="trash")]
for screen in screens:
    sm.add_widget(screen)

class ClipManager(App):
    def build(self):
        return sm

if __name__ == "__main__":
    ClipManager().run()