import time, random
Num=2**32
#参数   
IV=0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
t= [0x79cc4519, 0x7a879d8a]
#10进制转2进制
def OtoB(i,length):
    b=list(bin(i)[2:])
    while len(b)<length:
        b.insert(0,'0')
    b=''.join(b)
    return b
#循环左移
def leftRotate(words,num):
    text=list(OtoB(words,32))
    i=0
    while i<num:
        temp=text.pop(0)
        text.append(temp)
        i=i+1
    text=''.join(text)
    return int(text,2)
#消息填充
def fill(msg):
    msg=bin(msg)[2:]#消息转换成二进制
    for i in range(4):
        if (len(msg)%4!=0):
            msg='0'+msg
        else:
            break
    l=len(msg)    
    k=448-(l+1)%512
    if k<0:
        k+=512
    msg=msg+'1'+'0'*k+OtoB(l,64)
    return msg


#置换函数
def P(x,mode):
    if mode == 0:
        ans = x^leftRotate(x,9)^leftRotate(x,17)
    else:
        ans = x^leftRotate(x,15)^leftRotate(x,23)
    return ans
#布尔函数
def T(j):
    if j<=15:
        return t[0]
    else:
        return t[1]
def FF(x,y,z,j):
    if ((j>=0)&(j<=15)):
        return x^y^z
    else:
        return (x&y)|(x&z)|(y&z)
#取反函数
def Not(a):
    a=OtoB(a,32)
    result = ''
    for ch in a:
        if ch == '1':
            result = result + '0'
        else:
            result = result + '1'
    return int(result,2)
def GG(x,y,z,j):
    if ((j>=0)&(j<=15)):
        return x^y^z
    else:
        return (x&y)|(Not(x)&z)   
#压缩函数
def Compress(IV,b,w,w1):
    tmp=[]
    for i in range(8):
        temp=IV[32*i:32*(i+1)]
        tmp.append(int(temp,2))
    for j in range(64):
        SS1=leftRotate((leftRotate(tmp[0],12)+tmp[4]+leftRotate(T(j),j%32))%Num,7)
        SS2=SS1^leftRotate(tmp[0],12)
        TT1=(FF(tmp[0],tmp[1],tmp[2],j)+tmp[3]+SS2+w1[j])%Num
        TT2=(GG(tmp[4],tmp[5],tmp[6],j)+tmp[7]+SS1+w[j])%Num
        tmp[3] = tmp[2]
        tmp[2] = leftRotate(tmp[1], 9)
        tmp[1] = tmp[0]
        tmp[0] = TT1
        tmp[7] = tmp[6]
        tmp[6] = leftRotate(tmp[5], 19)
        tmp[5] = tmp[4]
        tmp[4] = P(TT2,0)
    temp=OtoB(tmp[0],32)+OtoB(tmp[1], 32)+OtoB(tmp[2], 32)+OtoB(tmp[3], 32)+\
         OtoB(tmp[4], 32)+OtoB(tmp[5], 32)+OtoB(tmp[6], 32)+OtoB(tmp[7], 32)
    temp=int(temp,2)
    return temp^int(IV,2)
#消息扩展
def Expand(b):
    w=[]
    w1=[]
    for i in range(16):
        temp=b[i*32:(i+1)*32]
        w.append(int(temp,2))
    for j in range(16,68,1):
        tmp=P(w[j-16]^w[j-9]^leftRotate(w[j-3],15),1)^leftRotate(w[j-13],7)^w[j-6]
        w.append(tmp)
    for k in range(64):
        w1.append(w[k]^w[k+4])
    return w,w1
#迭代
def Iter(msg):
    n=int(len(msg)/512)
    v=[]
    v.append(OtoB(IV,256))
    for i in range(n):
        w,w1=Expand(msg[512*i:512*(i+1)])
        temp = Compress(v[i], msg[512 * i:512 * (i + 1)], w, w1)
        temp=OtoB(temp,256)
        v.append(temp)
    return v[n]
#SM3实现
def SM3(msg):
    msg=fill(msg)
    hex(int(msg,2))
    output=Iter(msg)
    output=hex(int(output,2))
    return output[2:]
#生日攻击
def birth_attack(n):
    for i in range(2**n):
        p=random.randint(0,(2**n)-1)
        q=random.randint(0,(2**n)-1)
        SM3_p=SM3(p)[:n//4]
        SM3_q=SM3(q)[:n//4]
        if SM3_p==SM3_q:
            print("生日攻击成功，尝试次数为",i)
            print("实现碰撞对应值为",SM3_p)
            return True
        elif i==(2**n)-1:
            print("生日攻击失败")

if __name__=="__main__":
    time1=time.time()
    birth_attack(8)
    time2=time.time()
    timesum=time2-time1
    print("运行时间为：",timesum,"s")
        
        
    
        


    

    
