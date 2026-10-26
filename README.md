# Prévisions probabilistes vs marché : Ligue des champions 2026-27

Suivi en temps réel de prévisions 1N2 (résultat à 90 minutes) sur la Ligue des champions, comparées aux probabilités implicites du marché.

La question de départ : **est-ce qu'un ajustement humain, appuyé sur des faits datés, améliore les probabilités du marché, ou est-ce qu'il les dégrade ?** C'est un test d'efficience de marché appliqué au sport, avec un historique daté qu'on ne peut pas réécrire.

## Méthode

1. **Probabilités du marché** : cotes 1N2 de trois opérateurs (Winamax, Unibet, Betclic), converties en probabilités, marge retirée par normalisation proportionnelle, puis moyennées.
2. **Contrôle Elo** : classement ClubElo, comparé à `P(1) + 0,5·P(N)`. Il sert de contrôle de cohérence et n'entre pas dans le calcul.
3. **Ajustement** : ±3 points maximum par issue, somme nulle, seulement avec un fait postérieur à la collecte des cotes ou manifestement absent du marché (sinon on compte deux fois la même info).
4. **Archivage avant le match** : chaque prévision est datée (`heure_prevision`) et ne change plus jamais. L'historique git en fait foi.

Le détail des versions de la méthode est dans [CRITERES.md](CRITERES.md).

## Mesures

- **Brier multiclasse** : somme des écarts au carré entre probabilités et issue (0 = parfait, 0,667 = 1/3 partout).
- **Log-loss** : pénalise fortement les certitudes ratées.
- **Brier skill score** : gain relatif par rapport à une prévision naïve 1/3, 1/3, 1/3.
- **Modèle − marché** : différence de Brier match par match, avec un intervalle de confiance à 95 % par bootstrap.
- **Calibration** : quand le modèle annonce 60 %, l'issue arrive-t-elle environ 6 fois sur 10 ?

## Résultats

Voir [resultats/RESULTATS.md](resultats/RESULTATS.md), régénéré à chaque journée.

## Lancer

```bash
python3 evaluer.py
```

Python 3.10+ et rien d'autre (pas de dépendance externe).

## Données

`data/archive_previsions.csv` contient une ligne par match. Les colonnes principales :

| Colonne | Sens |
|---|---|
| `p1, pN, p2` | probabilités finales (après ajustement) |
| `p1_marche, pN_marche, p2_marche` | consensus du marché au même moment |
| `heure_prevision` | heure limite d'information |
| `version_methode` | version de la méthode utilisée |
| `resultat_90min` | issue (1 / N / 2) et score, ajoutés après le match |

`data/marche_cloture_J2-J3.csv` comble les journées 2 et 3, qui n'ont pas été archivées avant les matchs. Il contient seulement les cotes de clôture Betclic, Winamax et Unibet, relevées après coup sur Flashscore, et le résultat. Ces 36 matchs servent à évaluer le marché. Ils ne comptent jamais dans la comparaison modèle contre marché, puisque aucune prévision n'a été faite avant ces matchs.

## Limites

- Petit échantillon : les écarts au marché ne deviendront significatifs qu'après plusieurs centaines de matchs.
- Le marché utilisé est celui de trois opérateurs français, pas les cotes de clôture d'un marché très liquide (Pinnacle, Betfair).
