#!/usr/bin/env python3
"""Genere le carton de fin ANIME — 3 s, 25 images/s.

POURQUOI (14/08) : le carton produit par le modele video sortait casse a chaque
generation — "SOPHIEAI Agent" colle, filet en carres vides, apostrophe manquante.
Un carton fixe n'a aucune raison d'etre genere par un modele : c'est du texte sur
fond noir. Rendu ici image par image, il est identique sur les douze spots et
plus rien ne peut le casser.

L'ANIMATION : le nom apparait en fondu et monte legerement, la fonction suit,
le filet se TRACE de la gauche vers la droite, la marque monte, la baseline
arrive en dernier. Rien ne clignote, rien ne rebondit — c'est un generique,
pas une transition de diaporama.

Usage : animer.py NOM "Fonction" sortie.mp4
"""
import os, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

NOM      = sys.argv[1] if len(sys.argv) > 1 else "SOPHIE"
FONCTION = sys.argv[2] if len(sys.argv) > 2 else "AI Project Manager"
SORTIE   = sys.argv[3] if len(sys.argv) > 3 else "/tmp/carton.mp4"

FPS, DUREE = 25, 3.0
N = int(FPS * DUREE)
GABARIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carton_anim.html")


def douceur(t):
    """Courbe d'attenuation : depart franc, arrivee posee. Pas de rebond."""
    return 1 - pow(1 - max(0.0, min(1.0, t)), 3)


def etat(i):
    """Etats des six elements a l'image i. Les retards sont echelonnes pour que
    l'oeil suive une lecture, pas une apparition simultanee."""
    t = i / FPS
    def elem(debut, duree=0.7, montee=14):
        p = douceur((t - debut) / duree)
        return p, (1 - p) * montee
    o1, y1 = elem(0.10)
    o2, y2 = elem(0.35)
    o4, y4 = elem(1.05)
    o5, y5 = elem(1.35)
    o6, y6 = elem(1.75, 0.8, 10)
    # le filet se trace : sa largeur va de 0 a 210 px
    largeur = 210 * douceur((t - 0.75) / 0.9)
    # le portrait monte tres lentement, presque imperceptiblement, du debut
    # jusqu a la fin : c est ce qui donne le sentiment d une affiche vivante
    fond = 0.16 * douceur(t / 1.6)
    return {
        "--o1": o1, "--y1": f"{y1:.2f}px", "--o2": o2, "--y2": f"{y2:.2f}px",
        "--w3": f"{largeur:.1f}px",
        "--o4": o4, "--y4": f"{y4:.2f}px", "--o5": o5, "--y5": f"{y5:.2f}px",
        "--o6": o6, "--y6": f"{y6:.2f}px", "--of": f"{fond:.3f}",
    }


with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 768, "height": 1344}, device_scale_factor=1)
    pg.goto("file://" + GABARIT)
    pg.wait_for_timeout(2500)                      # chargement des polices
    pg.evaluate("([n,f]) => { document.querySelector('.nom').textContent = n;"
                "document.querySelector('.role').textContent = f; }", [NOM, FONCTION])
    for i in range(N):
        css = ";".join(f"{k}:{v}" for k, v in etat(i).items())
        pg.evaluate("s => document.querySelector('.c').style.cssText = s", css)
        pg.screenshot(path=os.path.join(tmp, f"{i:04d}.png"))
    b.close()

    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-framerate", str(FPS),
        "-i", os.path.join(tmp, "%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", SORTIE,
    ], check=True)

print(f"ecrit : {SORTIE}  ({N} images, {DUREE} s)")
