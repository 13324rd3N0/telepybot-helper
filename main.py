# -*- coding: utf-8 -*-

import os
import subprocess
import configparser
from telegram.ext import Updater, CommandHandler


config = configparser.ConfigParser()
config.read('bot.cfg')

def parse_command(line):
    return line.split(' ', maxsplit=1)[1]


def help_(bot, update):
    help_line = """show - аналог ls
execute - выполнить скрипт
download - скачать файл
Примеры:
"/show /usr/local/bin"
"/execute date"
"/download /etc/fstab"
"""
    bot.sendMessage(chat_id=update.message.chat_id, text=help_line)


def show(bot, update):
    line = parse_command(update.message.text)
    try:
        dirs = os.listdir(line)
        bot.sendMessage(chat_id=update.message.chat_id, text="\n".join(dirs))
    except:
        bot.sendMessage(chat_id=update.message.chat_id, text='Что-то пошло не так, введите валидный путь.')
    return None


def download(bot, update):
    document = parse_command(update.message.text)
    f = open(document, 'rb')
    try:
        bot.sendDocument(chat_id=update.message.chat_id, document=f)
    except:
        bot.sendMessage(chat_id=update.message.chat_id, text='Что-то пошло не так, введите валидный путь до файла.')
    f.close()


def execute(bot, update):
    command = parse_command(update.message.text)
    bot.sendMessage(chat_id=update.message.chat_id, text='Начинаем выполнять команду {0}\nresult:'.format(command))
    try:
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = result.stdout.read().decode('utf-8')
    except:
        bot.sendMessage(chat_id=update.message.chat_id, text='Что-то пошло не так.')
    bot.sendMessage(chat_id=update.message.chat_id, text='{0}'.format(result))


updater = Updater(token=config['KEYS']['TOKEN'])

updater.dispatcher.add_handler(CommandHandler('show', show))
updater.dispatcher.add_handler(CommandHandler('help', help_))
updater.dispatcher.add_handler(CommandHandler('execute', execute))
updater.dispatcher.add_handler(CommandHandler('download', download))


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()