#install xelatex for pgf files.


from numpy import *
from matplotlib import pyplot as plt
from ISA_calculator import ISA

#values we need to check and change!!!
h = 3048#3048#11887.2
m_to = 775#kg
print("Altitude = " + str(h) + "m")
C_L_max_clean = 1.41#1.3944#2.023
S_ref = 9
cruise_speed= 61 #m/s
C_L_alpha_M0 = 4.633 #lift curve at mach zero (nothing moment related)
MAC = 1.5
#VERY IMPORTANT COMMENT: one should check line 130 (N_k) for the maximum load factor at TO and 'line3' should be changed to correct formula

#values that can be changed but probably will not anymore
n_max = 2.5#2.1 + 24000/(m_to*2.205+10000)
n_min = -n_max*0.4
print('n max = ',n_max, ' n min = ', n_min)
accuracy = 0.01
n_max_VTOL = 2
n_min_VTOL = -0.5
n_safe_to_conv = 1.22

#fixed values
rho_0 = 1.225
rho = ISA(h)[2]
speed_of_sound = ISA(h)[3]
S_flapped = 1.25 * S_ref
g = 9.80665
C_L_max_HLD = 2.36 #does not need to be changed, it is not used
n_max_HLD = 1.5
#M_C = 0.79

#calculations
w = m_to*g/S_ref #wing loading

V_S_new = sqrt(2 * m_to * g / (rho_0 * C_L_max_clean * S_ref))
print(V_S_new)
diff = 1.
loopcount = 0
while diff > 0.0000001:
    V_S_old = V_S_new
    V_S_new = sqrt(2 * m_to * g / (rho_0 * C_L_max_clean * sqrt(1-(V_S_old/speed_of_sound)*(V_S_old/speed_of_sound)) * S_ref))
    diff = abs(V_S_new-V_S_old)
    #print(diff)
    loopcount= loopcount+1
V_S = V_S_new
print(V_S)
print(loopcount)

V_A = V_S * sqrt(n_max)
V_C = cruise_speed*sqrt(rho/rho_0)#*M_C*ISA(11887.2)[3]#118.5
V_D = V_C/0.8 #148.125

V_S_1_new = sqrt(2 * m_to * g / (rho_0 * C_L_max_HLD * S_flapped))
diff2 = 1.
counter2=0
while diff2 > 0.0000001:
    V_S_1_old = V_S_1_new
    print(counter2, V_S_1_old)
    V_S_1_new = sqrt(2 * m_to * g / (rho_0 * C_L_max_HLD * sqrt(1-(V_S_1_old/speed_of_sound)*(V_S_1_old/speed_of_sound)) * S_flapped))
    diff2 = abs(V_S_1_new-V_S_1_old)
    counter2=counter2+1
V_S_1 = V_S_1_new
print(V_S_1)

V_EAS = arange(0., V_D+accuracy, accuracy)#+0.00001*accuracy, accuracy)

def C_L_alpha(V, h):
    M = V/ISA(h)[3]
    return C_L_alpha_M0/sqrt(1-M*M)

def n1(V):
    return V*V/(V_S*V_S)

def n_HLD(V):
    return V*V/(V_S_1 * V_S_1)#C_L_max_HLD * rho_0 * S_flapped / (2 * m_to * g)

def n4(V):
    return ((0-n_min)/(V_D-V_C))*(V - V_D) + 0

def n6(V):
    return -V*V/(V_A*V_A)


line1 = zeros(V_EAS.shape)
line2 = zeros(V_EAS.shape)
line_HLD = zeros(V_EAS.shape)

go_on_3 = True
go_on_4 = True


for i in range(len(V_EAS)):
    if n1(V_EAS[i]) <= n_max:
        line1[i] = n1(V_EAS[i])
    else:
        line1[i] = n_max

    if n6(V_EAS[i]) >= n_min:
        line2[i] = n6(V_EAS[i])
    elif V_EAS[i] <= V_C:
        line2[i] = n_min
    else:
        line2[i] = n4(V_EAS[i])

    if go_on_3 & (n_HLD(V_EAS[i]) <= n_max_HLD):
        line_HLD[i] = n_HLD(V_EAS[i])
    elif go_on_3 & (n_HLD(V_EAS[i]) > n_max_HLD):
        line_HLD[i] = n_max_HLD

    if go_on_4 & (n1(V_EAS[i]) >= n_max_HLD):
        i_G = i
        go_on_4 = False

    #if go_on_3 & (V_EAS[i] <= V_S_1):
    #    line_HLD[i] = n_HLD(V_EAS[i])
    #elif go_on_3 & (V_EAS[i] > V_S_1):
     #   line_HLD[i:] = n_HLD(V_EAS[i])
     #   go_on_3 = False

   # if go_on_4 & (n1(V_EAS[i]) >= n_HLD(V_S_1)):
     #   i_G = i
    #    go_on_4 = False

########## VTOL envelope calculations
n_K = 1.5 ############ Assumption!!!! Do proper power calculation (n_K is determined by maximum available lift at take-off)
line3 = zeros(V_EAS.shape)
line3 = (1.5*m_to*g+C_L_max_clean*0.5*rho_0*(V_EAS**2)*S_ref)/(m_to*g)#0.5 / 15 * V_EAS + n_K ### fill line 3 with calculation about proprotor lift + wing lift
end_index_line3 = 0
for i in range(len(line3)):
    if line3[i] <= n_max_VTOL:
        end_index_line3 = i

line3 = line3[0:end_index_line3 + 1]

V_EAS_line3 = V_EAS[0:end_index_line3 + 1]

V_H = 0
#find velocity where line1 (stall line of airplane mode) = 1.22
V_H = sqrt(n_safe_to_conv*V_S*V_S)    

#find velocity where line2 (negative stall line of airplane mode)equals n_min_VTOL
V_end_n_min_VTOL = sqrt(-n_min_VTOL*V_A*V_A)
   
for i in range(len(V_EAS)):
    if V_EAS[i] < V_H:
        index_V_H = i
    
line1a = line1[0:index_V_H]
V_EAS_line1a = V_EAS[0:index_V_H]
line1b = line1[index_V_H:]
V_EAS_line1b = V_EAS[index_V_H:]


for i in range(len(V_EAS)):
    if V_EAS[i] < V_end_n_min_VTOL:
        index_V_end_n_min_VTOL = i

line2a = line2[0:index_V_end_n_min_VTOL]
V_EAS_line2a = V_EAS[0:index_V_end_n_min_VTOL]
line2b = line2[index_V_end_n_min_VTOL:]
V_EAS_line2b = V_EAS[index_V_end_n_min_VTOL:]



fig1 = plt.figure()
#fig.suptitle("TEST")
maneuvers = fig1.add_subplot(111)


dashed_lines_color = "k"
#Flight envelope

envelope_linewidth = 2.5
m_envelope_color = "k"

maneuvers.plot(V_EAS_line1a, line1a, color=dashed_lines_color, linestyle="dashed", linewidth=envelope_linewidth)
maneuvers.plot(V_EAS_line1b, line1b, color=m_envelope_color, linewidth=envelope_linewidth)
maneuvers.vlines(V_D, 0., n_max, color=m_envelope_color, linewidth=envelope_linewidth)
maneuvers.plot(V_EAS_line2a, line2a, color=dashed_lines_color, linestyle="dashed", linewidth=envelope_linewidth)
maneuvers.plot(V_EAS_line2b, line2b, color=m_envelope_color, linewidth=envelope_linewidth)
# VTOL
maneuvers.vlines(0., n_min_VTOL, n_K, color=m_envelope_color, linewidth=envelope_linewidth)
maneuvers.plot(V_EAS_line3, line3, color=m_envelope_color, linewidth=envelope_linewidth)
maneuvers.hlines(n_max_VTOL, V_EAS[end_index_line3], V_H, color=m_envelope_color, linewidth=envelope_linewidth)
maneuvers.vlines(V_H, n_safe_to_conv, n_max_VTOL, color=m_envelope_color, linewidth=envelope_linewidth)
maneuvers.hlines(n_min_VTOL, 0, V_end_n_min_VTOL, color=m_envelope_color, linewidth=envelope_linewidth)


#Line for deployed flaps

#maneuvers.plot(V_EAS[:i_G], line_HLD[:i_G], color=m_envelope_color, linewidth=envelope_linewidth)

#Dashed lines



maneuvers.vlines(V_S, 0., 1., color=dashed_lines_color, linestyle="dashed")
maneuvers.vlines(V_A, n_min, n_max, color=dashed_lines_color, linestyle="dashed")
maneuvers.vlines(V_C, n_min, n_max, color=dashed_lines_color, linestyle="dashed")
maneuvers.hlines(1, -10, V_S, color=dashed_lines_color, linestyle="dashed")
maneuvers.hlines(n_max, -10, V_A, color=dashed_lines_color, linestyle="dashed")
maneuvers.hlines(n_min, -10, V_A, color=dashed_lines_color, linestyle="dashed")

#### VTOL
maneuvers.vlines(V_H, 0., n_safe_to_conv, color=dashed_lines_color, linestyle="dashed")
maneuvers.hlines(n_max_VTOL, -10, V_EAS[end_index_line3], color=dashed_lines_color, linestyle="dashed")
maneuvers.hlines(n_min_VTOL, -10, 0., color=dashed_lines_color, linestyle="dashed")
maneuvers.hlines(n_safe_to_conv, -10, V_H, color=dashed_lines_color, linestyle="dashed")





#Fixing the x-axis to the origin

#maneuvers.spines['left'].set_position('zero')
maneuvers.spines['right'].set_color('none')
maneuvers.spines['bottom'].set_position('zero')
maneuvers.spines['top'].set_color('none')
#maneuvers.spines['left'].set_smart_bounds(True)
#maneuvers.spines['bottom'].set_smart_bounds(True)
maneuvers.xaxis.set_ticks_position('bottom')
#maneuvers.yaxis.set_ticks_position('left')

maneuvers.grid(True)

maneuvers.set_title("(V, n)-diagram for maneuvers")
maneuvers.set_xlabel(r"$V_{EAS} [\frac{m}{s}]$")
maneuvers.xaxis.set_label_coords(1.08, 0.32)
maneuvers.set_ylabel(r"$n_m$")
maneuvers.set_xlim(-2, V_D +5) 

#maneuvers.text(V_S_1, 0 + 0.05, r"$V_{S_1}$")
maneuvers.text(V_S, 0 + 0.05, r"$V_S$")
maneuvers.text(V_H, 0 + 0.05, r"$V_{EOT}$")
maneuvers.text(V_A, 0 + 0.05, r"$V_A$")
maneuvers.text(V_C, 0 + 0.05, r"$V_C$")
maneuvers.text(V_D, 0 + 0.05, r"$V_D$")

#maneuvers.text(V_S_1 - 5, n_max_HLD + 0.05, "Flaps down")
maneuvers.text(V_A, n_max + 0.05, "A")
maneuvers.text(V_D, n_max + 0.05, "D")
maneuvers.text(V_C, n_min - 0.2, "F")
maneuvers.text(V_A, n_min - 0.2, "H")
#VTOL
maneuvers.text(V_end_n_min_VTOL, n_min_VTOL - 0.2, "G")
maneuvers.text(0, n_min_VTOL - 0.2, "J")
maneuvers.text(0, n_K + 0.05, "K")
maneuvers.text(V_EAS[end_index_line3], n_max_VTOL + 0.05, "L")
maneuvers.text(V_H, n_max_VTOL + 0.05, "M")

maneuvers.text(V_H/2 , n_K, "VTOL/CONV")
maneuvers.text(V_C + 2 , n_K, "Airplane")

#plt.show()

####################################### Gust envelope

g_envelope_color = "k"

if (h >= 0.) & (h <= 6096.):
    U_B = 20.12
    U_C = 15.24
    U_D = 7.62
elif (h > 6096.) & (h <= 15240):
    U_B = ((20.12-11.5)/(6096-15240))*(h-15240)+11.5
    U_C = ((15.24-7.62)/(6096-15240))*(h-15240)+7.62
    U_D = ((7.62-3.81)/(6096-15240))*(h-15240)+3.81
else:
    SystemExit

def my_g(V):
    return 2*w/(rho * MAC * C_L_alpha(V, h) * g)

def K_g(V):
    return 0.88 * my_g(V)/(5.3+my_g(V))

def ng(U, V):
    return 1 + (0.5 * rho_0 * C_L_alpha(V, h) / (m_to * g / S_ref)) * U * V * K_g(V)

def st_stall(V):
    return (V/V_S)*(V/V_S)


def abc(a, b, c):
    return [(-b+sqrt(b*b-4*a*c))/(2*a),(-b-sqrt(b*b-4*a*c))/(2*a)]

#V_stst6 = abc(1 / (V_S*V_S), rho_0 * C_L_alpha() * S_ref * U_B * K_g() / (2 * m_to * g), -1.)[0]
V_B = 0. #V_S * sqrt(1 + 0.88 * ((2*w/(rho*MAC*C_L_alpha*g))/(5.3+(2*w/(rho*MAC*C_L_alpha*g)))) * U_B * V_C * C_L_alpha/w) # Not correct yet!!!

ng1 = 0.
ng2 = 0.
ng3 = 0.
ng4 = 0.
ng5 = 0.
ng6 = 0.



gline1 = zeros(V_EAS.shape)
gline2 = zeros(V_EAS.shape)
gline3 = zeros(V_EAS.shape)
gline4 = zeros(V_EAS.shape)
gline5 = zeros(V_EAS.shape)
gline6 = zeros(V_EAS.shape)

gline12 = zeros(V_EAS.shape)
gline23 = zeros(V_EAS.shape)
gline45 = zeros(V_EAS.shape)
gline56 = zeros(V_EAS.shape)


static_stall = zeros(V_EAS.shape)

go_on = True
go_on_2 = True
i_V_B = 0
i_V_C = 0
i_V_D = 0
i_V_stst6 = 0

V_B = V_S*sqrt(ng(U_C, V_C))
if V_B>V_C:
    V_B=V_C


#Construct the curves/lines for each gust speed U & the static stall curve
for i in range(len(V_EAS)):
    gline1[i] = ng(U_B, V_EAS[i])
    gline2[i] = ng(U_C, V_EAS[i])
    gline3[i] = ng(U_D, V_EAS[i])
    gline4[i] = ng(-U_D, V_EAS[i])
    gline5[i] = ng(-U_C, V_EAS[i])
    gline6[i] = ng(-U_B, V_EAS[i])

    if (V_EAS[i] >= V_B-0.5*accuracy) & (V_EAS[i] <= V_B+0.5*accuracy):
        i_V_B = i
    if (V_EAS[i] >= V_C-0.5*accuracy) & (V_EAS[i] <= V_C+0.5*accuracy):
        i_V_C = i
    if (V_EAS[i] >= V_D-0.5*accuracy) & (V_EAS[i] <= V_D+0.5*accuracy):
        i_V_D = i
    #if (V_EAS[i] >= V_stst6-0.5*accuracy) & (V_EAS[i] <= V_stst6+0.5*accuracy):
    #    i_V_stst6 = i

    if go_on & (st_stall(V_EAS[i]) <= gline1[i]):
        static_stall[i] = st_stall(V_EAS[i])
    elif go_on & (st_stall(V_EAS[i]) > gline1[i]):
        static_stall[i] = st_stall(V_EAS[i])
        #V_B = V_EAS[i]
        #i_V_B = i
        #print(V_B)
        #ng1 = st_stall(V_EAS[i])
        #print(ng1)
        go_on = False

    if go_on_2 & (st_stall(V_EAS[i]) > gline6[i]):
        V_stst6 = V_EAS[i]
        i_V_stst6 = i
        ngstst6 = st_stall(V_EAS[i])
        go_on_2 = False

ng1 = st_stall(V_B)
ng1old = ng(U_B, V_B)
ng2 = ng(U_C, V_C)
ng3 = ng(U_D, V_D)
ng4 = ng(-U_D, V_D)
ng5 = ng(-U_C, V_C)
ng6 = ng(-U_B, V_B)

#print(ng2, ng3, ng4, ng5, ng6)

#Construct the straight connection lines
for i in range(len(V_EAS)):
    if V_B!=V_C:
        gline12[i] = ((ng2 - ng1) / (V_C - V_B)) * (V_EAS[i] - V_C) + ng2
        gline23[i] = ((ng3 - ng2) / (V_D - V_C)) * (V_EAS[i] - V_C) + ng2
        gline45[i] = ((ng5 - ng4) / (V_C - V_D)) * (V_EAS[i] - V_C) + ng5
        gline56[i] = ((ng6 - ng5) / (V_B - V_C)) * (V_EAS[i] - V_C) + ng5
    else:
        #gline12[i] = ((ng2 - ng1) / (V_C - V_B)) * (V_EAS[i] - V_C) + ng2
        gline23[i] = ((ng3 - ng2) / (V_D - V_C)) * (V_EAS[i] - V_C) + ng2
        gline45[i] = ((ng5 - ng4) / (V_C - V_D)) * (V_EAS[i] - V_C) + ng5
        #gline56[i] = ((ng6 - ng5) / (V_B - V_C)) * (V_EAS[i] - V_C) + ng5

i_gline5_end = 0
i_gline6_end = 0
i_gline45_start = 0
for i in range(len(V_EAS)):
    if gline5[i]>n_min:
        i_gline5_end = i
    if gline6[i]>n_min:
        i_gline6_end = i
    if gline45[i]<n_min:
        i_gline45_start = i

fig2 = plt.figure()
gusts = fig2.add_subplot(111)

gusts.plot(V_EAS[:i_V_B+1], gline1[:i_V_B+1], color=g_envelope_color, linestyle="dashed")
#gusts.plot(V_EAS[st_stall_stop_at:], gline1[st_stall_stop_at:], color=g_envelope_color, linestyle="solid")
gusts.plot(V_EAS[:i_V_C+1], gline2[:i_V_C+1], color=g_envelope_color, linestyle="dashed")
gusts.plot(V_EAS[:i_V_D+1], gline3[:i_V_D+1], color=g_envelope_color, linestyle="dashed")
gusts.plot(V_EAS[:i_V_D+1], gline4[:i_V_D+1], color=g_envelope_color, linestyle="dashed")
gusts.plot(V_EAS[:i_V_C+1], gline5[:i_V_C+1], color=g_envelope_color, linestyle="dashed")
gusts.plot(V_EAS[:i_V_stst6+1], gline6[:i_V_stst6+1], color=g_envelope_color, linestyle="dashed")
#gusts.plot(V_EAS[i_V_stst6:i_V_B+1], gline6[i_V_stst6:i_V_B+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)
gusts.plot(V_EAS[i_V_stst6:i_gline6_end+1], gline6[i_V_stst6:i_gline6_end+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)
gusts.plot(V_EAS[i_gline6_end:i_V_B+1], gline6[i_gline6_end:i_V_B+1], color=g_envelope_color, linestyle="dashed")
gusts.plot(V_EAS[:i_V_B+1], static_stall[:i_V_B+1], color=g_envelope_color, linestyle="dashed")
gusts.plot(V_EAS[i_V_stst6:i_V_B+1], static_stall[i_V_stst6:i_V_B+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)


gusts.plot(V_EAS[i_V_B:i_V_C+1], gline12[i_V_B:i_V_C+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)
gusts.plot(V_EAS[i_V_C:i_V_D+1], gline23[i_V_C:i_V_D+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)
#gusts.plot(V_EAS[i_V_C:i_V_D+1], gline45[i_V_C:i_V_D+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)
gusts.plot(V_EAS[i_gline45_start:i_V_D+1], gline45[i_gline45_start:i_V_D+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)

#gusts.plot(V_EAS[i_V_B:i_V_C+1], gline56[i_V_B:i_V_C+1], color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)
gusts.vlines(V_D, ng4, ng3, color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)

gusts.vlines(V_C, min(0.,n_min), ng2, color=g_envelope_color, linestyle="dashed")
gusts.vlines(V_B, min(0.,ng6), ng1old, color=g_envelope_color, linestyle="dashed")
gusts.vlines(V_D, 0., ng4, color=g_envelope_color, linestyle="dashed")
gusts.vlines(V_S, 0., 1., color=g_envelope_color, linestyle="dashed")

#if V_B==V_C:
    #gusts.vlines(V_B, ng6, ng5, color=g_envelope_color, linestyle="solid", linewidth=envelope_linewidth)
    
gusts.hlines(n_min, V_EAS[i_gline6_end], V_EAS[i_gline45_start], color=m_envelope_color, linewidth=envelope_linewidth)
gusts.hlines(n_min, V_EAS[i_gline6_end], V_EAS[i_gline45_start], color=m_envelope_color, linewidth=envelope_linewidth)

gusts.axhline(1., color=g_envelope_color, linestyle="dashed")
gusts.axhline(-1., color=g_envelope_color, linestyle="dashed")


#Fixing the x-axis to the origin

#gusts.spines['left'].set_position('zero')
gusts.spines['right'].set_color('none')
gusts.spines['bottom'].set_position('zero')
gusts.spines['top'].set_color('none')
#gusts.spines['left'].set_smart_bounds(True)
#gusts.spines['bottom'].set_smart_bounds(True)
gusts.xaxis.set_ticks_position('bottom')
#gusts.yaxis.set_ticks_position('left')

gusts.grid(True)

gusts.set_title("(V, n)-diagram for gusts")
gusts.set_xlabel(r"$V_{EAS} [\frac{m}{s}]$")
gusts.xaxis.set_label_coords(1.08, 0.32)
gusts.set_ylabel(r"$n_g$")

gusts.text(V_S, 0 + 0.05, r"$V_S$")

if V_B==V_C:
    gusts.text(V_B, 0 + 0.05, r"$V_B=V_C$")
else:
    gusts.text(V_B, 0 + 0.05, r"$V_B$")
    gusts.text(V_C, 0 + 0.05, r"$V_C$")
gusts.text(V_D, 0 + 0.05, r"$V_D$")

gusts.text(V_B + 0.8, ng1old + 0.05, "1")
gusts.text(V_C + 0.8, ng2 + 0.05, "2")
gusts.text(V_D + 0.8, ng3 + 0.05, "3")
gusts.text(V_D + 0.8, ng4 - 0.14, "4")
gusts.text(V_C + 0.8, ng5 - 0.14, "5")
gusts.text(V_B + 0.8, ng6 - 0.14, "6")

#gusts.text(0 + 5, 0.9 * ng1, "h = " + str(h) + "m")
#gusts.text(0 + 5, 0.9 * ng1 - 0.2, "m = " + str(m_to) + "kg")


plt.show()

print('V_S', V_S, 'V_A', V_A , 'V_C', V_C,'V_B', V_B, 'V_D', V_D, 'VEOT/VH', V_H)
