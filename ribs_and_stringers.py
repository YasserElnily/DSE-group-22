
import numpy as np

t1 = 0.002 #spar
t2 = 0.0015 #skin
E = 70*10**9
v = 0.33
halfspan = 3.15

c = 1.5 #chord
max_sigma = 130*10**6 #UPDATE
max_tau = 15*10**6 #UPDATE
height = 0.367

ribs = 1
stringers = 1
sigma_cr = 0
tau_cr = 0

while tau_cr<max_tau:

    a1 = halfspan/ribs
    b1 = height

    ratio1 = a1/b1
    
    if ratio1>2:
        k = 6
    elif ratio1>1.5 and ratio1<=2:
        k = 7
    elif ratio1>1 and ratio1<=1.5:
        k = 8
    elif ratio1<=1:
        k = 9

    tau_cr = (k * (np.pi**2 * E))*(t1/b1)**2/(12*(1-v**2))

    if tau_cr<max_tau:
        ribs += 1

    print(tau_cr)
    print(ribs)

    if ribs>20:
        break
    

while sigma_cr<max_sigma:

    a2 = halfspan/ribs
    b2 = c/stringers

    ratio2 = a2/b2


    if ratio2>0.5:
        k = 4

    if ratio2<=0.5:
        k = 9

    sigma_cr = k * (np.pi**2 * E)*(t2/b2)**2 / (12*(1-v**2))

    if sigma_cr<max_sigma:
        stringers+=1

    print(sigma_cr)
    print(stringers)

    if stringers>30:
        break

print("# of ribs not including start and end: ",ribs)
print("# stringers: ",stringers)
