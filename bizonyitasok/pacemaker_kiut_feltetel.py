"""Pacemaker kiut-feltetel: allitas bizonyitasa = az ellentetenek (ellenpelda) keresese.

Minden vizsgalat ugyanazt csinalja: a Z3-tol a TAGADAST kerdezzuk.
  unsat -> nincs ellenpelda -> az allitas bizonyitott
  sat   -> van ellenpelda  -> az allitas hamis (a modell mutatja a konkret esetet)
"""
from z3 import *

LO, HI, S, D = 40, 165, 60, 2  # pacemaker.bio: HR 40..165, failsafe rate 60, 2 BPM/s


def E(h):
    return And(h >= LO, h <= HI)


def R_literal(h, g):  # a fajl szo szerint: rate_accel <= 2.0 (csak felfele korlat)
    return And(E(g), g - h <= D)


def R_symmetric(h, g):  # a klinikai szandek: |valtozas| <= 2 BPM/s
    return And(E(g), g - h <= D, h - g <= D)


def prove(name, claim):
    s = Solver()
    s.add(Not(claim))
    r = s.check()
    if r == unsat:
        print(f"[BIZONYITOTT ] {name}")
    else:
        print(f"[ELLENPELDA  ] {name}  -> {s.model()}")
    return r


h, g, y, prev, i = Reals("h g y prev i")

print("=== 1. Gyenge kiut-feltetel: minden megengedett allapotbol van megengedett folytatas ===")
for nm, R in (("szo szerinti", R_literal), ("szimmetrikus", R_symmetric)):
    prove(f"{nm}: minden h-hoz letezik g", ForAll([h], Implies(E(h), Exists([g], R(h, g)))))

print("\n=== 2. Eros kiut-feltetel: a FAILSAFE (60) egy lepesben elerheto MINDEN allapotbol ===")
for nm, R in (("szo szerinti", R_literal), ("szimmetrikus", R_symmetric)):
    prove(f"{nm}: h -> 60 egy lepesben", ForAll([h], Implies(E(h), R(h, S))))

print("\n=== 3. Hatarolt visszaterheto: legfeljebb hany lepes (mp) alatt ert el a 60-at a legrosszabb allapotbol? ===")
for nm, ok in (
    ("szo szerinti (lefele szabad)", lambda k: Implies(E(h), S - h <= D * k)),
    ("szimmetrikus", lambda k: Implies(E(h), If(h >= S, h - S, S - h) <= D * k)),
):
    for k in range(1, 100):
        s = Solver()
        s.add(Not(ForAll([h], ok(k))))
        if s.check() == unsat:
            print(f"[BIZONYITOTT ] {nm}: legfeljebb {k} lepes (mp) elegendo, {k-1} mar nem")
            break

print("\n=== 4. A kapu-tetel a pacemakerre: BARMELY javaslat (y) mellett a kimenet megengedett ===")
lo = If(prev - D > LO, prev - D, LO)
hi = If(prev + D < HI, prev + D, HI)
out = If(y < lo, lo, If(y > hi, hi, y))
prove("kimenet in E es |valtozas| <= 2, minden prev in E-re, minden y valos szamra",
      ForAll([prev, y], Implies(E(prev), And(E(out), out - prev <= D, prev - out <= D))))

print("\n=== 5. Redundancia: az interval_ms >= 250 kovetkezik-e a HR <= 165-bol? (i*h = 60000) ===")
prove("E(h) es i*h==60000 => i >= 250", ForAll([h, i], Implies(And(E(h), i * h == 60000), i >= 250)))

print("\n=== 6. Realis (IEEE-754 Float64) kapu: minden 2^64 bitminta, NaN-nal es vegtelennel egyutt ===")
fy = FP("y", Float64())
flo, fhi, fs = FPVal(LO, Float64()), FPVal(HI, Float64()), FPVal(S, Float64())


def fin_range(o):
    return And(fpLEQ(flo, o), fpLEQ(o, fhi))


# naiv kapu: "ha tul nagy -> HI; ha tul kicsi -> LO" (ahogy kezzel irnank)
naive = If(fpGT(fy, fhi), fhi, If(fpLT(fy, flo), flo, fy))
prove("NAIV kapu: kimenet in [40,165] minden y-ra", fin_range(naive))

# javitott kapu: csak akkor engedjuk at, ha POZITIVAN igazolt, kulonben biztonsagos ertek
fixed = If(And(fpLEQ(flo, fy), fpLEQ(fy, fhi)), fy, fs)
prove("JAVITOTT kapu: kimenet in [40,165] minden y-ra", fin_range(fixed))

print("\n=== 7. OPTIMALIS tartomany (a nyelvtan tartomanyt ismer): sav = 60+100*a +- 5, a in [0,1] ===")
a0, a1, p = Reals("a0 a1 p")
TAU = 5


def band(x, a):
    return And(x >= 60 + 100 * a - TAU, x <= 60 + 100 * a + TAU)


for dl in ("0.02", "0.03"):
    d = RealVal(dl)
    prove(f"a kornyezet legfeljebb {dl}/mp-et valtozik => a kapu a savban tud maradni (|valtozas|<=2)",
          ForAll([a0, a1, p],
                 Implies(And(a0 >= 0, a0 <= 1, a1 >= 0, a1 <= 1, a1 - a0 <= d, a0 - a1 <= d, band(p, a0)),
                         Exists([g], And(E(g), band(g, a1), g - p <= D, p - g <= D)))))
