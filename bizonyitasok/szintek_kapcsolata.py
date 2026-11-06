"""Szintek kozotti kapcsolat: sejt (also szint) es kozosseg (felso szint).

Modszer minden allitasra: a TAGADASAT kerdezzuk a Z3-tol.
  unsat -> nincs ellenpelda -> az allitas bizonyitott (a megadott elofeltevesek mellett)
  sat   -> van ellenpelda   -> az allitas hamis (a modell mutatja a konkret esetet)
"""
from z3 import *


def vizsgal(nev, *feltetelek, tagadando):
    """Allitas: feltetelek => tagadando.  Kerdezzuk: feltetelek es NEM tagadando."""
    s = Solver()
    s.add(*feltetelek)
    s.add(Not(tagadando))
    r = s.check()
    if r == unsat:
        print(f"[BIZONYITOTT ] {nev}")
    else:
        m = s.model()
        print(f"[ELLENPELDA  ] {nev}  -> " + ", ".join(f"{d}={m[d]}" for d in m))
    return r


def lehetseges(nev, *feltetelek):
    """Letezik-e olyan allapot, amely mindegyik feltetelt kielegiti?"""
    s = Solver()
    s.add(*feltetelek)
    r = s.check()
    if r == sat:
        m = s.model()
        print(f"[LEHETSEGES  ] {nev}  -> " + ", ".join(f"{d}={m[d]}" for d in sorted(m, key=str)))
    else:
        print(f"[LEHETETLEN  ] {nev}  (minden elosztas kizarva)")
    return r


print("=== 1. Helyi szabalybol NEM kovetkezik a kozos: 2 sejt, kozos keszlet S=8, mindkettore u<=5 ===")
u1, u2 = Reals("u1 u2")
vizsgal("u1<=5 es u2<=5  =>  u1+u2<=8",
        u1 >= 0, u2 >= 0, u1 <= 5, u2 <= 5,
        tagadando=(u1 + u2 <= 8))

print("\n=== 2. Garancia-feltevés: a kozosseg kvotat oszt (osszeg <= S), a sejtek betartjak => kozos szabaly kovetkezik ===")
for N in (2, 3, 5, 8):
    u = [Real(f"u{i}") for i in range(N)]
    q = [Real(f"q{i}") for i in range(N)]
    S = Real("S")
    vizsgal(f"N={N}: (osszeg q <= S) es (minden u_i<=q_i) => osszeg u <= S",
            Sum(q) <= S, *[u[i] <= q[i] for i in range(N)],
            tagadando=(Sum(u) <= S))

print("\n=== 3. A lanc ereje: ha EGY sejt kapuja hianyzik (u_2 korlatlan), a kozos garancia megdol ===")
N = 3
u = [Real(f"u{i}") for i in range(N)]
q = [Real(f"q{i}") for i in range(N)]
S = Real("S")
vizsgal("kapu csak a 0. es 1. sejten van, a 2. korlatlan",
        Sum(q) <= S, u[0] <= q[0], u[1] <= q[1], u[2] >= 0,
        tagadando=(Sum(u) <= S))

print("\n=== 4. Kozossegi eletkepesseg: mindenkinek van minimuma (m=3 mindegyik), osztható-e a kereszt S-bol? ===")
m = [3, 3, 3]
for Sv in (9, 8):
    q = [Real(f"q{i}") for i in range(3)]
    lehetseges(f"S={Sv}: van olyan kvotaelosztas, ahol mindenki >= minimum es osszeg <= S",
               *[q[i] >= m[i] for i in range(3)], Sum(q) <= Sv)

print("\n=== 5. Sebesseg es koncentracio: az ellatas d-vel csokken egy lepesben; sejtenkent legfeljebb r=1-et lehet csokkenteni, minimum 1 ===")
S0, r, minv, d = 9, 1, 1, 2
def kovetkezo_osszeg(us):
    # a sejt a kovetkezo lepesben legfeljebb r-rel csokkentheti, de nem megy a minimum ala
    return Sum([If(x - r > minv, x - r, minv) for x in us])

u = [Real(f"u{i}") for i in range(3)]
alap = [*[x >= minv for x in u], Sum(u) <= S0]
vizsgal(f"korlat nelkul: osszeg(u)<=9 => a leggyorsabb csokkentes utan osszeg <= {S0 - d}",
        *alap, tagadando=(kovetkezo_osszeg(u) <= S0 - d))
vizsgal(f"egy sejt legfeljebb 4-et hasznalhat (koncentracio-korlat): ugyanaz",
        *alap, *[x <= 4 for x in u], tagadando=(kovetkezo_osszeg(u) <= S0 - d))
