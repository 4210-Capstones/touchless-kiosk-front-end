import discord
from datetime import datetime

from classes.datetime_manager import DTManager as dtm


class AvailabilityUI(discord.ui.View):
    def __init__(self, date: str):
        super().__init__()
        self.date: str = date
        self.date_dt: datetime = dtm.string_to_datetime(date, False)
        self.embed = discord.Embed(
            title=f"Availability Chart: {self.date_dt.strftime('%B %d, %Y')}",
            color=discord.Color.yellow()
        )

    def get_embed(self):
        return self.embed
    
    def set_embed(self, schedule1: str, schedule2: str):
        self.embed.clear_fields()
        self.embed.add_field(name="", value=schedule1, inline=False)
        self.embed.add_field(name="", value=schedule2, inline=False)


    def availability_to_embed(self, availability_slots: list):
        schedule1: str = ""
        schedule2: str = ""

        for i in range(len(availability_slots)):
            if i % 12 == 0:
                if i < 24:
                    schedule1 += ("—" * 21)
                    schedule1 += "\n"
                else:
                    schedule2 += ("—" * 21)
                    schedule2 += "\n"

                if i == 0:
                    suffix = "<:am:1309573725296787456>"
                    schedule1 += f"<:twelve:1309573684645593098>{suffix} :one:{suffix} :two:{suffix} :three:{suffix} :four:{suffix} :five:{suffix}\n"
                elif i == 12:
                    suffix = "<:am:1309573725296787456>"
                    schedule1 += f":six:{suffix} :seven:{suffix} :eight:{suffix} :nine:{suffix} :number_10:{suffix} <:eleven:1309573626626052231>{suffix}\n"
                elif i == 24:
                    suffix = "<:pm:1309573767202078791>"
                    schedule2 += f"<:twelve:1309573684645593098>{suffix} :one:{suffix} :two:{suffix} :three:{suffix} :four:{suffix} :five:{suffix}\n"
                elif i == 36:
                    suffix = "<:pm:1309573767202078791>"
                    schedule2 += f":six:{suffix} :seven:{suffix} :eight:{suffix} :nine:{suffix} :number_10:{suffix} <:eleven:1309573626626052231>{suffix}\n"

            if i < 24:
                schedule1 += ":green_square:" if availability_slots[i] == 0 else ":red_square:"
            else:
                schedule2 += ":green_square:" if availability_slots[i] == 0 else ":red_square:"

            if (i % 12) % 2 == 1:
                if i < 24:
                    schedule1 += " "
                else:
                    schedule2 += " "

            if i % 12 == 11:
                if i < 24:
                    schedule1 += "\n"
                else:
                    schedule2 += "\n"
        
        self.set_embed(schedule1, schedule2)