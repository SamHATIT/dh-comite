#!/usr/bin/env python3
"""Controle des depots — signale ce qui n est ni commite ni pousse.

POURQUOI (14/08) : quatre jours de travail sont restes hors de tout historique.
Fiches d agents modifiees, cockpit, releve des couts, correctifs de prix — rien
n etait commite, rien n etait pousse. Le distant de la plateforme s arretait au
10/08, celui du comite aussi, et le site vitrine n a aucun distant.

Un crochet post-commit existe depuis le 06/08 et fonctionne : il regenere
JOURNAL.md a chaque commit. Mais il ne se declenche QU AU COMMIT. Le maillon
manquant n etait pas la documentation, c etait le commit lui-meme — et rien ne
le verifiait.

Ce controle est EXTERIEUR a la discipline de celui qui travaille. C est le seul
moyen fiable : une regle ecrite quelque part et que rien ne verifie peut etre
oubliee trois fois de suite.

Usage : controle-depots.py [--alerte]   (--alerte envoie sur Telegram)
Sortie : 0 si tout est propre, 1 sinon.
"""
import os, subprocess, sys, urllib.parse, urllib.request
from datetime import datetime, timezone

DEPOTS = [
    ("plateforme",   "/root/workspace/digital-humans-production"),
    ("comite",       "/root/workspace/dh-comite"),
    ("site vitrine", "/var/www/dh-preview"),
]
SEUIL_HEURES = 24


def sh(cwd, *args):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception:
        return ""


def controler(nom, chemin):
    if not os.path.isdir(os.path.join(chemin, ".git")):
        return [f"{nom} : pas un depot git"]
    pb = []

    modifies = [l for l in sh(chemin, "git", "status", "--short").split("\n") if l.strip()]
    if modifies:
        pb.append(f"{nom} : {len(modifies)} fichier(s) non commite(s)")

    branche = sh(chemin, "git", "rev-parse", "--abbrev-ref", "HEAD")
    distant = sh(chemin, "git", "remote")
    if not distant:
        pb.append(f"{nom} : AUCUN DEPOT DISTANT — le travail n existe que sur ce serveur")
    else:
        local = sh(chemin, "git", "rev-parse", "HEAD")
        ref = sh(chemin, "git", "ls-remote", "origin", f"refs/heads/{branche}")
        tete = ref.split("\t")[0] if ref else ""
        if not tete:
            pb.append(f"{nom} : branche {branche} absente du distant")
        elif tete != local:
            avance = sh(chemin, "git", "rev-list", "--count", f"{tete}..HEAD") or "?"
            pb.append(f"{nom} : {avance} commit(s) non pousse(s)")

    # anciennete du dernier commit
    ts = sh(chemin, "git", "log", "-1", "--format=%ct")
    if ts.isdigit():
        h = (datetime.now(timezone.utc).timestamp() - int(ts)) / 3600
        if h > SEUIL_HEURES and modifies:
            pb.append(f"{nom} : dernier commit il y a {int(h)} h, et des fichiers ont change depuis")
    return pb


def main():
    tout = []
    for nom, chemin in DEPOTS:
        tout += controler(nom, chemin)

    if not tout:
        print("Depots : tout est commite et pousse.")
        return 0

    print("═══ DEPOTS — TRAVAIL NON SAUVEGARDE ═══", file=sys.stderr)
    for p in tout:
        print("  " + p, file=sys.stderr)
    print(file=sys.stderr)
    print("  Un depot non pousse disparait avec le serveur.", file=sys.stderr)

    if "--alerte" in sys.argv:
        env = "/root/workspace/dh-comite/.env"
        tok = chat = None
        if os.path.exists(env):
            for l in open(env):
                if l.startswith("TELEGRAM_BOT_TOKEN="): tok = l.split("=", 1)[1].strip()
                if l.startswith("TELEGRAM_CHAT_ID="):   chat = l.split("=", 1)[1].strip()
        if tok and chat:
            txt = "⚠️ Depots non sauvegardes :\n" + "\n".join("· " + p for p in tout)
            try:
                urllib.request.urlopen(
                    f"https://api.telegram.org/bot{tok}/sendMessage",
                    urllib.parse.urlencode({"chat_id": chat, "text": txt}).encode(),
                    timeout=15)
            except Exception:
                pass
    return 1


if __name__ == "__main__":
    sys.exit(main())
