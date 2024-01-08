from time import sleep
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import shutil
from random import randint

def selenium_upload(video, channel):
    """This function use the Selenium webdriver relationed in the Google Chrome Beta to open the youtube and post the clip
    addressed in the function, all automatically.
    OBS: This upload is not recomended: YOUTUBE does not ALLOW this AUTOMATIC TYPE of UPLOAD. RISKS of HAVING 0 VIEWS!"""

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("user-data-dir=C:\\Users\\picha\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"        
    bot = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)             
    print("Abriu o Chrome")
    sleep(randint(2,4))
    bot.get("https://studio.youtube.com")
    sleep(randint(10,20))
    avatar_button = bot.find_element(By.XPATH, '//*[@id="avatar-btn"]')
    avatar_button.click()
    sleep(randint(1,4))
    print("Chegou no Youtube")
    alterar_button = bot.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]/a/tp-yt-paper-item')
    alterar_button.click()                      
    sleep(randint(2,6))
    print("Clicou nos botão")

    nick_botao = bot.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer[1]/div[1]/ytd-google-account-header-renderer/div[2]/div[1]/yt-formatted-string')
    if nick_botao.text != channel:
       nick_botão2 = bot.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer[2]/div[2]/ytd-account-item-section-renderer/div[2]/ytd-account-item-renderer/tp-yt-paper-icon-item/tp-yt-paper-item-body/yt-formatted-string[1]')
       if nick_botão2.text == channel:
           nick_botão2.click()
       else:
           nick_botão3 = bot.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer[3]/div[2]/ytd-account-item-section-renderer/div[2]/ytd-account-item-renderer/tp-yt-paper-icon-item/tp-yt-paper-item-body/yt-formatted-string[1]')    
           nick_botão3.click()
    print("Achou o canal")
    sleep(randint(4,6))

    upload_button = bot.find_element(By.XPATH, '//*[@id="create-icon"]')
    upload_button.click()
    sleep(randint(1,5))
    
    sleep(randint(2,4))
    upload_button = bot.find_element(By.XPATH, '//*[@id="text-item-0"]')
    upload_button.click()
    sleep(randint(1,3))

    file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
    abs_path = os.path.abspath(video)
    file_input.send_keys(abs_path)
    sleep(randint(6,10))
    print("Envio o video")

    #Description input
    text_box_input = bot.find_element(By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div")
    description = f"Créditos: Inscreva-se no canal para acompanhar todos os clips. Videos novos todos os dias! ;)\n\nTem algum clip favorito?? Mande o link neste email: queenasheclips@gmail.com\n#leagueoflegends #lol #clips #clipslol #corteslol"
    text_box_input.send_keys(description)
    sleep(randint(10,27))
    
    #Colocou a descrição
    next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
    for i in range(3):
        print(f"Apertou o botão {i+1}")
        next_button.click()
        sleep(i+randint(1,3)*1.777)

    done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
    done_button.click()
    print("Upload do video completado com sucesso!")
    sleep(randint(3,5))
    bot.quit()
    shutil.move(video, "C:/Users/picha/Desktop/Things of the project/Clips postados/")
