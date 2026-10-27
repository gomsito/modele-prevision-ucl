# Suivi prévisions UCL 2026-27 — critères et versions

## v0.1 (2026-09-08)
- Mode B : consensus des probabilités implicites de Winamax, Unibet.fr, Betclic (normalisation proportionnelle par book, puis moyenne), marché 1N2 90 min.
- Contrôle : Elo ClubElo (espérance domicile hors nul, avec avantage domicile 0 et +60) ; utilisé comme signal de cohérence, jamais converti en 1N2.
- Ajustement manuel expérimental : ±3 points max par issue, somme nulle, motivé dans la fiche. Deux séries archivées (marché brut / v0.1 ajustée) pour mesurer si l'ajustement apporte quelque chose.
- Scores exacts : distribution implicite du marché « score exact » Winamax normalisée (marge ~60 %, donc indicative).
- Sélection (seuil provisoire, à revoir après ~30 matchs) : retenu si P(choix) ≥ 55 % et aucune incertitude identifiée ne peut changer le favori. « À réévaluer » = compos officielles susceptibles de modifier P de plus de ~3 points.
- Heure limite d'information : heure_prevision dans le CSV. Rien de postérieur n'est utilisé.
- Résultat 90 min à remplir après match : « 1 », « N » ou « 2 » + score.

Bilan à produire : taux de bons choix (tous / retenus), couverture, réussite par issue, Brier multiclasses, log-loss, comparé au marché brut au même horaire.

## v0.2 (2026-09-09)
- **Correction du contrôle Elo.** En v0.1 l'espérance Elo était comparée au ratio marché P(1)/(P(1)+P(2)) : les deux quantités ne mesurent pas la même chose. L'espérance Elo vaut P(1) + 0,5·P(N). La comparaison se fait désormais entre `Elo(HA=60)` et `P(1)+0,5·P(N)` du marché. Les écarts observés au 09/09 tombent de 20-25 pts à 1-7 pts : la v0.1 fabriquait une divergence artificielle.
- Aucune probabilité archivée de la J1 du 08/09 n'est modifiée : l'Elo n'entrait pas dans le calcul, il ne servait que de contrôle.
- Le reste (mode B, consensus 3 books, ajustement ±3 pts somme nulle, seuil 55 %, scores exacts Winamax) est inchangé.
- Limite nouvelle identifiée : sur les matchs très déséquilibrés, la case « Autre » du marché score exact Winamax pèse 8 à 20 % ; la distribution de scores y est tronquée et le 1N2 reconstitué à partir des scores n'est pas exploitable. À ne pas présenter comme une seconde estimation.
- Cas d'un book manquant : si un opérateur ne renvoie rien (Unibet sur PSG-Slovan le 09/09), le consensus est calculé sur les books disponibles et le nombre de books est archivé dans les sources.

## v0.3 (2026-09-10)
- **Ajustement manuel neutralisé (0,0,0) sur les six matchs.** Règle nouvelle : l'ajustement ±3 pts n'est appliqué que si je détiens un fait concret *postérieur* à la collecte des cotes ou manifestement non intégré au marché. Le 10/09, toutes les absences connues (Guendouzi, Oosterwolde, Schouten, Baumgartner, de Ligt, Gradit…) étaient publiques avant la collecte : les intégrer une seconde fois aurait été du double comptage. Conséquence : p_finale = consensus marché pour cette journée, et les deux séries archivées sont identiques.
- Piège outil identifié : `cotes.py` applique par défaut `--min-cote 1.30`, ce qui **supprime la cote du favori** sur les matchs très déséquilibrés (Bayern 1.06, Man United 1.06 absents à la première collecte). Toute collecte 1N2 doit utiliser `--min-cote 0`.
- Contrôle Elo impossible quand un club n'est pas classé par ClubElo (Sabah FK le 10/09).
- Rappel v0.2 confirmé : sur Bayern-Bodø et Man United-Sabah, la case « Autre » du marché score exact pèse 18,1 % et 14,3 %. Le score modal y est donné comme projection indicative, pas comme résultat d'une distribution complète.

## Note du 2026-10-26 : trou J2-J3 et réparation de l'archive
- **J2 (13-14/10) et J3 (20-21/10) non archivées avant les matchs.** Aucune prévision n'est reconstituée après coup. Les cotes de clôture Betclic/Winamax/Unibet ont été relevées sur Flashscore le 26/10 dans `marche_cloture_J2-J3.csv` (même consensus : normalisation par book, puis moyenne). Elles servent seulement à évaluer le marché, jamais le modèle.
- **Réparation de format.** Les 6 lignes du 10/09 (J1c) contenaient une virgule sans guillemets dans `mode`, ce qui décalait toutes les colonnes d'un cran. Le champ a été recollé et le fichier réécrit en CSV correctement échappé. Aucune probabilité n'a été modifiée. La sauvegarde d'avant est dans `archive_previsions.csv.bak-2026-10-26`.
- Résultats 90 min des 6 matchs J1c ajoutés (Flashscore).
- **À partir de la J4 (03-04/11), retour au protocole** : archivage avant le coup d'envoi.

## v0.4-auto (2026-11-03)
- **Archivage automatique** par la tâche planifiée `ucl-archivage-auto` (mardi au jeudi, 11h30), via `archiver.py` : consensus 3 books (normalisation par book puis moyenne), au moins 2 books, matchs déjà commencés jamais archivés.
- **Ajustement manuel = 0** : l'automate n'a pas de fait postérieur à la collecte, donc p_finale = marché (même règle qu'en v0.3). Sur ces lignes, modèle et marché sont identiques par construction.
- Cotes : scraper-cotes en priorité ; si le réseau bloque les sites de paris (pare-feu Fortinet constaté le 26/10), cotes avant-match Betclic/Winamax/Unibet relevées sur Flashscore. La source est écrite dans `sources`.
- Elo ClubElo toujours en contrôle seulement.
