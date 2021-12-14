#群签类，参数已经固定
#!/usr/bin/env python
# coding: utf-8

# Ref: 耿永军 等, "适合大群组的高效群签名方案改进", 华中科技大学学报, Vol. 37, 1999. 

# 部分参考:
# * 
# 卡米歇尔(Carmichael)函数,lambda(n), pp91, 现代密码学, 第4版.
# * 
# https://docs.sympy.org/latest/modules/ntheory.html#sympy.ntheory.generate.randprime

# In[1]:


from collections import namedtuple
from random import randint
from functools import reduce
from hashlib import sha1


# In[2]:


from sympy import randprime, isprime, gcd
from sympy.ntheory import totient, discrete_log, primitive_root, reduced_totient
from sympy.core.numbers import mod_inverse


# In[3]:


PrivateKeyGM = namedtuple('PrivateKeyGM', ['d','x'])
PublicKeyGM = namedtuple('PublicKeyGM', ['n','e','f','g','y'])
JoinRequestSigner = namedtuple('JoinRequestSigner', ['signer_name','z','p'])
CertForSigner = namedtuple('CertForSigner', ['r','s','w'])
KeepForOpen = namedtuple('KeepForOpen', ['signer_name','w','z'])
Signature = namedtuple('Signature', ['u','t','s1','s2'])


# In[4]:


class MixInUtil:
    def get_a_random_rZs(self, n,lower_bound=5): # 获取, 集合${_R}{Z}^{*}_{f}$中的一个元素.
            # print(lower_bound,n)
            #---
            # t = randint(lower_bound,n)
            # t = randprime(lower_bound,n) - 1
            while True: 
                t = randprime(lower_bound,n)
                if gcd(t,n)==1:
                    break
            return t
    
    def H(self, message):
        hash_obj = sha1()
        hash_obj.update(message.encode('utf-8'))
        return sum([ord(c) for c in hash_obj.hexdigest()])
        


# In[5]:



class GroupManager(MixInUtil): 
    keep_dict = {}
    private_key = None
    public_key = None
    phi_n = None
    
    def __init__(self, prime_range=[5,1000], verbose=False):
#         p = None
#         q = None
#         f = None
#         while not (isprime(p) and
#                    isprime(q) and
#                    p_!=f and q_!=f and p_!=q_):
# #             print('looking for: f,p,q')
#             p_ = randprime(*prime_range)
#             q_ = randprime(*prime_range)
#             f = randprime(*prime_range)
#             p = 2 * f * p_ + 1
#             q = 2 * f * q_ + 1
#
#         n = p*q
#         phi_n = (p-1)*(q-1)      # 或用: totient(n)
#         # print('phi_n:{}; f:{}; phi_n/f:{}'.format(phi_n,f,int(phi_n/f)))
#         #---获取 e
#         iter_count = 0
#         while True:
#             # print('\r{}) looking for: e'.format(iter_count), end='', flush=True)
#             e = randprime(prime_range[0],phi_n)
#             if gcd(e, phi_n)==1:
#                 d = mod_inverse(e,phi_n)
#                 print('')
#                 break
#             iter_count =+ 1
#
#         #---获取 g
#         iter_count = 0
#         while True:
# #             print('\r{}) looking for: g'.format(iter_count), end='', flush=True)   #
#             h = self.get_a_random_rZs(n)
#             # t = int(phi_n/f)              # 原文的第2页(67)第2栏第4行似乎有误, 欧拉函数应换成卡米歇尔(Carmichael)函数.
#             t = int(reduced_totient(n)/f)   # 卡米歇尔(Carmichael)函数,lambda(n), pp91, 现代密码学, 第4版.
#             g = pow(h, t, n)
#             # if verbose:
#             #     print('\r{}) looking for g: n:{} | g:{} | t:{} | h: {} |'.format(iter_count,n,g,t,h), end='', flush=True)   #
#             if g>1:
#                 print('')
#                 break
#             iter_count = iter_count + 1
#
#         x = self.get_a_random_rZs(f)
#         y = pow(g, x, n)
        
        #===
        # self.private_key  = PrivateKeyGM(d,x)
        # self.public_key   = PublicKeyGM(n,e,f,g,y)
        # self.p_           = p_
        # self.q_           = q_
        # self.p            = p
        # self.q            = q
        # self.n            = n
        # self.phi_n        = phi_n
        # self.h            = h

        self.private_key = PrivateKeyGM(d=563855816705931616314845255, x=1898227)
        self.public_key = PublicKeyGM(n=780567732442067355567247393, e=426369600063783374195114551, f=2886451, g=512052623558150884735906713, y=587102373567492054080659516)
        self.p_ = 3443819
        self.q_ = 6801143
        self.p = 19880829592739
        self.q = 39262332026987
        self.n = 780567732442067355567247393
        self.phi_n = 780567732442008212405627668
        self.h = 148423217502507875009625533
        
        #===
        if verbose:
            print('\n'*1 + '='*50)
            print('A GroupManager is initialized: ')
            self.show_info()
    
    def show_info(self,):
        print(repr(self.private_key))
        print(repr(self.public_key))
        print(
            ' p_: {},\n'.format(self.p_),
            'q_: {},\n'.format(self.q_),
            'p: {},\n'.format(self.p),
            'q: {},\n'.format(self.q),
            'n: {},\n'.format(self.n),
            'phi_n: {},\n'.format(self.phi_n),
            'h: {},\n'.format(self.h),
             )
    
    
    def approve_join_request(self,request):
        signer_name, z = request.signer_name, request.z
        d, x  = self.private_key.d, self.private_key.x
        f,n,g = self.public_key.f, self.public_key.n, self.public_key.g
        #---
        k = self.get_a_random_rZs(f)
        r = pow(g, k, n)
        digest = self.H(str(z)+str(r))
        s = (k - x * digest) % f
        g_inv = mod_inverse(g, n)
        z_inv = mod_inverse(z, n)
        w = (pow(g_inv, s*d, n) * pow(z_inv, d, n)) % n
        ff=open('./usersign.txt','r')
        aa=eval(ff.read())
        ff.close()
        if signer_name in aa:
            cert=eval(aa[signer_name]['cert'])
            w=eval(aa[signer_name]['w'])
            z_inv=eval(aa[signer_name]['z_inv'])
            g_inv=eval(aa[signer_name]['g_inv'])
            s=eval(aa[signer_name]['s'] )
            digest=eval(aa[signer_name]['digest'])
            r=eval(aa[signer_name]['r'])
            k=eval(aa[signer_name]['k'] )
            f=eval(aa[signer_name]['f'])
            n=eval(aa[signer_name]['n'] )
            g=eval(aa[signer_name]['g'])
            d=eval(aa[signer_name]['d'])
            z=eval(aa[signer_name]['z'])
        else:
            cert = CertForSigner(r,s,w)
            ff = open('./usersign.txt', 'r')
            aa = eval(ff.read())
            ff.close()
            aa[signer_name]={}
            aa[signer_name]['cert']=str(CertForSigner(r,s,w))
            aa[signer_name]['w'] = str(w)
            aa[signer_name]['z_inv']=str(z_inv)
            aa[signer_name]['g_inv'] = str(g_inv)
            aa[signer_name]['s'] = str(s)
            aa[signer_name]['digest'] = str(digest)
            aa[signer_name]['r'] = str(r)
            aa[signer_name]['k'] = str(k)
            aa[signer_name]['f'] = str(f)
            aa[signer_name]['n'] = str(n)
            aa[signer_name]['g'] = str(g)
            aa[signer_name]['d'] = str(d)
            aa[signer_name]['x'] = str(x)
            aa[signer_name]['z'] = str(z)

            ff = open('./usersign.txt', 'w')
            ff.write(str(aa))
            ff.close()

        self.keep_dict[signer_name] = KeepForOpen(signer_name,w,z)
        
        return cert
        
    
    def open_signature(self, signature=None, verbose=True):
        d         = self.private_key.d
        n         = self.public_key.n
        u,t,s1,s2 = signature.u, signature.t, signature.s1, signature.s2
        #---
        w = (pow(s2,d,n)*mod_inverse(t,n)) % n
        for name, keep in self.keep_dict.items():
            if w == keep.w:
                print('\nGM: the signer is {}'.format(keep.signer_name))
                return keep.signer_name
        print('\nGM: No such signer')
        return 'No'
        
        
#         keep = keep_dict[]


# In[6]:


class Signer(MixInUtil):
    join_equest_signer = None
    private_key = None
    public_key = None
    public_key_GM = None
    
    
    def __init__(self, signer_name=None, public_key_GM=None):
        self.signer_name = signer_name 
        self.public_key_GM = public_key_GM
        ff = open('./usersign.txt', 'r')
        aa = eval(ff.read())
        ff.close()
        if self.signer_name+'s' in aa:

            self.xA = eval(aa[signer_name+'s']['xa'])
        else:
            self.xA=self.get_a_random_rZs(public_key_GM.f)
            aa[signer_name+'s']={}
            aa[signer_name+'s']['xa']=str(self.xA)
            ff = open('./usersign.txt', 'w')
            ff.write(str(aa))
            ff.close()
    
    def apply_join_in(self,):
        g, n = self.public_key_GM.g, self.public_key_GM.n
        xA   = self.xA
        self.z  = pow(g,xA,n)
        # sympy.ntheory.residue_ntheory.discrete_log(n, a, b)
        # Compute the discrete logarithm of a to the base b modulo n.
        #  print(n, self.z, g)
        #  self.p = discrete_log(n, self.z, g)
        self.p = None
        self.join_request_signer = JoinRequestSigner(self.signer_name, self.z, self.p)
        return self.join_request_signer

    
    def verify_cert(self, cert, verbose=True):
        if verbose:
            print('\n{}: Obtained certificate from GM, {}'.format(self.signer_name, repr(cert)))
        #---
        z     = self.z
        r,s,w = cert.r,cert.s,cert.w
        g,e,n = self.public_key_GM.g, self.public_key_GM.e, self.public_key_GM.n
        y     = self.public_key_GM.y
        #---
        digest = self.H(str(z)+str(r))
        r_ = (pow(g,s,n)*pow(y,digest,n))%n
        #---
        assert r==r_
        print('\n{}: Certificate from GM is successfully verified'.format(self.signer_name))
        self.cert = cert
 
    
    def sign_message(self, m=None):
        print('\n{}: signning message, "{}"'.format(self.signer_name,m))
        z,xA    = self.z, self.xA
        r,s,w   = self.cert.r, self.cert.s, self.cert.w
        g,e,n,f = self.public_key_GM.g, self.public_key_GM.e, self.public_key_GM.n, self.public_key_GM.f
        #---
        ksai = self.get_a_random_rZs(f)
        t = pow(g,ksai,n)
        u = self.H(str(t)+str(m))
        s1 = (ksai + u*(s+xA-ksai*e)) % f
        s2 = (pow(g,ksai*e,n)*pow(w,e,n)) % n             
        
        return Signature(u,t,s1,s2)    # Signature = namedtuple('Signature', ['u','t','s1','s2'])


# In[7]:


class Verifier(MixInUtil):
    public_key_GM = None
    verifier_name = None
    def __init__(self, verifier_name, public_key_GM=None):
        self.verifier_name = verifier_name
        self.public_key_GM = public_key_GM
    
    def verify_signature(self, signature=None, m=None, verbose=True):
        g,n       = self.public_key_GM.g, self.public_key_GM.n
        u,t,s1,s2 = signature.u, signature.t, signature.s1, signature.s2
        t_ = (pow(g,s1,n)*pow(s2,u,n))%n
        u_ = self.H(str(t_)+str(m))
        if verbose:
            # print('t_: {}, t: {}, u_: {}, u: {}'.format(t_, t, u_, u)) 
            if u_==u:
                print('\n{}: Signature verified; the message is:\n\t"{}"'.format(self.verifier_name,m))
                return self.verifier_name
            else:
                print('\n{}: Oh NOOOOOOO, no can verify signature!!!'.format(self.verifier_name))   
                return 'no'


# In[8]:



# gm = GroupManager(prime_range=[5,10000000],verbose=True)
#
#
# # In[9]:
#
#
# signer_1 = Signer(signer_name='signer_1', public_key_GM=gm.public_key)
# request = signer_1.apply_join_in()
# cert = gm.approve_join_request(request)
# signer_1.verify_cert(cert)
# verifier_1 = Verifier(verifier_name='vr1',public_key_GM=gm.public_key)
#
#
#
# signer_2 = Signer(signer_name='signer_2', public_key_GM=gm.public_key)
# request = signer_2.apply_join_in()
# cert = gm.approve_join_request(request)
# signer_2.verify_cert(cert)
# verifier_2 = Verifier(verifier_name='vr1',public_key_GM=gm.public_key)
# # In[10]:
#
#
# msg='hello world'
# sg1 = signer_1.sign_message(m=msg)
#
# verifier_1.verify_signature(signature=sg1, m=msg)
# gm.open_signature(sg1)
#
# msg='hello world'
# sg2 = signer_2.sign_message(m=msg)
#
# verifier_1.verify_signature(signature=sg2, m=msg)
# gm.open_signature(sg2)
#
# # ## Group Signature
#
# # In[11]:
#
#
# signer_namelist = ['Alice','Bob','Charlie','Eve']
# group_signer = [Signer(signer_name=name, public_key_GM=gm.public_key) for name in signer_namelist]
# for s in group_signer:
#     request = s.apply_join_in()
#     cert = gm.approve_join_request(request)
#     s.verify_cert(cert)
#
#
# # In[12]:
#
#
# verifier_namelist = ['Jack','Queen','King']
# group_verifier = [Verifier(verifier_name=name, public_key_GM=gm.public_key) for name in verifier_namelist]
#
#
# # In[13]:
#
#
# msg01='hello world'
# msg02='python setup.py install'
# msg03='Some number theoretic functions'
#
#
# # In[14]:
#
#
# m=msg01
# sg=group_signer[2].sign_message(m=m)
# group_verifier[1].verify_signature(signature=sg1, m=m)
# gm.open_signature(sg)
#
#
# # In[15]:
#
#
# m=msg02
# sg=group_signer[1].sign_message(m=m)
# group_verifier[1].verify_signature(signature=sg, m=m)
# gm.open_signature(sg)
#
#
# # <br><br><br><br>
#
# # <br><br>
# # <br><br>
