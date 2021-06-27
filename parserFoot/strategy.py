import requests

def send_telegram(text: str, channel: str):
    token = ""
    url = "https://api.telegram.org/bot"
    channel_id = channel
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")


def strategybot(time: int, channel: str, jspar):
    try:
        for info in jspar:
            msg = []
            totalbk = 0
            totalscore = 0 
            tyellowcard = 0
            vstvor = 0
            if "match_time_minute" in info:
                if info["match_time_minute"] == time:
                    if "league_name_ru" in info:#имя лиги                        
                        msg.append(info["league_name_ru"])                   
                    if "opponent_1_name_ru" and "opponent_2_name_ru" in info:#                      
                        msg.append(info["opponent_1_name_ru"] + " - " + info["opponent_2_name_ru"])
                    if "match_time_minute" in info:# текущее время матча
                        msg.append("\nВремя: " + str(info["match_time_minute"]) + "\n")
                    if "initial_market_total.c" and "initial_market_total.ce" and "initial_market_total.p" in info:#кэф-ср-колво
                        count = 0
                        for val in list(zip(info["initial_market_total.c"], info["initial_market_total.ce"], info["initial_market_total.p"])):
                            if val[1] == 1 and count == 0:
                                #print("ср.тотал по линии ТБ " + str(val[2]) + " кф-" + str(val[0]))                                
                                totalbk = val[2]
                                count = 1
                                continue
                            if val[1] == 1 and count == 1:
                                #print("ср.тотал по линии ТМ " + str(val[2]) + " кф-" + str(val[0]))                                
                                count = 2
                                continue
                    if "match_score_opponent_1" and "match_score_opponent_2" and "minutes_of_goals_opponent_1" and "minutes_of_goals_opponent_2" in info:
                        totalscore = info["match_score_opponent_1"] + info["match_score_opponent_2"]
                        msg.append("Счет: " + str(info["match_score_opponent_1"]) + ":" + str(info["match_score_opponent_2"]) + "\n")
                    if "opponent_1_yellow_card" and "opponent_2_yellow_card":
                        tyellowcard = info["opponent_1_yellow_card"] + info["opponent_2_yellow_card"]                       
                    if "opponent_1_shots_on" and "opponent_2_shots_on":                        
                        vstvor = info["opponent_1_shots_on"] + info["opponent_2_shots_on"]
                    msg.append("id: " + str(tyellowcard)+str(vstvor))#чтоб запутать шпеоноввв хехехех
            newmsg = ""
            for msgtotg in msg:
                newmsg += msgtotg + "\n"
            if len(msg) > 2:
                if totalbk > totalscore:
                    if tyellowcard < 2:
                        if vstvor > 7:
                            send_telegram(newmsg, channel)
    except:
        time.sleep(30)



def strategybot1time(time: int, channel: str, jspar):
    try:
        for info in jspar:
            msg = []
            totalbk = 0
            totalscore = 0 
            tyellowcard = 0
            vstvor = 0
            if "match_time_minute" in info:
                if info["match_time_minute"] == time:
                    if "league_name_ru" in info:#имя лиги                        
                        msg.append(info["league_name_ru"])                   
                    if "opponent_1_name_ru" and "opponent_2_name_ru" in info:#                      
                        msg.append(info["opponent_1_name_ru"] + " - " + info["opponent_2_name_ru"])
                    if "match_time_minute" in info:# текущее время матча
                        msg.append("\nВремя: " + str(info["match_time_minute"]) + "\n")
                    if "initial_market_total.c" and "initial_market_total.ce" and "initial_market_total.p" in info:#кэф-ср-колво
                        count = 0
                        for val in list(zip(info["initial_market_total.c"], info["initial_market_total.ce"], info["initial_market_total.p"])):
                            if val[1] == 1 and count == 0:
                                #print("ср.тотал по линии ТБ " + str(val[2]) + " кф-" + str(val[0]))                                
                                totalbk = val[2]
                                count = 1
                                continue
                            if val[1] == 1 and count == 1:
                                #print("ср.тотал по линии ТМ " + str(val[2]) + " кф-" + str(val[0]))                                
                                count = 2
                                continue
                    if "match_score_opponent_1" and "match_score_opponent_2" and "minutes_of_goals_opponent_1" and "minutes_of_goals_opponent_2" in info:
                        totalscore = info["match_score_opponent_1"] + info["match_score_opponent_2"]
                        msg.append("Счет: " + str(info["match_score_opponent_1"]) + ":" + str(info["match_score_opponent_2"]) + "\n")
                    if "opponent_1_yellow_card" and "opponent_2_yellow_card":
                        tyellowcard = info["opponent_1_yellow_card"] + info["opponent_2_yellow_card"]                       
                    if "opponent_1_shots_on" and "opponent_2_shots_on":                        
                        vstvor = info["opponent_1_shots_on"] + info["opponent_2_shots_on"]
                    msg.append("id: " + str(tyellowcard)+str(totalscore))#чтоб запутать шпеоноввв хехехех
            newmsg = ""
            for msgtotg in msg:
                newmsg += msgtotg + "\n"
            if len(msg) > 2:
                if totalscore == 0:
                    if tyellowcard > 0:                      
                        send_telegram(newmsg, channel)
                        
    except:
        time.sleep(30)