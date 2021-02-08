#!/usr/bin/env python3

import discord

# secret config
from config import TOKEN, ADMIN_ROLES, CHANNELS
# non-secret config
from config import DELETION_DELAY, DELETION_RESPONSE


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
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
        if not message.attachments:
            await message.delete()
            await self.warn_and_delete(message.channel, message.author, DELETION_RESPONSE)

    async def warn_and_delete(self, channel, user, response):
        print('Warning user {:s}: {:s}'.format(user.name, response))
        response = response.replace("@user", "<@{:d}>".format(user.id))
        await channel.send(response, delete_after=DELETION_DELAY)


if __name__ == "__main__":
    client = MyClient()
    client.run(TOKEN)
