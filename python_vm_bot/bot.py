#!/usr/bin/env python
import logging
import traceback


from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown

from cloud_services.yandex_api import list_clouds, list_folders, list_vm, start_vm, stop_vm, restart_vm

from config_reader import read_config_key
from database import check_user, clear_user, set_token, set_folder
from alertmanager import request_log

NOLOGIN_ERROR = 'Please use /start to log in with Yandex Cloud first'
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

chat_id = 'YOUR_CHAT_ID'

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\! This bot will require access to your Yandex Cloud VM deployments\. Please follow {escape_markdown("https://cloud.yandex.com/en-ru/docs/iam/operations/api-key/create", version=2)}, create a new service account with `editor` role and send it here via /settoken\.',
        )

    else:
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\! Yandex Cloud is already set and working on your account\! You can pick a work folder with /listcloud /listfolder \{{cloud\_id\}} and /setfolder \{{folder\_id\}} \.'
        )


def help_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        update.message.reply_text('''
        /settoken {token} - sets your service account token
        /listcloud - shows available clouds to manage
        /listfolder {cloud_id} - shows available folders
        /setfolder {folder_id} - sets folder for your servers
        /listvm - shows available vms
        /startvm {vm_name} - starts a vm by name
        /stopvm {vm_name} - stops a vm by name
        /restartvm {vm_name} - restarts a vm by name
        /help - this list :)
        /reset - resets Yandex Cloud login for this Telegram account
        ''')


def settoken(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    check_user(user.id)
    set_token(user.id, context.args[0])
    request_log(chat_id, 'set_token', 'info', f'Somebody auth with token: {context.args[0]}')
    update.message.reply_text('Your token was updated. Check available folders with /listcloud and /listfolder {cloud_id}')


def setfolder(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        set_folder(user.id, context.args[0])
        update.message.reply_text(fr'Your folder was set to {context.args[0]}. Check available VMs with /listvm')


def listcloud(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        try:
            result = list_clouds(user.id)
            update.message.reply_text(result)
            request_log(chat_id, 'list_clouds', 'info', 'Somebody watch list of cloud')
        except BaseException as e:
            update.message.reply_text(f'Unexpected error {e}')


def listfolder(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        try:
            result = list_folders(user.id, context.args[0])
            update.message.reply_text(result)
        except BaseException as e:
            update.message.reply_text(f'Unexpected error {e}')


def listvm(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        try:
            result = list_vm(user.id)
            update.message.reply_text(result)
            print(result)
            request_log(chat_id, 'list_vm', 'info', 'Somebody watch list of vm')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            update.message.reply_text(f'Unexpected error {e}')


def startvm(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        try:
            result = start_vm(user.id, context.args[0])
            update.message.reply_text(result)
        except BaseException as e:
            update.message.reply_text(f'Unexpected error {e}')


def stopvm(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        try:
            result = stop_vm(user.id, context.args[0])
            update.message.reply_text(result)
        except BaseException as e:
            update.message.reply_text(f'Unexpected error {e}')


def restartvm(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if check_user(user.id):
        update.message.reply_text(NOLOGIN_ERROR)
    else:
        try:
            result = restart_vm(user.id, context.args[0])
            update.message.reply_text(result)
        except BaseException as e:
            update.message.reply_text(f'Unexpected error {e}')


def reset(update: Update, context: CallbackContext) -> None:
    clear_user(update.effective_user.id)
    update.message.reply_text('Your Yandex Cloud authentication was cleared. Use /start to log in again.')


def reply_generic(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please use /help for a list of commands.')


if __name__ == '__main__':
    updater = Updater(read_config_key('telegram_token'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start, run_async=True))
    dispatcher.add_handler(CommandHandler("help", help_command, run_async=True))
    dispatcher.add_handler(CommandHandler("reset", reset, run_async=True))
    dispatcher.add_handler(CommandHandler("settoken", settoken, run_async=True))
    dispatcher.add_handler(CommandHandler("setfolder", setfolder, run_async=True))
    dispatcher.add_handler(CommandHandler("listcloud", listcloud, run_async=True))
    dispatcher.add_handler(CommandHandler("listfolder", listfolder, run_async=True))
    dispatcher.add_handler(CommandHandler("listvm", listvm, run_async=True))
    dispatcher.add_handler(CommandHandler("startvm", startvm, run_async=True))
    dispatcher.add_handler(CommandHandler("stopvm", stopvm, run_async=True))
    dispatcher.add_handler(CommandHandler("restartvm", restartvm, run_async=True))
    #dispatcher.add_handler(CommandHandler("balance", balance, run_async=True))



    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_generic, run_async=True))

    # Start the Bot
    updater.start_polling()

    updater.start_webhook(listen='0.0.0.0',
                      port=8443,
                      url_path='YUOR_URL_PATH',
                      key='/home/alien/Software/git/prometheus_bot/source/python_vm_bot/private.key',
                      cert='/home/alien/Software/git/prometheus_bot/source/python_vm_bot/cert.pem',
                      webhook_url='https://<YOUR_HOST>:8443/YOUR_URL_PATH')

    updater.idle()
