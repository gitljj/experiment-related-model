# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 23:27:29 2022

@author: Lin Junjie
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

class Mac:
    A=129.46 # Constant in the energy model for calculating time
    B=2.52 # Constant in the energy model for calculating time
    C=-58.23 # Constant in the time model for calculating oxygen filling time
    D=88.02 # Constant in the time model for calculating oxygen filling time
    E=0.0838 # Constant in the time model for calculating heating time
    F=2.364 # Constant in the time model for calculating heating time
    G=82.844 # Constant in the time model for calculating heating time
    H=0.5048 # Constant in the time model for calculating cooling time
    I=192.96 # Constant in the time model for calculating cooling time
    J=18545 # Constant in the time model for calculating cooling time

    
    def __init__(self,subsyspower,kij,otherparams):
        self.basic_system_w=subsyspower[0]
        self.heater_w=subsyspower[1]
        self.water_cooling_w=subsyspower[2]
        self.water_circulation_w=subsyspower[3]
        self.recoter_motor_w=subsyspower[4]
        self.electric_valves_w=subsyspower[5]
        self.gas_circulation_pump_motor_w=subsyspower[6]
        self.concentration_oxygen_initial=otherparams[0]
        self.concentration_oxygen_end=otherparams[1]
        
        self.kij=kij
        
    #def Load_data(filename):
#class part:   
       
class Batch:
    def __init__(self,batchparams):
        self.part_volume=batchparams[0]
        self.part_surface_area=batchparams[1]
        self.support_volume=batchparams[2]
        self.slice_number=batchparams[3]
    #def Load_data(filename):
        
class Process:
    def __init__(self,processparams):
        self.scanning_power={'boder':processparams[0][0],'fill_contour':processparams[0][1],'volume_hatching':processparams[0][2],'support_structure':processparams[0][3]}
        self.scanning_speed={'boder':processparams[1][0],'fill_contour':processparams[1][1],'volume_hatching':processparams[1][2],'support_structure':processparams[1][3]}
        self.layer_thickness={'boder':processparams[2][0],'fill_contour':processparams[2][1],'volume_hatching':processparams[2][2],'support_structure':processparams[2][3]}
        self.hatching_distance={'volume_hatching':processparams[3][0],'support_structure':processparams[3][1]}
        self.scanning_number=processparams[4][0]
        self.start_heater_temp=processparams[5][0]
        self.end_heater_temp=processparams[6][0]
        self.start_cooling_temp=processparams[7][0]
        self.end_cooling_temp=processparams[8][0]
        self.recoter_time_single=processparams[9][0]
    #def Load_data(filename):

class Energy_Model():
    
    def Cal_Time (self,mac,process,batch):  
        
        t0=mac.C*math.log(mac.concentration_oxygen_initial,math.e)-mac.D
        t1=mac.C*math.log(mac.concentration_oxygen_end,math.e)-mac.D
        delta_t_oxygen=t1-t0
        t2=mac.E*(process.start_heater_temp)**2+mac.F*(process.start_heater_temp)-mac.G
        t3=mac.E*(process.end_heater_temp)**2+mac.F*(process.end_heater_temp)-mac.G
        delta_t_heater=t3-t2
        t4=mac.H*(process.start_cooling_temp)**2-mac.I*(process.start_cooling_temp)+mac.J
        t5=mac.H*(process.end_cooling_temp)**2-mac.I*(process.end_cooling_temp)+mac.J
        delta_t_cooling=t5-t4
        self.gas_filling_time=delta_t_oxygen
        self.heater_time=delta_t_heater
        
        self.scanning_boder_time=(batch.part_surface_area)/((process.scanning_number)*(process.scanning_speed['boder'])*(process.layer_thickness['boder']))
        self.fill_contour_time=(batch.part_surface_area)/((process.scanning_number)*(process.scanning_speed['fill_contour'])*(process.layer_thickness['fill_contour'] ))                                        
        self.volume_hatching_time=batch.part_volume/((process.scanning_number)*(process.scanning_speed['volume_hatching'])*(process.layer_thickness['volume_hatching'])*(process.hatching_distance['volume_hatching'])) 
        self.support_building_time=batch.support_volume/((process.scanning_number)*process.scanning_speed['support_structure']*process.layer_thickness['support_structure']*(process.hatching_distance['support_structure'])) 
        self.recoter_time_all=process.recoter_time_single*batch.slice_number
        self.cooling_time=delta_t_cooling
        self.bulding_time=self.scanning_boder_time+self.fill_contour_time+self.volume_hatching_time+self.support_building_time
        time_toal=self.heater_time+self.bulding_time+self.recoter_time_all+self.cooling_time
        print('''
              Gas filling time is %d
              Heating time is %d
              Boundary scanning time is %d
              Contour filling time is %d
              Volume hatching time is %d
              Support structure building time is %d
              Powder laying time is %d
              Cooling time is %d
              Total time is %d
              '''%(self.gas_filling_time,self.heater_time,self.scanning_boder_time,self.fill_contour_time,self.volume_hatching_time,self.support_building_time,self.recoter_time_all,self.cooling_time,time_toal)) 
        print('=============================================================')

        return self.heater_time,self.scanning_boder_time,self.fill_contour_time,self.volume_hatching_time,self.support_building_time,self.recoter_time_all,self.cooling_time,time_toal
    def Cal_Energy(self,mac,process,batch):
        
        
     
        realpower_scanning_boder=process.scanning_number*(mac.A+process.scanning_power['boder']*mac.B)
        realpower_scanning_fill_contour=process.scanning_number*(mac.A+process.scanning_power['fill_contour']*mac.B)
        realpower_scanning_volume_hatching=process.scanning_number*(mac.A+process.scanning_power['volume_hatching']*mac.B)
        realpower_scanning_support_volume=process.scanning_number*(mac.A+process.scanning_power['support_structure']*mac.B)
        P=np.array([mac.basic_system_w,
        mac.heater_w,
        mac.water_circulation_w,
        mac.water_cooling_w,
        realpower_scanning_boder,
        realpower_scanning_fill_contour,
        realpower_scanning_volume_hatching,
        realpower_scanning_support_volume,           
        mac.recoter_motor_w,
        mac.electric_valves_w,
        mac.gas_circulation_pump_motor_w])
        T=np.array([self.heater_time,
        self.scanning_boder_time,
        self.fill_contour_time,
        self.volume_hatching_time,
        self.support_building_time,
        self.recoter_time_all,
        self.cooling_time
           ])
        
        
        K=np.array(mac.kij)
        EPC=np.dot(np.dot(P, K), T.T)
        PKT=[]
        for i in range(11):
            K_row=[]
            for j in range(7):
                K_row.append(int(P[i]*K[i][j]*T[j]))
            PKT.append(K_row)
        data=np.array(PKT)  
        ev_singel_sysec=data.sum(axis=1)
        ev_single_stage=data.sum(axis=0)
        print("--------",ev_single_stage)
        print('''
              Subsystem power consumption is %d
              Heater power consumption is %d
              Water circulation system power consumption is %d
              Water cooling unit power consumption is %d
              Scanning boundary power consumption is %d
              Contour filling power consumption is %d
              Part building power consumption is %d
              Support part building power consumption is %d
              Recoater motor power consumption is %d
              Electric valve power consumption is %d
              Gas circulation motor power consumption is %d
              Total energy consumption is %d
              '''%(ev_singel_sysec[0],ev_singel_sysec[1],ev_singel_sysec[2],ev_singel_sysec[3],ev_singel_sysec[4],ev_singel_sysec[5],ev_singel_sysec[6],ev_singel_sysec[7],ev_singel_sysec[8],ev_singel_sysec[9],ev_singel_sysec[10],EPC))

        print('=============================================================')
        dataframe={
            'Preheating phase': data[:,0],
            'Scanning boundary phase': data[:,1],
            'Contour filling phase': data[:,2],
            'Part building phase': data[:,2],
            'Support structure building phase': data[:,2],
            'Powder laying phase': data[:,2],
            'Cooling phase': data[:,2]
            }
        every_stage_ec=pd.DataFrame(dataframe, index=['Basic subsystem', 'Heater','Water circulation system','Water cooling system','Scanning boundary system','Contour filling system','Volume hatching system','Support structure building system','Powder laying system','Electric valve system','Gas circulation motor system'])
        print('Energy matrix is\n{}'.format(every_stage_ec))

        return ev_singel_sysec[0],ev_singel_sysec[1],ev_singel_sysec[2],ev_singel_sysec[3],ev_singel_sysec[4],ev_singel_sysec[5],ev_singel_sysec[6],ev_singel_sysec[7],ev_singel_sysec[8],ev_singel_sysec[9],ev_singel_sysec[10],EPC
       
 

# ---------------------------------------


SubSysPower = [ 569.7, # Power of the basic subsystem
               1122.3, # Power of the heater
               1739.4, # Power of the water circulation system
               713.3,  # Power of the water cooling unit
               52.1,   # Power of the powder laying motor
               32.1,   # Power of the electric valve
               69.1 ]  # Power of the gas circulation motor

kij=[[1,1,1,1,1,1,1], # Power coefficient of the basic system across 7 stages
 [1,0.4826,0.4826,0.4826,0.4826,0.4826,0], # Power coefficient of the heater across 7 stages
 [1,1,1,1,1,1,1], # Power coefficient of the water circulation system across 7 stages
 [0.168,0.353,0.353,0.353,0.353,0.353,0.216], # Power coefficient of the water cooling unit across 7 stages
 [0,1,0,0,0,0,0], # Power coefficient during the scanning boundary process across 7 stages
 [0,0,1,0,0,0,0], # Power coefficient during the contour filling process across 7 stages
 [0,0,0,1,0,0,0], # Power coefficient during the part building stage across 7 stages
 [0,0,0,0,1,0,0], # Power coefficient during the support structure building in 7 stages
 [0,0,0,0,0,1,0], # Power coefficient during the powder laying process across 7 stages
 [1,1,1,1,1,1,0], # Power coefficient of the electric valve across 7 stages
 [0,1,1,1,1,1,0] # Power coefficient of the gas circulation motor across 7 stages
 ]
 

OthermacParams = [ 21, 0.1] # Initial oxygen concentration, final oxygen concentration

M1 = Mac(SubSysPower, kij, OthermacParams)

ProcessParams_case1 = [[300,300,350,350], # Power for scanning boundary, filling contour, volume incubation, building support structure
                       [730,730,1650,1000], # Scanning speed for scanning boundary, filling contour, volume incubation, building support structure
                       [0.03,0.03,0.03,0.03], # Layer thickness for scanning boundary, filling contour, volume incubation, building support structure
                       [0.13,0.18], # Incubation distance during volume incubation, incubation distance during support structure building
                       [2], # Number of lasers
                       [27], # Initial heating temperature
                       [150], # Final heating temperature
                       [150], # Initial cooling temperature
                       [80], # Final cooling temperature
                       [11] # Powder laying time
                       ]


ProcessParams_case2 = [[300,300,350,350],
                       [730,730,1650,1000],
                       [0.03,0.03,0.03,0.03],
                       [0.13,0.18],
                       [2],
                       [48.5],
                       [150],
                       [150],
                       [80],
                       [8]
                       ]

P1 = Process(ProcessParams_case1)
P2 = Process(ProcessParams_case2)
#==========30个零件==================
BatchParams_case1 =[391153,198980,145296,1730] #Part volume,surface area,support volume，number of slice
# BatchParams_case2 = [347374,169829,137813,2030]
BatchParams_case2 = [192609,145220,88872,2030]
#==========25个零件==================
# BatchParams_case1 =[385425,191389,143511,1730] #Part volume,surface area,support volume，number of slice
# # BatchParams_case2 = [265669,154210,86999,2030]
# BatchParams_case2 = [100510,74232,68338,1730]
#==========20个零件==================
# BatchParams_case1 =[382338,188338,141966,1730] #Part volume,surface area,support volume，number of slice
# # BatchParams_case2 = [265669,154210,86999,2030]
# BatchParams_case2 = [220686,146219,108954,2030]
BM1 = Batch(BatchParams_case1)
BM2 = Batch(BatchParams_case2)

energy_model=Energy_Model()

energy_model.Cal_Time(M1,P1,BM1)
energy_model.Cal_Energy(M1,P1,BM1)

energy_model.Cal_Time(M1,P1,BM2)
energy_model.Cal_Energy(M1,P1,BM2)

    
    
    
    
    
     