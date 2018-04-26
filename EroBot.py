from telegram import InputMediaPhoto, Update, Bot
from telegram.ext import (Updater, CommandHandler)

from Providers import OBoobsProvider, OButtsProvider, EroticBeautiesProvider, ErolubProvider

from Logger import logger


def error(bot, update: Update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


class EroBot:
    _HELP_MESSAGE = """Welcome to <b>ITD-Eroland bot!</b>
List of commands:
<i>/boobs</i> - returns set of 5 images with boobs
<i>/butts</i> - returns 5 images with boobs (at this moment all images sends separately)
<i>/beauty</i> - returns set of 5 images from www.eroticbeauties.net
<i>/erolub</i> - returns set of 5 images from www.erolub.com/photo/
<i>/help</i> - prints help message"""

    def __init__(self, access_token: str):
        self.updater = Updater(access_token)
        self.boobs_provider = OBoobsProvider()
        self.butts_provider = OButtsProvider()
        self.beauty_provider = EroticBeautiesProvider()
        self.erolub_provider = ErolubProvider()
        self.providers = [self.boobs_provider, self.butts_provider, self.beauty_provider, self.erolub_provider]
        self._init()

    def _init(self):
        handlers = (
            CommandHandler('start', self._start),
            CommandHandler('help', self._help),
            CommandHandler('boobs', self._boobs),
            CommandHandler('butts', self._butts),
            CommandHandler('beauty', self._beauty),
            CommandHandler('erolub', self._erolub)
        )
        for handler in handlers:
            self.updater.dispatcher.add_handler(handler)
        self.updater.dispatcher.add_error_handler(error)

    def _start(self, bot: Bot, update: Update):
        self._help(bot, update)

    def _help(self, bot: Bot, update: Update):
        update.message.reply_text(self._HELP_MESSAGE, quote=False, parse_mode='HTML', disable_web_page_preview=True)

    def _boobs(self, bot: Bot, update: Update):
        media = [InputMediaPhoto(url) for url in self.boobs_provider.get_random_images(5)]
        bot.send_media_group(update.message.chat.id, media, disable_notification=True)

    def _butts(self, bot: Bot, update: Update):
        media = self.butts_provider.get_random_images(5)
        for image in media:
            try:
                bot.send_photo(update.message.chat.id, image, disable_notification=True)
            except Exception as e:
                print(str(e))

        # bot.send_media_group(update.message.chat.id, media, disable_notification=True)

    def _beauty(self, bot: Bot, update: Update):
        update.message.reply_text('It will take some time. So, wait patiently :)', quote=False)
        try:
            media = [InputMediaPhoto(url) for url in self.beauty_provider.get_random_images(5)]
            bot.send_media_group(update.message.chat.id, media, disable_notification=True)
        except Exception as e:
            print(str(e))

    def _erolub(self, bot: Bot, update: Update):
        update.message.reply_text('It will take some time. So, wait patiently :)', quote=False)
        try:
            media = [InputMediaPhoto(url) for url in self.erolub_provider.get_random_images(5)]
            bot.send_media_group(update.message.chat.id, media, disable_notification=True)
        except Exception as e:
            print(str(e))

    def start_bot(self, timeout=120, idle=False):
        self.updater.start_polling(timeout=timeout)
        if idle:
            self.updater.idle()
