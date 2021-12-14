#用于证明生成并自动传输至节点服务器
import hashlib
import os
from time import time

configure_f=open('./config.txt','r')
configure=str(configure_f.read())
configure_f.close()
#返回Merkle兄弟节点坐标，不依赖于具体的块
def checkM(nodeIndex):
    brotherNodes = []
    current = nodeIndex
    brother = ''
    layer = 0
    layerNode = [['0', '1', '2', '3', '4', '5', '6', '7'], ['01', '23', '45', '67'], ['0123', '4567'], ['01234567']]
    while current != '01234567':
        nowLayer = layerNode[layer]
        li = nowLayer.index(current)
        if li % 2 == 0:
            brother = nowLayer[li + 1]
            current += brother
        else:
            brother = nowLayer[li - 1]
            current = brother + current
        layer += 1
        brotherNodes.append(brother)
    return brotherNodes


#遍历file_dir文件jia下的文件名
def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(os.path.join(root, file)[len(file_dir):])
    return L

#资产注册证明
def assetProve(sk,assetid,sigma):
    pk = hashlib.sha256(bytes.fromhex(str(hex(sk))[2:].zfill(128))).hexdigest()
    ORresult = int(pk, 16) | sigma | int(assetid, 16)
    ORresult = hex(ORresult)[2:].zfill(128)
    index_256 = hashlib.sha256(bytes.fromhex(ORresult)).hexdigest()
    # pk = hashlib.sha256(bytes.fromhex(str(hex(100))[2:].zfill(128))).hexdigest()
    # for i in range(8):
    #     print(int(pk[8 * i:8 * i + 8], 16), end=' ')
    # sigma = 5
    # a = sigma | int(pk, 16) | 0
    index_256=index_256.zfill(64)
    commands=str(sigma)+' '+str(sk)+' '
    pk=pk.zfill(64)
    for i in range(8):
        commands+=str(int(pk[8 * i:8 * i + 8], 16))+' '

    for i in range(8):
        commands+=str(int(index_256[8 * i:8 * i + 8], 16))+' '
    assetid=assetid.zfill(64)
    for i in range(8):
        commands+=str(int(assetid[8 * i:8 * i + 8], 16))+' '


    p = os
    p.popen(
         'export PATH=$PATH:'+configure+'\ncd ./assetZKP\nzokrates compute-witness -a '+commands+'\nzokrates generate-proof').readlines()
    if 'proof.json' in file_name('./assetZKP/'):

        return index_256
    else:

        return False

#资产授权证明
def auth(sk,assetid,sigma,sigmab,pkb,user):
    pk = hashlib.sha256(bytes.fromhex(str(hex(sk))[2:].zfill(128))).hexdigest()
    pk=pk.zfill(64)
    commands =str(sigma)+' '+str(sigmab)+' '+str(sk)+' '
    for i in range(8):
        commands +=str(int(pk[8 * i:8 * i + 8], 16))+' '
    a = sigma | int(pk, 16) | int(assetid, 16)

    index512 = hashlib.sha256(bytes.fromhex(str(hex(a))[2:].zfill(128))).hexdigest()




    index512=index512.zfill(64)
    for i in range(8):
        commands +=str(int(index512[8 * i:8 * i + 8], 16))+' '

    assetid = assetid.zfill(64)
    for i in range(8):
        commands += str(int(assetid[8 * i:8 * i + 8], 16)) + ' '

    pkb = pkb.zfill(64)
    for i in range(8):
        commands += str(int(pkb[8 * i:8 * i + 8], 16)) + ' '

    f=open('./Users/'+str(user)+'/userAssetinfo.txt','r')
    usinfo=eval(f.read())

    f.close()
    filename='./BlockData/'+str(eval(usinfo[assetid])[0])+'.block'
    fileindex=str(eval(usinfo[assetid])[1])
    Mlist=checkM(fileindex)


    tempp=str(fileindex)
    f=open(filename,'r')
    f.readline()
    p = eval(f.readline())
    f.close()

    for x in Mlist:
        temn = p[x].zfill(64)

        for i in range(8):
            commands += str(int(temn[8 * i:8 * i + 8], 16)) + ' '
        if int(x)>int(tempp):
            commands+='0 '
            tempp=tempp+x

        else:
            commands+='1 '
            tempp =  x+tempp



    temn = p['01234567'].zfill(64)

    for i in range(8):
        commands += str(int(temn[8 * i:8 * i + 8], 16))+' '


    z = int(pk, 16) | int(pkb,16) | sigmab | int(assetid, 16)
    index512 = hashlib.sha256(bytes.fromhex(str(hex(z))[2:].zfill(128))).hexdigest()
    index512=index512.zfill(64)
    for i in range(8):
        commands += str(int(index512[8 * i:8 * i + 8], 16)) + ' '



    p = os
    p.popen(
         'export PATH=$PATH:'+configure+'\ncd ./AuthZKP\nzokrates compute-witness -a '+commands+'\nzokrates generate-proof').readlines()
    if 'proof.json' in file_name('./AuthZKP/'):
        return index512
    else:
        return False

#资产已授权的验证证明
def generateAuthProve(skb,assetID,group='hospital'):
    f=open('./'+group+'/HaveAuth.txt','r')
    info=eval(f.read())
    f.close()
    assetID = assetID.zfill(64)
    pka=info[assetID][2]
    sigmaAB=info[assetID][1]
    locationInfo=eval(info[assetID][0])
    filename='./BlockData/'+str(locationInfo[0])+'.block'
    fileindex=str(locationInfo[1])
    Mlist = checkM(fileindex)

    f = open(filename, 'r')
    f.readline()
    p = eval(f.readline())
    f.close()


    commands=str(sigmaAB)+' '+str(skb)+' '
    pk = hashlib.sha256(bytes.fromhex(str(hex(skb))[2:].zfill(128))).hexdigest().zfill(64)
    for i in range(8):
        commands+=str(int(pk[8 * i:8 * i + 8], 16))+' '
    pka=pka.zfill(64)
    for i in range(8):
        commands += str(int(pka[8 * i:8 * i + 8], 16)) + ' '


    z = int(pk, 16) | int(pka, 16) | sigmaAB | int(assetID,16)
    index512 = hashlib.sha256(bytes.fromhex(str(hex(z))[2:].zfill(128))).hexdigest().zfill(64)
    for i in range(8):
        commands += str(int(index512[8 * i:8 * i + 8], 16)) + ' '


    # alpha id
    for i in range(8):
        commands += str(int(assetID[8 * i:8 * i + 8], 16)) + ' '
    tempp=str(fileindex)
    for x in Mlist:
        temn = p[x].zfill(64)

        for i in range(8):
            commands += str(int(temn[8 * i:8 * i + 8], 16)) + ' '
        if int(x)>int(tempp):
            commands+='0 '
            tempp=tempp+x

        else:
            commands+='1 '
            tempp =  x+tempp

    temn = p['01234567'].zfill(64)

    for i in range(8):
        commands += str(int(temn[8 * i:8 * i + 8], 16)) + ' '
    p = os
    start=time()
    p.popen(
        'export PATH=$PATH:'+configure+'\ncd ./auProGe\nzokrates compute-witness -a ' + commands + '\nzokrates generate-proof').readlines()
    stop=time()
    p_time=start-stop
    start=time()
    t=os
    try:
        result = t.popen(
            'export PATH=$PATH:'+configure+'\ncd ./auProGe\nzokrates verify\nrm -rf proof.json\n').readlines()[
                     1][:-2]
    except:
        result='a'
    stop=time()
    v_time=start-stop
    return result == 'PASSE',p_time,v_time



# auth(100,'0f179fbfd346fdd67b2f7276afcef7e3b617e71e86088ae47bc5cec86d9e5594',5,10,'00','A')
# assetProve(100,'0f179fbfd346fdd67b2f7276afcef7e3b617e71e86088ae47bc5cec86d9e5594',5)
#generateAuthProve(0,'a325d2b1c02a0f957b78702a10d8cf29819c2bb6ed7202953015368b017c5f84
# assetProve(100,'0f179fbfd346fdd67b2f7276afcef7e3b617e71e86088ae47bc5cec86d9e5594',5)