#!/bin/sh
# Recopie l'archive de travail dans le dépôt puis régénère les résultats.
set -e
cd "$(dirname "$0")"
SRC="$HOME/Other/Predictions/ucl-2026-27"
cp "$SRC/archive_previsions.csv" data/
cp "$SRC/CRITERES.md" .
python3 evaluer.py
