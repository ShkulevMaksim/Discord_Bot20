import openai
import os
from discord.ext import commands
import discord
import fileProcessing
from discord.ui import View, Button
from discord import app_commands

from base64 import b64decode

steel_guild_id = "486150910473535499"
AI_TOKEN = os.getenv('CHATGPT_TOKEN')

openai.api_key =AI_TOKEN

config = fileProcessing.read_config()
roles = config["roles"]

# messages_history=[]

class chatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    @commands.command(name='gpt',aliases=['Пудж', 'пудж', 'Пудж,'],description = "ChatGPT")
    @commands.has_any_role(*roles)
    async def gpt(self, ctx, *, query: str): 
    
        # messages_history.append({"role": "user", "content": query})
        async with ctx.typing(): 
            embed = discord.Embed(color=discord.Color.blurple()) 
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
            # messages=messages_history
            )          
            embed.title = 'Пудж поясняет:'

            embed.description = completion.choices[0].message.content
            # messages_history.append({"role": "assistant", "content": completion.choices[0].message.content})
             
        await ctx.send(embed=embed)
        
            
    @commands.command(name="talk")
    async def start_conversation(self, ctx):
        message = await ctx.send("Давай поговорим в ветке")
        await message.create_thread(name="Вопросы?", auto_archive_duration=60)
        

    @commands.command(name="clear_history", aliases=['end', 'все', 'Все'])
    async def clear_messges_history(self, ctx):
        messages_history.clear
        await ctx.send("История разговора очищенна")

    @commands.command(name='img',description = "Генерирует 4 изображения но основе текста")
    @commands.has_any_role(*roles)
    async def image(self, ctx, *, query: str, num=1, m_size="256x256"):   
        if num >4:
            await ctx.send("Слишком много изображений")
        else:
            async with ctx.typing(): 

                response = openai.Image.create(
                prompt=query,
                n=num,
                size=m_size,
                )      
                embed_list =[]

                for i in response["data"]:
                    embed = discord.Embed(color=discord.Color.blurple()) 
                    embed.set_image(url = i["url"])
                    embed_list.append(embed)
                view = discord.ui.View() # Establish an instance of the discord.ui.View class
                style = discord.ButtonStyle.gray  # The button will be gray in color
                
                for i in range (num):
                    item = discord.ui.Button(style=style, label="Regenerate " + str(i))  # Create an item to pass into the view class.
                    view.add_item(item=item)
             

        await ctx.send(embeds=embed_list,view = view)
          

async def setup(bot):
    await bot.add_cog(chatGPT(bot))
