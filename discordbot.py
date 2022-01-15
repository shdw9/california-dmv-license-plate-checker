from discord.ext import commands
from requests.structures import CaseInsensitiveDict
import discord, asyncio, datetime, requests

bot = commands.Bot(command_prefix='!')

# UPDATE LINE 20, GET YOUR OWN COOKIES 

url = "https://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do"

headers = CaseInsensitiveDict()
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
headers["Accept-Language"] = "en-US,en;q=0.5"
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Origin"] = "https://www.dmv.ca.gov"
headers["Connection"] = "keep-alive"
headers["Referer"] = "https://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do"
headers["Cookie"] = "_ga=GA1.2.2128232942.1623958651; _abck=F2B02BB5ECB745DB068626215DAFDC4C~-1~YAAQxdscuLML+LN9AQAAGaSBWgeqzixbVME5Wez78EOy5+fzX3mPFrVoQBE4U0iIYvjVTVm8NrSQmneCPXrYH5BUXBRv7pYclBvymkHNkv53/gJO9911rn7I+SOPE6h0K4SteMGnVDqWPfP1tm/GUePjF2iiqozQNpVyOL8mInrwaqeeZ1OFtLoI8FLLsrKlk02gEAEo/onQlZVRKg8+iq3dj2P3BBgEq62/iZk4bvdjxidZMSLWRLRbhdZ7N8CsmQ8g03u8Z7SngObCcnCyh/ysQQSc8AQqHnK4BrEN2w7kJkJl+/49eKg2LVuqU8YzGXQme70fARvmMhPGY35ZVb46eo5ETkXEDhQnl51XyQjUjBy24nu+/wt92GptFNMNndZeGQ2aYhnKngSWm/k6CW1feP8AjA==~-1~-1~-1; PD_STATEFUL_0531fc7e-9a22-11ea-bf4d-fa163e384dc6=%2Fportal; TS013cb4be=01da805aaf25df787ca52266369a7d6d2495d8fc5258ab9749e86b900b83137a1cdbbb424a15dcb2b5f9f58a9c7854d0379051601732478034753f22c841b6d2a4275b3d229ba9b287a6466d1b0cf7a0f04451cd15; TS013cb4be028=018c127eb82084bf4c43191ace059911dc88cdc78d80c95f00182ab2ec8dd6e2853ba68d8289a123f7fb00f4412ee39d8b0bdf72c8; JSESSIONID=0000fiqPGm1OdNcLqudpB_ypKYm:18u4e7n8r; PD_STATEFUL_00bcef52-0c5a-11e4-98a1-a224e2a50102=%2Fwasapp; AWSALB=i7uNIoI3KT1aowBGz0vDCngk65EhUvvovlwdeKzPb0k10483d3MUHVooNDoa8Ddjy0aGlYItuQUNnYy+RcDI+9WSxSnx+VSFdh+9i+4xH6WhI/vQJS0/JCkTZ1Wk; AWSALBCORS=i7uNIoI3KT1aowBGz0vDCngk65EhUvvovlwdeKzPb0k10483d3MUHVooNDoa8Ddjy0aGlYItuQUNnYy+RcDI+9WSxSnx+VSFdh+9i+4xH6WhI/vQJS0/JCkTZ1Wk; mdLogger=false; kampyleUserSession=1642233506494; kampyleSessionPageCounter=1; kampyleUserSessionsCount=5; iv_user=unauthorized; kampyleUserPercentile=16.998329209678044"
headers["Upgrade-Insecure-Requests"] = "1"
headers["Sec-Fetch-Dest"] = "document"
headers["Sec-Fetch-Mode"] = "navigate"
headers["Sec-Fetch-Site"] = "same-origin"
headers["Sec-Fetch-User"] = "?1"
headers["Sec-GPC"] = "1"
headers["TE"] = "trailers"

async def processInput(plate):
    data = "kidsPlate=&plateType=Z&plateLength=7&plateNameLow=1960+legacy"
    for letter in range(len(plate)):
        data += "&plateChar" + str(letter) + "=" + plate[letter]
    if (len(plate) != 7):
        for letter in range(7-len(plate)):
            data += "&plateChar" + str(letter + len(plate)) + "="
    return data

async def getImage(plate):
    url = "https://www.dmv.ca.gov/wasapp/ipp2/showPlateImage.do?backGroundCode=Z"
    for letter in range(len(plate)):
        url += "&imageFile=" + plate[letter]
    if (len(plate) != 7):
        for letter in range(7-len(plate)):
            url+= "&imageFile="
    url += "&kidsPlate="
    print(url)
    return url

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CALIFORNIA DMV"))
    print('=> Logged in as {0.user}'.format(bot))

@bot.command()
async def check(ctx, arg):
    arg = arg.upper()
    if (len(arg) < 8):
        resp = requests.post(url, headers=headers, data=await processInput(arg))
        if "The license plate number you have selected is no longer available. Please try another plate number" in resp.text:
            print("License plate " + arg + " is taken!")
            await ctx.reply(":x: " + arg + " is already taken!")
            await ctx.message.add_reaction('❌')
        elif "You must agree" in resp.text:
            print("BAD COOKIES")
            await ctx.reply("An internal error occured!")
        else:
            print("License plate " + arg + " is NOT taken!")
            embed=discord.Embed(title=arg + " is available!",description="The license plate " + arg + " is available! [Order " + arg + "? ](https://www.dmv.ca.gov/portal/vehicle-registration/license-plates-decals-and-placards/california-license-plates/order-special-interest-and-personalized-license-plates/)",timestamp=datetime.datetime.utcnow(), color=0x62C979)
            embed.set_author(name="shdw's DMV - License Plate Checker")
            embed.set_thumbnail(url=await getImage(arg))
            embed.set_footer(text="powered by shdw 👻")
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('✅')
    else:
        await ctx.reply("License plates must be less than 8 characters!")

async def background_task():
    await bot.wait_until_ready()

    while(True): #refresh cookies
        resp = requests.post(url, headers=headers, data="kidsPlate=&plateType=Z&plateLength=7&plateNameLow=1960+legacy&plateChar0=&plateChar1=K&plateChar2=V&plateChar3=&plateChar4=&plateChar5=&plateChar6=")
        await asyncio.sleep(10)

bot.loop.create_task(background_task())

bot.run('TOKEN')
