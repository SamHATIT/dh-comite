"""Rend les cartons de fin en PNG. Un carton fixe n'a aucune raison d'etre
produit par un modele video : celui du 14/08 sortait "SOPHIEAI Agent" colle,
le filet en carres vides et l'apostrophe manquante. Incruste au montage, il
est identique sur les douze spots et le modele ne peut plus le casser."""
import sys
from playwright.sync_api import sync_playwright

src, dst = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 768, "height": 1344},
                    device_scale_factor=2)
    pg.goto("file://" + src)
    pg.wait_for_timeout(2500)          # laisse les polices se charger
    pg.screenshot(path=dst)
    b.close()
print("ecrit :", dst)
