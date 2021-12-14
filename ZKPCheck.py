#节点用于检查证明有效性和输入的合法性
import random
import hashlib
import os


configure_f=open('./config.txt','r')
configure=str(configure_f.read())
configure_f.close()
#证明通过性检查脚本
def addAssetCheck():
    p = os
    try:
        f=open('./verify/assetRe/proof.json','r')
        info=eval(f.read())
        f.close()
        if info['inputs'][-1][-1] !='1':
            return False


    except:
        return False

    try:

        result=p.popen(
            'export PATH=$PATH:'+configure+'\ncd ./verify/assetRe\nzokrates verify\nrm -rf proof.json\n').readlines()[1][:-2]
    except:
        result=False
    return result=='PASSE'


def authorizationCheck():
    p = os
    try:
        #检查证明文件结果
        f=open('./verify/AssetAuth/proof.json','r')
        info=eval(f.read())
        f.close()
        if info['inputs'][-1][-1] !='1':
            return False
        #检查证明文件输入的根是否伪造
        rootCheck=''
        ind=-17
        for i in range(8):
         rootCheck+=str(info['inputs'][ind+i][-8:])
        f = open('./temp/root.txt', 'r')
        k = eval(f.read())
        f.close()
        if not (rootCheck in k):
            return False


    except:
        return False

    try:
        result = p.popen(
            'export PATH=$PATH:'+configure+'\ncd ./verify/AssetAuth\nzokrates verify\nrm -rf proof.json\n').readlines()[
                     1][:-2]
    except:
        result = False
    return result == 'PASSE'

