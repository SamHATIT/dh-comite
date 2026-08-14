#!/usr/bin/env python3
"""Contre-jour par etalonnage — pas de generation.

POURQUOI (13/08) : la campagne des onze agents demande une silhouette a contre-jour
dont le visage ne se resout jamais. Premier essai fait avec un modele d image
(nano-banana / gemini-3-pro-image) : il a change la coiffure, resolu le visage en
profil, et fait flotter le document en l air. Un modele generatif REINVENTE ce qu on
lui demande de transformer.

Or le contre-jour n est pas une invention, c est un ETALONNAGE : assombrir le sujet,
bruler la fenetre, virer vers l ambre. Une courbe et deux masques. Et surtout :
REPRODUCTIBLE A L IDENTIQUE sur les onze agents, la ou un modele rendrait onze
interpretations differentes. C est l enjeu d une serie.

Le parti pris retenu avec Sam : profil perdu plutot que vue de dos. Le visage
reste tourne vers la fenetre et plonge dans l ombre — la grammaire du script est
respectee sans jamais rien generer.

Usage : contrejour.py <entree.png> <sortie.png> [--force 0.85]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


def contrejour(src, dst, force=0.85, portrait=True):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    a = np.asarray(im).astype(np.float32) / 255.0

    # Luminance perceptuelle — sert a distinguer la fenetre du sujet.
    lum = a[..., 0]*0.2126 + a[..., 1]*0.7152 + a[..., 2]*0.0722

    # 1. MASQUE DE FENETRE. La source de lumiere est a gauche (verifie sur
    #    l avatar : mur clair a droite, fenetre a gauche). On construit un
    #    degrade horizontal, pondere par la luminance reelle : ce qui est
    #    deja clair a gauche devient la source.
    gx = np.linspace(1.0, 0.0, w)[None, :] ** 1.6
    fenetre = np.clip(gx * (lum ** 1.2) * 2.4, 0, 1)
    fenetre = np.asarray(Image.fromarray((fenetre*255).astype(np.uint8))
                         .filter(ImageFilter.GaussianBlur(w*0.045)), np.float32)/255.0

    # 2. MASQUE DE SUJET : tout ce qui n est pas la fenetre. On l assombrit
    #    fortement pour que le visage ne se resolve plus.
    sujet = 1.0 - fenetre

    # 3. ASSOMBRISSEMENT du sujet.
    #
    #    CORRECTIF DU 13/08 : la premiere version laissait le visage lumineux —
    #    Sam l a decrit comme « eblouie plutot qu a contre-jour », et c etait
    #    exact. La cause : la courbe en puissance protege les tons clairs, or
    #    la peau EST un ton clair. On l ecrasait donc moins que le reste.
    #
    #    Le vrai contre-jour suppose deux choses : la source DERRIERE le sujet,
    #    et l eclairage frontal ETEINT. Ici on ne peut pas deplacer la source,
    #    mais on peut annuler son effet sur le sujet et ne garder qu un lisere
    #    de contour — c est lui, et lui seul, qui dit « contre-jour ».
    p = 1.0 + force * 4.4          # courbe bien plus dure qu en v1 (2,6)
    ombre = a ** p
    ombre *= (1.0 - force * 0.78)  # et un plancher plus bas

    # 3 bis. LISERE DE CONTOUR. On isole le bord du sujet tourne vers la
    #    lumiere par la difference entre l image et sa version floutee : les
    #    transitions franches ressortent, les aplats disparaissent. Ce lisere
    #    est REAJOUTE apres l assombrissement, sinon il serait ecrase avec
    #    le reste.
    fl = np.asarray(Image.fromarray((lum*255).astype(np.uint8))
                    .filter(ImageFilter.GaussianBlur(w*0.012)), np.float32)/255.0
    bord = np.clip((lum - fl) * 5.5, 0, 1) * gx[0][None, :].repeat(h, 0)
    bord = np.asarray(Image.fromarray((bord*255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(2.0)), np.float32)/255.0
    ombre = np.clip(ombre + bord[..., None] * np.array([1.0, 0.78, 0.45], np.float32) * 0.55, 0, 1)

    # 4. BRULURE de la fenetre vers un ambre chaud, pas un blanc pur.
    ambre = np.array([1.0, 0.82, 0.52], np.float32)
    brulee = np.clip(a * 0.35 + ambre * fenetre[..., None] * 1.55, 0, 1)

    # 5. COMPOSITION.
    out = ombre * sujet[..., None] + brulee * fenetre[..., None]

    # 6. VIRAGE GLOBAL vers l ambre et le noir profond (charte de la campagne).
    out[..., 0] = np.clip(out[..., 0] * 1.14 + 0.012, 0, 1)
    out[..., 1] = np.clip(out[..., 1] * 0.99, 0, 1)
    out[..., 2] = np.clip(out[..., 2] * 0.74, 0, 1)

    # 7. NOIRS ECRASES : le bas de la dynamique part au noir, sinon la
    #    silhouette reste grise et lit comme une sous-exposition ratee.
    out = np.clip((out - 0.045) / 0.955, 0, 1)

    img = Image.fromarray((out*255).astype(np.uint8))

    # 8. GRAIN ARGENTIQUE 35 mm — demande par le script.
    g = np.random.default_rng(7).normal(0, 5.2, (h, w, 1)).repeat(3, axis=2)
    img = Image.fromarray(np.clip(np.asarray(img, np.float32) + g, 0, 255).astype(np.uint8))
    img = ImageEnhance.Contrast(img).enhance(1.12)

    # 9. FORMAT PORTRAIT 9:16 pour LinkedIn, recadre au centre du sujet
    #    (legerement a droite, la ou se tient la personne).
    if portrait:
        cible = h * 9 / 16
        if w > cible:
            cx = int(w * 0.56)
            g0 = max(0, min(cx - int(cible/2), w - int(cible)))
            img = img.crop((g0, 0, g0 + int(cible), h))

    img.save(dst, quality=95)
    return img.size


if __name__ == "__main__":
    f = 0.85
    if "--force" in sys.argv:
        f = float(sys.argv[sys.argv.index("--force")+1])
    taille = contrejour(sys.argv[1], sys.argv[2], f)
    print(f"ecrit : {sys.argv[2]}  {taille[0]}x{taille[1]}")
