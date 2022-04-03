from operator import itemgetter
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
import re
import unicodedata
import asyncio
import aiohttp
import os
import time
import boto3
# To work with the .env file
from dotenv import load_dotenv
load_dotenv()
html = ""
commanders=[
    "Mudin Hazered",
    "Frozen Thug",
    "Emperor Hazered",
    "Pess Joeru",
    "Lady Hermionee",
    "Deniel Villa",
    "Frozen Camisadez",
    "Chicken Bacon Onion",
    "Tona Mentado",
    "Nina Goodenough",
    "Anferz villa",
    "Dereck Goodenouugh",
    "Manferz",
    "Mikeilita",
    "Demonique",
    "Mirricuh",
    "Beadu",
    "Masonw",
    "Mason Modo Zen",
    "Masxn",
    "Sutaw",
    "Suta",
    "Suta Belico",
    "Suta Chiflado",
    "Suta Mal",
    "Invictus Frozen",
    "Mudin Darksoul",
    "Kuba Powtorka Zrozrywki",
    "Bossy Blonde",
    "Taina Rush",
    "Nimbuz Prime",
    "Nimbuz Powtorka Zrozrywki",
    "Omar Infalible",
    "Omar Vlaze",
    "Ryno Infalible",
    "Rynoz Infalible",
    "Diex Gera",
    "Gera",
    "Gera Belico",
    "Gera Pro Sio",
    "Tuf Before",
    "Anferz Insane",
    "Manferz",
    "Anferz Insane",
    "Diex Torridzin",
    "Ancorsz",
    "Hippopotabner",
    "Ancor",
    "Tank Ferz"
    ]


whole_list = {}
total = {}
main = {}
maker = {}

#api_key = os.getenv('ALPHAVANTAGE_API_KEY')
url ="https://www.tibia.com/community/?subtopic=guilds&page=view&GuildName={}"
guilds= ['Seanarchy','Resilience','Vendetta','Loyalty','Winterians','Army Enterprise','Army Airdrop','Warguild Fallens','Eternity','Bastex Alliance','Bastex']
#','Fallens', 'Eternity','Army Enterprise','Bastex']
#friend_guilds = ['Dinastia Alliance','Dinastia de Perrones','Flameborn','Army Airdrop','Fallens', 'Eternity','True Hope Emera', 'Push Back']
guilds_web = []
for each in guilds:
    guilds_web.append(each.replace(" ","+"))
results = []

start = time.time()

def get_tasks(session):
    tasks = []
    for guild in guilds_web:
        tasks.append(asyncio.create_task(session.get(url.format(guild), ssl=False)))
    return tasks

async def get_symbols():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            global total
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "lxml")
            soup = unicodedata.normalize("NFKD",soup.text)
            guild_name = re.search("Players Online(.|\n)*Guild Information",soup).group(0).splitlines()[12]
            server = re.search("The guild was founded on (.*) on",soup).group(1)
            text =  re.search(".*Joining DateStatus(.|\n)*Invited Characters",soup).group(0).splitlines()
            if 'leadership of this guild' in text[-3]:
                if 'offline' in text[-3]:
                    text[-3]='offline'
                else:
                    text[-3]='online'
                text.pop()
            text = text[1:-1]
            def divide_chunks(l, n):
                for i in range(0, len(l), n): 
                    yield l[i:i + n]
            n = 5
            x = list(divide_chunks(text, n))
            if server not in whole_list:
                whole_list[server] = []
            if server in total:
                total[server]= total[server] + int(len(x))
            else:
                total[server]= int(len(x))
            for each in x:
                if "online" in each[4]:
                    whole_list[server].append([each[0],each[1],each[2],guild_name])

def sort_and_html(lista):
    global html
    global total
    html+="<!DOCTYPE html><html>"
    html+='<head>'
    html+='<meta http-equiv="refresh" content="10">'
    html+='<style>body {color: #eee;background-color:#2f3136;}a{color: #f4861c;} h1, h2, h3 { margin: 0; }</style>'
    html+='</head>'
    html+="<body>"
    html+="<center><h1>Allied Guilds</h1></center>"
    now = datetime.now()
    html+=" <center><h4>Last Updated: "+now.strftime("%m/%d/%Y %H:%M:%S")+"</h4></center>\n"
    html+='<table style="border:1px solid black; margin-left:auto;margin-right:auto;"><tr>'
    for server in lista:
        some_list = []
        if len(lista[server]) > 1:
            main = 0
            maker = 0
            for cada_lista in lista[server]:
                if int(cada_lista[2]) > 249:
                    main += 1
                else:
                    maker += 1
                some_list.append([cada_lista[0],cada_lista[1],int(cada_lista[2]),cada_lista[3]])
                some_list = sorted(some_list, key=itemgetter(1,2), reverse=True)
            html+='<td style="width: 259px; vertical-align:top">\n'
            html+="============================\n"
            html+="<center><h2>"+server+': <span style="color:#40E0D0">'+ str(len(lista[server]))+"</span>/"+str(total[server])+"</h2></center>\n"
            html+="<center><h2>Main: "+str(main)+"</h2></center>\n"
            html+="<center><h2>Maker: "+str(maker)+"</h2></center>\n"
            html+="<p line-height: 0.2>\n"
            html+="============================<br>"
            html+="<table>"
            color = "white"
            voc = "none"
            player = ""
            for member in some_list:
                if voc != member[1]:
                    html+='<tr><td colspan="2"><center><h3>'+member[1]+"</center></h3></td></tr>"
                    voc = member[1]
                if member[0] not in commanders:
                    player = member[0]
                else:
                    player='<mark>'+member[0]+"</mark>"
                if member[2] > 249:
                    color = "#FFFFFF"
                else:
                    color = "#40E0D0"
                html+='<tr><td><font color="'+color+'">['+str(member[2])+']</font></td><td><a href="https://www.tibia.com/community/?name='+member[0]+'" target="_blank" rel="noopener noreferrer"> '+player+'</a></td></tr>'
            html+="</table></p></td>"
    html+="</tr></table>"
    html+="<center>=====================================</center>"
    html+="<center>=====================================</center>"
    html+="</body>"
    html+="</html>"



asyncio.run(get_symbols())

sort_and_html(whole_list)


#file = open("sample.html","w")
#file.write(html)
#file.close()

bucket_name = "jokindude"
file_name = "Butterfingers_online.html"
my_acl = "public-read"
content_type = "text/html"
s3 = boto3.resource('s3')
object = s3.Object(bucket_name,file_name)
object.put(Body=html, ACL=my_acl, ContentType=content_type)

html=""



end = time.time()
total_time = end - start
print("It took {} seconds to make {} API calls".format(total_time, len(guilds)))
print('You did it!')
