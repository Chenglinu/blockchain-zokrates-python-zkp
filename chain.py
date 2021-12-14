#链类
from block import block
import hashlib
import os
import ZKPCheck as zk
import requests
from time import time
def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(os.path.join(root, file)[len(file_dir):])
    return L

class blockchain:
    def __init__(self):
        #初始化，找到目前最长链，并将已注册图片id送入内存
        L = file_name('./BlockData/')
        latestBlockIndex = -1
        for x in L:
            if int(x.strip('.block')) > latestBlockIndex:
                latestBlockIndex = int(x.strip('.block'))
        f=open('./searchIndex/asset.index','r')
        self.currentAssetIndexUsed=eval(f.read())
        f.close()
        self.currentBlock = block(latestBlockIndex + 1)
    #保存内存的块到文件，创建新的块接受数据
    def save(self,Minnerhash):

        try:
            previousFilename = str(self.currentBlock.selfIndex - 1) + '.block'
            f = open('./BlockData/' + previousFilename, 'r')
            rawdata = f.read()
            f.close()
            firstlinechk = hashlib.sha256(rawdata.encode('utf-8')).hexdigest()
            if firstlinechk!=Minnerhash:
                return 'Manner save data wrong'
            #数据写入文件
            content = Minnerhash + '\n'
            content += str(self.currentBlock.Merkle) + '\n'
            content += str(self.currentBlock.dataStorge) + '\n'
            content += str(self.currentBlock.dataStorgeIndex)
            currentFilename = str(self.currentBlock.selfIndex) + '.block'
            f = open('./BlockData/' + currentFilename, 'w')
            f.write(content)
            f.close()
            f = open('./searchIndex/asset.index', 'w')
            f.write(str(self.currentAssetIndexUsed))
            f.close()

            f=open('./temp/root.txt','r')
            k=eval(f.read())
            f.close()
            k.append(str(self.currentBlock.Merkle['01234567']))
            f = open('./temp/root.txt', 'w')
            f.write(str(k))
            f.close()
            self.currentBlock = block()
            return True
        except Exception as e:
            print('block save error')
            print(e)
            exit(-1)
            return False
#数据入块，返回用户块的编号以及位置
    def addAsset(self,index_256,content,assetID):
        #证明检查以及重复注册检查
        start=time()
        stop=start
        if zk.addAssetCheck() and not(str(assetID) in self.currentAssetIndexUsed):
            stop=time()
            searchInfo=self.currentBlock.addData(index_256,content,assetID)
        else:
            searchInfo=False
        if searchInfo:
            blockID,innerID=searchInfo
            self.currentAssetIndexUsed.append(str(assetID))

            return (blockID,innerID),stop-start
        else:
            print('add data error')
            return False

    def authorization(self,index_256_2,content,assetID):
        #证明检查
        start = time()
        stop = start
        if zk.authorizationCheck():
            stop = time()
            searchInfo=self.currentBlock.addData(index_256_2,content,assetID)
        else:
            searchInfo=False

        if searchInfo:
            blockID,innerID=searchInfo


            return (blockID,innerID),stop-start
        else:
            print('add data error')
            return False

#矿工类
class miner:
    #挖矿
    def mining(self):
        previousFilename = requests.request(url='http://127.0.0.1:9000/previousFile', method='GET').text
        f = open('./BlockData/' + previousFilename, 'r')
        rawdata = f.read()
        f.close()
        hashContent = hashlib.sha256(rawdata.encode('utf-8')).hexdigest()
        return hashContent
    #检查其他矿工的成果
    def check(self,othersHash):
        previousFilename = requests.request(url='http://127.0.0.1:9000/previousFile', method='GET').text
        f = open('./BlockData/' + previousFilename, 'r')
        rawdata = f.read()
        f.close()
        chk = hashlib.sha256(rawdata.encode('utf-8')).hexdigest()
        if chk != othersHash:
            return False
        else:
            return True



# p = blockchain()
#
# p.save()
# p.save()
# p.add('01'*64,'test','123')
# p.add('01'*64,'test','1234')
# p.save()
# p.add('01'*64,'test','123')
# p.save()
# print(block.checkM('0'))

# def p(b):
#     return b.add('11' * 64, 'yy', '113')
#
# a=blockchain()
# p(a)
# print(a.currentBlock.dataStorge)





