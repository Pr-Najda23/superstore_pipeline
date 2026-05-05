#!/usr/bin/env python3
"""
Staging Layer — Sélectionne le fichier raw le plus récent
et le valide avant le nettoyage.
"""

import os
import glob
import logging
import pandas as pd
from pathlib import Path

log = logging.getLogger("pipeline.staging")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

BASE_DIR = Path("/app")
STAGING_DIR = BASE_DIR / "staging"
DATA_DIR = BASE_DIR / "data" / "staging"


def run():
    log.info(" Staging layer démarré")

    # Cherche le fichier raw le plus récent
    patterns = [
        str(STAGING_DIR / "raw_*.csv"),
        str(DATA_DIR / "raw_*.csv"),
    ]

    raw_files = []
    for pattern in patterns:
        raw_files.extend(glob.glob(pattern))

    if not raw_files:
        raise FileNotFoundError(" Aucun fichier raw_*.csv trouvé dans staging/ ou data/staging/")

    latest = max(raw_files, key=os.path.getmtime)
    log.info(f" Fichier sélectionné: {latest}")

    df = pd.read_csv(latest)
    log.info(f" Lignes brutes: {len(df)}")

    # Validation basique
    required_cols = ["title", "price"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f" Colonnes manquantes: {missing}")

    # Supprime doublons
    before = len(df)
    df = df.drop_duplicates()
    log.info(f" Doublons supprimés: {before - len(df)}")

    # Sauvegarde comme fichier staging unifié
    output = STAGING_DIR / "avito_staged.csv"
    STAGING_DIR.mkdir(exist_ok=True)
    df.to_csv(output, index=False, encoding="utf-8-sig")
    log.info(f" Staging OK — {len(df)} lignes → {output}")


if __name__ == "__main__":
    run()
