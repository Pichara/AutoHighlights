from playwright.sync_api import sync_playwright
from zdefs import check_url, record_stream, evaluete_hype, reduce_time
from time import sleep

#STREAMING SECTION
threads_ativas = []

def streaming(button):
    """This function uses the name of a streamer to join in his twich/videos page and monitor the chat, evaluete it
    with the function evaluete_hype, then call record_stream to record the stream momment in this hype spike.
    OBS: It NEEDS to be adressed only in a button with the streamer's name"""
    
    global threads_ativas
    nick = button.text
    button.background_color = (1,1,0,1)
    
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()
        
        #Cria uma nova página e navega ate a Twitch
        chat_page = context.new_page()
        chat_page.set_default_timeout(100000)
        stream = (f"https://www.twitch.tv/{nick}/videos")
        chat_page.goto(stream)
        chat_page.wait_for_load_state("load")
        chat_page.locator('xpath=//*[@id="offline-channel-main-content"]/div[2]/div[1]/div[1]').click()
        print(1)
        
        #Streaming Finding Loop
        while True:
            for i in range(10):
                chat_page.keyboard.press("PageDown")
                sleep(1)
            sleep(2)

            #Video pos 1
            chat_page.mouse.click(425, 448)
            chat_page.wait_for_load_state("load")
            sleep(1)
            if chat_page.url == stream or "clip" in chat_page.url:
                button.background_color = (1,1,1,1)
                browser.close()
                if nick in threads_ativas:
                    threads_ativas.remove(nick)
                break
            if check_url(chat_page.url) == False:
                chat_page.go_back()
                for i in range(10):
                    chat_page.keyboard.press("PageDown")
                sleep(2)
                
                #Video pos 2 
                chat_page.mouse.click(730, 448)
                chat_page.wait_for_load_state("load")
                sleep(1)
                if chat_page.url == stream or "clip" in chat_page.url:
                    button.background_color = (1,1,1,1)
                    browser.close()
                    if nick in threads_ativas:
                        threads_ativas.remove(nick)
                    break
                if check_url(chat_page.url) == False:
                    chat_page.go_back()
                    for i in range(10):
                        chat_page.keyboard.press("PageDown")
                    
                    #Video Pos 3
                    chat_page.mouse.click(1030, 448)
                    chat_page.wait_for_load_state("load")
                    sleep(1)
                    if chat_page.url == stream or "clip" in chat_page.url:
                        button.background_color = (1,1,1,1)
                        browser.close()
                        if nick in threads_ativas:
                            threads_ativas.remove(nick)
                        break
                    if check_url(chat_page.url) == False:
                        button.background_color = (1,1,1,1)
                        browser.close()
                        if nick in threads_ativas:
                            threads_ativas.remove(nick)
                        break
            print(2)
            button.background_color = (0,1,0,1)
            threads_ativas.append(nick)
            chat_page.wait_for_load_state("load")

            #Caso apareça um botão de permisão para assistir
            start_watching = chat_page.locator('button:has-text("Start Watching")')
            if chat_page.locator('button:has-text("Start Watching")').is_visible():
                start_watching.click()
            
            #Iniciar a verificação do chat e o tratamento de hype
            text_currently_time = ' '
            message_text = ' '
            hype = 0
            print(3)
            
            #Desativar o Som da Pagina
            sleep(1)
            chat_page.evaluate('''
        // Localize o elemento de vídeo na página
        const video = document.querySelector('video');

        // Verifique se o elemento de vídeo existe
        if (video) {
            // Mute o vídeo
            video.muted = true;2
        }
    ''')        
            sleep(1)
            if chat_page.locator('xpath=//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[4]/div/div[3]/div/div/div/button').is_visible():
                chat_page.locator('xpath=//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[4]/div/div[3]/div/div/div/button').click()
            
            #Definir varios tempos finais para finilizar a stream
            l_text_final_time = chat_page.locator('xpath=//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[4]/div/div/div/div[1]/p[2]')
            text_final_time = l_text_final_time.text_content()
            ltime1 = reduce_time(text_final_time, 1)
            ltime2 = reduce_time(text_final_time, 5)
            ltime3 = reduce_time(text_final_time, 10)
            ltime4 = reduce_time(text_final_time, 12)
            ltime5 = reduce_time(text_final_time, 30)
            text_final_times = [ltime1,ltime2,ltime3,ltime4,ltime5]
            print(4)

            #Iniciar o recolhimento e avaliação de mensagens com gatilho para gravação
            while text_currently_time not in text_final_times:
                try:                                    
                    message = chat_page.locator('xpath=//*[@id="live-page-chat"]/div/div/div[2]/div/div/div[2]/div/div/ul/li[last()]/div/div[2]/div/div[1]/div/span[2]/span')
                    if message_text != message.text_content():
                        message_text = message.text_content()
                        hype += evaluete_hype(message_text)
                        print(f"{nick}: {message_text} = {hype}")
                
                    if hype < 0:
                        hype = 0
                    
                    if hype >= 20:
                        text_currently_time = chat_page.locator('xpath=//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[4]/div/div/div/div[1]/p[1]').text_content()
                        
                        try:
                            #31 segundos porque tive que cortar 1 segundo para deixar o video no formato do ffmpeg
                            record_stream(nick, chat_page.url, text_currently_time, 31, 0, 30, 0)
                            hype = 0
                            sleep(50)
                        except:
                            print(f"Houve um problema com a gravação do clip {nick}. Url: {chat_page.url}")
                    
                    text_currently_time = chat_page.locator('xpath=//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[4]/div/div/div/div[1]/p[1]').text_content()
                except:
                   None
                    
            
            chat_page.go_back()

