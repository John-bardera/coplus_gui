# coding:utf-8
import datetime
import requests
from bs4 import BeautifulSoup

def trafic():
    req=requests.get("https://trafficinfo.westjr.co.jp/kinki.html")
    soup = BeautifulSoup(req.content, "html.parser")

def weather():
    #現在の雨雲の動き
    req=requests.get("https://weather.yahoo.co.jp/weather/jp/28/6310/28203.html")
    soup=BeautifulSoup(req.content, "html.parser")
    table=soup.select("#wthimg ul li dl dd a img")
    img_res=requests.get(str(table[0]["src"]),stream=True)
    if img_res.status_code==200:
        with open("now_weather.gif","wb") as file:
            for chunk in img_res.iter_content(chunk_size=2048):
                file.write(chunk)
            file.close()
    #1~7:日付,8~13:天気,15~20:最高気温・最低気温,22~27:降水確率
    week_weather={}
    count=-1
    req=requests.get("https://weather.yahoo.co.jp/weather/jp/28/6310/28203.html")
    soup=BeautifulSoup(req.content, "html.parser")
    for table in soup.select("#yjw_week tr td"):
        data=str(table.small).split(">")[1].split("<")[0]
        count+=1
        if count%7==0:
            continue
        if count>=15 and count<=20:
            data1=str(table.small).split(">")[2].split("<")[0]
            data2=str(table.small).split(">")[5].split("<")[0]
            data=data1+","+data2
        week_weather[count]=data
    #print(week_weather)

def train_jr_get():
    source_req = requests.get("http://www.jr-odekake.net/eki/timetable.php?id=0610611")
    soup = BeautifulSoup(source_req.content, "html.parser")
    url = []
    for links in soup.select("td a"):
        url.append("".join(links["onclick"].split("'")[1].split("amp;")))

    """"#params ={"MODE": 11, "FUNC": 0, "EKI": "魚住", "SENK": "ＪＲ神戸線", "DITD": "2856012070100%2c2856012070110%2c2856012070400%2c2856012070410", "COMPANY_CODE": 4, "DDIV": "", "CDAY": ""}
    params = {}
    today = datetime.datetime.now()
    day = str(today.day)
    if len(day) == 1:
        day = "0" + day
    date = str(today.year) + str(today.month) + day
    params["DIR"] = dir
    params["DATE"] = date
    print(params)

    #req = requests.get("http://time.jr-odekake.net/cgi-bin/mydia.cgi?", params=params)
    if dir == "加古川・姫路方面":
        req = requests.get("http://time.jr-odekake.net/cgi-bin/mydia.cgi?MODE=11&FUNC=0&EKI=魚住&SENK=ＪＲ神戸線&DDIV=&CDAY=&DITD=2856012060100%2c2856012060110%2c2856012060400%2c2856012060410&COMPANY_CODE=4", params=params)
    if dir == "三ノ宮・大阪方面":
        req = requests.get("http://time.jr-odekake.net/cgi-bin/mydia.cgi?MODE=11&FUNC=0&EKI=魚住&SENK=ＪＲ神戸線&DDIV=&CDAY=&DITD=2856012070100%2c2856012070110%2c2856012070400%2c2856012070410&COMPANY_CODE=4", params=params)
    """
    ansd_list = []
    for i in range(2):
        req = requests.get(url[i])
        soup = BeautifulSoup(req.content, "html.parser")
        count = 0
        diagram = {}
        temp_list = []
        for tr in soup.select("table#weekday tr"):
            if count < 3:
                count += 1
                continue
            hour_ = tr.select("th")
            if hour_:
                hour = hour_[0].string
                for minute_ in tr.select("td"):
                    for minute in minute_.select("font"):
                        if hour not in diagram:
                            diagram[hour] = []
                        temp_list.append(minute.text)
                    if not temp_list:
                        continue
                    diagram[hour].append([temp_list[0], temp_list[2]])
                    temp_list = []
        ansd_list.append(diagram)
    return ansd_list


def train_sanyou_get():
    # 西代・阪神梅田方面　平日 334-23_D1_DW0
    # 土曜日 334-23_D1_DW1
    # 日曜日 334-23_D1_DW2

    # 山陽姫路方面 平日 334-23_D2_DW0
    # 土曜日 334-23_D2_DW1
    # 日曜日 334-23_D2_DW2
    if datetime.datetime.now().weekday() < 5:
        which_tables = ["334-23_D1_DW0", "334-23_D2_DW0"]
    if datetime.datetime.now().weekday() == 5:
        which_tables = ["334-23_D1_DW1", "334-23_D2_DW1"]
    else:
        which_tables = ["334-23_D1_DW2", "334-23_D2_DW2"]

    to_change_dir = {"高": "高速神戸", "磨": "山陽須磨", "開": "新開地", "さ": "神戸三宮(阪急)", "サ": "神戸三宮(阪急)", "東": "東須磨", "砂": "高砂", "姫": "山陽姫路", "飾":"飾磨", "二": "東二見"}
    ansd_list = []
    for i in range(2):
        diagram = {}
        req = requests.get("http://timetable.ekitan.com/train/TimeStation/{}.shtml".format(which_tables[i]))
        soup = BeautifulSoup(req.content, "html.parser")
        for tr in soup.select("tr"):
            hour = tr.th.text
            for td in tr.select("td"):
                for ul in td.select("ul"):
                    if ul.text:
                        if hour not in diagram:
                            diagram[hour] = []
                        to_split = ul.text.split("\n")
                        if to_split[1][-1] in to_change_dir:
                            to_split[1] = to_split[1][:-1] + to_change_dir[to_split[1][-1]]
                            if len(to_split[2]) == 2:
                                if to_split[2][0] == "0":
                                    to_split[2] = to_split[2][1]
                            diagram[hour].append([to_split[1], to_split[2]])
        ansd_list.append(diagram)
    return ansd_list


#print(train_sanyou_get()[0])
#print(train_sanyou_get()[1])
#print(train_jr_get()[0])
#print(train_jr_get()[1])
