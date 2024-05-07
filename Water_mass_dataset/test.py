P = 120000 # pascals converted frmo mbar
V = 720e-9 # mm^3 V converted to m^3
R = 8.31
T = 294 # K, assuming room temp is 21C

n = (P*V)/(R*T)
print(n)