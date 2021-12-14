#块类
import hashlib

class block:
    # 记录总块数(为实际块数和正在生产的块总数+1)
    blockIndex = 1
    # 自身块ID
    selfIndex = 0
    # 已注册的资产避免重复注册

    # 当前块的存储数量


    def __init__(self, blockIndex=1):
        # Merkle树处理的对象，应写入本地文件
        self.dataStorgeIndex = [str("00" * 64) for i in range(8)]
        # 数据存储区域（应在最后写入本地文件）
        self.dataStorge = {}
        # 索引
        self.indexToBlockID = {}
        self.storgeCount = 0
        # Merkle树
        self.Merkle = {}

        self.MerkleUpdate()
        if blockIndex > 1:
            block.blockIndex = blockIndex
        self.selfIndex = block.blockIndex
        block.blockIndex += 1

    # 数据上块
    def addData(self, index_256, content, assetID):
        if isinstance(index_256, str) and len(index_256) == 64 and self.storgeCount < 8:
            try:
                bytes.fromhex(index_256)
            except:
                return False
            self.dataStorgeIndex[self.storgeCount] = index_256
            self.dataStorge[index_256] = content
            self.storgeCount += 1
            self.MerkleUpdate()
            return (self.selfIndex, self.storgeCount - 1)
        else:
            return False

    # M树维护
    def MerkleUpdate(self):
        self.Merkle = {}
        node = [str(i) for i in range(8)]
        tik = 0
        parentname = ''
        while len(node) > 0:

            nodeName = node[0]
            del node[0]
            parentname += nodeName
            if tik == 1:
                node.append(parentname)
                parentname = ''
                tik = 0
            else:
                tik += 1
            if nodeName[:int(len(nodeName) / 2)] in self.Merkle:
                rawData = self.Merkle[nodeName[:int(len(nodeName) / 2)]].zfill(64)+ self.Merkle[
                    nodeName[int(len(nodeName) / 2):]].zfill(64)
            else:
                rawData = self.dataStorgeIndex[int(nodeName)]
            rawData=rawData.zfill(128)
            context = str(hashlib.sha256(bytes.fromhex(rawData)).hexdigest())
            self.Merkle[nodeName] = context.zfill(64)

    # M树返回兄弟节点


# a=block()
# print(a.Merkle)
# print(a.currentAssetIndexUsed)
# print(block.blockIndex)
# print(a.dataStorge,a.storgeCount)
# print('####################'*10)
# a.addData('01'*64,'test','123')
# print(a.Merkle)
# print(a.currentAssetIndexUsed)
# print(a.dataStorge,a.storgeCount)
#
# print('####################'*10)
# b=block()
# print(block.blockIndex)
# print('####################'*10)
# checkIndex='0'
# currentIndex=checkIndex
# print(a.checkM(checkIndex))
# node=a.dataStorgeIndex[0]
# print(node)
# currentHash=hashlib.sha256(bytes.fromhex(node)).hexdigest()
# for i in a.checkM(checkIndex):
#     if int(i)>int(checkIndex):
#         currentHash+=a.Merkle[i]
#         currentIndex+=i
#     else:
#         currentHash=a.Merkle[i]+currentHash
#         currentIndex =i+checkIndex
#     currentHash=hashlib.sha256(bytes.fromhex(currentHash)).hexdigest()
# print('####################' * 10)
# print(currentHash==a.Merkle['01234567'])
# print(currentHash==b.Merkle['01234567'])
# print(b.dataStorge)
# b.addData('11'*64,'yy','11')
# a.addData('11'*64,'yy','113')
# print(a.dataStorge)
# print(b.dataStorgeIndex)
