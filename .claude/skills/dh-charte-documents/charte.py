import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ENCRE="#2B2B2E"; LAITON="#C8A97E"; GRIS="#6B6B70"
ALERTE="#9B2C2C"; FAVORABLE="#2F6B4F"; FILET="#EDEAE4"

def poser_style():
    plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["DejaVu Sans"],
      "font.size":10,"axes.edgecolor":FILET,"axes.labelcolor":ENCRE,"axes.titlesize":13,
      "axes.titleweight":"bold","axes.titlecolor":ENCRE,"axes.spines.top":False,
      "axes.spines.right":False,"xtick.color":GRIS,"ytick.color":GRIS,
      "grid.color":FILET,"grid.linewidth":0.8,"figure.facecolor":"white","axes.facecolor":"white"})

def barres(donnees,titre="",unite="",seuil=None,libelle_seuil=""):
    l=list(donnees.keys()); v=list(donnees.values())
    c=[(FAVORABLE if seuil is not None and x>=seuil else ALERTE if seuil is not None else LAITON) for x in v]
    fig,ax=plt.subplots(figsize=(8,0.62*len(l)+1.6))
    b_=ax.barh(l,v,color=c,height=0.55); ax.invert_yaxis()
    ax.xaxis.grid(True,linewidth=0.8); ax.set_axisbelow(True)
    for b,x in zip(b_,v):
        ax.text(b.get_width()*1.015,b.get_y()+b.get_height()/2,f"{x:,.1f}{unite}".replace(","," "),
                va="center",fontsize=10,color=ENCRE,fontweight="bold")
    if titre: ax.set_title(titre,pad=16,loc="left")
    ax.set_xlim(0,max(v)*1.18); fig.tight_layout(); return fig,ax

def seuils(valeurs,plancher,parite,titre="",unite=" €"):
    l=list(valeurs.keys()); v=list(valeurs.values())
    fig,ax=plt.subplots(figsize=(8.4,0.6*len(l)+2.1))
    ax.axvspan(0,plancher,color=ALERTE,alpha=.07)
    ax.axvspan(plancher,parite,color=LAITON,alpha=.10)
    ax.axvspan(parite,max(v)*1.25,color=FAVORABLE,alpha=.07)
    c=[FAVORABLE if x>=parite else ALERTE if x<plancher else LAITON for x in v]
    b_=ax.barh(l,v,color=c,height=0.45); ax.invert_yaxis()
    for b,x in zip(b_,v):
        ax.text(b.get_width()*1.015,b.get_y()+b.get_height()/2,f"{x:,.0f}{unite}".replace(","," "),
                va="center",fontsize=10,color=ENCRE,fontweight="bold")
    # Les reperes vont EN BAS, sous l'axe : en haut ils chevauchent le titre.
    for x,lib,col in ((plancher,f"plancher {plancher:,.0f}{unite}".replace(","," "),ALERTE),
                      (parite,f"parité {parite:,.0f}{unite}".replace(","," "),FAVORABLE)):
        ax.axvline(x,color=col,linestyle="--",linewidth=1.3)
        ax.annotate(lib,xy=(x,len(l)-0.42),xytext=(x,len(l)-0.18),
                    fontsize=9,color=col,ha="center",fontweight="bold",
                    annotation_clip=False)
    if titre: ax.set_title(titre,pad=14,loc="left")
    ax.set_xlim(0,max(v)*1.25); ax.xaxis.grid(True,linewidth=0.8); ax.set_axisbelow(True)
    # Axe lisible : espace insecable comme separateur de milliers, unite affichee.
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda z,_: f"{z:,.0f}".replace(",","\u202f")+unite if z else "0"))
    fig.tight_layout(); return fig,ax

def sauver(fig,chemin,dpi=160):
    fig.savefig(chemin,dpi=dpi,bbox_inches="tight",facecolor="white"); plt.close(fig); return chemin
