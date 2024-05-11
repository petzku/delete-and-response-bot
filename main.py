#!/usr/bin/env python3

import discord
import re

# secret config
from config import TOKEN, ADMIN_ROLES, CHANNELS, LOG_CHANNELS

# non-secret config
from config import DELETION_DELAY, DELETION_RESPONSE, LOG_MESSAGE


LINK_REGEX = re.compile(
    r"(\b(https?)://[-A-Z0-9+&@#/%?=~_|!:,.;]*[-A-Z0-9+&@#/%=~_|])", re.IGNORECASE
)


intents = discord.Intents.default()
intents.message_content = True


def _has_link(message: discord.Message) -> bool:
    return LINK_REGEX.search(message.content) is not None


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # only act in specified channels
        if message.channel.id not in CHANNELS:
            return

        # ignore server admins
        for role in message.author.roles:
            if role.id in ADMIN_ROLES:
                return

        # delete messages without attachments in moderated channels
        # and give the user a slap on the wrist
        if not message.attachments and not _has_link(message):
            await self.warn_and_delete(message, message.author, DELETION_RESPONSE)
            await message.delete()
            if message.channel.id in LOG_CHANNELS:
                tgt = message.guild.get_channel(LOG_CHANNELS[message.channel.id])
                log_embed = discord.Embed()
                log_embed.set_author(
                    name=message.author.name, icon_url=message.author.avatar.url
                )
                log_embed.add_field(name="Message", value=message.content)
                await tgt.send(
                    LOG_MESSAGE.format(
                        user=f"<@{message.author.id}>",
                        channel=f"<#{message.channel.id}>",
                    ),
                    embed=log_embed,
                )

    async def warn_and_delete(
        self, target: discord.Message, user: discord.User, response: str
    ):
        print(f"Warning user {user.name} in {target.channel.name}: {response}")
        await target.reply(response, delete_after=DELETION_DELAY)


if __name__ == "__main__":
    client = MyClient(intents=intents)
    client.run(TOKEN)
