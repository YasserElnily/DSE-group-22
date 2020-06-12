# -*- coding: utf-8 -*-
"""
Created on Friday June 5 2020
@author: Roosa
"""

"""Normal stress function"""

#INPUTS:
"""

In total 20 input arguments

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

Moments caused by forces
- My = Moment around y-axis, positive for beam bending towards trailing edge
- Mx = Moment around x-axis, negative for beam bending upwards

"""

#OUTPUTS
"""
max_norm_upper
max_norm_loc_upper
max_norm_right
max_norm_loc_right
max_norm_lower
max_norm_loc_lower
max_norm_left
max_norm_loc_left
min_norm_upper
min_norm_loc_upper
min_norm_right
min_norm_loc_right
min_norm_lower
min_norm_loc_lower
min_norm_left
min_norm_loc_left
"""


def normal_stress(t1,t2,t3,t4,length_upper_skin,length_right_side,length_lower_skin,length_left_side,angle_from_horizontal_upper,angle_from_horizontal_lower,width,x_centroid,y_centroid,x_neutral_axis,y_neutral_axis,Ixx,Iyy,Ixy,My,Mx)

    #-------------------------------------------------------------------------
    #Convert length to mesh points
    #-------------------------------------------------------------------------
    """COMMENT"""
    #Feel free to change the stop value

    mesh1 = np.arange(0,100,1)
    #print(mesh1)

    """COMMENT"""
    #defining empty arrays to store values later
    y1 = np.empty(len(mesh1))
    y2 = np.empty(len(mesh1))
    y3 = np.empty(len(mesh1))
    y4 = np.empty(len(mesh1))

    x1 = np.empty(len(mesh1))
    x2 = np.empty(len(mesh1))
    x3 = np.empty(len(mesh1))
    x4 = np.empty(len(mesh1))

    sigma1 = np.empty(len(mesh1))
    sigma2 = np.empty(len(mesh1))
    sigma3 = np.empty(len(mesh1))
    sigma4 = np.empty(len(mesh1))


    #-------------------------------------------------------------------------
    #Normal stress in upper skin
    #-------------------------------------------------------------------------

    for i in mesh1:

        y1[i] = y_neutral_axis-np.sin(angle_from_horizontal_upper)*length_upper_skin*mesh1[i]/(len(mesh1))
        x1[i] = x_neutral_axis-np.cos(angle_from_horizontal_upper)*(length_upper_skin*mesh1[i]/(len(mesh1)))
        
        sigma1[i] = ((Mx*Iyy-My*Ixy)*y1[i]+(My*Ixx-Mx*Ixy)*x1[i])/(Ixx*Iyy-Ixy**2)

    #print(y1)
    #print(x1)
    #print(sigma1)

    #-------------------------------------------------------------------------
    #Normal stress in trailing edge spar
    #-------------------------------------------------------------------------

    for i in mesh1:
        
        y2[i] = (y_neutral_axis-(np.sin(angle_from_horizontal_upper)*length_upper_skin))-length_right_side*mesh1[i]/(len(mesh1))
        x2[i] = -(width-x_neutral_axis)

        sigma2[i] = ((Mx*Iyy-My*Ixy)*y2[i]+(My*Ixx-Mx*Ixy)*x2[i])/(Ixx*Iyy-Ixy**2)

    #print(y2)
    #print(x2)
    #print(sigma2)

    #-------------------------------------------------------------------------
    #Normal stress in lower skin
    #-------------------------------------------------------------------------

    for i in mesh1:
        
        y3[i]=-((length_left_side-y_neutral_axis-np.sin(angle_from_horizontal_lower)*(length_lower_skin-(length_lower_skin*mesh1[i]/len(mesh1)))))
        x3[i] = -(x_neutral_axis-np.cos(angle_from_horizontal_lower)*((length_lower_skin*mesh1[i])/(len(mesh1))))

        sigma3[i] = ((Mx*Iyy-My*Ixy)*y3[i]+(My*Ixx-Mx*Ixy)*x3[i])/(Ixx*Iyy-Ixy**2)

    #print(y3)
    #print(x3)
    #print(sigma3)

    #-------------------------------------------------------------------------
    #Normal stress in leading edge spar
    #-------------------------------------------------------------------------

    for i in mesh1:

        y4[i]=-((length_left_side-y_neutral_axis)-(length_left_side*mesh1[i]/len(mesh1)))
        x4[i] = x_neutral_axis
        
        sigma4[i] = ((Mx*Iyy-My*Ixy)*y4[i]+(My*Ixx-Mx*Ixy)*x4[i])/(Ixx*Iyy-Ixy**2)

    #print(y4)
    #print(x4)
    #print(sigma4)

    #-------------------------------------------------------------------------
    #Storing max and min stresses
    #-------------------------------------------------------------------------

    max_norm_upper = max(sigma1)/1000000
    max_norm_right = max(sigma2)/1000000
    max_norm_lower = max(sigma3)/1000000
    max_norm_left = max(sigma4)/1000000

    max_norm_loc_upper = np.argmax(sigma1)*length_upper_skin/len(mesh1)
    max_norm_loc_right = np.argmax(sigma2)*length_right_side/len(mesh1)
    max_norm_loc_lower = np.argmax(sigma3)*length_lower_skin/len(mesh1)
    max_norm_loc_left = np.argmax(sigma4)*length_left_side/len(mesh1)

    #print("Max normal stress in upper skin [MPa] and location", max_norm_upper, max_norm_loc_upper)
    #print("Max normal stress in right skin [MPa] and location", max_norm_right, max_norm_loc_right)
    #print("Max normal stress in lower skin [MPa] and location", max_norm_lower, max_norm_loc_lower)
    #print("Max normal stress in left skin [MPa] and location", max_norm_left, max_norm_loc_left)

    min_norm_upper = min(sigma1)/1000000
    min_norm_right = min(sigma2)/1000000
    min_norm_lower = min(sigma3)/1000000
    min_norm_left = min(sigma4)/1000000

    min_norm_loc_upper = np.argmin(sigma1)*length_upper_skin/len(mesh1)
    min_norm_loc_right = np.argmin(sigma2)*length_right_side/len(mesh1)
    min_norm_loc_lower = np.argmin(sigma3)*length_lower_skin/len(mesh1)
    min_norm_loc_left = np.argmin(sigma4)*length_left_side/len(mesh1)    

    #print("Min normal stress in upper skin [MPa] and location", min_norm_upper, min_norm_loc_upper)
    #print("Min normal stress in right skin [MPa] and location", min_norm_right, min_norm_loc_right)
    #print("Min normal stress in lower skin [MPa] and location", min_norm_lower, min_norm_loc_lower)
    #print("Min normal stress in left skin [MPa] and location", min_norm_left, min_norm_loc_left)
    

    return max_norm_upper,max_norm_loc_upper,max_norm_right, max_norm_loc_right,max_norm_lower, max_norm_loc_lower,max_norm_left, max_norm_loc_left,min_norm_upper, min_norm_loc_upper,min_norm_right, min_norm_loc_right,min_norm_lower, min_norm_loc_lower,min_norm_left, min_norm_loc_left
