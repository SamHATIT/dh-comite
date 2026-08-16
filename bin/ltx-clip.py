#!/usr/bin/env python3
"""Pilote LTX par l'API de ComfyUI — sans passer par l'interface.

POURQUOI (14/08) : Sam sur l'interface — « c'est galere comme outil, t'as pas
idee ». Il a raison : charger une image, coller un prompt, relancer, guetter la
file, recommencer onze fois. L'API fait la meme chose en une commande, et
surtout elle permet une BOUCLE sur les onze agents.

Le graphe a ete recupere depuis l'historique du serveur (une generation reussie),
donc c'est exactement ce qui tourne — pas une reconstruction approximative.

Trois points d'injection seulement :
  noeud 98    LoadImage       le portrait de l'agent
  noeud 92:3  CLIPTextEncode  le prompt
  noeud 92:11 RandomNoise     la graine, pour varier sans changer le texte

Usage :
  ltx-clip.py --image marcus-architect.png --prompt-fichier marcus.txt
  ltx-clip.py --image sophie-pm.png --prompt "..." --graine 42
"""
import argparse, json, os, subprocess, sys, time, urllib.request

GPU = os.environ.get("GPU_SSH", "ubuntu@50.35.188.68")
PORT = os.environ.get("GPU_PORT", "31810")
GRAPHE = "/root/workspace/dh-comite/config/marketing/comfy/graphe_ltx.json"
AVATARS = "/var/www/app-studio/avatars/large"
SORTIE = "/var/www/app-studio/tmp"


def gpu(cmd, timeout=60):
    r = subprocess.run(
        ["ssh", "-p", PORT, "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", GPU, cmd],
        capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()


def envoyer(image, prompt, graine):
    g = json.load(open(GRAPHE, encoding="utf-8"))
    g["98"]["inputs"]["image"] = image
    g["92:3"]["inputs"]["text"] = prompt
    g["92:11"]["inputs"]["noise_seed"] = graine
    charge = json.dumps({"prompt": g}).replace("'", "'\\''")
    r = gpu(f"curl -s -X POST http://127.0.0.1:8188/prompt "
            f"-H 'Content-Type: application/json' -d '{charge}'", timeout=90)
    try:
        return json.loads(r).get("prompt_id")
    except Exception:
        print("reponse inattendue :", r[:300], file=sys.stderr)
        return None


def attendre(pid, minutes=12):
    """La generation prend 1 a 3 minutes sur ce modele. On interroge l'historique
    plutot que de deviner : c'est le seul signal fiable de fin."""
    fin = time.time() + minutes * 60
    while time.time() < fin:
        h = gpu(f"curl -s http://127.0.0.1:8188/history/{pid}")
        if h and h != "{}":
            try:
                d = json.loads(h)[pid]
                st = d.get("status", {}).get("status_str")
                if st == "success":
                    for n in d.get("outputs", {}).values():
                        for v in n.get("videos", []) + n.get("gifs", []) + n.get("images", []):
                            return v.get("filename")
                    return "TERMINE_SANS_FICHIER"
                if st == "error":
                    return "ERREUR"
            except Exception:
                pass
        time.sleep(10)
    return "DELAI_DEPASSE"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--image", required=True, help="nom du portrait dans avatars/large")
    p.add_argument("--prompt")
    p.add_argument("--prompt-fichier")
    p.add_argument("--graine", type=int, default=10)
    p.add_argument("--nom", help="nom du fichier de sortie")
    a = p.parse_args()

    prompt = a.prompt
    if a.prompt_fichier:
        prompt = open(a.prompt_fichier, encoding="utf-8").read().strip()
    if not prompt:
        sys.exit("il faut --prompt ou --prompt-fichier")

    # televerser le portrait sur le GPU s'il n'y est pas
    src = os.path.join(AVATARS, a.image)
    if not os.path.exists(src):
        sys.exit(f"portrait introuvable : {src}")
    subprocess.run(["scp", "-P", PORT, "-o", "BatchMode=yes", src,
                    f"{GPU}:~/ComfyUI/input/{a.image}"], capture_output=True, timeout=90)

    print(f"envoi   : {a.image}, graine {a.graine}")
    pid = envoyer(a.image, prompt, a.graine)
    if not pid:
        sys.exit("envoi refuse")
    print(f"file    : {pid[:8]}")

    f = attendre(pid)
    if f in ("ERREUR", "DELAI_DEPASSE", "TERMINE_SANS_FICHIER", None):
        sys.exit(f"echec : {f}")

    nom = a.nom or f"ltx_{a.image.split('-')[0]}_{a.graine}.mp4"
    subprocess.run(["scp", "-P", PORT, "-o", "BatchMode=yes",
                    f"{GPU}:~/ComfyUI/output/video/{f}", os.path.join(SORTIE, nom)],
                   capture_output=True, timeout=180)
    os.chmod(os.path.join(SORTIE, nom), 0o644)
    print(f"pret    : https://app.digital-humans.fr/tmp/{nom}")


if __name__ == "__main__":
    main()
