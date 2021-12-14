#各功能接口
import random
import proveGenerate
import requests
import hashlib
from tqdm import tqdm
import ZKPCheck as zk
from chain import miner
import os
from time import  time
minerList = [miner() for i in range(3)]
#医院的公钥（需公开）
l={'f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b':'hospital'}
def users(user):
    return user

#用与授权用户间数据的传输/独立函数模拟可信通道
def sendtoPKB(pkb,info):
    filename='./'+l[pkb]+'/HaveAuth.txt'
    p=open(filename,'r')
    k=eval(p.read())
    p.close()
    k[info[0]]=info[1]
    p = open(filename, 'w')
    p.write(str(k))
    p.close()

#获取当前内存中的块存储情况
def getCount():
    a = requests.request(url='http://127.0.0.1:9000/storgecount', method='GET')
    return int(a.text)

#请求写入数据
def addAsset(sk, sigma, assetId, user):
#若内存中的块已满则先进性save处理产生新的块
    if getCount() > 7:
        saveCode = False
        while not saveCode:
            taskMiner = random.randint(0, 2)
            hashr = minerList[taskMiner].mining()
            for i in range(3):
                if i == taskMiner:
                    continue
                else:
                    if minerList[i].check(hashr):
                        p = requests.request(url='http://127.0.0.1:9000/save?hash=' + hashr, method='GET').text
                        if p == 'False':

                            print('save function wrong')
                            exit(0)
                        else:
                            saveCode = True
                            break
    # ORresult = int(pk, 16) | int(sigma, 16) | int(assetId, 16)
    # ORresult = hex(ORresult)[2:].zfill(128)
    # index_256 = hashlib.sha256(bytes.fromhex(ORresult)).hexdigest()
    # url = 'http://127.0.0.1:9000/addAsset?' + 'pk=' + str(pk) + '&sk=' + str(sk) + '&sigma=' + str(
    #     sigma) + '&assetID=' + str(assetId) + '&user=' + str(user) + '&index_256=' + str(index_256)
    # requests.request(url=url, method='GET')
    assetId=assetId.zfill(64)
#生产证明文件
    start=time()
    index256=proveGenerate.assetProve(sk,assetId,sigma)
    stop=time()
    content=users(user)
    if index256:
        p=os
        #传输证明文件至区块链
        p.popen('cp ./assetZKP/proof.json ./verify/AssetRe/\nrm -rf ./assetZKP/proof.json\n').readlines()
        #传输完成后请求上链
        url = 'http://127.0.0.1:9000/addAsset' + '?assetID=' + str(assetId) + '&index_256=' + str(index256)+'&content='+content
        templist=requests.request(url=url, method='GET').text

        templist=eval(str(templist))

        info,v_time=str(templist[0]),float(templist[1])
        if info!='ZKP prove false' and str(info) != 'False':
            f=open('./Users/'+str(user)+'/userAssetinfo.txt','r')
            userInfo=eval(f.read())
            f.close()
            f = open('./Users/' + str(user) + '/userAssetinfo.txt', 'w')
            userInfo[str(assetId)]=info
            f.write(str(userInfo))
            f.close()
    return start-stop,v_time


#结构同上
def authorization(sk,assetid,sigma,sigmab,pkb,user,content):
    if getCount() > 7:
        saveCode = False
        while not saveCode:
            taskMiner = random.randint(0, 2)
            hashr = minerList[taskMiner].mining()
            for i in range(3):
                if i == taskMiner:
                    continue
                else:
                    if minerList[i].check(hashr):
                        p = requests.request(url='http://127.0.0.1:9000/save?hash=' + hashr, method='GET').text
                        if p == 'False':
                            exit(0)
                            print('save function wrong')
                        else:
                            saveCode = True
                            break
    assetId = assetid.zfill(64)
    start = time()
    index256 = proveGenerate.auth(sk,assetid,sigma,sigmab,pkb,user)
    stop=time()

    if index256:
        p = os
        p.popen(
            'cp ./AuthZKP/proof.json ./verify/AssetAuth/\nrm -rf ./AuthZKP/proof.json\n').readlines()
        url = 'http://127.0.0.1:9000/sq' + '?assetID=' + str(assetId) + '&index_256=' + str(
            index256) + '&content=' + content
        templist = requests.request(url=url, method='GET').text
        templist = eval(str(templist))
        info, v_time = str(templist[0]), float(templist[1])
        if info != 'ZKP prove false' and str(info) != 'False':

            f = open('./searchIndex/data.index', 'r')
            authinfo = eval(f.read())
            f.close()
            f = open('./searchIndex/data.index', 'w')

            authinfo[str(index256)] = info
            pka=hashlib.sha256(bytes.fromhex(str(hex(sk))[2:].zfill(128))).hexdigest().zfill(64)
            sendtoPKB(pkb,[assetid,(info,sigmab,pka,content)])
            f.write(str(authinfo))
            f.close()
    else:
        print('prove generate fail')
    return start - stop, v_time

#保存内存的块到本地文件
def save():
    saveCode = False
    while not saveCode:
        taskMiner = random.randint(0, 2)
        hashr = minerList[taskMiner].mining()
        for i in range(3):
            if i == taskMiner:
                continue
            else:
                if minerList[i].check(hashr):
                    p = requests.request(url='http://127.0.0.1:9000/save?hash=' + hashr, method='GET').text

                    if p == 'False':
                        print('save function wrong')
                        exit(0)

                    else:
                        saveCode = True
                        break

#随机产生文件上链

