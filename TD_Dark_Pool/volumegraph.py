# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:10:30 2014

@author: Vincent Grosbois, Nicolas Lecrique
"""

import random
from math import * 
import matplotlib.pyplot as plt


#moving average function for results displaying
def MovingAverage(values, window):
    result = list()
    currentValue = float(sum(values[0:window-1]))    
    result.append(currentValue/window)
    for i in range(window,len(values)):
        currentValue += values[i]-values[i-window]
        result.append(currentValue/window)
    return result


#nb of dark pools
N  = 3


r1_list_vol = list()
r2_list_vol = list()
r3_list_vol = list()
cr_algo_list_vol = list()
cr_oracle_list_vol = list()
perf_list_vol = list()


volume_coeff_list = list()
for i in range(20):
    volume_coeff_list.append((1+i)*0.2)

for volume_coeff in volume_coeff_list:

    #discount of each dark pool
    rho = [0.01,0.03,0.05]
    
    #expected value and variance of Di: liquidity in each dark pool
    E_D = list()
    Var_D = list()
    for i in range(N):
        E_D.append(i + 1.)
        Var_D.append(1.)
        
    #expected value and variance of V:volume to execute
    Var_V = 1.
    E_V = sum(E_D)*volume_coeff #shortage of liquidity
    
    #compute parameters of lognormal laws from expected value and variance
    sigma_V =  sqrt( log( 1  + Var_V / (E_V*E_V) ) ) 
    mu_V = log (E_V) -  0.5*  log( 1  + Var_V / (E_V*E_V) )
    
    sigma_D = list()
    mu_D = list()
    for i in range(N):
        sigma_D.append( sqrt(log ( 1.  + Var_D[i] / (E_D[i]*E_D[i]) ) )  )
        mu_D.append( log (E_D[i]) -  0.5*  log( 1  + Var_D[i] / (E_D[i]*E_D[i]) ) )    
        
    #optimal allocation decided by algo
    r = list()
    #initialization with same value for each dark pool
    for i in range(N):
        r.append(1./N)
    
    #nb of simulations
    nb_simu = 10000;
        
    #reporting data
    Rel_CR_Oracle_list = list()
    Rel_CR_Algo_list = list()
    perf_Algo_list = list()
    perf_Oracle_list = list()
    r1_value_list = list();
    r2_value_list = list();
    r3_value_list = list();
    
            
    for n in range(nb_simu):
        
        r1_value_list.append(r[0])
        r2_value_list.append(r[1])
        r3_value_list.append(r[2])
        
        #quantity to execute
        V = random.lognormvariate(mu_V, sigma_V)
        #quantity available in each darl pool
        D = list()
        for i in range(N):
            D.append(random.lognormvariate(mu_D[i], sigma_D[i])) 
        
        #Compute cost reduction with optimisation algorithm
        CR_Algo = 0.
        for i in range(N):
            CR_Algo += rho[i]*min(r[i]*V,D[i])
    
        #Compute cost reduction with oracle
            #-Make a list of dar pool datas : rho and Di
            #-Sort by rho, big (more discount) to small
            #-take all the liquidity in sorted pools up to execute V
        CR_Oracle = 0.
        dark_pools = list()
        for i in range(N):
            dark_pools.append( (rho[i], D[i]))
                    
        dark_pools.sort(key=lambda x: -x[0])
        V_temp = V
        for item in dark_pools:
            if( item[1] > V_temp ):
                CR_Oracle += V_temp*item[0]
                break
            else:
                CR_Oracle += item[1]*item[0]
                V_temp -= item[1]
    
    
        #optimisation algorithm to determine optimal allocation for next iteration
            #-compute indicator fonction {riV<Di} of each dark pool
            #-compute 1/N * sum ( rho_j * indic_j) (S)
            #-apply fixed point formula
            #-bound ri in [0,1]
        indic = list()
        for i in range(N):
            if r[i]*V < D[i]:
                indic.append(1.)
            else:
                indic.append(0.)
         
        S = 0.
        for i in range(N):
            S = S + rho[i]*indic[i]  
        S = S/N
        
        for i in range(N):
            r[i] = r[i] + (1./(n+1))*V*(rho[i]*indic[i] - S)
    
        #bound ri in [0,1]
        for i in range(N):
            r[i] = min(1,max(0,r[i]))
        normalizationFactor = sum(r)
        for i in range(N):
            r[i] = r[i]/normalizationFactor
            
    
        #reporting data management
    
        #relative cost reduction to volume
        Rel_CR_Oracle = 100*CR_Oracle/V
        Rel_CR_Algo = 100*CR_Algo/V
        #performance relative to index    
        
        Rel_CR_Algo_list.append(Rel_CR_Algo)
        Rel_CR_Oracle_list.append(Rel_CR_Oracle)
        perf_Algo_list.append(Rel_CR_Algo/Rel_CR_Oracle)
        perf_Oracle_list.append(Rel_CR_Oracle/Rel_CR_Oracle)
    
    
    r1_list_vol.append(r[0])
    r2_list_vol.append(r[1])
    r3_list_vol.append(r[2])
    cr_algo_list_vol.append(mean(Rel_CR_Algo_list))
    cr_oracle_list_vol.append(mean(Rel_CR_Oracle_list))
    perf_list_vol.append(mean(perf_Algo_list)  )

plt.figure("perf indexes / V expected value")
plt.title("perf indexes / V expected value")
plt.plot(volume_coeff_list, perf_list_vol, label = "perf algo")
plt.legend(loc='upper right')

plt.figure("Allocation / V expected value")
plt.title("Allocation / V expected value")
plt.plot(volume_coeff_list, r1_list_vol, label = "r1")
plt.plot(volume_coeff_list, r2_list_vol, label = "r2")
plt.plot(volume_coeff_list, r3_list_vol, label = "r3")
plt.legend(loc='upper right')