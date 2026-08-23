# Relance automatique de l'inference locale — 23/08/2026

Deux unites, deux machines, une seule chaine. Chacune a ete **eprouvee par une
panne reelle**, pas seulement declaree.

    comite (conteneur dh-comite)
      -> 172.19.0.1:18084          ouverture ufw dediee
      -> tunnel-spark-vllm         VPS, autossh, Restart=always
      -> Spark 127.0.0.1:8001
      -> vllm-lightning            Spark, systemd utilisateur, Restart=always

## Installation

**Sur le VPS**, en root :

    cp tunnel-spark-vllm.service /etc/systemd/system/
    systemctl daemon-reload && systemctl enable --now tunnel-spark-vllm

**Sur le Spark**, en `spark-dh` (surtout pas en root — c'est un service
*utilisateur*) :

    mkdir -p ~/.config/systemd/user
    cp vllm-lightning.service ~/.config/systemd/user/
    systemctl --user daemon-reload
    systemctl --user enable --now vllm-lightning

`loginctl enable-linger spark-dh` doit etre actif, sinon les services
utilisateur s'arretent a la deconnexion. Il l'etait deja (comfyui.service).

## Ouverture pare-feu, obligatoire

`INPUT` est en `DROP` par defaut depuis le durcissement du 21/08. Le conteneur
`dh-comite` n'atteint l'hote que sur les ports explicitement ouverts a son
sous-reseau :

    ufw allow from 172.19.0.0/16 to any port 18084 proto tcp

**Sans cette regle, tout fonctionne sauf le comite** : le tunnel ecoute,
l'hote repond, et le conteneur obtient 000. C'est le mode d'echec le plus
trompeur de ce montage — verifie le 23/08.

## Trois details qui ne sont pas cosmetiques

**`ExecStopPost=docker rm -f vllm-test`** — le script lance `docker run --rm`.
Si systemd tue le script, `--rm` ne s'applique pas : le conteneur survit et
empeche la relance (nom deja pris). Sans cette ligne, `Restart=always` boucle
en echec.

**`TimeoutStartSec=900`** — chargement des poids (~120 s) + compilation des
noyaux (~180 s) + initialisation Mamba2. Au delai par defaut de systemd, le
service serait declare en echec **alors qu'il charge normalement**, puis tue,
puis relance, indefiniment.

**`GatewayPorts=yes` sur le tunnel** — le conteneur passe par la passerelle
172.19.0.1, pas par la boucle locale. Un `-L 127.0.0.1:18084` fonctionnerait
depuis l'hote et pas depuis le comite.

## Ce que la relance ne fait pas

Une relance coute **~5 minutes** de rechargement. Si vLLM tombe pendant une
ronde, **le service repart, la ronde non** : les directions recoivent
`ECONNRESET` et le comite est partiel — constate le 23/08, l'alerte fonctionne
et nomme les directions touchees.

Pour enchainer automatiquement il faudrait un `ExecStartPost` qui attend
`/health`. Non fait : acceptable pour du quotidien.

## Verifier

    # VPS
    systemctl is-active tunnel-spark-vllm
    curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:18084/health
    docker exec dh-comite curl -s -o /dev/null -w "%{http_code}\n" \
      http://172.19.0.1:18084/health

    # Spark
    systemctl --user is-active vllm-lightning
    systemctl --user show vllm-lightning -p NRestarts --value

## Retour a Nemotron

`tunnel-spark-llm` (VPS:18080 -> Spark:8080) reste en place et actif, mais
**rien n'ecoute sur 8080** : llama-server a ete arrete le 23/08 au profit de
Lightning. Pour revenir en arriere, relancer llama-server sur le Spark et
repointer `config/cadence.yaml` sur `http://172.19.0.1:18080`. Commande de
relance et pieges dans `../README-vllm-spark.md`.

Les deux ne cohabitent pas : ~91 Go pour vLLM, ~32 Go pour Nemotron, 121 Go de
memoire unifiee.
