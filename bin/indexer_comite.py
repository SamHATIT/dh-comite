#!/usr/bin/env python3
"""Indexe le corpus du comité dans ChromaDB pour le rendre INTERROGEABLE.

Pourquoi ce script existe — remarque de Sam, 09/08/2026 :

  « Ce que j'aime dans des solutions comme Obsidian, c'est que ça ne t'oblige
    pas à alourdir chaque contexte, mais tout est accessible et indexé donc
    efficace. »

Il a raison, et cela corrige la façon dont le problème était posé. On ne
cherche pas à CHARGER plus de contexte dans chaque agent — on cherche à rendre
le corpus INTERROGEABLE, pour que chacun aille chercher ce dont il a besoin au
moment où il en a besoin.

Ce qui est indexé : décisions, rapports de directions, comptes rendus de
comité, briefs quotidiens, documents de configuration. Autrement dit, tout ce
que le dispositif a produit et que personne ne peut relire.

Ce qui n'est PAS indexé : le code (il a son propre accès via /repo), et les
données clients (il n'y en a pas, et il n'y en aura jamais ici).
"""
import os, sys, glob, json, hashlib
sys.path.insert(0, "/root/workspace/digital-humans-production/backend")

import chromadb
import psycopg2

CHROMA = "/opt/digital-humans/rag/chromadb_v2"
COLLECTION = "comite_collection"
BASE = "/root/workspace/dh-comite"


def fragments(texte, titre, source, taille=1400, chevauchement=180):
    """Découpe en fragments qui se chevauchent, pour ne pas couper une idée."""
    texte = (texte or "").strip()
    if not texte:
        return []
    out, i, n = [], 0, 0
    while i < len(texte):
        bout = texte[i:i + taille]
        out.append({
            "texte": f"[{titre}]\n{bout}",
            "id": hashlib.sha1(f"{source}:{n}:{bout[:80]}".encode()).hexdigest()[:24],
            "meta": {"source": source, "titre": titre[:180], "fragment": n},
        })
        i += taille - chevauchement
        n += 1
    return out


def collecter():
    docs = []

    # ── Les décisions ──
    # La base du comité n'est joignable QUE depuis son conteneur (pas de port
    # exposé, et c'est bien ainsi). On exporte donc par `docker exec` dans un
    # fichier intermédiaire, plutôt que d'ouvrir la base sur l'hôte.
    import subprocess
    try:
        r = subprocess.run(
            ["docker", "exec", "dh-comite", "bash", "-c",
             "psql \"$COMITE_DB_DSN\" -tA -F '|' -c "
             "\"SELECT id, statut, origine, date::text, replace(texte, chr(10), ' ') "
             "FROM decisions;\""],
            capture_output=True, text=True, timeout=90)
        n = 0
        for ligne in r.stdout.splitlines():
            p_ = ligne.split("|", 4)
            if len(p_) < 5:
                continue
            did, statut, origine, date, texte = p_
            corps = f"Statut : {statut}\nOrigine : {origine}\nDate : {date}\n\n{texte}"
            docs += fragments(corps, f"Décision {did}", f"decision:{did}")
            n += 1
        print(f"  décisions : {n} décisions, {len(docs)} fragments")
    except Exception as e:
        print(f"  décisions : ECHEC ({e})")

    avant = len(docs)

    # ── Rapports des directions et documents de configuration ──
    for motif in ("config/*/*.md", "config/*.md", "briefs/*.md"):
        for f in sorted(glob.glob(f"{BASE}/{motif}")):
            nom = f.replace(BASE + "/", "")
            try:
                docs += fragments(open(f, encoding="utf-8", errors="replace").read(),
                                  nom, f"fichier:{nom}")
            except Exception:
                pass
    print(f"  documents : {len(docs) - avant} fragments")

    # ── Rondes des directeurs (JSON) ──
    avant = len(docs)
    for f in sorted(glob.glob(f"{BASE}/rondes/*.json"))[-120:]:
        nom = f.replace(BASE + "/", "")
        try:
            d = json.load(open(f, encoding="utf-8"))
            corps = json.dumps(d, ensure_ascii=False, indent=1)
            docs += fragments(corps, nom, f"ronde:{nom}")
        except Exception:
            pass
    print(f"  rondes    : {len(docs) - avant} fragments")
    return docs


def main():
    docs = collecter()
    if not docs:
        print("rien à indexer"); return 1

    client = chromadb.PersistentClient(path=CHROMA)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(
        COLLECTION,
        metadata={"description": "Corpus du comité : décisions, rapports, briefs, rondes"},
    )

    # Dédoublonnage : ChromaDB refuse les identifiants en double.
    vus, textes, ids, metas = set(), [], [], []
    for d in docs:
        if d["id"] in vus:
            continue
        vus.add(d["id"])
        textes.append(d["texte"]); ids.append(d["id"]); metas.append(d["meta"])

    for i in range(0, len(textes), 400):
        col.add(documents=textes[i:i+400], ids=ids[i:i+400], metadatas=metas[i:i+400])
        print(f"  ... {min(i+400, len(textes))}/{len(textes)}")

    print(f"OK — {col.count()} fragments dans {COLLECTION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
