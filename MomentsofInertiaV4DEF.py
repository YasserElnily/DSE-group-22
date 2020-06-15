'''
General Notes:
The code was verified using external websites and
data for a perfectly rectangular box. 
The moments of inertia and centroid for the 
stringers are correct, and the centroid location for 
the box+stringers combination falls in the
center for a rectangular wingbox. Moments of inertia
of the full box couldn't be verified with other codes. 
These need to be checked by hand by someone else. 
On first glance, the Ixx and Ixy total look alright, 
based on their comparative orders of magnitude, 
but I don't know how to check Ixy. 
'''

import numpy as np

##############################
# GENERAL INPUTS
# All lengths/sizes in meters,
# Areas in m2 unless otherwise
# specified. 
##############################


c = 1               #Chord length

l1 = 0.35*c           #Wingbox dimensions
l2 = 0.05341297*2*c
l3 = 0.35*c
l4 = 0.05341297*2*c
alpha = 0.0013956381959478988 #0 *np.pi/180          #top skin angle [deg]
beta = 0.0013956381959478988 #0 *np.pi/180           #bottom skin angle [deg]



t1 = 0.00013667                 #Top skin thickness
t2 = 0.00013667                 #Trailing Edge skin thickness
t3 = 0.00013667                 #Bottom skin thickness
t4 = 0.00013667                 #Leading Edge skin thickness

 
t_s = 0.002                       #stringer dimensions
h_s = 0.025


def mom_of_inertia (c,l1,l2,l3,l4,alpha,beta,t1,t2,t3,t4,t_s,h_s,nstringers_top,nstringers_bottom):
    w_s = h_s + t_s
    A_s = h_s*t_s + w_s*t_s        #Cross-sectional area of the corner stiffeners
    
    
    
    ##############################
    # Stringer Moment of Inertia
    ##############################
    
    x_centroid_s = ((t_s*w_s) * 0.5*w_s + (t_s*h_s) *0.5*t_s)/A_s                   
    y_centroid_s = ((t_s*w_s)* 0.5*t_s + (t_s*h_s)*(t_s+0.5*h_s))/A_s               
    Ixx_s = (1/12 * w_s * t_s**3 + w_s*t_s * (y_centroid_s - t_s * 0.5)**2) + (1/12 * t_s * h_s**3 + h_s*t_s*(y_centroid_s - (t_s+0.5*h_s))**2)
    Iyy_s = (1/12 * w_s**3 *t_s + w_s*t_s * (x_centroid_s-w_s*0.5)**2) + (1/12 * t_s**3 * h_s + h_s*t_s*(x_centroid_s - t_s*0.5)**2) 
    Ixy_s = (w_s*t_s) * (x_centroid_s - 0.5*w_s)*(y_centroid_s - 0.5*t_s)  + (t_s*h_s) *(x_centroid_s - 0.5* t_s)*(y_centroid_s- (t_s+0.5*h_s)) 
                                                                              
     
    
    ##############################
    # Centroid determination
    ##############################
    
    #Taking bottom left corner as reference
    
    #step 1: skin contribution parameters
    x_pos_bottom = l3/2 * np.cos(beta)
    y_pos_bottom = l3/2 * np.sin(beta)
    A_bottom = l3*t3
    Ixx_bottom = ((l3**3)*t3*(np.sin(beta))**2) /12
    Iyy_bottom = ((l3**3)*t3*(np.cos(beta))**2) /12
    Ixy_bottom = ((l3**3)*t3*(np.sin(2*beta))) /24
     
    
    x_pos_top = (l1/2) * np.cos(alpha)
    y_pos_top = l4 + (l1/2) * np.sin(alpha)
    A_top = l1*t1
    Ixx_top = ((l1**3)*t1*(np.sin(alpha))**2) /12
    Iyy_top = ((l1**3)*t1*(np.cos(alpha))**2) /12
    Ixy_top = ((l1**3)*t1*(np.sin(2*alpha))) /24
    
    
    x_pos_LE = 0.5*t4    #can also be 0. Shouldn't matter too much
    y_pos_LE = 0.5*l4 
    A_LE = l4*t4
    Ixx_LE = (1/12) * t4 * l4**3
    Iyy_LE = (1/12) * t4**3 * l4
    Ixy_LE = 0
    
    
    x_pos_TE = l3*np.cos(beta) - 0.5*t2 
    y_pos_TE = l3*np.sin(beta) + 0.5*l2
    A_TE = l2*t2
    Ixx_TE = (1/12) * t2 * l2**3
    Iyy_TE = (1/12) * t2**3 * l2
    Ixy_TE = 0
    
    
    
    #step2 : add the stringers
    n_stringers = 4 +nstringers_top + nstringers_bottom                #Change this number to add more stringers
    x_positions_stringers = np.array([0.15, 0.5, 0.5, 0.15])*c - 0.15*c                #Change this array to add more stringers
    y_positions_stringers = np.array([0.05341297,  0.0529245 , -0.0529245 , -0.05341297])*c + 0.05341297*c   #Change this array to add more stringers
    #more stringers

    add_stringer = np.array([[],[]])

    for n in range(1,nstringers_top+1):
        dx = (x_positions_stringers[1]-x_positions_stringers[0]) / (nstringers_top+1)
        dy = (y_positions_stringers[1]-y_positions_stringers[0]) / (nstringers_top+1)
        add_stringer = np.append(add_stringer,[[dx*n+x_positions_stringers[0]],[dy*n+y_positions_stringers[0]]],axis=1)
        
    for n in range(1,nstringers_bottom+1):
        dx = (x_positions_stringers[1]-x_positions_stringers[0]) / (nstringers_bottom+1)
        dy = (y_positions_stringers[1]-y_positions_stringers[0]) / (nstringers_bottom+1)
        add_stringer = np.append(add_stringer,[[dx*n+x_positions_stringers[0]],[dy*n+y_positions_stringers[0]]],axis=1)

        
    x_positions_stringers = np.append(x_positions_stringers,add_stringer[0])
    y_positions_stringers = np.append(y_positions_stringers,add_stringer[1])
    Areas_stringers = np.ones(n_stringers)*A_s

    
    #step3: set up arrays
    x_positions_skin = np.array([x_pos_bottom, x_pos_top, x_pos_LE, x_pos_TE])
    y_positions_skin = np.array([y_pos_bottom, y_pos_top, y_pos_LE, y_pos_TE])
    Areas_skin = np.array([A_bottom, A_top, A_LE, A_TE])
    
    
    #Final centroid calculation
    x_positions = np.append(x_positions_skin, x_positions_stringers)
    y_positions = np.append(y_positions_skin, y_positions_stringers)
    Areas = np.append(Areas_skin, Areas_stringers)
    
    x_centroid_box = np.sum(np.multiply(Areas,x_positions))/np.sum(Areas)
    y_centroid_box = np.sum(np.multiply(Areas,y_positions))/np.sum(Areas)
    
    
    
    ##############################
    # Moments of Inertia
    ##############################
    
    #Ixx = I_element + A_element*deltay^2
    
    
    Ixx_skin = np.array([Ixx_bottom, Ixx_top, Ixx_LE, Ixx_TE])
    Iyy_skin = np.array([Iyy_bottom, Iyy_top, Iyy_LE, Iyy_TE])
    Ixy_skin = np.array([Ixy_bottom, Ixy_top, Ixy_LE, Ixy_TE])
    deltay2_skin = np.square(y_positions_skin-y_centroid_box)
    deltax2_skin = np.square(x_positions_skin-x_centroid_box)
    deltaxy_skin = np.multiply(x_centroid_box-x_positions_skin, y_centroid_box-y_positions_skin)
    
    
    Ixx_stringers = np.ones(n_stringers)*Ixx_s
    Iyy_stringers = np.ones(n_stringers)*Iyy_s
    Ixy_stringers = np.ones(n_stringers)*Ixy_s
    deltay2_stringers = np.square(y_positions_stringers-y_centroid_box)
    deltax2_stringers = np.square(x_positions_stringers-x_centroid_box)
    deltaxy_stringers = np.multiply(x_centroid_box-x_positions_stringers, y_centroid_box-y_positions_stringers)
    
    
    #For skin pannels: Ixx_panel + A_pannel * deltay^2_pannel, all summed up
    #Same for stringers, then add both these up. 
    Ixx_total = np.sum(Ixx_skin + np.multiply(Areas_skin,deltay2_skin)) + np.sum(Ixx_stringers+np.multiply(Areas_stringers,deltay2_stringers))
    Iyy_total = np.sum(Iyy_skin + np.multiply(Areas_skin,deltax2_skin)) + np.sum(Iyy_stringers+np.multiply(Areas_stringers,deltax2_stringers))
    Ixy_total = np.sum(Ixy_skin + np.multiply(Areas_skin,deltaxy_skin)) + np.sum(Ixy_stringers+np.multiply(Areas_stringers,deltaxy_stringers))
    
    
    return (x_centroid_box, y_centroid_box, Ixx_total, Iyy_total, Ixy_total)
























