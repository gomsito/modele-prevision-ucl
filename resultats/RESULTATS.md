# Résultats

Généré le 26/11/2026 par `evaluer.py` sur 54 matchs joués.

| Série | Brier (↓) | RPS (↓) | Log-loss (↓) | Brier skill vs 1/3 |
|---|---|---|---|---|
| Modèle | 0.4158 | 0.1494 | 0.7355 | +37.6% |
| Marché | 0.4125 | 0.1481 | 0.7305 | +38.1% |
| Uniforme (1/3 partout) | 0.6667 | 0.2562 | 1.0986 | 0 |

**Modèle − marché (Brier)** : +0.0033, IC 95 % bootstrap [+0.0012 ; +0.0059].

**Modèle − marché (RPS)** : +0.0013, IC 95 % bootstrap [+0.0005 ; +0.0025].

Négatif = le modèle fait mieux que le marché. Si l'intervalle contient 0, la différence n'est pas significative.

## Choix principal

- Tous les matchs : 76% de bons choix (54 matchs)
- Matchs retenus (P ≥ 55 %) : 78% (32 matchs)

## Calibration

![Calibration](calibration.svg)

| Proba prévue (moy.) | Fréquence observée | N |
|---|---|---|
| 0.13 | 0.12 | 51 |
| 0.27 | 0.15 | 61 |
| 0.51 | 0.80 | 25 |
| 0.70 | 0.67 | 18 |
| 0.87 | 1.00 | 7 |

Avec 54 matchs (162 probabilités), la calibration reste très bruitée : à lire à partir de ~100 matchs.

## Marché seul, toutes journées

Les journées J2 et J3 n'ont pas été archivées avant les matchs. Leurs cotes de clôture ont été relevées après coup (`marche_cloture_J2-J3.csv`) : elles mesurent le marché, jamais le modèle, et n'entrent pas dans la comparaison ci-dessus.

- 90 matchs (54 de la J1 + 36 des J2-J3)
- Brier marché : 0.4514 (uniforme : 0.6667, skill +32.3%)
- Log-loss marché : 0.7908
- Favori du marché gagnant : 70%

| Proba marché (moy.) | Fréquence observée | N |
|---|---|---|
| 0.13 | 0.13 | 86 |
| 0.27 | 0.18 | 102 |
| 0.50 | 0.75 | 40 |
| 0.70 | 0.69 | 32 |
| 0.86 | 0.90 | 10 |
