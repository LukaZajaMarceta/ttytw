#!/usr/bin/python3

import json
import urllib.request
import os
import sys
import configparser



config = configparser.ConfigParser()
config.read("config.ini")


def strumz():
    EndMessage = config.get("MYCFG", "EndMessage")
    DisplayedStreams = config.get("MYCFG", "DisplayedStreams")
    StreamQuality = config.get("MYCFG", "StreamQuality")
    streams = urllib.request.urlopen("https://api.twitch.tv/kraken/streams?limit=99").read()
    data = json.loads(streams.decode())["streams"]
    link_list= []
    count=1
    if config.has_option("MYCFG", "blacklisted"):
        for s in data:
            if s["game"] not in config["MYCFG"]["Blacklisted"].split("!"):
                link_list.append(s["channel"]["url"])
                print (str(count), s["channel"]["display_name"], s["channel"]["url"], s["game"], s["channel"]["status"],       sep="  ***  ")
                count += 1
            if count > int(DisplayedStreams):
                break
    elif config.has_option("MYCFG", "whitelisted"):
        for s in data:
            if s["game"] in config["MYCFG"]["Whitelisted"].split("!"):
                link_list.append(s["channel"]["url"])
                print (str(count), s["channel"]["display_name"], s["channel"]["url"], s["game"], s["channel"]["status"],       sep="  ***  ")
                count += 1
            if count > int(DisplayedStreams):
                break            
    else:
        for s in data:
            link_list.append(s["channel"]["url"])
            print (str(count), s["channel"]["display_name"], s["channel"]["url"], s["game"], s["channel"]["status"],       sep="  ***  ")
            count += 1
            if count >= int(DisplayedStreams):
                break            
    print("******")
    print(EndMessage)
    choice = input("your stream of choice sir?  ")
    if choice == "exit!":
        print("Good luck in your future endevours!")
        sys.exit()
    elif choice.isdigit():
        os.system("livestreamer " + link_list[int(choice)-1] + " best")
        strumz()
    elif choice == "cfg!":
        print("*****")
        cfg()
    else:
        os.system("livestreamer twitch.tv/" + choice + " best")
        strumz()

def cfg():
    print("1 x -> change the number of top streams parsed to x(25-99)")
    print("2 y -> change endmessage to y (leave blank to remove)")
    print("if you want blacklist/whitelist: in commands bellow use twitch game names, blacklist/whitelist is mutually exclusive, if you pick one the other one is deleted")
    print("3 game1!game2!game3 -> add/(remove if already in) games to blacklist")
    print("4 game1!game2!game3 -> add(remove if already in) games to whitelist")
    print("5 z-> change to z quality as default(audio, high, low, medium, mobile, worst, source, best)")
    print("6 -> to change all settings back to default")
    print("7 -> list streams")
    print("exit! -> exit program")
    cfg_choice = input("what do? ")
    if cfg_choice[0] == "1":
        number = cfg_choice[1:]
        if 24<int(number)<100:
            config.set("MYCFG", "DisplayedStreams", number)
            print("success, changed to " + number + " anything else?")
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            cfg()
        else:
            print("number from 25-99, try again")
            print("***")
            cfg()
    elif cfg_choice[0] == "2":
        endmessage = cfg_choice[2:]
        config.set("MYCFG", "endmessage", endmessage)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("success, changed to " + endmessage + " anything else?")
        print("***")
        cfg()
    elif cfg_choice[0] == "3":
        config.remove_option("MYCFG", "whitelisted")
        games = cfg_choice[2:].split("!")
        if config.has_option("MYCFG", "Blacklisted"):
            oldgames = config["MYCFG"]["Blacklisted"].split("!")
        else:
            oldgames = []    
        newstate = []
        for game in oldgames:
            if game not in games:
                newstate.append(game)
        for game in games:
            if game not in oldgames:
                newstate.append(game)
        config.set("MYCFG", "blacklisted", "!".join(newstate))
        print("Blacklisted games: " + ", ".join(newstate))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        cfg()
            
    elif cfg_choice[0] == "4":
        config.remove_option("MYCFG", "blacklisted")
        games = cfg_choice[2:].split("!")
        if config.has_option("MYCFG", "Whitelisted"):
            oldgames = config["MYCFG"]["Whitelisted"].split("!")
        else:
            oldgames = []            
        newstate = []
        for game in oldgames:
            if game not in games:
                newstate.append(game)
        for game in games:
            if game not in oldgames:
                newstate.append(game)
        print("whitelisted games: " + ", ".join(newstate))
        config.set("MYCFG", "whitelisted", "!".join(newstate))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        cfg()
    elif cfg_choice[0] == "5":
        quality = cfg_choice[2:]
        quality_options = [audio, high, low, medium, mobile, worst, source, best]
        if quality in quality_options:
            config.set("MYCFG", "streamquality", quality)
            with open("config.ini", "w") as configfile:
                config.write(configfile)
            print("success! Default quality changed to " + quality)
            cfg()
        else:
            print("You failed!, try better!")
            cfg()   
    elif cfg_choice[0] == "6":
        config.remove_section("MYCFG")
        config.add_section("MYCFG")
        for key in config["DEFAULTSETTINGS"]:
            config.set("MYCFG", key, config["DEFAULTSETTINGS"][key])
            print("new " + key + ": " + config["MYCFG"][key])
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        cfg()
    elif cfg_choice[0] == "7":
        strumz()
    elif cfg_choice == "exit!":
        sys.exit()
    else:
        print("are you dumb?? something failed, try again, but differently, k?")
        print("***")
        cfg()

strumz()
print("holy potato! you made it somehow to the end of scrypt! O.o")
