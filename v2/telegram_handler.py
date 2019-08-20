import logging
import telegram

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,\
    MessageHandler, Filters

import threading
from threading import Thread

def discardAllPreviousMessages(bot):
    lastUpdate = bot.get_updates(offset=-1)
    if len(lastUpdate):
        lastUpdate = bot.get_updates(offset=lastUpdate[-1].update_id+1)

class TelHandler:
    # Group Chat
    chat_id = -231826985
    botToken = "773804465:AAGyQZmJiGGBBQ-5M1RXl8FGvLe_q76hGpc"

    def __init__(self):
        self.updater = Updater(token=self.botToken)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('open', self.onCmdOpen))
        self.dispatcher.add_handler(CommandHandler('show', self.onCmdShow))
        self.dispatcher.add_handler(CommandHandler('close', self.onCmdClose))

        self.bot = telegram.Bot(token=self.botToken)

    def _startListening(self):
        self.updater.start_polling()

    def startListening(self):
        discardAllPreviousMessages(self.bot)
        threading.Thread(target=self._startListening).start()
    
    def onCmdShow(self, bot, update):
        self.callbackShow(self)
         
    def setCallbackShow(self, cb):
        self.callbackShow = cb

    def onCmdOpen(self, bot, update):
        self.callbackOpen(self)

    def setCallbackOpen(self, cb):
        self.callbackOpen = cb
    
    def onCmdClose(self, bot, update):
        self.callbackClose(self)

    def setCallbackClose(self, cb):
        self.callbackClose = cb

    def sendPhoto(self, path):
        self.bot.sendPhoto(
        chat_id=self.chat_id, photo=open(path, 'rb'))

    def sendCmdList(self):
        self.bot.send_message(chat_id=self.chat_id,
                     text="For more images /show or \n /open to let the cat in \n /close to close door")
    def notifyOpen(self):
        self.bot.send_message(chat_id=self.chat_id,
                     text="Opening")

    def text(self, t):
        self.bot.send_message(chat_id=self.chat_id, text=t)
