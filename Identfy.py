#群成员识别
from group_signature_e04_20210718 import GroupManager,Signer,Verifier
from collections import namedtuple
Signature = namedtuple('Signature', ['u','t','s1','s2'])
gm = GroupManager(prime_range=[5,10000000],verbose=True)

#用户识别
#用于新建群签用户
gm = GroupManager(prime_range=[5,10000000],verbose=True)
#用户列表
Users=['A','B']
# In[9]:
verifier_1 = Verifier(verifier_name='vr1',public_key_GM=gm.public_key)
for x in Users:
    signer_1 = Signer(signer_name=x, public_key_GM=gm.public_key)
    request = signer_1.apply_join_in()
    cert = gm.approve_join_request(request)
    signer_1.verify_cert(cert)
    # msg = 'auth'
    # sg1 = signer_1.sign_message(m=msg)
    # print(sg1)
    # f = open('authcontent.txt', 'r')
    # a = eval(f.read())
    # f.close()
    # a[x] = str(sg1)
    # f = open('authcontent.txt', 'w')
    # f.write(str(a))
    # f.close()


# signer_1 = Signer(signer_name='A', public_key_GM=gm.public_key)
# request = signer_1.apply_join_in()
# cert = gm.approve_join_request(request)
# signer_1.verify_cert(cert)
# verifier_1 = Verifier(verifier_name='vr1',public_key_GM=gm.public_key)
#
#
#
# signer_2 = Signer(signer_name='B', public_key_GM=gm.public_key)
# request = signer_2.apply_join_in()
# cert = gm.approve_join_request(request)
# signer_2.verify_cert(cert)
# verifier_2 = Verifier(verifier_name='vr1',public_key_GM=gm.public_key)
# In[10]:

f=open('./hospital/HaveAuth.txt','r')
c=eval(f.read())
f.close()



msg='auth'
for x in c:
    verifier_1.verify_signature(signature=eval(c[x][-1]), m=msg)
    gm.open_signature(eval(c[x][-1]))

