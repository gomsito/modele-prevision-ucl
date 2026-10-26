# Résultats

Généré le 26/10/2026 par `evaluer.py` sur 12 matchs joués.

| Série | Brier (↓) | Log-loss (↓) | Brier skill vs 1/3 |
|---|---|---|---|
| Modèle | 0.3087 | 0.5866 | +53.7% |
| Marché | 0.2939 | 0.5641 | +55.9% |
| Uniforme (1/3 partout) | 0.6667 | 1.0986 | 0 |

**Modèle − marché (Brier)** : +0.0148, IC 95 % bootstrap [+0.0072 ; +0.0225].
Négatif = le modèle fait mieux que le marché. Si l'intervalle contient 0, la différence n'est pas significative.

## Choix principal

- Tous les matchs : 83% de bons choix (12 matchs)
- Matchs retenus (P ≥ 55 %) : 100% (6 matchs)

## Calibration

![Calibration](calibration.svg)

| Proba prévue (moy.) | Fréquence observée | N |
|---|---|---|
| 0.10 | 0.00 | 7 |
| 0.25 | 0.11 | 18 |
| 0.53 | 0.88 | 8 |
| 0.72 | 1.00 | 1 |
| 0.89 | 1.00 | 2 |

Avec 12 matchs (36 probabilités), la calibration reste très bruitée : à lire à partir de ~100 matchs.
