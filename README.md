# A határ alkotmánya: vibe-coding kapuval

A HInTa (Hargita Informatikusok Találkozója), 2026. november 7. előadásának anyaga: diák, tanulmány, szószedet és a bizonyító szkriptek.

**Élő változat:** https://vibe-coding.metaspace.bio

## A tézis egy mondatban

A gép írta kód **biztonságos kimenete** kikényszeríthető a kód ismerete nélkül, de **nem a szakterület ismerete nélkül**: a megengedettet és a veszélyeket a területet ismerő mondja ki, és a kapu a programtól független. Nem a programozást kell tudni, hanem azt, amit a program kiszolgál. A **helyességhez** (hogy a program el is végzi a dolgát) ezen felül tesztelés kell.

A kapu-lemma egyszerű (egy ellenőrzés és egy tartalék érték); a szakirodalom futásidejű kikényszerítésnek, biztonsági pajzsnak hívja. Nem ez az újdonság, és ezt a diák is kimondják. Részletek: [`szotar.html`](szotar.html).

## Közreműködés

Az anyag **Claude-dal** (Anthropic nyelvi modell) közösen készült. A tézist, a keretet, a MetaSpace-eszközt, a döntéseket és a felelősséget a szerző adta; a szöveg és a kód nagy részét a modell írta. A főelőadást és a kiegészítőt a szerző diánként hagyta jóvá; a 2026. november 6-i átdolgozás diánkénti jóváhagyás nélkül készült. A modell tévedhet: az átdolgozás során hét túlzó állítást találtunk és javítottunk. **Független ellenőrzés nincs.** Részletesen: [`kozremukodes.html`](kozremukodes.html).

## Mi van a repóban

| Fájl | Mi ez |
|---|---|
| `eloadas.html` | az élő változat (12 dia, jegyzetnézet: N, előadói ablak: J) |
| `diak.html` | az olvasható főelőadás (21 dia, ellenpróbákkal) |
| `kiegeszito.html` | a kiegészítő (8 dia, Studio-demó) |
| `szotar.html`, `szotar_adat.py` | a szószedet és annak forrása |
| `kozremukodes.html` | ki mit csinált: az MI és a szerző viszonya |
| `tanulmany.html`, `tanulmany.pdf` | a teljes levezetés |
| `tipusos/` | a pacemaker `.bio` specifikációi (t1: eredeti, t2: + veszély, t3: javított) és a t3-ból generált kód (Python, ipari vezérlő, C) |
| `dosszie_pacemaker_tipusos.html` | a Studio igazolási dossziéja (a Studio saját kimenete) |
| `bizonyitasok/` | két önálló Z3-bizonyító szkript |
| `proba/teszt_kapu.py` | a kapu két ágának próbája |

A `tavirany.html` a telefonos távirányító; működéséhez szerveroldali szinkron kell, a repóban nem fut.

## Hogyan futtasd a bizonyításokat

Kell: Python 3.9 vagy újabb, és a Z3.

```
pip install z3-solver
python -B proba/teszt_kapu.py
python -B bizonyitasok/pacemaker_kiut_feltetel.py
python -B bizonyitasok/szintek_kapcsolata.py
```

Mindhárom körülbelül egy másodperc alatt lefut. Amit látnod kell:

- **`teszt_kapu.py`**: a halmaz-tagság 200 012 bemenetre nem sérül (nem szám és végtelen is); viszont az időben összefüggő szabály (esés legfeljebb 2 ütés/perc/mp) sérül: a 150-ről 60-ra cserélés 90-es esés egy lépésben. Vagyis a lemma egy jel értékére igaz, időben összefüggő szabálynál az átmenet is számít.
- **`pacemaker_kiut_feltetel.py`**: a kapu-lemma bizonyítása, a naiv lebegőpontos kapu ellenpéldája (nem szám) és a javított kapu bizonyítása az összes 2⁶⁴ bitmintára, a kiút-feltétel (a vészállapot nem érhető el egy lépésben minden állapotból; legfeljebb 10, illetve 53 másodperc kell hozzá), az optimális sáv (0,02/mp bizonyított, 0,03 ellenpélda).
- **`szintek_kapcsolata.py`**: a helyi szabályból nem következik a közös (4 + 5 > 8), a kvóta-szerződés (N = 2, 3, 5, 8), a hiányzó kapu, a 3-3-3 minimum (9-ből lehetséges, 8-ból nem), a koncentrációs korlát.

## Mi reprodukálható, és mi nem

- **Reprodukálható itt:** a fenti három szkript; a diák, a tanulmány és a szószedet olvasása.
- **Reprodukálható a Studióban (élőben, internet kell):** a PASS / FAIL / PASS futtatások. Nyisd meg a https://studio.metaspace.bio/app oldalt, másold be a `tipusos/t1_eredeti_tipusos.bio`, `t2_veszellyel.bio`, `t3_javitott.bio` fájlokat (beillesztés előtt Ctrl+A), és nyomd meg a Verify gombot. Mért: MetaSpace Studio 2.12, 2026-11-01. A Studio új verziója mást adhat.
- **Nincs a repóban:** a MetaSpace zárt forrása, és három, ahhoz kötött mérőszkript. Ezek eredményei csak a szerző gépén futnak, és nem reprodukálhatók innen. A diákon és a tanulmányban szereplő, a Studióval mért állításokat a fenti élő futtatás ellenőrzi.

## Amit ez nem bizonyít

A bizonyítások egy **modellre** és **kimondott előfeltevésekre** (P1–P4) igazak. Nem bizonyítják, hogy a cél helyes, hogy a modell a valóság, hogy a program a dolgát elvégzi, és hogy az ellenőrző hibátlan. Az eszközt a szerzője igazolta; független ellenőrzése nincs.

## Szedd szét

Ha hibát, túlzó állítást vagy ellenpéldát találsz (a szövegben, a szkriptekben vagy a Studióban), nyiss egy [issue-t](https://github.com/LemonScripter/hinta-vibe-coding/issues). Ez az anyag pontosan ezt kéri.

## Licenc

A kód (`*.py`, `*.bio`) MIT licenc alatt, a szövegek és diák (`*.html`, `*.pdf`) CC BY 4.0 alatt. Részletek: [`LICENSE.md`](LICENSE.md).
