"""A szószedet egyetlen forrása. Innen készül: szotar.html és szotar_tabla.md (a tanulmány táblázata).
Futtatás: python -B szotar_adat.py   (a _hinta_eloadas mappából)
Oszlopok: kifejezés | itt jelentése | honnan jön | bevett informatikai név | nem azonos azzal / hol sántít"""
import html
from pathlib import Path

DATUM = "2026-11-06"

CSOPORTOK = [
    ("Az alapfogalmak: határ, halmaz, kapu", [
        ("Rendszer", "A világ egy elkülönített része, amelynek van határa.",
         "rendszerelmélet",
         "komponens; szolgáltatás; program a környezetével",
         "nem a világ egésze (annak nincs külseje, ezért nincs hová kaput állítani)"),
        ("Határ", "Azon változók összessége, amelyeken át a program és a környezete egymásra hat (pacemakerben: a kimenő pulzus).",
         "rendszerelmélet (Ashby, Bernard); biológia (sejthártya)",
         "interfész; bizalmi határ (trust boundary)",
         "nem a program fizikai burka; nem a teljes világ (annak nincs külseje)"),
        ("Doboz", "A program belseje, amelyről semmit sem tételezünk fel.",
         "rendszerelmélet (fekete doboz)",
         "megvalósítás (implementáció); fekete doboz (black box)",
         "nem azt állítjuk, hogy ismerhetetlen, hanem azt, hogy a bizonyítás nem használja fel"),
        ("Megengedett halmaz (E)", "A határ azon értékeinek halmaza, amelyeket a szabály megenged (pacemakerben: 40–165 ütés/perc).",
         "matematika (halmaz)",
         "biztonsági burkoló (safe set, safety envelope); engedélyezési lista (allowlist)",
         "nem az optimális sáv; nem az összes lehetséges érték"),
        ("Optimális sáv", "E kitüntetett része: a cél tartománya (-tól -ig).",
         "szabályozáselmélet",
         "üzemi tartomány (operating range) a biztonsági burkolón belül",
         "nem egyetlen pont; az E-nél szűkebb, és más kérdés: a hasznosság, nem a biztonság"),
        ("Kapu", "A határon álló, a programtól független őr: a megengedett értéket átengedi, a többit előre kijelölt biztonságos értékre cseréli.",
         "saját szó",
         "kimeneti őr: futásidejű figyelő (runtime monitor), biztonsági pajzs (safety shield), kimenő szűrő (egress filter)",
         "nem tűzfal (az főleg a bejövő forgalmat szűri); nem teszt; nem a program belsejéről dönt, csak a kimenetről"),
        ("Biztonságos érték (s)", "Az E-nek előre kijelölt eleme, amelyre a kapu cserél (pacemakerben: 60 ütés/perc).",
         "saját szó",
         "biztonságos állapot (safe state); tartalék érték (fallback); hibabiztos állapot (fail-safe)",
         "időben összefüggő szabálynál az s-hez vezető átmenet is számít: 150-ről 60-ra ugrani sérti a „legfeljebb 2 ütés/perc/mp” szabályt"),
        ("Hatás és ok", "A hatás: ami a határon kilép és a világot éri. Az ok: a parancs vagy a belső döntés, amely ezt kiváltotta. A kapu a hatást ítéli meg.",
         "okságfilozófia",
         "kimenet-alapú ellenőrzés (utófeltétel, postcondition) szemben a bemenet- vagy kódalapú ellenőrzéssel",
         "a „hatás” itt a határon mérhető kimenet, nem a világ minden következménye"),
        ("Zárt világ elve", "A kapu azt sorolja fel, ami megengedett. Ami a szabályban nincs, az a határon át nem jut ki.",
         "logika (Reiter, 1978)",
         "alapértelmezett tiltás (default-deny); engedélyezési lista (allowlist); hibabiztos alapértelmezés (fail-safe defaults)",
         "nem tiltólista (az kifelejti, amire nem gondoltunk); nem a fizikai világ tulajdonsága"),
        ("Mellékút", "Minden út, amelyen a hatás a kapu megkerülésével jut ki.",
         "saját szó",
         "megkerülés (bypass); a teljes közvetítés hiánya (complete mediation, Saltzer–Schroeder, 1975)",
         "a kapu-állítás csak akkor érvényes, ha nincs mellékút: ezt a rendszer szintjén kell kikényszeríteni"),
        ("Megkerülhetetlenség (rendszermag-szint, DCC Ring 0)", "A kapu kikényszerítése a rendszermagban, hogy a program ne tudja kijátszani.",
         "MetaSpace (DCC)",
         "referencia-figyelő (reference monitor, Anderson, 1972): mindig meghívott, kijátszhatatlan, ellenőrizhető",
         "mért állapot (a védelmi ledger szerint): fájlírásra, egy eldobható virtuális gépen (Linux 6.1, 2026-08-07-i építés); nincs üzembe helyezve; root ellen nem véd; független ellenőrzés nincs"),
    ]),
    ("Filozófia és nyelv → informatika", [
        ("Tudni-hogyan és tudni-hogy", "Tudni-hogyan: helyesen cselekedni a szabály kimondása nélkül. Tudni-hogy: a szabályt kimondani.",
         "filozófia (Ryle, 1949)",
         "implicit tudás szemben a specifikációval",
         "a kettő nem zárja ki egymást; a nyelvtan nélkül is helyesen beszélünk, de ettől a nyelvtan nem felesleges"),
        ("Hallgatólagos tudás", "Amit tudunk, de nem tudunk szabályként kimondani (a „Látom a kutyát” helyességét felismerjük).",
         "filozófia (Polanyi, 1966)",
         "felismerő (osztályozó, oracle) szemben az előállítóval (generátorral)",
         "a kapunak felismerni kell a helyeset, nem előállítani; ezért elég egy halmaz-ellenőrzés, nem kell hozzá a program ismerete"),
        ("Szerkezeti analógia", "Két terület hasonló szerkezetű: a megfeleltetés a viszonyokra áll, nem a részletekre. Szemléltet, nem bizonyít.",
         "filozófia (analógia, szerkezetleképezés)",
         "–",
         "nem izomorfia (az kölcsönösen egyértelmű, szerkezetmegőrző leképezés); legfeljebb részleges homomorfia. A nyelvtan leírás, a kód ok: ez az eltérés"),
        ("Többszörös megvalósíthatóság", "Ugyanaz a helyes viselkedés többféle belsővel is létrejöhet.",
         "elmefilozófia (Putnam, Fodor)",
         "interfész és megvalósítás szétválasztása",
         "a helyes viselkedés a kimeneten ítélhető meg; a belső ettől független (de a belső okozza a viselkedést)"),
        ("A beszélőközösség mint kapu", "A gyerek a kimenetén át tanul: a közösség kijavítja. A belsejét senki nem vizsgálja.",
         "nyelvelsajátítás",
         "külső visszacsatolás; kimeneti ellenőrzés (output validation)",
         "a közösség sem tévedhetetlen; a nyelvnél nincs kimondott E, a pacemakernél van"),
        ("Alkotmány", "A határra vonatkozó, véges, kimondott, megszeghetetlen szabályok: a megengedett halmaz és a vészállapot.",
         "jog- és politikafilozófia (hasonlat)",
         "invariáns (mindig fennálló feltétel); biztonsági tulajdonság; specifikáció",
         "metafora: a pontos fogalom az invariáns. Az alkotmány azt mondja meg, mi nem történhet meg; a törvény (leírás) azt, mi történik"),
        ("Törvény (leíró)", "A működés leírása: mi történik (a glükóz lebomlik).",
         "természettudomány",
         "modell; viselkedésleírás",
         "nem előírás; ez az alkotmány szerepe"),
        ("Tökéletes", "A kimenet minden elérhető helyzetben E-ben van. A célhoz viszonyított teljesség.",
         "arisztotelészi filozófia (teleios)",
         "biztonsági tulajdonság teljesül (safety)",
         "nem hibátlan program; nem optimális; nem azt jelenti, hogy a program el is végzi a dolgát"),
        ("Százszázalékos", "Minden előfeltevés ki van mondva, és a következtetés ezekből szükségszerű.",
         "logika",
         "feltételes garancia (assume–guarantee)",
         "nem azt jelenti, hogy a valóságban semmi nem romolhat el"),
    ]),
    ("Biztonság, helyesség, bizonyítás", [
        ("Biztonság (safety)", "„Valami rossz soha nem történik meg”: például a kimenet soha nincs E-n kívül.",
         "számítástudomány (Lamport, 1977; Alpern–Schneider, 1985)",
         "biztonsági tulajdonság (safety property)",
         "ezt a kapu kikényszeríti. A futásidejű őrök általában csak ilyen tulajdonságot tudnak kikényszeríteni (Schneider, 2000)"),
        ("Élősség (liveness)", "„Valami jó előbb-utóbb megtörténik”: a pacemaker ténylegesen ütemet ad.",
         "számítástudomány (Lamport, 1977; Alpern–Schneider, 1985)",
         "élősségi tulajdonság (liveness property)",
         "ezt a kapu nem garantálja: egy mindig 60-at adó program is átmegy rajta"),
        ("Helyesség", "A program azt teszi, amire való.",
         "informatika",
         "funkcionális helyesség (functional correctness)",
         "nem azonos a biztonsággal; ehhez a szakterület ismerete és tesztelés kell"),
        ("Lemma („kapu-tétel”)", "Ha y eleme E-nek, a kapu átengedi, különben s-t ad, s pedig eleme E-nek: a kimenet mindig E-ben marad.",
         "matematika",
         "a futásidejű kikényszerítés alapállítása; egy ellenőrzés és egy tartalék érték",
         "egyszerű, nem ez az újdonság. Időben összefüggő szabálynál indukció és életképesség kell hozzá"),
        ("Bizonyított", "A modellre és a kimondott előfeltevésekre igaz.",
         "logika",
         "formálisan ellenőrzött (adott modellre)",
         "három különböző dolgot is jelent, ne keverd: (1) matematikai lemma, (2) Z3 PASS, vagyis a szabályok ellenőrzése, (3) mért futás. Egyik sem azt jelenti, hogy a valóságban igaz"),
        ("PASS / FAIL (Z3)", "A szabályok ellentmondásmentesek-e, és kizárják-e a megnevezett veszélyt. FAIL esetén egy konkrét ellenpéldát kapunk.",
         "formális módszerek",
         "SMT-megoldó eredménye (sat / unsat)",
         "a szabályokat vizsgálja, a programot nem; a hiányzó, meg nem nevezett veszélyt nem találja meg"),
        ("Ellenpélda", "Egy konkrét eset, amely az állítást megcáfolja (például 40 ütés/perc és 3 ütés/perc/mp esés).",
         "logika",
         "ellenpélda (counterexample); az SMT-ben egy kielégítő modell",
         "nem statisztikai kivétel"),
        ("Veszély (HAZARD)", "Egy megnevezett, elkerülendő helyzet. A gép azt vizsgálja, hogy a szabályok kizárják-e.",
         "biztonságtechnika",
         "veszélyforrás (hazard)",
         "a veszélyt az ember nevezi meg; amit senki nem nevezett meg, azt a gép nem ellenőrzi"),
        ("Specifikáció (.bio)", "A határ leírása: jelek, szabályok, biztonságos állapot.",
         "informatika",
         "formális specifikáció; szerződés (contract)",
         "a specifikáció írása is programozás, de nem a megvalósításé; ezért mondjuk, hogy a megengedett halmazhoz a szakterület kell, a programnyelv nem"),
        ("Igazolási dosszié", "A Studio által készített napló: a specifikáció lenyomata, az eredmények, a hatókör.",
         "MetaSpace Studio",
         "bizonyíték-csomag (assurance case) – de mi magunk készítettük",
         "nem tanúsítvány, nem független ellenőrzés"),
        ("Bizalmi mag", "Az, amiben meg kell bíznunk: az ellenőrző és a kódgenerátor.",
         "biztonságtechnika",
         "megbízható számítási alap (TCB)",
         "ha az ellenőrző hibás, a bizonyítás sem megbízható (P4)"),
        ("Eldönthető", "Véges lépésben mindig megadható az igen/nem válasz.",
         "számításelmélet",
         "eldönthető (decidable)",
         "nem azt jelenti, hogy gyors"),
        ("Életképesség (kiút-feltétel)", "Bármely E-beli helyzetből van olyan következő lépés, amely E-ben tart, és onnan is van ilyen.",
         "rendszerelmélet (Aubin)",
         "életképességi mag (viability kernel); visszaállíthatóság",
         "nem az, hogy az állapot éppen E-ben van. Pacemakerben a 40→60 ugrás egy lépésben sérti a 2/mp szabályt"),
    ]),
    ("Rétegek és a használt szavak", [
        ("Szint", "A rendszerek rétege: az alsó szint rendszerei a felsőnek részei.",
         "rendszerelmélet",
         "rétegzés; összetétel (composition)",
         "nem rangsor. Nem azonos a Studio „fok” szavával"),
        ("Fok (1., 2., 3.)", "A kikényszerítés erőssége a Studióban.",
         "MetaSpace Studio",
         "kikényszerítési erősség (enforcement tier)",
         "nem a rendszerek rétege (ez a „szint”)"),
        ("Garancia–feltevés", "Az alsó szint garantál valamit, feltéve hogy a környezete teljesít valamit.",
         "formális módszerek",
         "garancia–feltevés szerződés (assume–guarantee contract)",
         "nem bizalom vagy hit"),
        ("Tárgynyelv és metanyelv", "A tárgynyelven a szabályokat mondjuk ki (.bio); a metanyelven a szabályokról állítunk (például hogy ellentmondásmentesek).",
         "logika (Tarski)",
         "specifikációs nyelv és ellenőrző (verifier)",
         "nem a tárgynyelv „fölötti parancs”"),
        ("Vibe-coding", "A programot mesterséges intelligencia írja, az ember a kívánt viselkedést mondja el, a kódot nem olvassa végig.",
         "szleng (Karpathy, 2025)",
         "MI-generált kód átnézés nélkül",
         "nem azt jelenti, hogy a hatás ellenőrzése felesleges – éppen azt kell kikényszeríteni"),
        ("Szerző és MI viszonya", "A szerző a megrendelő és specifikáló, a felelős szerkesztő; az MI a generátor és végrehajtó. Az ember adja a megengedett halmazt (P1), és viseli a felelősséget.",
         "kiadói etika (COPE, ICMJE); szoftvermérnökség",
         "megrendelő és kivitelező; megbízó és ügynök (principal és agent); ember a körben (human-in-the-loop)",
         "nem szerzőtárs: az MI nem lehet szerző, de a használatát közzé kell tenni. A tyúk–tojás kérdés akkor válik valódi problémává, ha az MI ellenőrzi az MI-t (nincs független kapu)"),
        ("Vibe-coder", "Aki MI-vel íratja a programot, és a kódot nem olvassa végig.",
         "szleng (Karpathy, 2025)",
         "specifikáló és jóváhagyó (az MI-asszisztált fejlesztésben)",
         "ebben a munkában a szerző nem tiszta vibe-coder: specifikált, irányított, a főelőadást és a kiegészítőt diánként jóváhagyta (a 2026-11-06-i átdolgozás kivételével)"),
        ("Független ellenőrzés", "Az ellenőrző olyan féltől jön, aki sem a doboz (a kód) írója, sem a szabályt kimondó fél. Ebben a munkában nincs; csak egy külső emberi bírálat vizsgálta.",
         "biztonságtechnika (a bizonyítás függetlensége)",
         "független ellenőrzés és validálás (IV&V)",
         "az MI-vel végzett önellenőrzés nem független: ugyanaz a modellcsalád hasonló hibákat követhet el"),
    ]),
]

SOROK = [(cs, t) for cs, lista in CSOPORTOK for t in lista]
FEJ = ["Kifejezés", "Itt jelentése", "Honnan jön", "Bevett informatikai név", "Nem azonos azzal / hol sántít"]


def md_cella(s):
    return s.replace("|", "/").replace("\n", " ")


def tabla_md():
    """4 oszlopos változat a tanulmányhoz (A4 álló): a „honnan jön” a 3. oszlopba kerül"""
    fej = ["Kifejezés", "Itt jelentése", "Bevett informatikai név (és eredet)", "Nem azonos azzal / hol sántít"]
    out = ["| " + " | ".join(fej) + " |", "| " + " | ".join("---" for _ in fej) + " |"]
    for _, t in SOROK:
        harmadik = ("%s. Eredet: %s." % (t[3], t[2])) if t[3] != "–" else ("Eredet: %s." % t[2])
        out.append("| " + " | ".join(md_cella(x) for x in (t[0], t[1], harmadik, t[4])) + " |")
    return "\n".join(out) + "\n"


CSS = """:root{--bg:#f6f4ee;--fg:#1d2a2c;--muted:#556569;--card:#ffffff;--line:#d8d4c6;--accent:#0f766e;--accent-soft:#d9efec;--warn:#92400e;--warn-soft:#fdf0d5}
@media (prefers-color-scheme: dark){:root{--bg:#101719;--fg:#e8efee;--muted:#9fb0b3;--card:#172123;--line:#2a393c;--accent:#4fd1c5;--accent-soft:#173533;--warn:#f6c76b;--warn-soft:#3a2f12}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Segoe UI",system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif;line-height:1.45;padding:1.5rem 1.2rem 3rem}
main{max-width:84rem;margin:0 auto}
.tag{font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0}
h1{font-size:1.9rem;margin:.2rem 0 .5rem}
h2{font-size:1.15rem;margin:1.8rem 0 .5rem;color:var(--accent)}
p{margin:.3rem 0}
.muted{color:var(--muted)}
.row{display:flex;gap:.7rem;flex-wrap:wrap;margin:.8rem 0 1rem;align-items:center}
.btn{display:inline-block;font-weight:700;color:var(--bg);background:var(--accent);text-decoration:none;border-radius:.45rem;padding:.4rem .9rem}
input{font:inherit;padding:.45rem .7rem;border:1px solid var(--line);border-radius:.45rem;background:var(--card);color:var(--fg);min-width:0;flex:1;max-width:30rem}
.note{background:var(--warn-soft);color:var(--fg);border-left:.3rem solid var(--warn);border-radius:.3rem;padding:.55rem .8rem;margin:.8rem 0}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);font-size:.92rem}
th,td{padding:.5rem .65rem;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--accent-soft);font-weight:700;position:sticky;top:0}
td:first-child{font-weight:700;width:11rem}
th:nth-child(2),td:nth-child(2){width:24%}
tr.hide{display:none}
a{color:var(--accent);font-weight:600}
@media (max-width:900px){td:first-child{width:auto}th:nth-child(2),td:nth-child(2){width:auto}table,thead,tbody,tr,th,td{display:block}thead{display:none}tr{border-bottom:2px solid var(--line);padding:.4rem 0}td{border:0;padding:.2rem .65rem}td::before{content:attr(data-h) ': ';font-weight:700;color:var(--muted)}}
td.g::before{content:none!important}
body{overflow-wrap:anywhere}
@media print{.row,input{display:none}th{position:static}}"""


def oldal():
    h = []
    h.append('<!doctype html>\n<html lang="hu">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex">')
    h.append("<title>Szószedet</title>\n<style>\n" + CSS + "\n</style>\n</head>\n<body>\n<main>")
    h.append('<p class="tag">HInTa · 2026. november 7. · változat: %s</p>' % DATUM)
    h.append("<h1>Szószedet: ki mit ért rajta</h1>")
    h.append('<p>Az előadás filozófiai, nyelvi és biológiai szavakat használ informatikai értelemben. Itt áll, melyik szó mit jelent, mi a bevett informatikai neve, és hol <b>nem</b> szabad szó szerint érteni.</p>')
    h.append('<div class="note"><b>Három szabály.</b> (1) A hasonlatok <b>szerkezeti analógiák</b>: szemléltetnek, nem bizonyítanak; a bizonyítás a kapu-lemmában van. (2) A kapu a <b>biztonságot</b> (a kimenet nem lép ki E-ből) garantálja, a <b>helyességet</b> (hogy a program el is végzi a dolgát) nem. (3) Minden „bizonyított” egy modellre és kimondott előfeltevésekre vonatkozik; az eszközt a szerzője igazolta, független ellenőrzés nincs.</div>')
    h.append('<div class="row"><input id="q" type="search" placeholder="Keresés a szószedetben (pl. kapu, safety, analógia)" aria-label="Keresés"><a class="btn" href="index.html">Kezdőlap</a><a class="btn" href="tanulmany.html">Tanulmány</a></div>')
    h.append("<table id=\"t\"><thead><tr>" + "".join("<th>%s</th>" % html.escape(x) for x in FEJ) + "</tr></thead><tbody>")
    for cs, lista in CSOPORTOK:
        h.append('<tr class="grp"><td class="g" colspan="5" style="background:var(--accent-soft);color:var(--accent);font-weight:700;white-space:normal">%s</td></tr>' % html.escape(cs))
        for t in lista:
            cells = "".join('<td data-h="%s">%s</td>' % (html.escape(FEJ[i]), html.escape(t[i])) for i in range(5))
            h.append("<tr>" + cells + "</tr>")
    h.append("</tbody></table>")
    h.append('<p class="muted" style="margin-top:1rem;font-size:.9rem">Források és állapotok: a „Honnan jön” oszlop a szó eredetét jelzi; a nevek és évszámok a hivatkozott művekre mutatnak, a pontos adatok a <a href="tanulmany.html">tanulmány</a> hivatkozás-listájában vannak. A „Megkerülhetetlenség” sor állapota a védelmi állítás-ledgerből való, és csak a hatást írja le.</p>')
    h.append("""<script>
(function(){var q=document.getElementById('q'),rows=[].slice.call(document.querySelectorAll('#t tbody tr'));
q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();var show=null;
rows.forEach(function(r){if(r.classList.contains('grp')){r.classList.toggle('hide',!!v);return;}
var m=!v||r.textContent.toLowerCase().indexOf(v)>=0;r.classList.toggle('hide',!m);});});})();
</script>""")
    h.append("</main>\n</body>\n</html>\n")
    return "\n".join(h)


if __name__ == "__main__":
    d = Path(__file__).resolve().parent
    (d / "szotar.html").write_text(oldal(), encoding="utf-8")
    (d / "szotar_tabla.md").write_text(tabla_md(), encoding="utf-8")
    print("szotar.html, szotar_tabla.md kész; sorok:", len(SOROK))
