#群内用户注册类
from group_signature_e04_20210718 import GroupManager,Signer,Verifier

#用于新建群签用户
gm = GroupManager(prime_range=[5,10000000],verbose=True)
#用户列表
Users=['A','B']
# In[9]:

for x in Users:
    signer_1 = Signer(signer_name=x, public_key_GM=gm.public_key)
    request = signer_1.apply_join_in()
    cert = gm.approve_join_request(request)
    signer_1.verify_cert(cert)
    verifier_1 = Verifier(verifier_name='vr1',public_key_GM=gm.public_key)
    msg = 'auth'
    sg1 = signer_1.sign_message(m=msg)
    print(sg1)
    f = open('authcontent.txt', 'r')
    a = eval(f.read())
    f.close()
    a[x] = str(sg1)
    f = open('authcontent.txt', 'w')
    f.write(str(a))
    f.close()


# In[10]:

#
# msg='auth'
# sg1 = signer_1.sign_message(m=msg)
# print(sg1)
# f=open('authcontent.txt','r')
# a=eval(f.read())
# f.close()
# a['A']=str(sg1)
#
# verifier_1.verify_signature(signature=sg1, m=msg)
# gm.open_signature(sg1)
#
# msg='auth'
# sg2 = signer_2.sign_message(m=msg)
# print(sg2)
# a['B']=str(sg2)
# f=open('authcontent.txt','w')
# f.write(str(a))
# f.close()
#
# verifier_1.verify_signature(signature=sg2, m=msg)
# gm.open_signature(sg2)