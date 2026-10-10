import discord

import bot.globals as bg
import bot.response as br
import bot.utils as bu
import scraper.tracker as st


@bg.tree.command(description='Binds the bot to the current channel or thread.')
async def bind(interaction: discord.Interaction):
    try:
        await bu.bindToChannel(interaction.channel)
        await interaction.response.send_message(f"Bound to channel '{interaction.channel.name}' (ID: {interaction.channel.id}) in server '{interaction.guild.name}' (ID: {interaction.guild.id})")
    except Exception as e:
        await interaction.response.send_message(e)


@bg.tree.command(description='Removes a binding of the bot from the current channel or thread.')
async def unbind(interaction: discord.Interaction):
    try:
        await bu.unbindToChannel(interaction.channel)
        await interaction.response.send_message(f"Unbound channel '{interaction.channel.name}' (ID: {interaction.channel.id}) in server '{interaction.guild.name}' (ID: {interaction.guild.id})")
    except Exception as e:
        await interaction.response.send_message(e)



@bg.tree.command(name="today", description="Sends the most recent post.")
async def today(interaction: discord.Interaction):
    try:
        content, image = bu.generateMessageContentAndImage(bg.day)
    except Exception as e:
        print(f"EXCEPTION IN 'today' COMMAND: {e}")
        await interaction.response.send_message("Failed to send today's post. Please contact the bot owner to report this issue.")
    else:
        await br.respondWithPost(interaction, content, image)


@bg.tree.command(name="day", description="Sends a specified post, if it is cached by the bot")
async def day(interaction: discord.Interaction, day: str):
    entry = st.getPostTrackingEntry(day)
    if (not entry):
        await interaction.response.send_message(f"This bot instance has not cached day '{day}'")
        return

    # On paper there shouldn't be a place for this to raise an exception that isn't covered by the above check, but I felt it was probably worth doing this try except just in case
    try:
        content, image = bu.generateMessageContentAndImage(day)
    except Exception as e:
        print(f"EXCEPTION IN 'day' COMMAND: {e}")
        await interaction.response.send_message("Failed to send the requested post. Please contact the bot owner to report this issue.")
    else:
        await br.respondWithPost(interaction, content, image)