# Résultats

Généré le 05/11/2026 par `evaluer.py` sur 36 matchs joués.

| Série | Brier (↓) | Log-loss (↓) | Brier skill vs 1/3 |
|---|---|---|---|
| Modèle | 0.3839 | 0.6929 | +42.4% |
| Marché | 0.3789 | 0.6854 | +43.2% |
| Uniforme (1/3 partout) | 0.6667 | 1.0986 | 0 |

**Modèle − marché (Brier)** : +0.0049, IC 95 % bootstrap [+0.0018 ; +0.0087].
Négatif = le modèle fait mieux que le marché. Si l'intervalle contient 0, la différence n'est pas significative.

## Choix principal

- Tous les matchs : 81% de bons choix (36 matchs)
- Matchs retenus (P ≥ 55 %) : 84% (19 matchs)

## Calibration

![Calibration](calibration.svg)

| Proba prévue (moy.) | Fréquence observée | N |
|---|---|---|
| 0.12 | 0.07 | 27 |
| 0.26 | 0.13 | 47 |
| 0.51 | 0.81 | 21 |
| 0.70 | 0.78 | 9 |
| 0.88 | 1.00 | 4 |

Avec 36 matchs (108 probabilités), la calibration reste très bruitée : à lire à partir de ~100 matchs.

## Marché seul, toutes journées

Les journées J2 et J3 n'ont pas été archivées avant les matchs. Leurs cotes de clôture ont été relevées après coup (`marche_cloture_J2-J3.csv`) : elles mesurent le marché, jamais le modèle, et n'entrent pas dans la comparaison ci-dessus.

- 72 matchs (36 de la J1 + 36 des J2-J3)
- Brier marché : 0.4443 (uniforme : 0.6667, skill +33.4%)
- Log-loss marché : 0.7833
- Favori du marché gagnant : 71%

| Proba marché (moy.) | Fréquence observée | N |
|---|---|---|
| 0.13 | 0.11 | 62 |
| 0.27 | 0.17 | 88 |
| 0.50 | 0.75 | 36 |
| 0.71 | 0.74 | 23 |
| 0.86 | 0.86 | 7 |
