import math as m
import time

# referance  http://cogsci.stackexchange.com/questions/5199/which-equatio
#  n-is-ebbinghauss-forgetting-curve-and-what-do-the-constants-repres

class Forge:
    def __init__(self,a=0.005,a_2=0.05,Lambda=0.05):
        self.a=m.fabs(a)
        self.a_2=m.fabs(a_2)
        self.lam=Lambda

    def stimulate_forge_type1(self,learnvalue,t):
        try:
            if not isinstance(learnvalue,list):
                C=learnvalue
                return C*m.exp(-1*self.a*t)
            else:
                Return=[]
                for i ,c in enumerate( learnvalue):
                    learnvalue[i]=c*m.exp(-1*self.a*t)
        except:
            print("---->Forge Model: Try to input 't' as standard datatime and 'learnvalue' as float or list")

# dR/dt = -aR  ---> R= Ce^(-at)
    def stimulate_forge_type2(self,learnvalue,t):
        try:
            if not isinstance(learnvalue,list):
                C=learnvalue
                return C/(1+self.a_2* m.log(1+self.lam*t))
            else:
                Return=[]
                for i ,c in enumerate( learnvalue):
                    learnvalue[i]=c/(1+self.a_2* m.log(1+self.lam*t))
        except:
            print("---->Forge Model: Try to input 't' as standard datatime and 'learnvalue' as float or list")

def test():
    forgevalue=[11111111,11111,111,11,5,3,2,1,0]
    forgevalue2=[11111111,11111,111,11,5,3,2,1,0]
    print(forgevalue)
    a=Forge()
    a.stimulate_forge_type1(forgevalue,120)
    print(forgevalue)
    a.stimulate_forge_type2(forgevalue2,120)
    print(forgevalue2)

    a.stimulate_forge_type1(forgevalue,0)
    print(forgevalue)
    a.stimulate_forge_type2(forgevalue2,0)
    print(forgevalue2)
if __name__=='__main__':
    test()
