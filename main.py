#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import telebot
from googletrans import Translator
from telebot import types
import os

BOT_TOKEN = os.environ(['BOT_TOKEN'])

bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()
actionType = "en"

bot.set_my_commands([
    telebot.types.BotCommand("start", "Start bot"),
    telebot.types.BotCommand("help", "Help"),
    telebot.types.BotCommand("lang_select", "Select a language"),
    telebot.types.BotCommand("lang_detection", "Detect a lnaguage")
])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Hi there i am translator bot! I can translate any text in english.
                Select destination language and just type in or copy past the text you want to translate!\
""", reply_markup= create_menu())
    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
To start translating you can just write anything. By default bot translates everything into english language.
                     If you want to select another language, click on button 'Select a language'
                     If you want to detect what language is text click on button 'Detect a language'\
""")
    
@bot.message_handler(commands=['lang_select'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Select language you want to translate the text to'\
""", reply_markup=create_menu())
    
@bot.message_handler(commands=['lang_detection'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Language detection activated. Type in text to detect what language it is.'\
""")
    global actionType
    actionType = "detect"

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global translator
    if(actionType == 'detect'): 
        detectedLang = translator.detect(message.text)
        bot.reply_to(message, detectedLang)
    else:
        translation = translator.translate(message.text, actionType)
        translatedText = translation.text
        bot.reply_to(message, translatedText)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global actionType
    actionType = call.data

    if(actionType == "ja"): bot.send_message(call.message.chat.id, "Japanese language selected")
    if(actionType == "en"): bot.send_message(call.message.chat.id, "English language selected")
    if(actionType == "de"): bot.send_message(call.message.chat.id, "German language selected")
    if(actionType == "kazakh"): bot.send_message(call.message.chat.id, "Kazakh language selected")
    if(actionType == "detect"): bot.send_message(call.message.chat.id, "Language detection selected")

def create_menu() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("japanese", callback_data="ja")
    btn2 = types.InlineKeyboardButton("english", callback_data="en")
    btn3 = types.InlineKeyboardButton("deutsch", callback_data="de")
    btn4 = types.InlineKeyboardButton("kazakh", callback_data="kk")

    markup.add(btn1, btn2, btn3, btn4)

    return markup


bot.infinity_polling()