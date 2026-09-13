import discord

import bot.globals as bg
import bot.response as br
import bot.utils as bu
import scraper.tracker as st


@bg.tree.command(description='Binds the bot to the current channel or thread.')
async def bind(interaction: discord.Interaction):
    flag = await bu.bindToChannel(interaction.channel)
    if (flag == 0):
        await interaction.response.send_message(f"Bound to channel '{interaction.channel.name}' (ID: {interaction.channel.id}) in server '{interaction.guild.name}' (ID: {interaction.guild.id})")
    else:
        await interaction.response.send_message(f"Already bound to channel '{interaction.channel.name}' (ID: {interaction.channel.id}) in server '{interaction.guild.name}' (ID: {interaction.guild.id})")


@bg.tree.command(name="today", description="Sends the most recent post.")
async def today(interaction: discord.Interaction):
    content, image = bu.generateMessageContent(bg.day)
    await br.respondWithPost(interaction, content, image)


@bg.tree.command(name="day", description="Sends a specified post, if it is cached by the bot")
async def day(interaction: discord.Interaction, day: str):
    entry = st.getPostTrackingEntry(day)
    if (not entry):
        await interaction.response.send_message(f"This bot instance has not cached day '{day}'")
        return
    
    content, image = bu.generateMessageContent(day)
    await br.respondWithPost(interaction, content, image)