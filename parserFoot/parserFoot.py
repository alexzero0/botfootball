import requests
import brotli
import json 
import time
import strategy


#def mprint(txt: str):
#    with open("log.txt", "a") as log:
#        log.write(txt)


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


def jsreq():
    try:
        r = requests.get('https://betlab.club/api/matches', headers = getdata, params = mparam) 
        strPost = "{\"matches\":" + r.text + ",\"date\":null,\"isFav\":false}"
        p = requests.post("https://betlab.club/api/matches/show", headers = postdata, data = strPost)
        jsonParser = json.loads(p.text)
        return jsonParser
    except:
        return ""


getdata = { "Host":"betlab.club",
         "Connection":"keep-alive",
         "Accept":"application/json, text/plain, */*",
         "X-CSRF-TOKEN":"mwlVNa9fKjA53aWWZWln5Lio9jG0Sv-mehKl52z3myzYbj0C3QYbXgiakN0KWB6N-c-Dfu4Szf5XVtCUCY7KXQ==",
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.284 (Edition Yx 05)",
         "X-Requested-With":"XMLHttpRequest",
         "Sec-Fetch-Site":"same-origin",
         "Sec-Fetch-Mode":"cors",
         "Sec-Fetch-Dest":"empty",
         "Referer":"https://betlab.club/live",
         "Accept-Encoding":"gzip, deflate, br",
         "Accept-Language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
         "Cookie":"__cfduid=dbf6653938c56ed9ac9e134ea3486b73c1609163168; _csrf=7e5820568bbac558cebda0e8cd735eee84d39e1ed639df35bf65d370eeb217a1a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Cgh7rY1n1G5Ko1yiAguOZX2X-DuseyQq%22%3B%7D; PHPSESSID=jf8ia3rsepk3i80rrem0n3bv2k"
        }
mparam = {"sort" : "startTime"}
postdata = { "Host":"betlab.club",
         "Connection":"keep-alive",
         "Accept":"application/json, text/plain, */*",
         "X-CSRF-TOKEN":"mwlVNa9fKjA53aWWZWln5Lio9jG0Sv-mehKl52z3myzYbj0C3QYbXgiakN0KWB6N-c-Dfu4Szf5XVtCUCY7KXQ==",
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.284 (Edition Yx 05)",
         "X-Requested-With":"XMLHttpRequest",
         "Content-Type": "application/json;charset=UTF-8",
         "Origin": "https://betlab.club",
         "Sec-Fetch-Site":"same-origin",
         "Sec-Fetch-Mode":"cors",
         "Sec-Fetch-Dest":"empty",
         "Referer":"https://betlab.club/live",
         "Accept-Encoding":"gzip, deflate, br",
         "Accept-Language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
         "Cookie":"__cfduid=dbf6653938c56ed9ac9e134ea3486b73c1609163168; _csrf=7e5820568bbac558cebda0e8cd735eee84d39e1ed639df35bf65d370eeb217a1a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Cgh7rY1n1G5Ko1yiAguOZX2X-DuseyQq%22%3B%7D; PHPSESSID=jf8ia3rsepk3i80rrem0n3bv2k"
        }


def signalbot(time: int, channel: str, jsonParser):
    try:       
        for info in jsonParser:
            msg = []
            if "match_time_minute" in info:
                if info["match_time_minute"] == time:
                    if "league_name_ru" in info:#имя лиги
                        #print(info["league_name_ru"])
                        msg.append(info["league_name_ru"])
                    if "country_code_id" in info:
                        msg.append("id: " + str(info["country_code_id"]))
                    if "start_time" in info:
                        msg.append("Начали: " + info["start_time"])
                    if "opponent_1_name_ru" and "opponent_2_name_ru" in info:#
                        #print(info["opponent_1_name_ru"] + " - " + info["opponent_2_name_ru"]) 
                        msg.append(info["opponent_1_name_ru"] + " - " + info["opponent_2_name_ru"])
                    if "match_time_minute" in info:# текущее время матча
                        #print("Время: " + str(info["match_time_minute"]))
                        msg.append("\nВремя: " + str(info["match_time_minute"]) + "\n")
                    if "initial_market_total.c" and "initial_market_total.ce" and "initial_market_total.p" in info:#кэф-ср-колво
                        count = 0
                        for val in list(zip(info["initial_market_total.c"], info["initial_market_total.ce"], info["initial_market_total.p"])):
                            if val[1] == 1 and count == 0:
                                #print("ср.тотал по линии ТБ " + str(val[2]) + " кф-" + str(val[0]))
                                msg.append("ср.тотал по линии ТБ " + str(val[2]) + " кф-" + str(val[0]))
                                count = 1
                                continue
                            if val[1] == 1 and count == 1:
                                #print("ср.тотал по линии ТМ " + str(val[2]) + " кф-" + str(val[0]))
                                msg.append("ср.тотал по линии ТМ " + str(val[2]) + " кф-" + str(val[0])+"\n")
                                count = 2
                                continue
                    #print("----Live стастистика----")# отображение статистика во время игры
                    msg.append("\n----Live стастистика----")
                    if "match_score_opponent_1" and "match_score_opponent_2" and "minutes_of_goals_opponent_1" and "minutes_of_goals_opponent_2" in info:
                        #print("Счет: " + str(info["match_score_opponent_1"]) + ":" + str(info["match_score_opponent_2"]))
                        #print(info["opponent_1_name_ru"] + ": " + str(info["minutes_of_goals_opponent_1"]))
                        #print(info["opponent_2_name_ru"] + ": " + str(info["minutes_of_goals_opponent_2"]))
                        msg.append("Счет: " + str(info["match_score_opponent_1"]) + ":" + str(info["match_score_opponent_2"]) + "\n")
                        msg.append(info["opponent_1_name_ru"] + ": " + str(info["minutes_of_goals_opponent_1"]))
                        msg.append(info["opponent_2_name_ru"] + ": " + str(info["minutes_of_goals_opponent_2"]))
                    if "opponent_1_ball_possession" and "opponent_2_ball_possession" in info:
                        #print("% владение мячом: " + str(info["opponent_1_ball_possession"]) + " - " + str(info["opponent_2_ball_possession"]))
                        msg.append("    % владение мячом: " + str(info["opponent_1_ball_possession"]) + " - " + str(info["opponent_2_ball_possession"]))                 
                    if "opponent_1_corner" and "opponent_2_corner" in info:
                        #print("Угловые: " + str(info["opponent_1_corner"]) + " - " + str(info["opponent_2_corner"]))
                        msg.append("    Угловые: " + str(info["opponent_1_corner"]) + " - " + str(info["opponent_2_corner"]))
                    if "opponent_1_yellow_card" and "opponent_2_yellow_card" in info:
                        #print("ЖК: " + str(info["opponent_1_yellow_card"]) + " - " + str(info["opponent_2_yellow_card"]))
                        msg.append("    ЖК: " + str(info["opponent_1_yellow_card"]) + " - " + str(info["opponent_2_yellow_card"]))
                    if "opponent_1_red_card" and "opponent_2_red_card" in info:
                        #print("КК: " + str(info["opponent_1_red_card"]) + " - " + str(info["opponent_2_red_card"]))
                        msg.append("    КК: " + str(info["opponent_1_red_card"]) + " - " + str(info["opponent_2_red_card"]))
                    if "opponent_1_shots_on" and "opponent_2_shots_on" in info:
                        #print("В створ: " + str(info["opponent_1_shots_on"]) + " - " + str(info["opponent_2_shots_on"]))
                        msg.append("    В створ: " + str(info["opponent_1_shots_on"]) + " - " + str(info["opponent_2_shots_on"]))
                    if "opponent_1_shots_off" and "opponent_2_shots_off" in info:
                        #print("Мимо: " + str(info["opponent_1_shots_off"]) + " - " + str(info["opponent_2_shots_off"]))
                        msg.append("    Мимо: " + str(info["opponent_1_shots_off"]) + " - " + str(info["opponent_2_shots_off"]))
                    if "opponent_1_attacks" and "opponent_2_attacks" in info:
                        #print("атак: " + str(info["opponent_1_attacks"]) + " - " + str(info["opponent_2_attacks"]))
                        msg.append("    атак: " + str(info["opponent_1_attacks"]) + " - " + str(info["opponent_2_attacks"]))
                    if "opponent_1_dan_attacks" and "opponent_2_dan_attacks" in info:
                        #print("оп.атак: " + str(info["opponent_1_dan_attacks"]) + " - " + str(info["opponent_2_dan_attacks"]))
                        msg.append("    оп.атак: " + str(info["opponent_1_dan_attacks"]) + " - " + str(info["opponent_2_dan_attacks"]))
                    msg.append("   -активность игры(15м)-")
                    if "stats_last_15_opponent_1_corner" and "stats_last_15_opponent_2_corner" in info:
                        msg.append("    Угловые: " + str(info["stats_last_15_opponent_1_corner"]) + " - " + str(info["stats_last_15_opponent_2_corner"]))
                    if "stats_last_15_opponent_1_shots_on" and "stats_last_15_opponent_2_shots_on" in info:
                        msg.append("    В створ: " + str(info["stats_last_15_opponent_1_shots_on"]) + " - " + str(info["stats_last_15_opponent_2_shots_on"]))
                    if "stats_last_15_opponent_1_shots_off" and "stats_last_15_opponent_2_shots_off" in info:
                        msg.append("    Мимо: " + str(info["stats_last_15_opponent_1_shots_off"]) + " - " + str(info["stats_last_15_opponent_2_shots_off"]))
                    if "stats_last_15_opponent_1_attacks" and "stats_last_15_opponent_2_attacks" in info:
                        msg.append("    атак: " + str(info["stats_last_15_opponent_1_attacks"]) + " - " + str(info["stats_last_15_opponent_2_attacks"]))
                    if "stats_last_15_opponent_1_dan_attacks" and "stats_last_15_opponent_2_dan_attacks" in info:
                        msg.append("    оп.атак: " + str(info["stats_last_15_opponent_1_dan_attacks"]) + " - " + str(info["stats_last_15_opponent_2_dan_attacks"]))
                    #print("---последнии 5 игр---")# рассматриваем последнии 5 игр хозяев и гостей
                    home_away_game_1 = []
                    away_home_game_1 = []
                    home_away_game_2 = []
                    away_home_game_2 = []
                    if "opponent_1_id" and "opponent_2_id" in info:# проверяем id команд
                        if "h2h_t1_games.t1_xid" and "h2h_t1_games.t2_xid" and "h2h_t1_games.t1_score" and "h2h_t1_games.t2_score" in info:
                            for id in list(zip(info["h2h_t1_games.t1_xid"], info["h2h_t1_games.t1_score"])):# совмещаем id и количество голов
                                home_away_game_1.append(id)
                            for id in list(zip(info["h2h_t1_games.t2_xid"], info["h2h_t1_games.t2_score"])):
                                away_home_game_1.append(id)               
                        newstr_1 = ""
                        for id in list(zip(home_away_game_1, away_home_game_1)):
                            if id[0][0] == info["opponent_1_id"]:
                                newstr_1 += "    home(" + str(id[0][1]) + ") - away(" + str(id[1][1]) + ")\n"
                            elif id[1][0] == info["opponent_1_id"]:
                                newstr_1 += "    away(" + str(id[0][1]) + ") - home(" + str(id[1][1]) + ")\n"
                        #print("---игры хозяев")# выводим игры со счетом
                        #print(newstr_1)
                        msg.append("---игры хозяев---")
                        msg.append(newstr_1)
                        
                        if "h2h_t2_games.t1_xid" and "h2h_t2_games.t2_xid" and "h2h_t2_games.t1_score" and "h2h_t2_games.t2_score" in info:
                            for id in list(zip(info["h2h_t2_games.t1_xid"], info["h2h_t2_games.t1_score"])):# совмещаем id и количество голов
                                home_away_game_2.append(id)
                            for id in list(zip(info["h2h_t2_games.t2_xid"], info["h2h_t2_games.t2_score"])):
                                away_home_game_2.append(id)
                        newstr_2 = ""
                        for id in list(zip(home_away_game_2, away_home_game_2)):
                            if id[0][0] == info["opponent_2_id"]:
                                newstr_2 += "    home(" + str(id[0][1]) + ") - away(" + str(id[1][1]) + ")\n"
                            elif id[1][0] == info["opponent_2_id"]:
                                newstr_2 += "    away(" + str(id[0][1]) + ") - home(" + str(id[1][1]) + ")\n"
                        #print("---игры гостей")# выводим игры со счетом
                        #print(newstr_2)
                        msg.append("---игры гостей---")
                        msg.append(newstr_2)
            newmsg = ""
            for msgtotg in msg:
                newmsg += msgtotg + "\n"
            if len(msg) > 5:
                send_telegram(newmsg, channel)
    except:
        time.sleep(30)
                      

def work():
    while True:
        jspar = jsreq()
        signalbot(59, "@statsfootball60", jspar)
        signalbot(89, "@statsfootball90", jspar)
        signalbot(46, "@statsfootball46", jspar)
        strategy.strategybot(59, "@testfootball95", jspar)
        strategy.strategybot1time(15, "@testfootball15", jspar)
        time.sleep(60)

if __name__ == "__main__":
    while True:
        try:
            work()
        except:
            time.sleep(10)
            continue