import random, math
LO,HI,SAFE=40.0,165.0,60.0
def gate(y):                      # memoriamentes kapu: pozitiv igazolas
    return y if (LO<=y<=HI) else SAFE   # NaN-ra is SAFE (a ket oldalu osszehasonlitas hamis)
# 1) a kapu-tetel (halmaz-tagsag): veletlen + szelsoertekek
bad=0
cands=[float('nan'),float('inf'),-float('inf'),0,-1,200,1e308,-1e308,40,165,39.999,165.001]+[random.uniform(-1e4,1e4) for _ in range(200000)]
for y in cands:
    o=gate(y)
    if not (LO<=o<=HI): bad+=1
print("1) halmaz-tagsag megsertve:",bad,"/",len(cands))
# 2) a deck sajat demoja: allapotos szabaly rate_decel<=2 (ut/perc/mp), 1 mp-es lepes
def sim(seq):
    prev=70.0; viol=0; steps=0
    for y in seq:
        o=gate(y); d=prev-o
        if d>2.0: viol+=1
        steps+=1; prev=o
    return viol,steps
seq=[150.0]*3+[500.0]*3          # a program 150-et kuld, majd hibas 500-at
print("2) memoriamentes kapu, sorozat 150,150,150,500,500,500 -> lecsokkenes>2 megsertes:",sim([150.0,150,150,500,500,500]))
print("   a 150 -> 60 ugras:",150-gate(500.0),"ut/perc 1 mp alatt (limit 2)")
print("   a SAFE=60 benne van E-ben:",LO<=SAFE<=HI,"| de benne van-e az allapotos E-ben a 150 utan:",abs(150-SAFE)<=2)
