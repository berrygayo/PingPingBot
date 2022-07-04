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



client.run(discord_token) # 토큰 적는곳