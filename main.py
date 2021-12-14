#节点主线程
from chain import blockchain,miner
import datetime,time
import ZKPCheck as zp
from flask import Flask,render_template,request
app = Flask(__name__)
# start=blockchain()
start=blockchain()


#区块链启动程序

#资产注册
@app.route('/addAsset', methods=['GET', 'POST'])
def addRequest():
    # ordersn_list=str(request.form['ordersn_list'])
    # shopid=int(request.form['shopid'])
    # a=str(request.args.get('id'))
    # print(a)

    assetID=request.args.get('assetID')

    content=request.args.get('content')
    index_256=request.args.get('index_256')

    if len(request.args)==3:
        print(index_256,content,assetID)
        info,v_time=start.addAsset(index_256,content,assetID)



        return '['+str(info)+','+str(v_time)+']'
    else:
        return '(ZKP prove false,0)'




#保存内存的区块到本地文件
@app.route('/save', methods=['GET', 'POST'])
def saveRequest():
    try:
        firstline=request.args.get('hash')
        info=start.save(firstline)
        return str(info)
    except Exception as e:
        print(e)
        return 'False'

#返回当前区块存储容量信息
@app.route('/storgecount', methods=['GET', 'POST'])
def infoCount():
    return str(start.currentBlock.storgeCount)

#返回静态文件中最新的块
@app.route('/previousFile', methods=['GET', 'POST'])
def prefile():
    return str(start.currentBlock.blockIndex-2)+'.block'

#授权请求
@app.route('/sq', methods=['GET', 'POST'])
def sq():
    # ordersn_list=str(request.form['ordersn_list'])
    # shopid=int(request.form['shopid'])
    # a=str(request.args.get('id'))
    # print(a)

    assetID=request.args.get('assetID')

    index_256_2=request.args.get('index_256')

    content = request.args.get('content')


    if len(request.args)==3:

        info,v_time=start.authorization(index_256_2, content, assetID)

        return '[' + str(info) + ',' + str(v_time) + ']'
    else:
        return '(ZKP prove false,0)'

#71c6818d7b0f63728222fe1d39be96e1027bb901fac8a2ed8e59993098bef0e7

if __name__ == '__main__':


    app.run(host='127.0.0.1', port=9000, debug=True)

