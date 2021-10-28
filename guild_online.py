from operator import itemgetter
from dominate.tags import *
import requests, json, os
html = ""

def sort_by_level(json_data):
    some_list = []
    for rank in json_data:
        for member in rank["characters"]:
            if member["status"] == "online":
                some_list.append([member["name"],member["vocation"],member["level"]])
                some_list = sorted(some_list, key=itemgetter(2), reverse=True)
    return some_list

def search_guild(guild_name):
    global html
    formatted_guild_name = guild_name.replace(" ", "+")
    response = requests.get("https://api.tibiadata.com/v2/guild/"+formatted_guild_name+".json")
    json_data = response.json()['guild']['members']
    if response.json()["guild"]["data"]["online_status"] == 0:
        return response.json()["guild"]["data"]["online_status"]
    else:

        html+='<td style="width: 259px; vertical-align:top">\n'
        html+="=====================================\n"
        html+="<h2>"+response.json()["guild"]["data"]["world"]+" online: "+ str(response.json()["guild"]["data"]["online_status"])+"</h2>\n"
        html+=" <h4>Last Updated: "+response.json()["information"]["last_updated"]+"</h4>\n"
        html+="<p line-height: 0.7>\n"
        html+="=====================================<br>"
        html+="<table><tr><th>Character</th><th>Vocation</th><th>Level</th></tr>\n"
        sorted_data = sort_by_level(json_data)
        for member in sorted_data:
            html+="""<tr><td><a href="https://www.tibia.com/community/?name="""+member[0]+'" target="_blank" rel="noopener noreferrer"> '+member[0]+"</a></td><td>"+member[1]+"</td><td>"+str(member[2])+"</td></tr>"
        html+="</table></p></td>"
        return response.json()["guild"]["data"]["online_status"]

html+="<!DOCTYPE html><html>"
html+='<head><meta http-equiv="refresh" content="30"></head>'
html+="<body>"
html+="<center><h1>Reappers</h1></center>"
html+='<table style="border:1px solid black; margin-left:auto;margin-right:auto;"><tr>'
total = 0
total = total + search_guild("Gold Reappers") + search_guild("Diamond Reappers") + search_guild("Reappers") + search_guild("Final Act") + search_guild("Retro Reappers")+search_guild("Reappers Belicos")
html+="</tr></table>"
html+="<center>=====================================</center>"
html+="<center><h2>Total numbers in all guild: "+str(total)+"</h2></center>"
html+="<center>=====================================</center>"
html+="</body>"
html+="</html>"
os.remove("/home/ruslex/Documents/enemy_online.html")
with open("/home/ruslex/Documents/enemy_online.html","w") as myfile:
    myfile.write(html)
