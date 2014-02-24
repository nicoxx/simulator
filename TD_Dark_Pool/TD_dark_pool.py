# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:10:30 2014

@author: Vincent Grosbois
"""

import random 

N  = 3

vol_V = 1
vols = list()
rho = list()


for i in range(N):
    vols.append(1)
    rho.append(1./(i+2))
    

print vols
print rho

r = list()

for i in range(N):
    r.append(1./N)
    

print(r)
 
        
for n in range(50000):
    
    V = random.lognormvariate(0, vol_V)
    
    D = list()
    for i in range(N):
        D.append(random.lognormvariate(0, vols[i])) 
    
    
    indic = list()
    for i in range(N):
        if r[i]*V < D[i]:
            indic.append(1)
        else:
            indic.append(0)
    
    
    S = 0
    for i in range(N):
        S = S + rho[i]*indic[i]
        
    S = S/N
    
    
    
    for i in range(N):
        r[i] = r[i] + (1./(n+1))*V*(rho[i]*indic[i] - S)

print "r estimé"
print r

print sum(r)

C1_tot = 0
C2_tot = 0
test_n = 10000
for n in range(test_n):
    V = random.lognormvariate(0, vol_V)
    
    D = list()
    for i in range(N):
        D.append(random.lognormvariate(0, vols[i]))
        
    C1 = 0
    C2 = 0
    
    dark_pools = list()  
    
    for i in range(N):
        dark_pools.append( (rho[i], D[i]))
        if( D[i] > r[i]*V):
            C1 += rho[i]*r[i]*V
        else:
            C1 += rho[i]*D[i]
            
    dark_pools.sort(key=lambda x: -x[0])
    
    V_temp = V
    for item in dark_pools:
        if V_temp <= 0:
            break
        
        if( item[1] > V_temp ):
            C2 += V_temp*item[0]
            V_temp = 0
        else:
            C2 += item[0]*item[1]
            V_temp -= item[1]
        
    
    C1 /= N
    C2 /= N
    
    C1_tot += C1
    C2_tot += C2
    

C1_tot /= test_n
C2_tot /= test_n


print( "C1" )
print (C1_tot)
        
print( "C2" )
print (C2_tot)  

print("perf index") 
print(C1_tot / C2_tot)
    


