# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import numpy as np
from WingimportTool import *
from Aircraft_constance_Data import *
from ReactionForces import *
from MomentsofInertiaV4DEF import *
from structurefools import *
from function_shear_flow import *
from function_normal_stress import *


##################################
#INPUTS TO FILL IN TO RUN THE CODE
##################################

"""Wing geometry"""

width_fuselage = 0.7
span = 7
taper = 1

"""Wing cross-section geometry"""

chordroot = 1.72   # in m
airfoil = 'airfoil.dat'

t1 = 0.001 #Wanted top web thickness in m
t2 = 0.001 #Wanted rear spar thickness in m
t3 = 0.001 #Wanted bottom web thickness in m
t4 = 0.001 #Wanted front spar thickness in m

t_s = 0.002 #Stringer thickness
h_s = 0.02 #Stringer dimension

"""Load factors"""

n_vtol = 2
n_horiz = 3.2
safety_factor = 1.5

"""Loads and weights"""

aircraft_mass = 700 
wingloading = 0 #lift distribution
thrust =  0 #
vtol_thrust = 0 #should be separated from thrust to run everything at once
controlloads_hor = 0 #horizontal control loads
controlloads_ver = 0 #vertical control loads
dragloading = 0 #drag distribution

mrotor = 0 #mass of rotor
wing_weight = 0 #mass, if added to calculation stresses will be lowered


"""Material"""

#Aluminium coefficients

alpha_Al = 0.8
n_Al = 0.6
sig_y6061 = 280 * 10**6
sig_ult6061 = 338 * 10**6   
E_6061 = 70 * 10**9 
G_6061 = 27 * 10**9

##################################
#CALCULATOR STARTS
##################################
   

halfspan = (span-width_fuselage)/2

#Assuming that all forces are applied at aerodynamic center!!

"""forces on the structure in the x direction"""
dragloading = dragloading*safety_factor
thrust = thrust*safety_factor
controlloads_hor = controlloads_hor*safety_factor

"""forces on the structure in the z direction"""
wingloading = wingloading*safety_factor*n_horiz
rotorweight = -mrotor*9.81*safety_factor
wingmassloading = -wing_weight/halfspan*safety_factor
vtolthrust = vtol_thrust*safety_factor*n_vtol
controlloads_ver = controlloads_ver*safety_factor

"""Chosen material"""

G = G_6061
E = E_6061
v = 0.33
sig_y = sig_y6061
sig_ult = sig_ult6061



#creation of the forces array
stepsize = 0.7 #meter
steps = int(halfspan/stepsize+1)

#Take-off loadcase 
def loadcase1(stepsize,chordroot,taper,span):
    loadcase1 = np.empty([steps,6])
    for n in range(steps):
        #the y location
        y = stepsize *n
        c = chordroot-2*(chordroot-chordroot*taper)*y/(span)
    
        loadcase1[n,0] = y
        #shear forcesz
        loadcase1[n,1] = reaction_forces("VTO", halfspan, aircraft_mass, 0, 0, 0)[2]
        #shear forcesx
        loadcase1[n,2] = reaction_forces("VTO", halfspan, aircraft_mass, 0, 0, 0)[0]
        #momentz
        loadcase1[n,3] = reaction_forces("VTO", halfspan, aircraft_mass, 0, 0, 0)[5]
        #momentx
        loadcase1[n,4] = reaction_forces("VTO", halfspan, aircraft_mass, 0, 0, 0)[3]
        #Torsion
        loadcase1[n,5] = reaction_forces("VTO", halfspan, aircraft_mass, 0, 0, 0)[4]
        return loadcase1


#Cruise flight loadcase
def loadcase2(stepsize, chordroot, taper, span):
    loadcase2 = np.empty([steps,6])
    for n in range(steps):
        #the y location
        y = stepsize *n
        c = chordroot-2*(chordroot-chordroot*taper)*y/(span)
        
        loadcase2[n,0] = y
        #shear forcesz
        loadcase2[n,1] = reaction_forces("cruise", halfspan, aircraft_mass, 0, 0, 0)[2]
        #shear forcesx
        loadcase2[n,2] = reaction_forces("cruise", halfspan, aircraft_mass, 0, 0, 0)[0]
        #momentz
        loadcase2[n,3] = reaction_forces("cruise", halfspan, aircraft_mass, 0, 0, 0)[5]
        #momentx
        loadcase2[n,4] = reaction_forces("cruise", halfspan, aircraft_mass, 0, 0, 0)[3]
        #Torsion
        loadcase2[n,5] = reaction_forces("cruise", halfspan, aircraft_mass, 0, 0, 0)[4]
    return loadcase2



#Take-off loadcase
loadcasearray = [loadcase1(stepsize,chordroot,taper,span),loadcase2(stepsize,chordroot,taper,span)]


for loadcase in loadcasearray: 

    """[yloc,maxtauTskin,maxsigTskin,maxtauRspar,maxsigRspar,maxtauBskin,maxsigBskin,maxtauLspar,maxsigLspar]"""
    stressarray = np.empty([steps,10]) #do we need this?????????
    
    nbottomstring = 0
    ntopstring = 0
    l4st,l2st,l1st,l3st,alpha,beta =  wingboxdimension(airfoil,frontspar,rearspar)
    print("loadcase")
    
    
    for force in loadcase:
        print("run")
        dstring = 1 
        y = force[0]                
        c = chordroot*(taper + (y)/halfspan)
        while dstring > 0:
            dstring = nbottomstring + ntopstring    
            
            l4,l2,l1,l3 = l4st*c,l2st*c,l1st*c,l3st*c
            hf = l4
            Izz = mom_of_inertia(c,l1,l2,l3,l4,alpha,beta,t1,t2,t3,t4,t_s,h_s,ntopstring,nbottomstring)[3]
            Ixx = mom_of_inertia(c,l1,l2,l3,l4,alpha,beta,t1,t2,t3,t4,t_s,h_s,ntopstring,nbottomstring)[2]
            Ixz = mom_of_inertia(c,l1,l2,l3,l4,alpha,beta,t1,t2,t3,t4,t_s,h_s,ntopstring,nbottomstring)[4]
    
            x_centroid_box = mom_of_inertia(c,l1,l2,l3,l4,alpha,beta,t1,t2,t3,t4,t_s,h_s,ntopstring,nbottomstring)[0]
            y_centroid_box = mom_of_inertia(c,l1,l2,l3,l4,alpha,beta,t1,t2,t3,t4,t_s,h_s,ntopstring,nbottomstring)[1]
            
            width = rearspar*c-frontspar*c #Width of the wingbox within the chordlength
            Vy = -force[1] #positive downwards
            Vx = -force[2] #positive towards trailing edge
            x_Vy = x_centroid_box+frontspar-xac*c #force applied at distance x from centroid, x towards leading edge
            z_Vx = 0.5*hf-y_centroid_box #force applied at distance z from centroid, z downwards
            #
            #I hate myself for having to write these inputs and outputs here
            x_sc,y_sc,tau1,tau1_loc,tau2,tau2_loc,tau3,tau3_loc,tau4,tau4_loc,tau5,tau5_loc,tau6,tau6_loc,tau7,tau7_loc,tau8,tau8_loc,twist = shear_stress(t1,t2,t3,t4,l1,l2,l3,l4,alpha,beta,width,x_centroid_box,(hf-y_centroid_box),x_centroid_box,(hf-y_centroid_box),Ixx,Izz,Ixz,G,Vy,Vx,x_Vy,z_Vx)
            #1,2,3,4 max stresses on webs 1,2,3,4
            #5,6,7,8 min stresses on webs 1,2,3,4
            #loc gives position of max/min stress as A POSITION IN METERS w.r.t the web
    
            Mx = force[3] #Moment around y-axis, positive for beam bending towards trailing edge
            Mz = force[4] #Moment around x-axis, negative for beam bending upwards
            sigma1,sigma1_loc,sigma2,sigma2_loc,sigma3,sigma3_loc,sigma4,sigma4_loc,sigma5,sigma5_loc,sigma6,sigma6_loc,sigma7,sigma7_loc,sigma8,sigma8_loc,=   normal_stress(t1,t2,t3,t4,l1,l2,l3,l4,alpha,beta,width,x_centroid_box,(hf-y_centroid_box),x_centroid_box,(hf-y_centroid_box),Ixx,Izz,Ixz,Mz,Mx)
            #1,2,3,4 max stresses on webs 1,2,3,4
            #5,6,7,8 min stresses on webs 1,2,3,4
            #loc gives position of max/min stress as A POSITION IN METERS w.r.t the web
            print("y {:.3e}".format(y),"Vx {:.3e}".format(Vx),"Vy {:.3e}".format(Vy),"Mx {:.3e}".format(Mx),"Mz {:.3e}".format(Mz))
            print("tau1 {:.3e}".format(tau1),"tau1_loc {:.3e}".format(tau1_loc),"tau2 {:.3e}".format(tau2),"tau2_Loc {:.3e}".format(tau2_loc),"sigma1 {:.3e}".format(sigma1),"sigma1_loc {:.3e}".format(sigma1_loc),"sigma2 {:.3e}".format(sigma2),"sigma2_loc {:.3e}".format(sigma2_loc))
            #TopsKing
            CCstress = stiffendskincalculation(chord,y,ntopstring,E,v,stringer(material("AL6061")))
            while CCstress < sigma5:
                ntopstring+=1
                CCstress = stiffendskincalculation(chord,y,ntopstring,E,v,stringer(material("AL6061")))
                if ntopstring > 10:
                    print("BREAK CCSTRESS")
                    break
            #Bottomsking
            CCstress = stiffendskincalculation(chord,y,nbottomstring,E,v,stringer(material("AL6061")))
            while CCstress < sigma7:
                nbottomstring+=1
                CCstress = stiffendskincalculation(chord,y,nbottomstring,E,v,stringer(material("AL6061")))
                if nbottomstring > 10:
                    print("BREAK CCSTRESS")
                    break    
            dstring = - nbottomstring - ntopstring
        print("number of topstringers",ntopstring,"number of bottomstringers",nbottomstring)
        
        ##########
        #some space for stringer pitch
        #some space for rib pitch
        #some space for weight estimation
        ##########
            
