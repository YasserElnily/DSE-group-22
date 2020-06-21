# -*- coding: utf-8 -*-
"""
Created on Friday June 5 2020
@author: Roosa
"""

"""Shear flow function"""

#INPUTS:
"""
In total 22 input arguments
Cross section dimensions:
- t1 = thickness upper skin
- t2 = thickness trailing edge spar
- t3 = thickness lower skin
- t4 = thickness leading edge spar
- length_upper_skin
- length_right_side
- length_lower_skin
- length_left_side
- angle_from_horizontal_upper = angle of upper skin as seen from leading edge spar
- angle_from_horizontal_lower = angle of lower skin as seen from leading edge spar
- width = 0.60%-0.15% of chord
Cross section geometrical properties:
- x_centroid = from top left corner
- y_centroid = from top left corner
- x_neutral_axis = from top left corner
- y_neutral_axis = from top left corner
- Ixx
- Iyy 
- Ixy
Material properties:
- G = shear modulus
#Shear forces:
- Vy = positive downwards)
- Vx = positive towards trailing edge)
- x_Vy = forces applied at distance from centroid, x towards leading edge
- z_Vx = force applied at distance from centroid, z downwards
"""

#OUTPUTS:
"""
In total 19 output arguments
xi = Shear center x coordinate from top left corner
eta = Shear center y coordinate from top left corner
max_shear_upper = Max shear stress in upper skin panel
max_shear_loc_upper = Location of the above in the upper skin panel (given as length)
max_shear_right = Max shear stress in trailing edge spar panel
max_shear_loc_right = Location of the above in the trailing edge spar panel (given as length)
max_shear_lower = Max shear stress in lower skin panel
max_shear_loc_lower = Location of the above in the lower skin panel (given as length)
max_shear_left = Max shear stress in leading edge spar panel
max_shear_loc_left = Location of the above in the leading edge spar panel (given as length)
min_shear_upper = Min shear stress in upper skin panel
min_shear_loc_upper = Location of the above in the upper skin panel (given as length)
min_shear_right = Min shear stress in trailing edge spar panel
min_shear_loc_right = Location of the above in the trailing edge spar panel (given as length)
min_shear_lower = Min shear stress in lower skin panel
min_shear_loc_lower = Location of the above in the leading edge spar panel (given as length)
min_shear_left = Min shear stress in leading edge spar panel
min_shear_loc_left = Location of the above in the upper skin panel (given as length)
angle_of_twist = angle of twist in the cross section (given in rad/m)
"""
import numpy as np


def shear_stress(t1,t2,t3,t4,length_upper_skin,length_right_side,length_lower_skin,length_left_side,angle_from_horizontal_upper,angle_from_horizontal_lower,width,x_centroid,y_centroid,x_neutral_axis,y_neutral_axis,Ixx,Iyy,Ixy,G,Vy,Vx,x_Vy,z_Vx):
       


    #-------------------------------------------------------------------------
    #Convert length to mesh points
    #-------------------------------------------------------------------------
    """COMMENT"""
    #Feel free to change the stop value

    mesh1 = np.arange(0,1000,1)
    #print(mesh1)

    #-------------------------------------------------------------------------
    #Basic shear flow due to forces in y
    #-------------------------------------------------------------------------
    yds_1 = np.empty(len(mesh1))
    yds_2 = np.empty(len(mesh1))
    yds_3 = np.empty(len(mesh1))
    yds_4 = np.empty(len(mesh1))

    int_yds_luru = np.empty(len(mesh1))
    int_yds_rurb = np.empty(len(mesh1))
    int_yds_rblb = np.empty(len(mesh1))
    int_yds_lblu = np.empty(len(mesh1))

    """COMMENT"""
    #Integrating through the mesh points
    #yds_1,2,3 and 4 indicate expression for y in terms of s (mesh location along the skin length) 
    #int_yds indicates integration of the aforementioned expression

    #Naming convention for wing skin
    #l=left
    #r=right
    #u=upper
    #b=bottom

    for i in mesh1:
        
        yds_1[i] = y_neutral_axis-np.sin(angle_from_horizontal_upper)*length_upper_skin*mesh1[i]/(len(mesh1))
        int_yds_luru[i] = y_neutral_axis*length_upper_skin*mesh1[i]/(len(mesh1))-np.sin(angle_from_horizontal_upper)*(length_upper_skin*mesh1[i]/len(mesh1))**2/2

        yds_2[i] = (y_neutral_axis-(np.sin(angle_from_horizontal_upper)*length_upper_skin))-length_right_side*mesh1[i]/(len(mesh1))
        int_yds_rurb[i] = (y_neutral_axis-(np.sin(angle_from_horizontal_upper)*length_upper_skin))*(length_right_side*mesh1[i]/(len(mesh1)))-(length_right_side*mesh1[i]/len(mesh1))**2/2

        yds_3[i] = (length_left_side-y_neutral_axis-np.sin(angle_from_horizontal_lower)*(length_lower_skin-(length_lower_skin*mesh1[i]/len(mesh1))))
        int_yds_rblb[i] = (length_left_side-y_neutral_axis)*(length_lower_skin*mesh1[i]/len(mesh1))-np.sin(angle_from_horizontal_lower)*(length_lower_skin*(length_lower_skin*mesh1[i]/len(mesh1))-(length_lower_skin*mesh1[i]/len(mesh1))**2/2)

        yds_4[i] = -((length_left_side-y_neutral_axis)-(length_left_side*mesh1[i]/len(mesh1)))
        int_yds_lblu[i] = -((length_left_side-y_neutral_axis)*(length_left_side*mesh1[i]/len(mesh1))-(length_left_side*mesh1[i]/len(mesh1))**2/2)

    #print(int_yds_luru)
    #print(int_yds_rurb)
    #print(int_yds_rblb)
    #print(int_yds_lblu) 

    """COMMENT"""
    #the following q indicates the change in shear flow from one mesh point to next one
    #signs are matched to the assumed direction and shape of the shear flow

    q_luru_y = -t1*((Vy*Iyy-Vx*Ixy)/(Ixx*Iyy-Ixy**2))*int_yds_luru
    #print(q_luru_y)

    q_rurb_y = np.empty(len(mesh1))
    for i in range(0,len(mesh1)):
        if i<= np.argmax(int_yds_rurb):
            q_rurb_y[i] = -t2*((Vy*Iyy-Vx*Ixy)/(Ixx*Iyy-Ixy**2))*int_yds_rurb[i]
        else:
            q_rurb_y[i] = t2*((Vy*Iyy-Vx*Ixy)/(Ixx*Iyy-Ixy**2))*int_yds_rurb[i]
        
    #print(q_rurb_y)
                                      
    q_rblb_y = t3*((Vy*Iyy-Vx*Ixy)/(Ixx*Iyy-Ixy**2))*int_yds_rblb
    #print(q_rblb_y)

    q_lblu_y = np.empty(len(mesh1))
    for i in range(0,len(mesh1)):
        if i<= np.argmin(int_yds_lblu):
            q_lblu_y[i] = -t4*((Vy*Iyy-Vx*Ixy)/(Ixx*Iyy-Ixy**2))*int_yds_lblu[i]
        else:
            q_lblu_y[i] = t4*((Vy*Iyy-Vx*Ixy)/(Ixx*Iyy-Ixy**2))*int_yds_lblu[i]

    #print(q_lblu_y)

    """COMMENT"""
    #and now finally the basic shear flow value at each point is computed!


    flow_upper = []
    flow_right = []
    flow_lower = []
    flow_left = []
    shearvalue1 = 0
    shearvalue2 = sum(q_luru_y)
    #print(shearvalue2)
    shearvalue3 = sum(q_luru_y)+sum(q_rurb_y)
    shearvalue4 = sum(q_luru_y)+sum(q_rurb_y)+sum(q_rblb_y)

    for i in range(0,len(mesh1)):
        #print(i)
        shearvalue1 += q_luru_y[i]
        flow_upper.append(shearvalue1/len(mesh1))
        shearvalue2 += q_rurb_y[i]
        flow_right.append(shearvalue2/len(mesh1))
        shearvalue3 += q_rblb_y[i]
        flow_lower.append(shearvalue3/len(mesh1))
        shearvalue4 += q_lblu_y[i]
        flow_left.append(shearvalue4/len(mesh1))


    flow_upper = np.array(flow_upper)
    flow_right = np.array(flow_right)
    flow_lower = np.array(flow_lower)
    flow_left = np.array(flow_left)

    #print(len(flow_upper))
    #print(len(flow_right))
    #print(len(flow_lower))
    #print(len(flow_left))

    #print(flow_upper)
    #print(flow_right)
    #print(flow_lower)
    #print(flow_left)

    #-------------------------------------------------------------------------
    #Shear center x coordinate
    #-------------------------------------------------------------------------


    q01 = sum(flow_upper*(length_upper_skin/len(mesh1)))
    q02 = sum(flow_right*(length_right_side/len(mesh1)))
    q03 = sum(flow_lower*(length_lower_skin/len(mesh1)))
    q04 = sum(flow_left*(length_left_side/len(mesh1)))


    """COMMENT"""
    #Defining constant shear flow q0 through the cut closed section

    q0 = (q01/(G*t1)+q02/(G*t2)+q03/(G*t3)+q04/(G*t4))/(length_upper_skin/(G*t1)+length_right_side/(G*t2)+length_lower_skin/(G*t3)+length_left_side/(G*t4))
    # print(q01)
    # print(q02)
    # print(q03)
    # print(q04)
    # print(q0)

    Am = 0.5*(length_left_side+length_right_side)*(width)
    #print(Am)

    """COMMENT"""
    #Defining the distance xi from top left corner to shear center

    if abs(Vy)<0.1:
        xi_luru_corner = 0
    else:
        xi_luru_corner = (-2*q0*Am+sum(flow_right*(length_right_side/len(mesh1)))*width+sum(flow_lower*(length_lower_skin/len(mesh1)))*length_left_side*np.cos(angle_from_horizontal_lower))/Vy

    # print("Shear center x-coordinate", round(abs(xi_luru_corner),3))


    #Distance from shear center to centroid
    xi = abs(x_centroid)-abs(xi_luru_corner)


    #-------------------------------------------------------------------------
    #Basic shear flow due to forces in x
    #------------------------------------------------------------------------- 

    xds_1 = np.empty(len(mesh1))
    xds_2 = np.empty(len(mesh1))
    xds_3 = np.empty(len(mesh1))
    xds_4 = np.empty(len(mesh1))

    int_xds_luru = np.empty(len(mesh1))
    int_xds_rurb = np.empty(len(mesh1))
    int_xds_rblb = np.empty(len(mesh1))
    int_xds_lblu = np.empty(len(mesh1))

    """COMMENT"""
    #Integrating through the mesh points
    #yds_1,2,3 and 4 indicate expression for y in terms of s (mesh location along the skin length) 
    #int_yds indicates integration of the aforementioned expression

    #Naming convention for wing skin
    #l=left
    #r=right
    #u=upper
    #b=bottom

    for i in mesh1:
        
        xds_1[i] = x_neutral_axis-np.cos(angle_from_horizontal_upper)*(length_upper_skin*mesh1[i]/(len(mesh1)))
        int_xds_luru[i] = x_neutral_axis*(length_upper_skin*mesh1[i]/(len(mesh1)))-np.cos(angle_from_horizontal_upper)*(length_upper_skin*mesh1[i]/(len(mesh1)))**2/2

        xds_2[i] = -(width-x_neutral_axis)
        int_xds_rurb[i] = -width*(length_right_side*mesh1[i]/(len(mesh1)))+x_neutral_axis*(length_right_side*mesh1[i]/(len(mesh1)))

        xds_3[i] = -(x_neutral_axis-np.cos(angle_from_horizontal_lower)*((length_lower_skin*mesh1[i])/(len(mesh1))))
        int_xds_rblb[i] = -(x_neutral_axis*(length_lower_skin*mesh1[i])/(len(mesh1))-np.cos(angle_from_horizontal_lower)*((length_lower_skin*mesh1[i])/(len(mesh1)))**2/2)

        xds_4[i] = x_neutral_axis
        int_xds_lblu[i] = x_neutral_axis*(length_left_side*mesh1[i]/(len(mesh1)))

    #print(xds_1)
    #print(xds_2)
    #print(xds_3)
    #print(xds_4)

    #print(int_xds_luru)
    #print(int_xds_rurb)
    #print(int_xds_rblb)
    #print(int_xds_lblu)

    q_luru_x = np.empty(len(mesh1))
    for i in range(0,len(mesh1)):
        if i<= np.argmax(int_xds_luru):
            q_luru_x[i] = -t1*((Vx*Ixx-Vy*Ixy)/(Ixx*Iyy-Ixy**2))*int_xds_luru[i]
        else:
            q_luru_x[i] = t1*((Vx*Ixx-Vy*Ixy)/(Ixx*Iyy-Ixy**2))*int_xds_luru[i]

    #print(q_luru_x)

    q_rurb_x = t2*((Vx*Ixx-Vy*Ixy)/(Ixx*Iyy-Ixy**2))*int_xds_rurb
    #print(q_rurb_x)

    q_rblb_x = np.empty(len(mesh1))
    for i in range(0,len(mesh1)):
        if i<= np.argmax(int_xds_rblb):
            q_rblb_x[i] = t3*((Vx*Ixx-Vy*Ixy)/(Ixx*Iyy-Ixy**2))*int_xds_rblb[i]
        else:
            q_rblb_x[i] = -t3*((Vx*Ixx-Vy*Ixy)/(Ixx*Iyy-Ixy**2))*int_xds_rblb[i]
    #print(q_rblb_x)

    q_lblu_x = -t4*((Vx*Ixx-Vy*Ixy)/(Ixx*Iyy-Ixy**2))*int_xds_lblu
    #print(q_lblu_x)

    """COMMENT"""
    #and now finally the basic shear flow value at each point is computed!

    flow_upper_x = []
    flow_right_x = []
    flow_lower_x = []
    flow_left_x = []
    shearvalue5 = 0
    shearvalue6 = sum(q_luru_x)
    #print(shearvalue6)
    shearvalue7 = sum(q_luru_x)+sum(q_rurb_x)
    shearvalue8 = sum(q_luru_x)+sum(q_rurb_x)+sum(q_rblb_x)

    for i in range(0,len(mesh1)):
        #print(i)
        shearvalue5 += q_luru_x[i]
        flow_upper_x.append(shearvalue5/len(mesh1))
        shearvalue6 += q_rurb_x[i]
        flow_right_x.append(shearvalue6/len(mesh1))
        shearvalue7 += q_rblb_x[i]
        flow_lower_x.append(shearvalue7/len(mesh1))
        shearvalue8 += q_lblu_x[i]
        flow_left_x.append(shearvalue8/len(mesh1))


    flow_upper_x = np.array(flow_upper_x)
    flow_right_x = np.array(flow_right_x)
    flow_lower_x = np.array(flow_lower_x)
    flow_left_x = np.array(flow_left_x)

    #print(len(flow_upper_x))
    #print(len(flow_right_x))
    #print(len(flow_lower_x))
    #print(len(flow_left_x))

    #print(flow_upper_x)
    #print(flow_right_x)
    #print(flow_lower_x)
    #print(flow_left_x)

    #-------------------------------------------------------------------------
    #Shear center y coordinate
    #-------------------------------------------------------------------------


    q05 = sum(flow_upper_x*(length_upper_skin/len(mesh1)))
    q06 = sum(flow_right_x*(length_right_side/len(mesh1)))
    q07 = sum(flow_lower_x*(length_lower_skin/len(mesh1)))
    q08 = sum(flow_left_x*(length_left_side/len(mesh1)))


    """COMMENT"""
    #Defining constant shear flow q0 through the cut closed section

    q0_x = (q05/(G*t1)+q06/(G*t2)+q07/(G*t3)+q08/(G*t4))/(length_upper_skin/(G*t1)+length_right_side/(G*t2)+length_lower_skin/(G*t3)+length_left_side/(G*t4))
    # print(q05)
    # print(q06)
    # print(q07)
    # print(q08)
    # print(q0_x)

    Am = 0.5*(length_left_side+length_right_side)*(width)
    #print(Am)

    """COMMENT"""
    #Defining the distance eta from top left corner to shear center

    if abs(Vx)<0.1:
        eta_luru_corner = 0

    else:
        eta_luru_corner = (-2*q0_x*Am-sum(flow_right_x*(length_right_side/len(mesh1)))*width+sum(flow_lower_x*(length_lower_skin/len(mesh1)))*length_left_side*np.cos(angle_from_horizontal_lower))/Vx

    # print("Shear center y-coordinate", round(abs(eta_luru_corner),3))


    #Distance from shear center to centroid
    eta = abs(y_centroid)-abs(eta_luru_corner)

    #-------------------------------------------------------------------------
    #Total constant shear flow
    #-------------------------------------------------------------------------

    """COMMENT"""
    #Constant shear flow

    if abs(Vy)<0.1:
        qb1=0
        qb2=0
        qb3=0
        qb4=0

    else:
        qb1=q01
        qb2=q02
        qb3=q03
        qb4=q04

    if abs(Vx)<0.1:
        qb5 = 0
        qb6 = 0
        qb7 = 0
        qb8 = 0

    else:    
        qb5 = sum(flow_upper_x*(length_upper_skin/len(mesh1)))
        qb6 = sum(flow_right_x*(length_right_side/len(mesh1)))
        qb7 = sum(flow_lower_x*(length_lower_skin/len(mesh1)))
        qb8 = sum(flow_left_x*(length_left_side/len(mesh1)))

    #print(qb1)
    #print(qb2)
    #print(qb3)
    #print(qb4)
    #print(qb5)
    #print(qb6)
    #print(qb7)
    #print(qb8)

    """COMMENT"""
    #Forces applied at distance from top left corner

    dy_Vx = length_left_side-y_centroid+z_Vx
    dx_Vy = width-x_centroid-x_Vy

    #print(dy_Vx)
    #print(dx_Vy)



    #qs0_test = (-Vy*dx_Vy-Vx*dy_Vx-(qb2+qb6)*width-(qb3+qb7)*length_left_side*np.cos(angle_from_horizontal_lower))/(2*Am)
    #qs0_test2 = -(qb1+qb2+qb3+qb4+qb5+qb6+qb7+qb8)/(length_upper_skin+length_right_side+length_lower_skin+length_left_side)

    #Taking moments around line of action of forces
    rho_lower = ((length_left_side-dy_Vx)/np.cos(angle_from_horizontal_lower))-((length_left_side-dy_Vx)*np.tan(angle_from_horizontal_lower)+dx_Vy)*np.sin(angle_from_horizontal_lower)
    rho_upper = (dy_Vx*np.cos(angle_from_horizontal_upper))-(dx_Vy+np.tan(angle_from_horizontal_upper)*dy_Vx)*np.sin(angle_from_horizontal_upper)
    qs0 = -((qb1+qb5)*(rho_upper)+(qb2+qb6)*(width-dx_Vy)+(qb3+qb7)*(rho_lower)+(qb4+qb8)*(dx_Vy))/(2*Am)

    #print(qs0)

    flow_qs0 = qs0*len(mesh1)


    #-------------------------------------------------------------------------
    #Total shear flow and shear stress at each point of mesh
    #-------------------------------------------------------------------------

    if abs(Vy)<0.1:
        q_luru_y=q_luru_y*0
        q_rurb_y=q_rurb_y*0
        q_rblb_y=q_rblb_y*0
        q_lblu_y=q_lblu_y*0
        
    if abs(Vx)<0.1:
        q_luru_x=q_luru_x*0
        q_rurb_x=q_rurb_x*0
        q_rblb_x=q_rblb_x*0
        q_lblu_x=q_lblu_x*0
            
    total_shear_flow_upper = []
    total_shear_flow_right = []
    total_shear_flow_lower = []
    total_shear_flow_left = []
    shear_luru = flow_qs0
    shear_rurb = flow_qs0+sum(q_luru_y)+sum(q_luru_x)
    shear_rblb = flow_qs0+sum(q_luru_y)+sum(q_luru_x) + sum(q_rurb_y)+sum(q_rurb_x)
    shear_lblu = flow_qs0+sum(q_luru_y)+sum(q_luru_x) + sum(q_rurb_y)+sum(q_rurb_x) + sum(q_rblb_y) + sum(q_rblb_x)

    for i in range(0,len(mesh1)):
        shear_luru += q_luru_y[i]+q_luru_x[i]
        total_shear_flow_upper.append(shear_luru/len(mesh1))
        shear_rurb += q_rurb_y[i]+q_rurb_x[i]
        total_shear_flow_right.append(shear_rurb/len(mesh1))
        shear_rblb += q_rblb_y[i]+q_rblb_x[i]
        total_shear_flow_lower.append(shear_rblb/len(mesh1))
        shear_lblu += q_lblu_y[i]+q_lblu_x[i]
        total_shear_flow_left.append(shear_lblu/len(mesh1))

    total_shear_flow_upper = np.array(total_shear_flow_upper)
    total_shear_flow_right = np.array(total_shear_flow_right)
    total_shear_flow_lower = np.array(total_shear_flow_lower)
    total_shear_flow_left = np.array(total_shear_flow_left)

    # print(total_shear_flow_upper)
    # print(total_shear_flow_right)
    # print(total_shear_flow_lower)
    # print(total_shear_flow_left)

    max_shear_upper = max(total_shear_flow_upper)/t1/1000000
    max_shear_right = max(total_shear_flow_right)/t2/1000000
    max_shear_lower = max(total_shear_flow_lower)/t3/1000000
    max_shear_left = max(total_shear_flow_left)/t4/1000000

    max_shear_loc_upper = np.argmax(total_shear_flow_upper)*length_upper_skin/len(mesh1)
    max_shear_loc_right = np.argmax(total_shear_flow_right)*length_right_side/len(mesh1)
    max_shear_loc_lower = np.argmax(total_shear_flow_lower)*length_lower_skin/len(mesh1)
    max_shear_loc_left = np.argmax(total_shear_flow_left)*length_left_side/len(mesh1)


    # print("Max shear stress in upper skin [MPa] and location", max_shear_upper, max_shear_loc_upper)
    # print("Max shear stress in right skin [MPa] and location", max_shear_right, max_shear_loc_right)
    # print("Max shear stress in lower skin [MPa] and location", max_shear_lower, max_shear_loc_lower)
    # print("Max shear stress in left skin [MPa] and location", max_shear_left, max_shear_loc_left)

    min_shear_upper = min(total_shear_flow_upper)/t1/1000000
    min_shear_right = min(total_shear_flow_right)/t2/1000000
    min_shear_lower = min(total_shear_flow_lower)/t3/1000000
    min_shear_left = min(total_shear_flow_left)/t4/1000000

    min_shear_loc_upper = np.argmin(total_shear_flow_upper)*length_upper_skin/len(mesh1)
    min_shear_loc_right = np.argmin(total_shear_flow_right)*length_right_side/len(mesh1)
    min_shear_loc_lower = np.argmin(total_shear_flow_lower)*length_lower_skin/len(mesh1)
    min_shear_loc_left = np.argmin(total_shear_flow_left)*length_left_side/len(mesh1)    

    # print("Min shear stress in upper skin [MPa] and location", min_shear_upper, min_shear_loc_upper)
    # print("Min shear stress in right skin [MPa] and location", min_shear_right, min_shear_loc_right)
    # print("Min shear stress in lower skin [MPa] and location", min_shear_lower, min_shear_loc_lower)
    # print("Min shear stress in left skin [MPa] and location", min_shear_left, min_shear_loc_left)

    #-------------------------------------------------------------------------
    #Rate of twist
    #-------------------------------------------------------------------------

    if abs(Vy)<0.1:
        Vy = 0
    
    if abs(Vx)<0.1:
        Vx = 0

    Torque_due_to_shear_forces = abs(dy_Vx-abs(eta_luru_corner))*-Vx+abs(dx_Vy-abs(xi_luru_corner))*Vy

    #print(Torque_due_to_shear_forces)
    J=Ixx+Iyy
    
    angle_of_twist = Torque_due_to_shear_forces/(J*G)
    #print("Rate of twist", angle_of_twist_per_unit_length*180/np.pi)


    return xi,eta,max_shear_upper, max_shear_loc_upper,max_shear_right, max_shear_loc_right,max_shear_lower, max_shear_loc_lower,max_shear_left, max_shear_loc_left,min_shear_upper, min_shear_loc_upper,min_shear_right, min_shear_loc_right,min_shear_lower, min_shear_loc_lower,min_shear_left, min_shear_loc_left,angle_of_twist
