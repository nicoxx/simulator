# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:10:30 2014

@author: Vincent Grosbois
"""

import random
import matplotlib.pyplot as plt


N  = 3

E_D = list()
Var_D = list()

rho = list()
for i in range(N):
    E_D.append(i + 1)
    Var_D.append(1)
    rho.append(1./((i+2)*(i+2)))



rho[0] = 0.01
rho[1] = 0.03
rho[2] = 0.05


print('E_D')
print(E_D)
print('Var_D')
print(Var_D)

Var_V = 1
E_V = sum(E_D)*3/2


print('E_V')
print(E_V)
print('Var_V')
print(Var_V)

sigma_V =  sqrt( log( 1  + Var_V / E_V*E_V ) ) 
mu_V = log (E_V) -  0.5*  log( 1  + Var_V / E_V*E_V )



sigma_D = list()
mu_D = list()


for i in range(N):
    sigma_D.append( sqrt( log( 1  + Var_D[i] / E_D[i]*E_D[i] ) )  )
    mu_D.append( log (E_D[i]) -  0.5*  log( 1  + Var_D[i] / E_D[i]*E_D[i] ) )    
    
   



print "rho :"
print rho

r = list()

for i in range(N):
    r.append(1./N)
    
        
for n in range(100000):
    
    V = random.lognormvariate(mu_V, sigma_V)
    
    D = list()
    for i in range(N):
        D.append(random.lognormvariate(0, sigma_D[i])) 
    
    
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
test_n = 20000

C1_list = list()
C2_list = list()
perf_list = list()

for n in range(test_n):
    V = random.lognormvariate(mu_V, sigma_V)
    
    D = list()
    for i in range(N):
        D.append(random.lognormvariate(mu_D[i], sigma_D[i]))
        
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
            C2 += item[1]*item[0]
            V_temp -= item[1]
        
    
    
    C1_tot += C1 / V
    C2_tot += C2 / V
    C1_list.append(C1_tot / (n+1))
    C2_list.append(C2_tot / (n+1))
    perf_list.append( C1_tot / C2_tot )
    

C1_tot /= test_n + 1
C2_tot /= test_n + 1


print( "C1" )
print (C1_tot)
        
print( "C2" )
print (C2_tot)  

print("perf index") 
print(C1_tot / C2_tot)
    

plt.plot(C1_list)
plt.plot(C2_list)
plt.figure()
plt.plot(perf_list)