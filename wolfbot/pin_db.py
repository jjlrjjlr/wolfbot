import sqlite3
import settings
import lightbulb
import hikari
from datetime import datetime
import utils
import json

def create_database(bot: lightbulb.BotApp):
    database = sqlite3.connect(bot.d.settings.get_save_database_file())
    curser = database.cursor()
    curser.execute(
        '''CREATE TABLE pins(
            message_id INTEGER PRIMARY KEY,
            message_content TEXT,
            author_id INTEGER,
            author TEXT,
            avatar_hash TEXT,
            avatar_url TEXT,
            avatar_file TEXT,
            date_posted INTEGER,
            date_saved INTEGER,
            attached_files TEXT,
            attachment_urls TEXT)'''
    )
    database.commit()
    database.close()

def save_to_database(
    bot: lightbulb.BotApp,
    message: hikari.messages.Message):
    database = sqlite3.connect(bot.d.settings.get_save_database_file())
    curser = database.cursor()
    attachments = []
    curser.execute(
        '''INSERT OR IGNORE INTO pins(
            message_id,
            message_content,
            author_id,
            author,
            avatar_hash,
            avatar_url,
            avatar_file,
            date_posted,
            date_saved,
            attached_files,
            attachment_urls)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
            (
                message.id,
                message.content,
                message.author.id,
                message.author.username,
                message.author.avatar_hash,
                message.author.avatar_url.url,
                utils.save_file('./avatars/', ''.join([str(message.author.id), '_', message.author.avatar_hash, '.', message.author.avatar_url.extension]), message.author.avatar_url),
                message.timestamp,
                datetime.now(),
                get_attachments(message.attachments),
                get_attachment_urls(message.attachments)
            )
        )
    database.commit()
    database.close()

def get_attachments(attachments: []) -> str:
    if len(attachments) > 0:
        path_list = []
        for attachment in attachments:
            path_list.append(utils.save_file('./attachments/', ''.join([str(attachment.id), '_', attachment.filename]), attachment.url))
        return json.dumps(path_list)

def get_attachment_urls(attachments: []) -> str:
    if len(attachments) > 0:
        urls = []
        for attachment in attachments:
            urls.append(attachment.url)
        return json.dumps(urls)