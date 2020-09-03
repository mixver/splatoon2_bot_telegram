import os
import time
import random
import json

import sys
sys.path.append('../splatoon2_bot_core/')

from base_config import API_RANKED, API_REGULAR, API_LEAGUE,TMP_IMG,TMP_DIR
from translation import STAGES, TIME, BATTLE_TYPES,CN_LEAGUE, CN_RANKED, CN_REGULAR
from battle import getBattleImage
from random_weapon import generateFinalRandomWeaponImage
from salmon_run import getSalmonRunData

MODES = {API_LEAGUE: CN_LEAGUE, API_RANKED: CN_RANKED, API_REGULAR: CN_REGULAR}
MINUTES_EPOCH = 60
HOURS_EPOCH = 60 * MINUTES_EPOCH

def dict_rand_value(d: dict):
    return list_rand_value(list(d.values()))

def list_rand_value(l: list):
    size = len(l)
    if size > 0:
        return l[random.randint(0, size - 1)]
    else:
        return None

def replySalmonRun(requester,requestTime):
    salmonRunImage=getSalmonRunData(requestTime)
    photo=open(salmonRunImage,"rb")
    requester.message.reply_photo(photo)

def replyBattle(requester,
                 mode: str,
                 msg_time: float,
                 request_input: str,
                 txt: bool = True,
                 img: bool = True):          
    if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)
    queryTime = msg_time
    if "下" in request_input:
        queryTime = msg_time + (2 * HOURS_EPOCH) * request_input.count("下")
    elif "小时后" in request_input:
        index = request_input.index("小时后") - 1
        num_char = request_input[index]
        try:
            parsed = int(num_char)
        except ValueError:
            parsed = TIME.get(request_input[index], 0)
        queryTime = msg_time + parsed * HOURS_EPOCH
    filename=getBattleImage(mode,queryTime,TMP_IMG)
    photo=open(filename,"rb")
    requester.message.reply_photo(photo)

def replyRandom(requester,keyword):
    if "祭典" in keyword:
        isFestRandom=1
    else:
        isFestRandom=0
    randomWeaponJson=[]
    password=""
    hasRandomWeapon=False
    # 获取当前时间戳
    imageTimestamp=time.time()
    intImageTimestamp=int(imageTimestamp)
    strImageTimestamp=str(intImageTimestamp)
    # 目标文件路径
    randomWeaponData="D:/mixver_project/test_splatoon_bot/splatoon2_bot_core/data/random-weapon-room.json"
    finalRandomDir="./final-random-weapon-image/"
    finalRandomImage=finalRandomDir+strImageTimestamp+'.png'    
    tmpStageDir="./tmp-random-stage/"
    if not os.path.exists("./tmp/"):
        os.mkdir("./tmp/")
    if not os.path.exists(finalRandomDir):
        os.mkdir(finalRandomDir)
    if not os.path.exists(tmpStageDir):
        os.mkdir(tmpStageDir)
    if not os.path.exists(randomWeaponData):
        open(randomWeaponData,'w')
    # 读取密码随机武器私房数据
    if os.path.getsize(randomWeaponData)!=0:
        with open(randomWeaponData,'r') as load_f:
            randomWeaponJson = json.load(load_f)
    else:
        randomWeaponJson=[]
    if "+" in keyword:
        strIndex=keyword.index("+")
        password=keyword[strIndex+1:].encode('unicode_escape').decode("utf-8").replace("\\u", "")
        finalRandomImage=finalRandomDir+strImageTimestamp+'+'+password+'.png'
    if "+" in keyword:
        for i,v in enumerate(randomWeaponJson):
            if v['timestamp']<(intImageTimestamp-100):
                myImage=v['image']
                del randomWeaponJson[i]
                # if os.path.exists(myImage):
                    # os.remove(myImage)
        for i,v in enumerate(randomWeaponJson):
            if v['password']==password:
                hasRandomWeapon=True
                mode=v['mode']
                finalRandomImage=v['image']
        if not hasRandomWeapon:
            # 生成随机模式图片
            mode = dict_rand_value(BATTLE_TYPES)
            generateFinalRandomWeaponImage(mode,finalRandomImage,isFestRandom)
            randomWeaponJson.append({
                "mode": mode,
                "image":finalRandomImage,
                "timestamp":intImageTimestamp,
                "password":password
            })
        json_str = json.dumps(randomWeaponJson)
        new_dict = json.loads(json_str)

        with open(randomWeaponData,"w") as f:
            json.dump(new_dict,f,sort_keys=True, indent=4, separators=(',', ': '))
    if "+" not in keyword:
        # 生成随机模式图片
        mode = dict_rand_value(BATTLE_TYPES)
        generateFinalRandomWeaponImage(mode,finalRandomImage,isFestRandom)
    photo=open(finalRandomImage,"rb")
    requester.message.reply_photo(photo)
    # if "+" not in keyword:
        # os.remove(finalRandomImage)