from Minner import authorization,addAsset,save
from time import time
from  tqdm import tqdm
import proveGenerate
start=time()
time_sum=0
time_list=[]
v_sum=0
v_lisy=[]
for i in tqdm(range(100)):

    proving_time,v_time=addAsset(100,5,hashlib.sha256(str(random.randint(1, 100000000000)*random.randint(1,1000000000000)).encode('utf-8')).hexdigest().zfill(64),'A')
    time_sum+=proving_time

    v_sum+=v_time
    time_list.append(proving_time)
    v_lisy.append(v_time)
    if (i+1)%7==0:
        save()
save()
stop=time()
print('资产注册总时间：'+str(stop-start))
print('资产证明生成时间：'+str(time_sum))
print('资产证明生成时间分开统计：'+str(time_list))
print('资产证明验证总时长：'+str(v_sum))
print('资产证明验证时长列表'+str(v_lisy))

f=open('./Users/A/userAssetinfo.txt')
p=eval(f.read())
f.close()

#授权给hospital
start=time()
time_sum=0
time_list=[]
v_sum=0
v_lisy=[]
i=0
for x in tqdm(p):
    f = open('authcontent.txt', 'r')
    a = eval(f.read())
    f.close()
    userName='A'
    #f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b为hosipitol PK

    proving_time,v_time=authorization(100,x,5,10,'f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b',userName,a[userName])
    time_sum += proving_time
    v_sum += v_time
    time_list.append(proving_time)
    v_lisy.append(v_time)
    if (i+1)%7==0:
        save()
    i+=1
save()
stop=time()
print('资产授权总时间：'+str(stop-start))
print('资产授权证明生成时间：'+str(time_sum))
print('资产授权证明生成时间分开统计：'+str(time_list))
print('资产授权证明验证总时长：'+str(v_sum))
print('资产授权证明验证时长列表'+str(v_lisy))


#授权验证，


start=time()
time_sum=0
time_list=[]
v_sum=0
v_lisy=[]
i=0


f=open('./hospital/HaveAuth.txt','r')
info=eval(f.read())
f.close()
i=0
for x in tqdm(info):
    t,proving_time,v_time=proveGenerate.generateAuthProve(0,x)
    time_sum += proving_time
    v_sum += v_time
    time_list.append(proving_time)
    v_lisy.append(v_time)
    if t:
        ###################################
        #        此处可进行授权文件传输      #
        #                                #
        ###################################
        a=1

stop=time()
print('资产授权验证证明总时间：'+str(stop-start))
print('资产授权验证证明生成时间：'+str(time_sum))
print('资产授权验证证明生成时间分开统计：'+str(time_list))
print('资产授权验证证明验证总时长：'+str(v_sum))
print('资产授权验证证明验证时长列表'+str(v_lisy))