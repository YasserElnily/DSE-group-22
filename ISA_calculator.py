# ****    ISA Calculator    ****

from math import *

def ISA(h):

    R = 287.
    g = 9.80665
    T0 = 288.15
    p0 = 101325.
    h0 = 0.



    # ISA calculations

    # Space h > 86 km
    if h > 86000:
        SystemExit
    else:
        # Troposphere 0 - 11 km
        if h >= 0:
            h1 = min(h,11000)
            a = -0.0065

            T1 = T0 + a*(h1 - h0)
            p1 = p0 *(T1/T0)**(-g/(a*R))
            rho = p1/(R*T1)

        # Tropopause 11 - 20 km isotherm
        if h > 11000:
            h0 = 11000
            T0 = T1
            p0 = p1

            #a = 0

            h1 = min(h,20000)

            p1 = p0 * exp((-g/(R*T0))*(h1-h0))
            rho = p1/(R*T1)

        # Stratosphere 20 - 32 km
        if h > 20000:
            h0 = 20000
            T0 = T1
            p0 = p1

            a = 0.001

            h1 = min(h,32000)

            T1 = T0 + a*(h1 - h0)
            p1 = p0 *(T1/T0)**(-g/(a*R))
            rho = p1/(R*T1)

        # Stratosphere 32 - 47 km
        if h > 32000:
            h0 = 32000
            T0 = T1
            p0 = p1

            a = 0.0028

            h1 = min(h,47000)

            T1 = T0 + a*(h1 - h0)
            p1 = p0 *(T1/T0)**(-g/(a*R))
            rho = p1/(R*T1)

        # Stratopause 47 - 51 km isotherm
        if h > 47000:
            h0 = 47000
            T0 = T1
            p0 = p1

            #a = 0

            h1 = min(h,51000)

            p1 = p0 * exp((-g/(R*T0))*(h1-h0))
            rho = p1/(R*T1)

        # Mesophere 51 - 71 km
        if h > 51000:
            h0 = 51000
            T0 = T1
            p0 = p1

            a = -0.0028

            h1 = min(h,71000)

            T1 = T0 + a*(h1 - h0)
            p1 = p0 *(T1/T0)**(-g/(a*R))
            rho = p1/(R*T1)

        # Mesosphere 71 - 86 km
        if h > 71000:
            h0 = 71000
            T0 = T1
            p0 = p1

            a = -0.002

            h1 = min(h,86000)

            T1 = T0 + a*(h1 - h0)
            p1 = p0 *(T1/T0)**(-g/(a*R))
            rho = p1/(R*T1)

        return [T1, p1, rho, sqrt(1.4*287.058*T1)] #[Temp (K), Press (Pa), Density (kg/m^3), Speed of sound (m/s)]
