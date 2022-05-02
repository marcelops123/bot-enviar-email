from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import pyautogui
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from PySimpleGUI import PySimpleGUI as sg
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
import os
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email import encoders
import pygame
sg.theme('BrightColors')
layout = [
    [sg.Text('Seu Email:'), sg.Input(key='emailuser', size=(64, 1))],
    [sg.Text('Sua Senha:'), sg.Input(
        key='senhauser', password_char='*', size=(63, 1))],
    [sg.Text('Email do destinatário:'), sg.Input(
        key='remetenteuser', size=(55, 1))],
    [sg.Text('Digite a mensagem que deseja enviar:'),
     sg.Input(key='mensagem', size=(42, 1))],
    [sg.Button('Entrar')]

]

janela = sg.Window('Enviar Email Automático(sem bloqueio google)', layout)
while True:
    eventos, valores = janela.read()
    if eventos == sg.WIN_CLOSED:
        break

    if eventos == 'Entrar':

        pygame.init()
        pygame.mixer.music.load('In The End.mp3')
        pygame.mixer.music.play()
        pygame.event.wait()
        # Entra no site da cnn e tira print da manchete
        driver = uc.Chrome(use_subprocess=True)
        driver.maximize_window()
        driver.get('https://www.cnnbrasil.com.br/')
        clicar_manchete = driver.find_element(
            by=By.XPATH, value='/html/body/div[3]/div/main/section[1]/ul/li[1]')
        clicar_manchete.click()
        salvar_print = driver.save_screenshot('print.png')

        # Fazendo Login no Email

        EMAIL_ADDRESS = (valores['emailuser'])
        EMAIL_PASSWORD = (valores['senhauser'])

        # Montando o email
        msg = MIMEMultipart()
        msg['Subject'] = 'Mensagem automática'
        msg['From'] = (valores['emailuser'])
        msg['To'] = (valores['remetenteuser'])
        msg.attach(MIMEText(valores['mensagem']))

        # caminho do print
        cam_arquivo = ("C:\Bot Email Automatico nd\print.png")
        attachment = open(cam_arquivo, 'rb')

        # Transforma o print em BASE64
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att)

        # Envia o email
        att.add_header('Content-Disposition',
                       f'attachment; filename= print.png')
        attachment.close()
        msg.attach(att)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            driver.get('https://tela-email-enviado.vercel.app/')
            time.sleep(3)
            driver.close()
            pygame.quit()
