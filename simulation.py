""" 模拟社会
by waterfish"""
import numpy as np
import math
import random
import pygame

nf=10 #农民人口
nw=5 #工人人口
nb=2 #商人人口
nt=2 #税务官人口
npl=1 #民生官员人口
nm=1 #军事官员人口
ntea=0 #教师人口
ng=1 #总督人口
nser=nt+npl+nm+ntea+ng #公务员总人口

'''定义智力'''

inf=np.random.normal(50, 15, nf)
inw=np.random.normal(loc=50, scale=15, size=nw)
inb=np.random.normal(loc=50, scale=15, size=nb)

'''赋予初始资产a1（粮食），初始产品累积a2，国库为a3，初始满意度s为8，
bf,bw为要农民、工人出售的粮食、产品量，b为公务员需要购买产品量，
fp为农民购买产品的价格food price，pp为工人产品售价product price,
bp为商人总收益,bc为商人总成本,商人向农民售价与成本的倍数为cp,Commodity Price,直接给出两个商人的价位'''
a1f=np.ones(nf)*40
a1w=np.ones(nw)*40
a1b=np.ones(nb)*40
a1t=np.ones(nt)*40
a1pl=np.ones(npl)*40
a1m=np.ones(nm)*40
a1tea=np.ones(ntea)*40
a1g=np.ones(ng)*40
a1ser=np.ones(nser)*40
'''考虑加入一个公务员序列，这样不用写很多'''

a2f=np.ones(nf)*0
a2w=np.ones(nw)*0
a2b=np.ones(nb)*0
a2t=np.ones(nt)*0
a2pl=np.ones(npl)*0
a2m=np.ones(nm)*0
a2tea=np.ones(ntea)*0
a2g=np.ones(ng)*0
a2ser=np.ones(nser)*0
a2b1=np.ones(nb)*0

a3=0

sf=np.ones(nf)*8
sw=np.ones(nw)*8
sb=np.ones(nb)*8
st=np.ones(nt)*8
spl=np.ones(npl)*8
sm=np.ones(nm)*8
stea=np.ones(ntea)*8
sg=np.ones(ng)*8
sser=np.ones(nser)*8

bf=np.ones(nf)
bw=np.ones(nw)
b=0

fp=np.ones(nf)
pp=2.02
bp=np.ones(nb)
bc=np.ones(nb)
cp=np.ones(nb)*12
    
smilitary=0
print("您好长官，我们的国家由您来领导。")
print('目前公民分为农民、商人、工人、公务员四个阶级，您需要调控税收来满足他们对于粮食和产品的需求，并充实自己的国库。满意度过低或者过高可能会导致他们成为罪犯！')
print('请沉着应对突发的天灾和战争')
print('祝您好运！')

a=0.5
bb=0
aaa=0
war=0
anger=0
ywar=0
continue1=0
#aaa为0，未探索状态；aaa为1，与慷慨帝国相遇；aaa为2，与霸权帝国相遇；war等于0，和平；等于1，开战



a="y"
'''输入各种参数，有重新输入机会'''
while a=="y":
    
    year=100
    y=0
    
    
    tc=2
    
    y=0
    '''输入税率'''
    rtax=2
    while rtax<0 or rtax>1:
        try:
            rtax=input("请输入农民税率(0-1之间，默认0.05)：")
            rtax=float(rtax)
           
        except:
            rtax=0.05
    rtax1=2
    while rtax1<0 or rtax1>1:
        try:
            rtax1=input("请输入工人税率(0-1之间，默认0.1)：")
            rtax1=float(rtax1)
           
        except:
            rtax1=0.1
    rtax2=2
    while rtax2<0 or rtax2>1:
        try:
            rtax2=input("请输入商人税率(0-1之间，默认0.2)：")
            rtax2=float(rtax2)
           
        except:
            rtax2=0.2
    tax=0
    '''总税款tax，税率rtax'''
    ser=-10
    while ser==-10:
        try:
            ser=input("请输入公务员工资(默认20)：")
            ser=float(ser)
           
        except:
            ser=20
    
    
    print("游戏将进行",year,"年")
    print("运输成本为",tc)
    print("农民税率为",rtax)
    print("工人税率为",rtax1)
    print("商人税率为",rtax2)
    print("公务员工资为",ser)
    a=input("是否重新输入？（y/n）")

disas=0
pdisas=0.1
pharvest=0.2
pf=np.ones(nf)
pw=np.ones(nw)

while y<year:
    y +=1
    tax=0
    print('现在是第',y,'年')
    '''天灾系统，在五年后生效，会随机造成减产；也会出现丰收可能'''
    px=0
    #修正参数
    if y<=5:
        pa=random.random()
        if pa>0.66:
            disas=-0.2
            print('改革春风吹满地！增产20%')


    if y>5:
        pa=random.random()
        

        if y<15:
            
            if 4*pa>pdisas:
                disas=0.2
                print("天灾来临,减产20%")
            elif pa<1-pharvest:
                if pa>0.5:
                    disas=-0.3

                    print('粮食大丰收，洪水被赶跑！增产30%')
                else:
                    print('百姓安居乐业，齐夸党的领导！增产30%')
            
        else:
            
            if pa<pdisas-px:
                disas=0.8
                px+=0.05
                print('天灾蹂躏大地，减产80%')
                if px>0.04:
                    print('获得成就：天灾如影，常伴吾形')
            elif pa<3*pdisas-px:
                disas=0.5
                px+=0.03
                print('天灾扫过荒野，减产50%')
            elif pa<5*pdisas-px:
                disas=0.2
                px+=0.01
                print('天灾降临人间，减产20%')
            elif pa>1-pharvest*3/5:
                px=0
                
                if pa>0.5:
                    disas=-0.3

                    print('粮食大丰收，洪水被赶跑！增产40%')
                else:
                    print('百姓安居乐业，齐夸党的领导！增产40%')
            else:
                px=0
            
       
                
        
    '''计算农民、工人收益。并且农民计算粮食满意度，工人计算产品满意度'''
    for i in range(0,nf):
        if sf[i]>-10 and sf[i]<15:
            '''满意度在正常范围内'''
            pf[i]=(130+30*(inf[i]-50)/100)*(1-disas)
            tax=tax+pf[i]*rtax
            a1f[i]=a1f[i]+pf[i]*(1-rtax)
            bf[i]=a1f[i]-10-20
            '''用于购买商品的粮食为储备扣除需求，扣除储备需求'''
            if a1f[i]<10:
                bf[i]=0
                sf[i]=sf[i]-5
            else:
                if a1f[i]<30:
                    bf[i]=0
                    sf[i]=sf[i]-2
                else:
                    sf[i]=sf[i]+0.5
    for i in range(0,nw):
        if sw[i]>-10 and sw[i]<15:
            pw[i]=15+3*(inw[1]-50)/100
            if a1w[i]>pw[i]*2:
                a2w[i]=a2w[i]+pw[i]
                a1w[i]-=2*pw[i]
            else:
                pw[i]=a1w[i]/2
                a2w[i]=a2w[i]+pw[i]
                a1w[i]=0
                '''生产一个产品的成本为2，如果成本不足则全部生产'''
            if sw[i]>10 and sw[i]<15:
                if a2w[i]<2-(sw[i]-10)*(sw[i]-15)/3:
                    bw[i]=0
                    a2w[i]=0
                    sw[i]-=2
                elif a2w[i]<6-(sw[i]-10)*(sw[i]-15):
                    bw[i]=0
                    a2w[i]-=2-(sw[i]-10)*(sw[i]-15)/3
                else:
                    bw[i]=a2w[i]-6+(sw[i]-10)*(sw[i]-15)
                    a2w[i]-=2-(sw[i]-10)*(sw[i]-15)/3
                    sw[i]=sw[i]+0.5
            else:
                if a2w[i]<2:
                    bw[i]=0
                    a2w[i]=0
                    sw[i]-=2
                elif a2w[i]<6:
                    bw[i]=0
                    a2w[i]-=2
                else:
                    bw[i]=a2w[i]-6
                    a2w[i]-=2
                    sw[i]=sw[i]+0.5
                    
                
            if a1w[i]<30:
                pp1=(30-a1w[i])/(bw[i]*(1-rtax1))
                if pp<pp1:
                    pp=pp1
                    '''粮食不足需求时按照需求定价，超过需求时，定价不低于2.02。生产成本为2'''


    '''下面是商人购买过程，对于两个商人的时候'''
   
        
    for i in range(0,nw):
            for j in range(0,nb):
                if i%nb==j:
                    '''一半给商人1，一半给商人2'''
                    
                    a1w[i]=a1w[i]+pp*bw[i]*(1-rtax1)
                    a1b[j]=a1b[j]-pp*bw[i]
                    a2b[j] +=a2w[i]
                    
                    tax +=pp*a2w[i]*rtax1
                    bc[j] +=pp*bw[i]
                    bw[i]=0
    '''下面直接将商人的产品满意度进行判断，减去其所需'''
    for i in range(0,nb):
        if sb[i]>10 and sb[i]<15:

            if a2b[i]<2-(sb[i]-10)*(sb[i]-15)/3:
                a2b[i]=0
                sb[i]-=2
            elif a2w[i]<6-(sb[i]-10)*(sb[i]-15):
                a2b[i]-=2-(sb[i]-10)*(sb[i]-15)/3
            else:
                a2b[i]-=2-(sb[i]-10)*(sb[i]-15)/3
                sb[i]=sb[i]+0.5
        else:

            if a2b[i]<2:
                a2b[i]=0
                sb[i]=sb[i]-2
            elif a2w[i]<6:
                a2b[i]-=2
            else:
                a2b[i]-=2
                sb[i]=sb[i]+0.5
    '''对政府官员销售'''

    for i in range(0,nser):
            for j in range(0,nb):
                if i%nb==j:
                    if sser[i]>10 and sser[i]<15:
                        if a2ser[i]<6-(sser[i]-10)*(sser[i]-15):
                            '''产品少于需求的时候才买'''
                            b=6-(sser[i]-10)*(sser[i]-15)-a2ser[i]
                            #根据满意度和产品剩余量计算出需要购买的产品量b
                            
                            if a1ser[i]<30:
                                b=0
                            elif a1ser[i]<30+b*1.1*pp:
                                b=(a1ser[i]-30)/(1.1*pp)
                                if a2b[j]==0:
                                    break

                                if b>a2b[j]:
                                    a2ser[i]+=a2b[j]                                    
                                    a1ser[i]-=1.1*pp*a2b[j]
                                    a1b[j]+=1.1*pp*a2b[j]
                                    bp[j] +=1.1*pp*a2b[j]
                                    a2b[j]=0
                                else:

                                    a2ser[i] +=b
                                    a1ser[i]=30
                                    a1b[j] +=a1ser[i]-30
                                    a2b[j]=a2b[j]-b
                                    bp[j] +=a1ser[i]-30
                            else:                                
                                if a2b[j]==0:
                                    break
                                if b>a2b[j]:
                                    a2ser[i]+=a2b[j]                                    
                                    a1ser[i]-=1.1*pp*a2b[j]
                                    a1b[j]+=1.1*pp*a2b[j]
                                    bp[j] +=1.1*pp*a2b[j]
                                    a2b[j]=0
                                else:
                                   
                                    a1ser[i]=a1ser[i]-b*1.1*pp
                                    a2ser[i]=a2ser[i]+b
                                    a1b[j]+=b*1.1*pp
                                    a2b[j]=a2b[j]-b
                                    bp[j] +=b*1.1*pp
                    elif sser[i]>0 and sser[i]<=10:
                        if a2ser[i]<6:
                            '''产品少于需求的时候才买'''
                            b=6-a2ser[i]
                            #根据满意度和产品剩余量计算出需要购买的产品量b
                            if a1ser[i]<30:
                                b=0
                            elif a1ser[i]<30+b*1.1*pp:
                                b=(a1ser[i]-30)/(1.1*pp)
                                if a2b[j]==0:
                                    break

                                if b>a2b[j]:
                                    a2ser[i]+=a2b[j]                                    
                                    a1ser[i]-=1.1*pp*a2b[j]
                                    a1b[j]+=1.1*pp*a2b[j]
                                    bp[j] +=1.1*pp*a2b[j]
                                    a2b[j]=0
                                else:

                                    a2ser[i] +=b
                                    a1ser[i]=30
                                    a1b[j] +=a1ser[i]-30
                                    a2b[j]=a2b[j]-b
                                    bp[j] +=a1ser[i]-30
                            else:                                
                                if a2b[j]==0:
                                    break
                                if b>a2b[j]:
                                    a2ser[i]+=a2b[j]                                    
                                    a1ser[i]-=1.1*pp*a2b[j]
                                    a1b[j]+=1.1*pp*a2b[j]
                                    bp[j] +=1.1*pp*a2b[j]
                                    a2b[j]=0
                                else:
                                   
                                    a1ser[i]=a1ser[i]-b*1.1*pp
                                    a2ser[i]=a2ser[i]+b
                                    a1b[j]+=b*1.1*pp
                                    a2b[j]=a2b[j]-b
                                    bp[j] +=b*1.1*pp
                    else:
                        '''满意度过高或者过低的情况，会先从国库偷钱'''
                        

                        t=abs(sser[i]-7.5)-7.5
                        if 0.1*a3>20*t:
                            t=0.005*a3

                        a3=a3-20*t
                        a1ser[i]+=20*t
                        if a2ser[i]<6:
                            b=6-a2ser[i]
                           
                            if a1ser[i]<30:
                                b=0
                            elif a1ser[i]<30+b*1.1*pp:
                                b=(a1ser[i]-30)/(1.1*pp)
                                if a2b[j]==0:
                                    break

                                if b>a2b[j]:
                                    a2ser[i]+=a2b[j]                                    
                                    a1ser[i]-=1.1*pp*a2b[j]
                                    a1b[j]+=1.1*pp*a2b[j]
                                    bp[j] +=1.1*pp*a2b[j]
                                    a2b[j]=0
                                else:

                                    a2ser[i] +=b
                                    a1ser[i]=30
                                    a1b[j] +=a1ser[i]-30
                                    a2b[j]=a2b[j]-b
                                    bp[j] +=a1ser[i]-30
                                
                            else: 
                                if a2b[j]==0:
                                    break
                                if b>a2b[j]:
                                    a2ser[i]+=a2b[j]                                    
                                    a1ser[i]-=1.1*pp*a2b[j]
                                    a1b[j]+=1.1*pp*a2b[j]
                                    bp[j] +=1.1*pp*a2b[j]
                                    a2b[j]=0
                                else:
                                   
                                    a1ser[i]=a1ser[i]-b*1.1*pp
                                    a2ser[i]=a2ser[i]+b
                                    a1b[j]+=b*1.1*pp
                                    a2b[j]=a2b[j]-b
                                    bp[j] +=b*1.1*pp

      
    j=0
    for i in range(0,nt):
        
        a1t[i]=a1ser[j]
        a2t[i]=a2ser[j]
        st[i]=sser[j]
        j+=1
    for i in range(0,npl):
        a1pl[i]=a1ser[j]
        a2pl[i]=a2ser[j]
        spl[i]=sser[j]
        j+=1
    for i in range(0,nm):
        a1m[i]=a1ser[j]
        a2m[i]=a2ser[j]
        sm[i]=sser[j]
        j+=1
    for i in range(0,ntea):
        a1tea[i]=a1ser[j]
        a2tea[i]=a2ser[j]
        stea[i]=sser[j]
        j+=1
    for i in range(0,ng):
        a1g[i]=a1ser[j]
        a2g[i]=a2ser[j]
        sg[i]=sser[j]
        j+=1
    '''以上是把公务员的参数分给各个岗位'''

    '''下面考虑对农民销售'''
    for j in range(0,nb):
        if a2b[j]<nf*(6+6.25):
            a1b[j]=a1b[j]-tc*a2b[j]
            bc[j]+=tc*a2b[j]
            a2b1[j]=0
            #运输成本
        else:
            a2b1[j]=a2b[j]-nf*(6+6.25)
            a2b[j]=nf*(6+6.25)
    cp=np.ones(nb)*10    
    for k in range(1,12):
        for l in range(0,nb):
            if cp[l]>2:
                cp[l]-=1
            else:
                cp[l]=1.01
        for i in range(0,nf):
                for j in range(0,nb):
                    if i%nb==j:
                        if sf[i]>10 and sf[i]<15:
                            if a2f[i]<6-(sf[i]-10)*(sf[i]-15):
                                b=6-(sf[i]-10)*(sf[i]-15)-a2f[i]
                                
                                fp[i]=bf[i]/b
                                
                                if fp[i]>=cp[j]*(pp+tc):
                                    if a2b[j]==0:
                                        
                                        break
                                    
                                    if b>a2b[j]:
                                        
                                        a2f[i]+=a2b[j]                                    
                                        a1f[i]-=cp[j]*(pp+tc)*a2b[j]
                                        a1b[j]+=cp[j]*(pp+tc)*a2b[j]
                                        bp[j] +=cp[j]*(pp+tc)*a2b[j]
                                        a2b[j]=0
                                    else:
                                        a2f[i] +=b
                                        a1f[i] -=b*cp[j]*(pp+tc)
                                        a1b[j] +=b*cp[j]*(pp+tc)
                                        a2b[j] -=b
                                        bp[j] +=b*cp[j]*(pp+tc)
                                                                   
                        else:
                            '''对于幸福度不在（10，15）的情况'''
                            if a2f[i]<6:
                                b=6-a2f[i]
                                fp[i]=bf[i]/b
                               
                                if fp[i]>=cp[j]*(pp+tc):
                                    if a2b[j]==0:
                                        
                                        break

                                    if b>a2b[j]:
                                        a2f[i]+=a2b[j]                                    
                                        a1f[i]-=cp[j]*(pp+tc)*a2b[j]
                                        a1b[j]+=cp[j]*(pp+tc)*a2b[j]
                                        bp[j] +=cp[j]*(pp+tc)*a2b[j]
                                        a2b[j]=0
                                    else:
                                        
                                        a2f[i] +=b
                                        a1f[i] -=b*cp[j]*(pp+tc)
                                        a1b[j] +=b*cp[j]*(pp+tc)
                                        a2b[j] -=b
                                        bp[j] +=b*cp[j]*(pp+tc)

    '''下面考虑产品过于贵，以上流程没有将产品卖完，农民采用最低价尽可能买入'''
    for i in range(0,nf):
        for j in range(0,nb):
            if i%nb==j:
                if sf[i]>10 and sf[i]<15:
                    if a2f[i]<2-(sf[i]-10)*(sf[i]-15)/3:
                        b=bf[i]/(cp[j]*(pp+tc))
                                               
                        if a2b[j]==0:
                               
                            break
                                    
                        if b>a2b[j]:
                            a2f[i]+=a2b[j]                                    
                            a1f[i]-=cp[j]*(pp+tc)*a2b[j]
                            a1b[j]+=cp[j]*(pp+tc)*a2b[j]
                            bp[j] +=cp[j]*(pp+tc)*a2b[j]
                            a2b[j]=0
                        else:
                            a2f[i] +=b
                            a1f[i] -=b*cp[j]*(pp+tc)
                            a1b[j] +=b*cp[j]*(pp+tc)
                            a2b[j] -=b
                            bp[j] +=b*cp[j]*(pp+tc)
          

                
    '''下面计算商人税收'''
    for i in range(0,nb):
        if bp[i]>bc[i]:
            a1b[i]-=(bp[i]-bc[i])*rtax2
            tax+=(bp[i]-bc[i])*rtax2
        '''有收益才需要交税'''
        a2b[i]+=a2b1[i]
    
    '''计算公务员收入和国库'''
    a3+=tax
    for i in range(0,nser):
        a1ser[i]+=ser
        a3-=ser
  
        
    j=0    
    for i in range(0,nt):
        
        a1t[i]=a1ser[j]
        a2t[i]=a2ser[j]
        st[i]=sser[j]
        j+=1
    for i in range(0,npl):
        a1pl[i]=a1ser[j]
        a2pl[i]=a2ser[j]
        spl[i]=sser[j]
        j+=1
    for i in range(0,nm):
        a1m[i]=a1ser[j]
        a2m[i]=a2ser[j]
        sm[i]=sser[j]
        j+=1
    for i in range(0,ntea):
        a1tea[i]=a1ser[j]
        a2tea[i]=a2ser[j]
        stea[i]=sser[j]
        j+=1
    for i in range(0,ng):
        a1g[i]=a1ser[j]
        a2g[i]=a2ser[j]
        sg[i]=sser[j]
        j+=1

    '''计算消耗和满意度,国库会补贴农民和工人'''
    for i in range(0,nf):
        if a1f[i]<10 and sf[i]<=2:
            a1f[i]+=10
            a3-=10
            #国库补贴
        if sf[i]>10 and sf[i]<15:
            if a2f[i]<2-(sf[i]-10)*(sf[i]-15)/3:
                a2f[i]=0
                sf[i]-=2
            elif a2f[i]<6-(sf[i]-10)*(sf[i]-15):
                a2f[i]-=2-(sf[i]-10)*(sf[i]-15)/3
            else:
                a2f[i]-=2-(sf[i]-10)*(sf[i]-15)/3
                sf[i]+=0.5                
        else:
            if a2f[i]<2:
                a2f[i]=0
                sf[i]-=5
            elif a2f[i]<6:
                a2f[i]-=2
            else:
                a2f[i]-=2
                sf[i]+=0.5
                
    for i in range(0,nw):
        if a1w[i]<10 and sw[i]<=2:
            a1w[i]+=10
            a3-=10
            #国库补贴
        if a1w[i]<10:
            a1w[i]=0
            sw[i]-=5
        elif a1w[i]<30:
            a1w[i]-=10
            sw[i]-=2
        else:
            a1w[i]-=10
            sw[i]+=0.5

            
    for i in range(0,nb):
        #商人无补贴，粮食可以负债，粮食不足时成本价出卖产品
        if a1b[i]<0:
            #商人粮食不足，出卖产品
            if a1b[i]+2*a2b[i]<30:
                a2b[i]=0
                a1b[i]+=2*a2b[i]
            else:
                delta=a1b[i]
                a1b[i]=30
                a2b[i]-=(30-a1b[i])/2
            
            
        else:
            if a1b[i]<10:
                a1b[i]-=10
                sb[i]-=5
            elif a1b[i]<30:
                a1b[i]-=10
                sb[i]-=2
            else:
                a1b[i]-=10
                sb[i]+=0.5
            
    for i in range(0,nser):
        if a1ser[i]<10:
            a1ser[i]=0
            sser[i]-=5
        elif a1ser[i]<30:
            a1ser[i]-=10
            sser[i]-=2
        else:
            a1ser[i]-=10
            sser[i]+=0.5

        if sser[i]>10 and sser[i]<15:
            if a2ser[i]<2-(sser[i]-10)*(sser[i]-15)/3:
                a2ser[i]=0
                sser[i]-=2
            elif a2ser[i]<6-(sser[i]-10)*(sser[i]-15):
                a2ser[i]-=2
            else:
                a2ser[i]-=2
                sser[i]+=0.5                
        else:
            if a2ser[i]<2:
                a2ser[i]=0
                sser[i]-=2
            elif a2ser[i]<6:
                a2ser[i]-=2
            else:
                a2ser[i]-=2
                sser[i]+=0.5
    j=0    
    for i in range(0,nt):
        
        a1t[i]=a1ser[j]
        a2t[i]=a2ser[j]
        st[i]=sser[j]
        j+=1
    for i in range(0,npl):
        a1pl[i]=a1ser[j]
        a2pl[i]=a2ser[j]
        spl[i]=sser[j]
        j+=1
    for i in range(0,nm):
        a1m[i]=a1ser[j]
        a2m[i]=a2ser[j]
        sm[i]=sser[j]
        j+=1
    for i in range(0,ntea):
        a1tea[i]=a1ser[j]
        a2tea[i]=a2ser[j]
        stea[i]=sser[j]
        j+=1
    for i in range(0,ng):
        a1g[i]=a1ser[j]
        a2g[i]=a2ser[j]
        sg[i]=sser[j]
        j+=1
    '''计算阶级内最穷和最穷阶级'''
    avef=0
    avew=0
    aveser=0
    t=0
    least=a1f[0]+3*a2f[0]
    for i in range(0,nf):
        avef+=a1f[i]+3*a2f[i]
        if least>a1f[i]+3*a2f[i]:
            least=a1f[i]+3*a2f[i]
            t=i
    sf[t]-=0.4
    avef=avef/nf

    t=0
    least=a1w[0]+3*a2w[0]
    for i in range(0,nw):
        avew+=a1w[i]+3*a2w[i]
        if least>a1w[i]+3*a2w[i]:
            least=a1w[i]+3*a2w[i]
            t=i
    sw[t]-=0.4
    avew=avew/nw

    t=0
    least=a1ser[0]+3*a2ser[0]
    for i in range(0,nser):
        aveser+=a1ser[i]+3*a2ser[i]
        if least>a1ser[i]+3*a2ser[i]:
            least=a1ser[i]+3*a2ser[i]
            t=i
    sser[t]-=0.4
    aveser=aveser/nser
    b=[avef,avew,aveser]
    b1=np.min(b)
    b11=np.max(b)

    b2=np.where(b==b1)
    try:
        b3=b2[0][1]
        '''这说明b2中至少有两个元素，至少有两个阶级相等，都不减去满意度'''
    except:
        
        b3=b2[0][0]
        bear=0
        if b11>b1+10:
            d=b11-b1
            bear+=1
            if bear>1:
                bear=0
                if b3==0:
                    for i in range(0,nf):
                        sf[i]-=1.3*(math.atan(40)+math.atan(2*d-40))
                if b3==1:
                    for i in range(0,nw):
                        sw[i]-=1.3*(math.atan(40)+1.2*math.atan(2*d-40))
                if b3==2:
                    for i in range(0,nser):
                        sser[i]-=1.3*(math.atan(40)+1.2*math.atan(2*d-40))
    '''下面开始结算满意度对周围人的影响,cr为罪犯数量'''
    cr=0
    for i in range(0,nf):
        if sf[i]<0 and sf[i]>-10:
            sf[i-1]-=0.1*(sf[i])
            sf[i-2]-=0.1*(sf[i])
        elif sf[i]<-10 or sf[i]>20:
            j=abs(sf[i]-2.5)
            sf[i-1]-=1*(j-12.5)
            sf[i-2]-=1*(j-12.5)
            cr+=1
    for i in range(0,nw):
        if sw[i]<0 and sw[i]>-10:
            sw[i-1]-=0.2*(sw[i])
            sw[i-2]-=0.2*(sw[i])
        elif sw[i]<-10 or sw[i]>20:
            j=abs(sw[i]-2.5)
            sw[i-1]-=1*(j-12.5)
            sw[i-2]-=1*(j-12.5)
            cr+=1

    for i in range(0,nser):
        if sser[i]<0 and sser[i]>-10:
            sser[i-1]-=0.2*(sser[i])
            sser[i-2]-=0.2*(sser[i])
        elif sser[i]<-10 or sser[i]>20:
            j=abs(sser[i]-2.5)
            sser[i-1]-=1*(j-12.5)
            sser[i-2]-=1*(j-12.5)
            cr+=1
    if cr==0:
        #无罪犯时全员满意度加0.1
        for i in range(0,nf):
            sf[i]+=0.1
        for i in range(0,nw):
            sw[i]+=0.1
        for i in range(0,nser):
            sser[i]+=0.1
        for i in range(0,nb):
            sb[i]+=0.1

    j=0    
    for i in range(0,nt):
        a1t[i]=a1ser[j]
        a2t[i]=a2ser[j]
        st[i]=sser[j]
        j+=1
    for i in range(0,npl):
        a1pl[i]=a1ser[j]
        a2pl[i]=a2ser[j]
        spl[i]=sser[j]
        j+=1
    for i in range(0,nm):
        a1m[i]=a1ser[j]
        a2m[i]=a2ser[j]
        sm[i]=sser[j]
        j+=1
    for i in range(0,ntea):
        a1tea[i]=a1ser[j]
        a2tea[i]=a2ser[j]
        stea[i]=sser[j]
        j+=1
    for i in range(0,ng):
        a1g[i]=a1ser[j]
        a2g[i]=a2ser[j]
        sg[i]=sser[j]
        j+=1
    while war!='否':
        try:
            war=input('是否加入战争模式（是/否）')
            
        except:
            print('请重新输入')
            war='是'

    while war!='否':
       

        '''战争系统，实现国库的消耗并体现随机性'''
     
        if y>5:
            if aaa==0:
                p=random.random()
                if p<0.5+bb:
                    print('暂无外交风波')
                    bb+=0.15
                else:
                    p=random.random()
                    if p<0.25:

                        print('收到消息：我帝国物产丰盈，无所不有。国库+1000')
                        a3+=2000
                        print('成就：大国的见面礼')
                        mood=80
                        #mood为大国忍耐度

                        aaa=1
                    else:
                        print('收到消息：臣服于我，否则帝国的铁骑将荡平你的国家')
                        mood=75
                        aaa=2
            '''下面是与慷慨帝国交流状态'''
            if aaa==1:
                if mood>60:
                    print('你好我的朋友，看来我们需要一些友好交换')
                    player=input('是否进贡（是/否）')
                    if player=='是':
                        deltat=600+400*random.random()
                        a3-=deltat
                        mood+=2
                        print('国库失去',deltat)
                        p=random.random()
                        if p>0.25:
                            print('我们的友谊长青')
                            deltat=600+800*random.random()

                            a3+=deltat
                            print('国库获得',deltat)
                    else:
                        mood-=5
                        p=random.random()
                        if p>0.6:

                            print('我们的友谊不经考验吗？')
                        elif p>0.33:
                            print('我们仍留有回旋余地')
                        else:
                            print('望你好自为之')
                        deltat=800
                        a3+=deltat
                        print('国库获得',deltat)
                else:
                    print('我们已经解除外交关系')
                    ywar+=1
                    
                    #定义战争年份和总军费，帮助计算军费
                    p=random.random()
                    i=1
                    while i==1:
                        try:
                            military=input('目前有开战风险，请输入军费投入（大于等于零）')
                            military=int(military)
                            smilitary+=military
                            i=0
                            if military<0:
                                i=1
                                print('这是军费！不能克扣！')                            
                        except:
                            i=1
                            
                    if p>mood/60:
                        mood-=6
                        
                    else:
                        print('你已经挑战了我们的底线，现在开战！')
                        player=1

                        while player!=3:
                            try:
                                player=input('赔款（1），迎战（2）')
                                player=int(player)
                                if player==1:
                                    a3-=1200+200*p
                                    mood+=8
                                    player=3
                                if player==2:
                                    #开战状态
                                    mood-=6
                                    player=3
                                    p=random.random()
                                    pwin=smilitary/(smilitary+800*(ywar))
                                    if pwin>0.8:
                                        print('轻取敌军，大捷！')
                                        a3+=1500+500*p
                                        print('缴获战利品',1500+500*p)
                                        mood+=10
                                    if pwin<0.2:
                                        print('脆败')
                                        a3-=1800+500*p
                                        print('战争赔款',1800+500*p)
                                        mood+=12
                                    else:
                                        print('激烈的战斗！')
                                        input('任意键继续')
                                        if pwin>p:
                                            print('惨烈的胜利！')
                                            a3+=700+600*p
                                            print('国库获得',700+600*p)
                                            
                                        if pwin<p:
                                            print('功亏一篑')
                                            a3-=650+600*p
                                            print('赔款',650+600*p)
                                            mood+=4
                                        else:
                                            print('两败俱伤')
                                            a3-=400
                                            print('补给消耗',400)
                                            mood+=5
                                       
                            except:
                                player=1
                            


                        i=1
                        while i==1:
                            try:
                                military=input('目前有开战风险，请输入军费投入（大于等于零）')
                                military=int(military)
                                smilitary+=military
                                i=0
                                if military<0:
                                    i=1
                                    print('这是军费！不能克扣！')                            
                            except:
                                i=1
            '''下面是与霸权帝国交流状态'''
            if aaa==2:
                if mood>60:
                    print('你好，我们需要一些贡品')
                    player=input('是否进贡（是/否）')
                    if player=='是':
                        deltat=700+400*random.random()
                        a3-=deltat
                        mood+=2
                        print('国库失去',deltat)
                       
                        
                    else:
                        mood-=6
                        p=random.random()
                        if p>0.6:

                            print('看来你们有自己的想法')
                        elif p>0.33:
                            print('你们服从性太差')
                        else:
                            print('望你好自为之')
                      
                else:
                    print('我们已经解除外交关系')
                    ywar+=1
                    
                    #定义战争年份和总军费，帮助计算军费
                    p=random.random()
                    i=1
                    while i==1:
                        try:
                            military=input('目前有开战风险，请输入军费投入（大于等于零）')
                            military=int(military)
                            smilitary+=military
                            i=0
                            if military<0:
                                i=1
                                print('这是军费！不能克扣！')                            
                        except:
                            i=1
                    try:
                        i=input('按1显示军备情况')
                        i=int(i)
                        if i==1:
                            print('目前是开战的第',ywar,'年')
                            print('投入总军费',smilitary)
                    except:
                        i=1

                    if p>mood/60:
                        mood-=6
                        
                    else:
                        print('你已经挑战了我们的底线，现在开战！')
                        player=1

                        while player!=5:
                            try:
                                player=input('赔款（1），迎战（2）')
                                player=int(player)
                                if player==1:
                                    a3-=1200+200*p
                                    mood+=8
                                    player=5
                                if player==2:
                                    #开战状态
                                    mood-=6
                                    p=random.random()
                                    pwin=smilitary/(smilitary+800*(ywar))
                                    player=5
                                    if pwin>0.8:
                                        print('轻取敌军，大捷！')
                                        a3+=1500+500*p
                                        print('缴获战利品',1500+500*p)
                                        mood+=10
                                    elif pwin<0.2:
                                        print('脆败')
                                        a3-=1800+500*p
                                        print('战争赔款',1800+500*p)
                                        mood+=12
                                    else:
                                        print('激烈的战斗！')
                                        input('任意键继续')
                                        if pwin>p:
                                            print('惨烈的胜利！')
                                            a3+=700+600*p
                                            print('国库获得',700+600*p)
                                            
                                        if pwin<p:
                                            print('功亏一篑')
                                            a3-=650+600*p
                                            print('赔款',650+600*p)
                                            mood+=4
                                        else:
                                            print('两败俱伤')
                                            a3-=400
                                            print('补给消耗',400)
                                            mood+=5
                                       
                            except:
                                player=1
                            

                    
                    
                    
                        
                        
                    
            

    
    
    if cr>=8:
        print('罪犯数为',cr,'游戏结束')
        break
    if a3>=20000:
        print('国库储蓄为',a3,'游戏胜利')
        if continue1!=1:
            print('仍可继续')
            continue1=1
        

        
    if a3<=-20000:
        print('国库负债为',-a3,'游戏失败')
        input('按任意键退出')
        break
    if cr==0:
        print('看起来国内一切正常')
    elif cr<5:
        print('有一些隐患了看来是')
    else:
        print('山雨欲来了属于是')
    zz=''
    while zz!='e':
        
        if zz=='满意度':
            print('农民',sf)
            print('工人',sw)
            print('商人',sb)
            print('公务员',sser)
        if zz=='粮食':
            print('农民',a1f)
            print('工人',a1w)
            print('商人',a1b)
            print('公务员',a1ser)
        if zz=='产品':
            print('农民',a2f)
            print('工人',a2w)
            print('商人',a2b)
            print('公务员',a2ser)
        if zz=='国库':
            print(a3)
        if zz=='罪犯':
            print(cr,'名')
            
        zz=input('输入想查看的量（满意度、粮食、产品、国库、罪犯），继续游戏请输入e')

    if y%3==1:
        #每三年可以重新设置参数
        a=input("每三年可以修改参数，是否修改参数？（是/否）")


        '''输入各种参数，有重新输入机会'''
        while a=="是":
            
            
            '''输入税率'''
            rtax=2
            while rtax<0 or rtax>1:
                try:
                    rtax=input("请输入农民税率(0-1之间，默认0.05)：")
                    rtax=float(rtax)
                   
                except:
                    rtax=0.05
            rtax1=2
            while rtax1<0 or rtax1>1:
                try:
                    rtax1=input("请输入工人税率(0-1之间，默认0.1)：")
                    rtax1=float(rtax1)
                   
                except:
                    rtax1=0.1
            rtax2=2
            while rtax2<0 or rtax2>1:
                try:
                    rtax2=input("请输入商人税率(0-1之间，默认0.2)：")
                    rtax2=float(rtax2)
                   
                except:
                    rtax2=0.2
            tax=0
            '''总税款tax，税率rtax'''
            ser=-10
            while ser==-10:
                try:
                    ser=input("请输入公务员工资(默认20)：")
                    ser=float(ser)
           
                except:
                    ser=20
               
            print("农民税率为",rtax)
            print("工人税率为",rtax1)
            print("商人税率为",rtax2)
            print("公务员工资为",ser)
            a=input("是否重新输入？")
    if y%5==0:
        #每五年可以全面小康
        strategy='y'
        while strategy=='y':
            strategy=input('是否使用 全面小康（每五年可以使用，给某个阶级所有人补贴）（y/n）')
            if strategy!='y':
                break

            try:
                btje=input('输入补贴金额（默认10）')
                btje=int(btje)
            except:
                btje=10
            if strategy=='y':
                bttt=input('输入你想补贴的阶级农民（1），工人（2），商人（3），公务员（4）,任意键退出')
                if bttt=='1':
                    for i in range(0,nf):
                        a1f[i]+=10
                        a3-=10
                if bttt=='2':
                    for i in range(0,nw):
                        a1w[i]+=10
                        a3-=10
                if bttt=='3':
                    for i in range(0,nb):
                        a1b[i]+=10
                        a3-=10
                if bttt=='4':
                    for i in range(0,nser):
                        a1ser[i]+=10
                        a3-=10
                    j=0
                    for i in range(0,nt):
                        
                        a1t[i]=a1ser[j]
                        
                        j+=1
                    for i in range(0,npl):
                        a1pl[i]=a1ser[j]
                        
                        j+=1
                    for i in range(0,nm):
                        a1m[i]=a1ser[j]
                        
                        j+=1
                    for i in range(0,ntea):
                        a1tea[i]=a1ser[j]
                        
                        j+=1
                    for i in range(0,ng):
                        a1g[i]=a1ser[j]
                        
                        j+=1
                    '''以上是把公务员的参数分给各个岗位''' 
                
            
            
    aa=input('任意键进入下一年')
            
            
                    

