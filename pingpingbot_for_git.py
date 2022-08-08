import seaborn as sns 
import matplotlib.pyplot as plt

import pandas as pd 
import discord
import asyncio
import random
import numpy as np
import requests
import json
from os import remove
from discord.utils import get
from discord.ext import commands 
from multiprocessing import Pool
import time 


discord_token = 'token num 입력'
# api key 
api_key = 'api_key 입력' 


client = commands.Bot(command_prefix = '!')
client.remove_command('help')

@client.event
async def on_ready():
    print(client.user.name)
    print('핑핑봇 스타또 ~~~ ')
    game = discord.Game('~하는중') # ~~ 하는중
    await client.change_presence(status=discord.Status.online, activity=game)

@client.command(name='embed')
async def embed(ctx):
    embed=discord.Embed(title="PingPingBot", description="made by Gayoungmon", color=0xfb2a68)
    embed.set_author(name="Gayoungmon")
    embed.add_field(name="~~~ing", value="S2", inline=False)
    embed.set_footer(text="byebye")
    await client.process_commands(embed=embed)

# help 
@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = 'Bot Commands',
        description = 'Welcome to the help section. Here are all the commands!',
        color = discord.Colour.dark_magenta()

    )
    embed.set_thumbnail(url='https://github.com/berrygayo/PingPingBot/blob/main/%EC%98%81%EB%AA%AC.jpg?raw=true')
    embed.add_field(
        name='!help',
        value='List all of the commands',
        inline = False
    )
    embed.add_field(
        name='!랜덤라인',
        value='Top,Jg,Mid,Ad,Sup random pick --- ex)  !랜덤라인 가영 주넌 성군 새벽 어깨 ',
        inline = False
    )   
    embed.add_field(
        name='!전적검색',
        value='Show your rank --- ex) !전적검색 "가영몬" ',
        inline = False
    ) 
    embed.add_field(
        name='!와드',
        value='Show categorical ward Graph  --- ex)  !와드 가영몬',
        inline = False
    )    
    embed.add_field(
        name='!추첨하기',
        value='select n in user list(A-B) --- ex)  !추첨하기 2 "가영,주넌,진훈,동이" "가영"',
        inline = False
    )                 

    await ctx.send(embed=embed)

# 인사말 
@client.event
async def on_message(message):
    if message.content == "안녕": # 내가 '안녕'이라고 말하면
        await message.channel.send(f"안녕하세요~~~ ") # 봇이 '안녕하세요'라고 대답
    if message.content == "욤쓰는": 
        await message.channel.send(f"믓쨍이 토마토~~~ ") 
    if message.content == "하별구름은": 
        await message.channel.send(f"천사~~~S2 ")
    await client.process_commands(message)

###################################################################################
################################# 롤 ##############################################
###################################################################################

# 랜덤라인 지정 
# # /랜덤라인 가영 주넌 성군 새벽 어깨     
@client.command(name='랜덤라인')
async def random_line(ctx,name1,name2,name3,name4,name5):
    user_5_name = [name1,name2,name3,name4,name5]
    res_random_line = list(np.random.choice(user_5_name,5,False))
    await ctx.send(f'top: {res_random_line[0]}, jg: {res_random_line[1]}, mid: {res_random_line[2]}, ad: {res_random_line[3]}, sup: {res_random_line[4]}')

# 롤 전적검색 
@client.command(name='전적검색')
async def lol_info(ctx,name):
    print(name)
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name
    res = requests.get(URL, headers={"X-Riot-Token": api_key})
    if res.status_code == 200:
        #코드가 200일때
        resobj = json.loads(res.text)
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        rankinfo = json.loads(res.text)
        print(rankinfo)
        await ctx.send("소환사 이름: "+name)
        for i in rankinfo:
            if i["queueType"] == "RANKED_SOLO_5x5":
                #솔랭과 자랭중 솔랭
                rate = round(i["wins"]/(i["wins"]+i["losses"])*100, 2)
                await ctx.send("솔로랭크:")
                await ctx.send(f'티어: {i["tier"]} {i["rank"]}')
                await ctx.send(f'승: {i["wins"]}판, 패: {i["losses"]}판')
                await ctx.send(f'승률: {rate}%')
            else:
                 # 솔랭과 자랭중 자랭
                rate = round(i["wins"]/(i["wins"]+i["losses"])*100, 2)
                await ctx.send("자유랭크:")
                await ctx.send(f'티어: {i["tier"]} {i["rank"]}')
                await ctx.send(f'승: {i["wins"]}판, 패: {i["losses"]}판')
                await ctx.send(f'승률: {rate}%')
    else:
        # 코드가 200이 아닐때(즉 찾는 닉네임이 없을때)
        await ctx.send("소환사가 존재하지 않습니다")

# 선호 라인 
@client.command(name='라인')
async def lol_line(ctx, name):
    my_summoner_name = name
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+my_summoner_name
    res = requests.get(URL, headers={"X-Riot-Token": api_key})

    if res.status_code == 200:
        #코드가 200일때
        resobj = json.loads(res.text)
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        rankinfo = json.loads(res.text)
    
    request_header = {
        "X-Riot-Token": api_key
    }

    URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+resobj["puuid"]+'/ids?'+ 'type = ranked&start=0&count=20&' + api_key
    res = requests.get(URL, headers = request_header)
    game_list = json.loads(res.text)
    print(game_list)

    # 20 게임  
    summoner_api = "https://asia.api.riotgames.com/lol/match/v5/matches/" + game_list[0]
    res = requests.get(summoner_api, headers = request_header)
    df = pd.DataFrame(res.json())
    pt_df = pd.DataFrame(df['info']['participants'])
    test_dt_0  = pt_df[['summonerName','champExperience','champLevel', 'championName', 'kills','deaths','assists','goldEarned','lane','teamPosition','role','win','visionScore','wardsPlaced']]

    test_res = test_dt_0
    for i in range(1,20):
        summoner_api = "https://asia.api.riotgames.com/lol/match/v5/matches/" + game_list[i]
        res = requests.get(summoner_api, headers = request_header)
        df = pd.DataFrame(res.json())
        pt_df = pd.DataFrame(df['info']['participants'])
        test_dt  = pt_df[['summonerName','champExperience','champLevel', 'championName', 'kills','deaths','assists','goldEarned','lane','teamPosition','role','win','visionScore','wardsPlaced']]
        test_res = pd.concat([test_res,test_dt])
    
    test_res = test_res[test_res["summonerName"].isin([my_summoner_name])]
    # lane 설정 안한 라인 제거, 우르프나 칼바 제거
    test_res = test_res[test_res['lane']!="NONE"]
    test_res = test_res[test_res['teamPosition']!='']
    # 포지션 최빈값 추출 
    mode_position = test_res.teamPosition.mode().values[0]
    await ctx.send(f'{my_summoner_name}님의 최근 20게임 선호라인은 {mode_position} 입니다. ')
 
# 선호 라인 - 포인트용 
def line_match_func(my_summoner_name):
    start = int(time.time())
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+my_summoner_name
    res = requests.get(URL, headers={"X-Riot-Token": api_key})

    if res.status_code == 200:
        #코드가 200일때
        resobj = json.loads(res.text)
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        rankinfo = json.loads(res.text)
    
    request_header = {"X-Riot-Token": api_key}
    URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+resobj["puuid"]+'/ids?'+ 'type = ranked&start=0&count=20&' + api_key
    res = requests.get(URL, headers = request_header)
    game_list = json.loads(res.text)
    print(game_list)
    # 20 게임  
    summoner_api = "https://asia.api.riotgames.com/lol/match/v5/matches/" + game_list[0]
    res = requests.get(summoner_api, headers = request_header)
    df = pd.DataFrame(res.json())
    pt_df = pd.DataFrame(df['info']['participants'])
    test_dt_0  = pt_df[['summonerName','champExperience','champLevel', 'championName', 'kills','deaths','assists','goldEarned','lane','teamPosition','role','win','visionScore','wardsPlaced']]
    test_res = test_dt_0

    for i in range(1,20):
        summoner_api = "https://asia.api.riotgames.com/lol/match/v5/matches/" + game_list[i]
        res = requests.get(summoner_api, headers = request_header)
        df = pd.DataFrame(res.json())
        pt_df = pd.DataFrame(df['info']['participants'])
        test_dt  = pt_df[['summonerName','champExperience','champLevel', 'championName', 'kills','deaths','assists','goldEarned','lane','teamPosition','role','win','visionScore','wardsPlaced']]
        test_res = pd.concat([test_res,test_dt])
    test_res = test_res[test_res["summonerName"].isin([my_summoner_name])]

    # lane 설정 안한 라인 제거, 우르프나 칼바 제거
    test_res = test_res[test_res['lane']!="NONE"]
    test_res = test_res[test_res['teamPosition']!='']
    # 포지션 최빈값 추출 
    mode_position = test_res.teamPosition.mode().values[0]
    print(f'{my_summoner_name}님의 최근 20게임 선호라인은 {mode_position} 입니다. ')
    print("***run time(sec) :", int(time.time()) - start)
    return mode_position

@client.command(name='포인트')
async def lol_point(ctx,*args):
    lol_user_list = args[0].split(',')
    line_list = []
    for name in lol_user_list:
        line_list.append(line_match_func(name))
    await ctx.send(line_list)

# 팀짜기 - solo rank 기준, 55 나누기 
@client.command(name='팀짜기')
async def lol_balance(ctx,*args):
    lol_user_list = args[0].split(',')
    print(lol_user_list)
    for name in lol_user_list:
        URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name
        res = requests.get(URL, headers={"X-Riot-Token": api_key})    
        if res.status_code == 200:
            #코드가 200일때
            resobj = json.loads(res.text)
            URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
            res = requests.get(URL, headers={"X-Riot-Token": api_key})
            rankinfo = json.loads(res.text)
            print(rankinfo)
            for i in rankinfo:
                if i["queueType"] == "RANKED_SOLO_5x5":
                    print(f'{i["tier"]} {i["rank"]}')
                    # 선호라인 만들어내야함 
    await ctx.send('test중~~ ')

# 와드갯수 시각화 
@client.command(name='와드')
async def lol_ward(ctx, name):
    my_summoner_name = name
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+my_summoner_name
    res = requests.get(URL, headers={"X-Riot-Token": api_key})

    if res.status_code == 200:
        #코드가 200일때
        resobj = json.loads(res.text)
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        rankinfo = json.loads(res.text)
    
    request_header = {
        "X-Riot-Token": api_key
    }

    URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+resobj["puuid"]+'/ids?'+ 'type = ranked&start=0&count=20&' + api_key
    res = requests.get(URL, headers = request_header)
    game_list = json.loads(res.text)
    print(game_list)

    # 20 게임  
    summoner_api = "https://asia.api.riotgames.com/lol/match/v5/matches/" + game_list[0]
    res = requests.get(summoner_api, headers = request_header)
    df = pd.DataFrame(res.json())
    pt_df = pd.DataFrame(df['info']['participants'])
    test_dt_0  = pt_df[['summonerName','champExperience','champLevel', 'championName', 'kills','deaths','assists','goldEarned','lane','role','win','visionScore','wardsPlaced']]

    test_res = test_dt_0
    for i in range(1,20):
        summoner_api = "https://asia.api.riotgames.com/lol/match/v5/matches/" + game_list[i]
        res = requests.get(summoner_api, headers = request_header)
        df = pd.DataFrame(res.json())
        pt_df = pd.DataFrame(df['info']['participants'])
        test_dt  = pt_df[['summonerName','champExperience','champLevel', 'championName', 'kills','deaths','assists','goldEarned','lane','role','win','visionScore','wardsPlaced']]
        test_res = pd.concat([test_res,test_dt])
    
    test_res = test_res[test_res["summonerName"].isin([my_summoner_name])]
    # lane 설정 안한 라인 제거 ( Bug 1 : 우르프나 칼바 제거 )
    test_res = test_res[test_res['lane']!="NONE"]
    test_res = test_res[test_res['teamPosition']!='']
    # 챔피언 종류별 mean 
    test_res=test_res.groupby('championName').mean()
    test_res = test_res.reset_index()
    print(test_res)
    
    # 컬러 팔렛트
    colors = sns.color_palette('YlGn',len(test_res["championName"]))
    sns.set_theme(style ="whitegrid" )
    sns.set(font='NanumGothic')

    # 이미지 생성 
    plt.figure(figsize=(10,10)) 
    plt.bar(test_res["championName"],test_res["wardsPlaced"],color=colors)
    plt.title(f"{my_summoner_name}은/는 와드를 잘 박는가")
    plt.xlabel('챔프') 
    plt.ylabel('와드횟수')
    # 이미지 저장 
    plt.savefig("out.png") 
    await ctx.send(file=discord.File('out.png'))

###############################################################################
############################# 제 2의 나라 ######################################
###############################################################################

# 유물전 스킬북 
@client.command(name='추첨하기')
async def by_lot(ctx,n,*args):

    all_user_list = args[0].split(',')
    del_user_list = args[1].split(',')
    n = int(n)

    if len(all_user_list) < n:
        await ctx.send('유저수보다 당첨수가 많습니다.')

    if len(all_user_list) < len(del_user_list):
        await ctx.send('남은 인원이 없습니다.')
    
    user_list = list(set(all_user_list)-set(del_user_list))
    res_random_line = list(np.random.choice(user_list,n,False))
    
    await ctx.send(res_random_line)


###################################################################################
################################# 로아 ############################################
###################################################################################

# 로아 케릭 정보 가져오기 
@client.command(name='로아')
async def Roa_info(ctx,name):
    user_name = quote(name) # 한글깨짐 방지 
    url = "https://lostark.game.onstove.com/Profile/Character/"+ user_name 
    print (url)
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")

    # 서버/길드/직업 
    server_name = bsObject.find_all("div", {"class":"profile-character-info"})[0].find_all("span")[2].text.replace("@","")
    guild_name = bsObject.find_all("div", {"class":"game-info__guild"})[0].find_all("span")[1].text
    role = bsObject.select('#profile-avatar > div.profile-equipment__character > img')[0]['alt']
    embed = discord.Embed(
        title = "❤️" + str(name) + "❤️",
        description = f"서버:{server_name}, 길드:{guild_name}, 직업:{role}",
        color = discord.Colour.magenta()
    )
    #이미지 
    profile_avatar = bsObject.select('#profile-avatar > div.profile-equipment__character > img')[0]['src']
    embed.set_thumbnail(url=profile_avatar)
    
    # 템/전/원 레벨
    item_level = bsObject.find_all("div", {"class":"level-info2__item"})[0].find_all("span")[1].text
    level = bsObject.find_all("div", {"class":"level-info__item"})[0].find_all("span")[1].text
    expedition_level = bsObject.find_all("div", {"class":"level-info__expedition"})[0].find_all("span")[1].text

    embed.add_field(
        name='🔻 레벨',
        value=f"아이템:{item_level}, 전투:{level}, 원정대:{expedition_level}",
        inline = False
    )  

    #  특성
    pa_1_name = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[0].text
    pa_1_value = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[1].text
    pa_2_name = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[2].text
    pa_2_value = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[3].text
    pa_3_name = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[4].text
    pa_3_value = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[5].text
    pa_4_name = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[6].text
    pa_4_value = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[7].text
    pa_5_name = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[8].text
    pa_5_value = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[9].text
    pa_6_name = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[10].text
    pa_6_value = bsObject.find_all("div", {"class":"profile-ability-battle"})[0].find_all("span")[11].text
   
    embed.add_field(
        name='🔻 특성',
        value=f"{pa_1_name}:{pa_1_value},{pa_2_name}:{pa_2_value},{pa_3_name}:{pa_3_value},{pa_4_name}:{pa_4_value},{pa_5_name}:{pa_5_value},{pa_6_name}:{pa_6_value}",
        inline = False
    ) 
    # 각인 
    ability_engrave_list = bsObject.find_all("div", {"class":"profile-ability-engrave"})[0].find_all("span")
    ability_engrave = []
    for i in range(len(ability_engrave_list)):
        pa_engrave = bsObject.find_all("div", {"class":"profile-ability-engrave"})[0].find_all("span")[i].text
        ability_engrave.append(pa_engrave)
    embed.add_field(
        name='🔻 각인',
        value=ability_engrave,
        inline = False
    ) 

    # 5. 보석정보 
    # 보석 리스트 
    # 디코봇에서는 get_text를 써야 값이 가져와짐 확인 
    jewel_level = bsObject.select('#profile-ability > script')[0].string
    jewel_level_1 = []
    jewel_level_2 = []

    try:
        for i in range(11):
            tmp_level = re.split(r'의 보석', jewel_level)[i][-6:]
            tmp = re.split(r'의 보석', jewel_level)[i+1]
            tmp_skill = re.split('FONT COLOR',tmp)[3].split('</FONT>')[0].split('>')[1]
            jewel='Lv'+tmp_level[0]+' '+tmp_skill
            if "홍염" in tmp_level:
                jewel_level_1.append(jewel)
            else:
                jewel_level_2.append(jewel)
    except : 
        print("보석없음")        
    embed.add_field(
        name='🔻 홍염의 보석',
        value=jewel_level_1,
        inline = False
    ) 
    embed.add_field(
        name='🔻 멸화의 보석',
        value=jewel_level_2,
        inline = False
    ) 
    embed.set_footer(text=footer_text, icon_url ="https://github.com/berrygayo/PingPingBot/blob/main/%EC%98%81%EB%AA%AC.jpg?raw=true" )
    await ctx.send(embed=embed)

# 로아 내실 정보 
@client.command(name='내실')
async def Roa_contents_point(ctx,name):

    user_name = quote(name) # 한글깨짐 방지 
    url = "https://lostark.game.onstove.com/Profile/Character/"+ user_name 
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")

    # selenium setting 
    driver = webdriver.Chrome('~~ chromedriver 경로 ')
    driver.get(url)
    time.sleep(1)

    
    # embed basic 
    embed = discord.Embed(
        title = "❤️" + str(name) + "❤️",
        description = f"아직 수집되지 않은 내실 현황을 보여줍니다. ",
        color = discord.Colour.magenta()

    )
    #이미지 
    embed.set_thumbnail(url='https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/CumulativePoint/CumulativePoint_Greatpictures_4.png')

    # "수집형 포인트" 클릭
    search_box = driver.find_element("xpath", '//*[@id="profile-tab"]/div[1]/a[4]')
    search_box.click()
    
    #3:모코코, #6:세계수 제외 
    contents_point_list = [0,1,3,4,6,7]
    # 종류별 갯수 
    contents_dict = {'0':15,'1':96, '3':58, '4':47,'6':16, '7':9}
    contents_name_dict = {'0':'❤️ 거인의 심장','1':'🌍 섬의 마음', '3':'🖌️ 위대한 미술품','4':'🏴‍☠️ 항해 모험물','6':'🧩 이그네아의 징표', '7':'💫 오르페우스의 별' }

    for contents in contents_point_list:
        # 페이지 클릭 
        search_box = driver.find_element("xpath", f'//*[@id="tab1"]/div[1]/a[{contents+1}]')
        search_box.click()
        # setting 
        n = contents_dict[str(contents)]
        contents_name = contents_name_dict[str(contents)]
        not_get_list = []
        count = 0 
    
        for i in range(1,n+1):
            tmp = driver.find_element("xpath",f'//*[@id="lui-tab1-{contents}"]/div/div[2]/ul/li[{i}]').text

            if "획득" not in tmp:
                count += 1
                numbers = re.findall(r'\d+', tmp)
                not_get_list.append(numbers[0])

        get_count = n - count 

        embed.add_field(
            name=f" {contents_name} 미수집 번호 ({get_count}/{n}) ",
            value=not_get_list,
            inline = False
        )  
    # 모코코씨앗 갯수 
    tmp = driver.find_element("xpath",'//*[@id="tab1"]/div[1]/a[3]').text
    embed.add_field(
        name=f" 🍐 모코코 씨앗 ({tmp[6:]}/1304)",
        value=f"{tmp[6:]}개 모았음~ ",
        inline = False
    )  
    # 세계수 잎 
    tmp = driver.find_element("xpath",'//*[@id="tab1"]/div[1]/a[6]').text
    embed.add_field(
        name=f" 🍃 세계수 잎 ({tmp[6:]}/73)",
        value=f"{tmp[6:]}개 모았음~ ",
        inline = False
    )      
    embed.set_footer(text=footer_text, icon_url ="https://github.com/berrygayo/PingPingBot/blob/main/%EC%98%81%EB%AA%AC.jpg?raw=true" )
    await ctx.send(embed=embed)

client.run(discord_token) # 토큰 적는곳