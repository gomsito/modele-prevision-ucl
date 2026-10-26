"""Évalue les prévisions 1N2 archivées : Brier, log-loss, calibration, comparaison au marché.

Usage : python3 evaluer.py [chemin_csv]
Écrit resultats/RESULTATS.md et resultats/calibration.svg. Aucune dépendance hors stdlib.
"""

import csv
import math
import random
import sys
from datetime import date
from pathlib import Path

ICI = Path(__file__).parent
CSV_DEFAUT = ICI / "data" / "archive_previsions.csv"
CSV_MARCHE = ICI / "data" / "marche_cloture_J2-J3.csv"
SORTIE = ICI / "resultats"
ISSUES = ("1", "N", "2")
EPS = 1e-15
N_BOOTSTRAP = 5000


def charger(chemin):
    """Lignes jouées uniquement, avec issue observée et les deux séries de probabilités."""
    matchs = []
    with open(chemin, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            res = (r.get("resultat_90min") or "").strip()
            if not res:
                continue
            issue = res.split()[0].upper()
            if issue not in ISSUES:
                continue
            matchs.append({
                "id": r["identifiant_match"],
                "phase": r["phase"],
                "issue": issue,
                "modele": [float(r["p1"]), float(r["pN"]), float(r["p2"])],
                "marche": [float(r["p1_marche"]), float(r["pN_marche"]), float(r["p2_marche"])],
                "choix": r["choix_principal"].strip().upper(),
                "retenu": r["statut_selection"].strip().lower().startswith("retenu"),
            })
    return matchs


def charger_marche(chemin):
    """Journées sans prévision archivée : seulement le marché (cotes de clôture relevées après coup)."""
    if not chemin.exists():
        return []
    with open(chemin, newline="", encoding="utf-8") as f:
        return [{"issue": r["resultat_90min"].split()[0].upper(),
                 "marche": [float(r["p1_marche"]), float(r["pN_marche"]), float(r["p2_marche"])]}
                for r in csv.DictReader(f) if r["resultat_90min"].strip()]


def brier(p, issue):
    """Brier multiclasse : somme des écarts au carré sur les 3 issues (0 = parfait, 2 = pire)."""
    return sum((pi - (o == issue)) ** 2 for pi, o in zip(p, ISSUES))


def logloss(p, issue):
    return -math.log(max(p[ISSUES.index(issue)], EPS))


def moyenne(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def ic_bootstrap(diffs, graine=42):
    """IC à 95 % de la différence moyenne, par rééchantillonnage des matchs."""
    rng = random.Random(graine)
    n = len(diffs)
    stats = sorted(moyenne([diffs[rng.randrange(n)] for _ in range(n)]) for _ in range(N_BOOTSTRAP))
    return stats[int(0.025 * N_BOOTSTRAP)], stats[int(0.975 * N_BOOTSTRAP)]


def calibration(matchs, cle, n_bins=5):
    """Chaque probabilité (3 par match) tombe dans un bac ; on compare la proba moyenne à la fréquence observée."""
    bacs = [[] for _ in range(n_bins)]
    for m in matchs:
        for p, o in zip(m[cle], ISSUES):
            bacs[min(int(p * n_bins), n_bins - 1)].append((p, m["issue"] == o))
    return [(moyenne([p for p, _ in b]), moyenne([y for _, y in b]), len(b)) for b in bacs if b]


def svg_calibration(points_modele, points_marche, chemin):
    t, m = 400, 50  # taille du carré, marge
    def xy(p, f):
        return m + p * t, m + t - f * t
    lignes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{t + 2 * m}" height="{t + 2 * m}" font-family="sans-serif" font-size="12">',
        f'<rect width="100%" height="100%" fill="white"/>',
        f'<rect x="{m}" y="{m}" width="{t}" height="{t}" fill="none" stroke="#999"/>',
        f'<line x1="{m}" y1="{m + t}" x2="{m + t}" y2="{m}" stroke="#bbb" stroke-dasharray="4"/>',
    ]
    for i in range(6):
        v = i / 5
        x, y = xy(v, v)
        lignes.append(f'<text x="{x}" y="{m + t + 18}" text-anchor="middle">{v:.1f}</text>')
        lignes.append(f'<text x="{m - 8}" y="{y + 4}" text-anchor="end">{v:.1f}</text>')
    for points, couleur in ((points_marche, "#999"), (points_modele, "#1f5fbf")):
        coords = [xy(p, f) for p, f, _ in points]
        lignes.append('<polyline fill="none" stroke="{}" stroke-width="2" points="{}"/>'.format(
            couleur, " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)))
        for (x, y), (_, _, n) in zip(coords, points):
            lignes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3 + math.sqrt(n)}" fill="{couleur}" fill-opacity="0.6"/>')
    lignes += [
        f'<text x="{m + t / 2}" y="{m + t + 38}" text-anchor="middle">Probabilité prévue</text>',
        f'<text x="14" y="{m + t / 2}" text-anchor="middle" transform="rotate(-90 14 {m + t / 2})">Fréquence observée</text>',
        f'<text x="{m + 10}" y="{m + 20}" fill="#1f5fbf">● modèle</text>',
        f'<text x="{m + 10}" y="{m + 36}" fill="#999">● marché (cotes normalisées)</text>',
        "</svg>",
    ]
    chemin.write_text("\n".join(lignes), encoding="utf-8")


def taux(matchs):
    return moyenne([m["choix"] == m["issue"] for m in matchs]) if matchs else float("nan")


def main():
    chemin = Path(sys.argv[1]) if len(sys.argv) > 1 else CSV_DEFAUT
    matchs = charger(chemin)
    if not matchs:
        sys.exit(f"Aucun match joué dans {chemin}")
    n = len(matchs)
    uniforme = [1 / 3] * 3

    series = {}
    for nom, cle in (("Modèle", "modele"), ("Marché", "marche")):
        series[nom] = {
            "brier": [brier(m[cle], m["issue"]) for m in matchs],
            "logloss": [logloss(m[cle], m["issue"]) for m in matchs],
        }
    brier_unif = moyenne([brier(uniforme, m["issue"]) for m in matchs])

    diffs = [a - b for a, b in zip(series["Modèle"]["brier"], series["Marché"]["brier"])]
    bas, haut = ic_bootstrap(diffs)
    retenus = [m for m in matchs if m["retenu"]]

    SORTIE.mkdir(exist_ok=True)
    svg_calibration(calibration(matchs, "modele"), calibration(matchs, "marche"), SORTIE / "calibration.svg")

    md = [
        "# Résultats",
        "",
        f"Généré le {date.today():%d/%m/%Y} par `evaluer.py` sur {n} matchs joués.",
        "",
        "| Série | Brier (↓) | Log-loss (↓) | Brier skill vs 1/3 |",
        "|---|---|---|---|",
    ]
    for nom, s in series.items():
        b = moyenne(s["brier"])
        md.append(f"| {nom} | {b:.4f} | {moyenne(s['logloss']):.4f} | {1 - b / brier_unif:+.1%} |")
    md.append(f"| Uniforme (1/3 partout) | {brier_unif:.4f} | {math.log(3):.4f} | 0 |")
    md += [
        "",
        f"**Modèle − marché (Brier)** : {moyenne(diffs):+.4f}, IC 95 % bootstrap [{bas:+.4f} ; {haut:+.4f}].",
        "Négatif = le modèle fait mieux que le marché. Si l'intervalle contient 0, la différence n'est pas significative.",
        "",
        "## Choix principal",
        "",
        f"- Tous les matchs : {taux(matchs):.0%} de bons choix ({n} matchs)",
        f"- Matchs retenus (P ≥ 55 %) : {taux(retenus):.0%} ({len(retenus)} matchs)" if retenus else "- Aucun match retenu",
        "",
        "## Calibration",
        "",
        "![Calibration](calibration.svg)",
        "",
        "| Proba prévue (moy.) | Fréquence observée | N |",
        "|---|---|---|",
    ]
    md += [f"| {p:.2f} | {f:.2f} | {k} |" for p, f, k in calibration(matchs, "modele")]
    md += ["", f"Avec {n} matchs ({3 * n} probabilités), la calibration reste très bruitée : à lire à partir de ~100 matchs."]

    hors_protocole = charger_marche(CSV_MARCHE)
    if hors_protocole:
        tous = [{"issue": m["issue"], "marche": m["marche"]} for m in matchs] + hors_protocole
        nt = len(tous)
        b_m = moyenne([brier(m["marche"], m["issue"]) for m in tous])
        b_u = moyenne([brier(uniforme, m["issue"]) for m in tous])
        md += [
            "",
            "## Marché seul, toutes journées",
            "",
            f"Les journées J2 et J3 n'ont pas été archivées avant les matchs. Leurs cotes de clôture ont été relevées après coup "
            f"(`{CSV_MARCHE.name}`) : elles mesurent le marché, jamais le modèle, et n'entrent pas dans la comparaison ci-dessus.",
            "",
            f"- {nt} matchs ({n} de la J1 + {len(hors_protocole)} des J2-J3)",
            f"- Brier marché : {b_m:.4f} (uniforme : {b_u:.4f}, skill {1 - b_m / b_u:+.1%})",
            f"- Log-loss marché : {moyenne([logloss(m['marche'], m['issue']) for m in tous]):.4f}",
            f"- Favori du marché gagnant : {moyenne([max(range(3), key=lambda i: m['marche'][i]) == ISSUES.index(m['issue']) for m in tous]):.0%}",
            "",
            "| Proba marché (moy.) | Fréquence observée | N |",
            "|---|---|---|",
        ]
        md += [f"| {p:.2f} | {f:.2f} | {k} |" for p, f, k in calibration(tous, "marche")]
    (SORTIE / "RESULTATS.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"{n} matchs | Brier modèle {moyenne(series['Modèle']['brier']):.4f} "
          f"| marché {moyenne(series['Marché']['brier']):.4f} | uniforme {brier_unif:.4f}")
    print(f"Écrit : {SORTIE / 'RESULTATS.md'}, {SORTIE / 'calibration.svg'}")


if __name__ == "__main__":
    main()
