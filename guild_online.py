import requests
import json


def search_guild(guild_name):
    formatted_guild_name = guild_name.replace(" ", "+")
    #response = requests.get("https://api.tibiadata.com/v2/highscores/firmera/magic/paladin.json")
    response = requests.get("https://api.tibiadata.com/v2/guild/"+formatted_guild_name+".json")
    json_data = response.json()['guild']['members']
    print("=====================================")
    print("<h2>"+response.json()['guild']["data"]["name"]+" "+response.json()["guild"]["data"]["world"]+" online: "+ str(response.json()["guild"]["data"]["online_status"])+"</h2>")
    print(" <h4>Last Updated: "+response.json()["information"]["last_updated"]+"</h4>")
    print("<p line-height: 0.7>")
    print("=====================================<br>")
    print("<table><tr><th>Character</th><th>Vocation</th><th>Level</th></tr>")

    for rank in json_data:
        for member in rank["characters"]:
            if member["status"] == 'online':
                print("""<tr><td><a href="https://www.tibia.com/community/?name="""+member["name"]+'" target="_blank" rel="noopener noreferrer"> '+member["name"]+"</a></td><td>"+member["vocation"]+"</td><td>"+str(member["level"])+"</td></tr>")
                #print("<br>")
    print("</table>")
    print("</p>")
    return response.json()["guild"]["data"]["online_status"]


print("<!DOCTYPE html>")
print("<html>")
print("<body>")
total = 0
total = total + search_guild("Gold Reappers") + search_guild("Diamond Reappers") + search_guild("Reappers") + search_guild("Final Act")
print("=====================================")
print("<h2>Total numbers in all guild: "+str(total)+"</h2>")
print("=====================================")
print("</body>")
print("</html>")
