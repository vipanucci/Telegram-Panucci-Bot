import json
import telebot
import requests
from os import path
from datetime import datetime

TOKEN = '5979675444:AAEMIfNQJKLgzhbiYW99NJjQx3mbyIHHLks'
bot = telebot.TeleBot(TOKEN)
bot_name = '@Panucci_the_bot'


def command_start(id, first_name):
    text0 = f'Olá, {first_name}, bem-vindo(a) ao Panucci_Bot'\
            '\n\nDono: @duskdusks'
    text1 = f'O que eu posso fazer?'\
             '\n\n/cep para consultar um cep (online)'\
             '\n\nAproveite o bot.'
    bot.send_message(id, text0)
    bot.send_message(id, text1)


def command_cep(cep, id):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(url)
    
    if response.status_code == 200:
        info = response.json()
        bot.send_message(id, f'CEP: {info["cep"]}'\
                             f'\nRua: {info["logradouro"]}'\
                             f'\nBairro: {info["bairro"]}'\
                             f'\nCidade: {info["localidade"]}'\
                             f'\nEstado: {info["uf"]}'\
                             f'\nDDD: {info["ddd"]}'\
                             f'\n{bot_name}')
    else:
        bot.send_message(id, 'CEP inválido, tente novamente.'\
                             '\n\nExemplo: /cep 79290000')


def logs(first_name, username, id, text):
    hour, minute, second = list(str(datetime.now().time()).split(':'))
    year, month, day = list(str(datetime.now().date()).split('-'))
    file = f'logs/@{username}.txt'
    logText = f'{hour}:{minute}:{second[0:2]} | {day}/{month}/{year} | {text}\n'

    if path.exists(file):
        with open(file, 'a', encoding='utf-8') as write:
            write.write(logText)
            write.close()
    else:
        with open(file, 'w+', encoding='utf-8') as create:
            create.write(f'@{username} (ID: {id}) entrou no bot.\n\n')
            create.write(logText)
            create.close()


@bot.message_handler(func=lambda message: True)
def starter(message):
    first_name = message.from_user.first_name
    username = message.from_user.username
    id = message.chat.id
    text = str(message.text).split()
    logs(first_name, username, id, text)

    if text[0].lower() == '/start':
        command_start(id, first_name)
    elif text[0].lower() == '/cep':
        try:
            bot.reply_to(message, f'Consultando o CEP {text[1]}, por favor aguarde.')
            command_cep(text[1], id)
        except:
            bot.reply_to(message, 'CEP inválido, tente novamente.'\
                                  '\n\nExemplo: /cep 79290000')
    else:
        bot.reply_to(message, 'Não entendi o que você escreveu.')


print('O bot está ONLINE.')
bot.polling(non_stop=True, interval=0, timeout=0)
