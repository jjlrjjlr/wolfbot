# Description: Object to represent a pin to be saved to database.
# ----------------------------------------------------------------
from discord import Embed, Colour

class Pin:
    def __init__(self, creator_name, creator_id, date, message, message_id):
        self.creator_name = creator_name
        self.creator_id = creator_id
        self.date = date
        self.message = message
        self.message_id = message_id

    def get_embed(self):
        self.__embed = Embed(
            title='',
            color=Colour.blue(),
            description=self.message
            )
        self.__embed.add_field(name='Original ID', value=self.message_id)
        self.__embed.add_field(name='Pinned:', value=self.date)
        self.__embed.author(name=self.creator_name)
        return self.__embed
        