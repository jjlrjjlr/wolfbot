import json
from typing import Union
from os import path

class Settings:
    def __init__(self):
        self._settings = {
            'default': {
                'save_database': './message_database.db',
                'save_channel': None,
                'admin_role': None
            }
        }
        if not path.exists('./settings.json'):
            self.write_settings()
        self.read_settings()

    def get_save_database_file(self, guild_id='default'):
        return self._settings[str(guild_id)].get('save_database', ''.join(['./db/', guild_id, '_messages.db']))

    def set_save_database_file(self, guild_id: Union[str, int], save_file: str):
        self.verify_guild_key(str(guild_id))
        self._settings[str(guild_id)]['save_database'] = save_file
        self.write_settings()

    def get_save_channel(self, guild_id: Union[str, int]) -> int:
        return self._settings[str(guild_id)].get('save_channel')

    def set_save_channel(self, guild_id: str | int, channel_id: Union[str, int]):
        self.verify_guild_key(str(guild_id))
        self._settings[str(guild_id)]['save_channel'] = channel_id
        self.write_settings()

    def write_settings(self):
        with open('./settings.json', 'w') as settings_file:
            settings_file.write(json.dumps(self._settings, indent=4))

    def read_settings(self):
        with open('./settings.json', 'r') as settings_file:
            self._settings.update(json.load(settings_file))
    
    def verify_guild_key(self, key: str) -> None:
        if key not in self._settings.keys():
            self._settings[key] = {}