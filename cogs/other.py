"""
MIT License

Copyright (c) 2020 - µYert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import colorsys
from datetime import datetime
from io import BytesIO
import random
from typing import Union

from discord.ext import commands
from discord import Colour, Embed, File
from PIL import Image

from main import NewCtx
from utils.formatters import BetterEmbed

random.seed(datetime.utcnow())


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dice', aliases=['d'])
    async def _dice(self, ctx: NewCtx, dice: str = '1d6'):
        """Generates dice with the supplied format `NdN`"""
        dice_list = dice.lower().split('d')
        try:
            d_count, d_value = int(dice_list[0]), int(dice_list[1])
        except ValueError:
            raise commands.BadArgument("The entered format was incorrect, `NdN` only currently")

        counter = []
        crit_s, crit_f = 0, 0
        if d_count < 0 or d_value < 0:
            raise commands.BadArgument("You cannot have negative values")
        for dice_num in range(d_count):
            randomnum = random.randint(1, d_value)
            if randomnum == d_value:
                crit_s += 1
            if randomnum == 1:
                crit_f += 1
            counter.append(randomnum)

        total = sum(counter)

        embed = BetterEmbed()
        embed.description = f"{dice} gave {', '.join([str(die) for die in counter])} = {total} with {crit_s} crit successes and {crit_f} fails"

        await ctx.send(embed=embed)

    @commands.group(name='random', invoke_without_command=False)
    async def _random(self, ctx):

        pass

    @_random.command(name='number', aliases=['num'])
    async def _rand_num(self, ctx: NewCtx, start: Union[int, float] = 0, stop: Union[int, float] = 100):
        """Generates a random number from start to stop inclusive, if either is a float, number will be float"""

        if isinstance(start, float) or isinstance(stop, float):
            number = random.uniform(start, stop)
        else:
            number = random.randint(start, stop)

        embed = BetterEmbed()
        embed.description = f"Number between **{start}** and **{stop}**\n{number}"

        await ctx.send(embed=embed)

    @_random.command(name='colour')
    async def _rand_colour(self, ctx: NewCtx):
        """Generates a random colour, displaying its representation in Hex, RGB and HSV values"""
        col = Colour.from_rgb(*[random.randint(0, 255) for _ in range(3)])
        hex_v = hex(col.value).replace('0x', '#')

        r, g, b = col.r, col.g, col.b
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        h = round((h * 360))
        s = round((s * 100))
        v = round((h * 100))

        image_obj = Image.new('RGB', (125, 125), (r, g, b))
        new_obj = BytesIO()
        image_obj.save(new_obj, format='png')
        new_obj.seek(0)
        fileout = File(new_obj, filename='file.png')

        embed = Embed(colour=col, title='`Random colour: `')
        embed.description = f'Hex : {hex_v} / {hex(col.value)}\nRGB : {r}, {g}, {b}\nHSV : {h}, {s}, {v//1000}'
        embed.set_image(url="attachment://file.png")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed, file=fileout)


def setup(bot):
    """Cog entry point"""
    bot.add_cog(Other(bot))
