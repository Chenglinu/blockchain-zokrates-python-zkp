#节点测试文件，不参与
from chain import blockchain,miner
import datetime,time
import ZKPCheck as zp
from flask import Flask,render_template,request
app = Flask(__name__)
# start=blockchain()
start=blockchain()

@app.route('/addAsset', methods=['GET', 'POST'])
def addRequest():
    # ordersn_list=str(request.form['ordersn_list'])
    # shopid=int(request.form['shopid'])
    # a=str(request.args.get('id'))
    # print(a)
    pk=request.args.get('pk')
    sk=request.args.get('sk')
    assetID=request.args.get('assetID')
    sigma=request.args.get('sigma')
    user=request.args.get('user')
    index_256=zp.addAssetCheck(pk,sk,assetID,sigma)
    if index_256:
        info=start.add(index_256,'register asset',assetID)
        f=open('./Users/'+str(user)+'/userAsset.infomation','w+')
        userInfo=eval(f.read())
        userInfo[str(assetID)]=info
        f.write(str(userInfo))
        f.close()
        return str(info)
    else:
        return 'ZKP prove false'





@app.route('/save', methods=['GET', 'POST'])
def saveRequest():
    try:
        firstline=request.args.get('hash')
        info=start.save(firstline)
        return str(info)
    except:
        return 'False'


#71c6818d7b0f63728222fe1d39be96e1027bb901fac8a2ed8e59993098bef0e7

if __name__ == '__main__':


    app.run(host='127.0.0.1', port=9000, debug=True)

