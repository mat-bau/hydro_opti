#### Gestion optimale d'un barrage hydro´electrique

#### Projet LINMA1702 : Mod`eles et m´ethodes d'optimisation I Partie 1

Pierre Vernimmen & Francois Glineur

### 1 Introduction

Ce projet s'inspire de probl´ematiques r´eelles rencontr´ees dans l'exploitation industrielle de barrages hydro´electriques.

Les barrages hydro´electriques jouent un rˆole essentiel dans le systeme ´electrique belge. Ils permettent de produire de l'electricite par turbinage a partir de l'eau stock´ee dans un r´eservoir. Ils offrent egalement la possibilite `a d'autres moments de stocker de l'´energie ´electrique par pompage d'eau dans le r´eservoir, ce qui permet de la r´ecup´erer plus tard, lorsque les prix sont plus ´elev´es.

Dans ce projet, vous ´etudierez le fonctionnement d'un barrage inspir´e d'une installation r´eelle situ´ee en Belgique, en utilisant des donn´ees r´ealistes correspondant aux mois de juin et juillet. Ces donn´ees comprennent :

- le prix de l'´electricit´e, exprim´e en euros par m´egawatt-heure (e/MWh), qui varie chaque heure <sup>1</sup> ,
- les apports naturels d'eau dans le r´eservoir, exprim´es en m`etres cubes par heure (m3/h),
- les caract´eristiques physiques du barrage.

L'objectif est de d´eterminer comment exploiter le barrage afin de maximiser les revenus totaux issus de la vente d'´electricit´e.

Ce projet vous demandera de transformer une description physique en mod`ele d'optimisation, de r´esoudre ce mod`ele et d'analyser les r´esultats obtenus d'un point de vue math´ematique, physique et ´economique.

Cette premi`ere partie a pour objectif de vous familiariser avec le fonctionnement du syst`eme ´etudi´e, ainsi qu'avec sa mod´elisation et sa r´esolution dans un cadre simple. La seconde partie introduira des mod`eles plus avanc´es. Vous serez alors encourag´es `a explorer diff´erents sc´enarios, et `a analyser de mani`ere quantitative et qualitative les r´esultats obtenus, notamment du point de vue math´ematique, computationnel, ´economique et physique.

# 2 Description du syst`eme

On consid`ere que le barrage est aliment´e par un flux d'eau entrant total F(t) (en m3/h), provenant d'un cours d'eau et d'apports naturels. Le barrage est mod´elis´e comme un r´eservoir contenant un volume d'eau V (t) (en m<sup>3</sup> ) `a l'instant t.

A tout moment, vous pouvez d´ecider d'envoyer un certain flux d'eau ` T(t) (en m3/h) depuis le r´eservoir en direction de la turbine, g´en´erant ainsi une certaine puissance ´electrique E(t) (en MW). Vous pouvez ´egalement d´ecider de d´elester le r´eservoir d'un certain flux D(t) (en m3/h), c'est-`a-dire vider le r´eservoir sans production d'´electricit´e. Ces deux actions peuvent ˆetre

<sup>1.</sup> Initialement depuis <https://www.kaggle.com/datasets/henriupton/electricity-dayahead-prices-entsoe>

effectu´ees simultan´ement. L'´electricit´e produite est suppos´ee vendue instantan´ement au march´e, `a un prix variant en fonction du temps P(t) (en e/MW h).

Il est ´egalement possible de pomper un certain flux d'eau M(t) (en m3/h) depuis l'aval vers le r´eservoir, ce qui consomme une certaine puissance ´electrique S(t) (en MW). L'´electricit´e consomm´e est ´egalement suppos´ee achet´ee instantan´ement au prix du march´e variant en fonction du temps P(t) (en e/MW h).

Il est n´ecessaire de tenir compte de certaines contraintes technologiques. Le barrage ne peut accueillir un volume d'eau sup´erieur au niveau maximal Vmax, ni descendre en dessous d'un volume minimal Vmin. De mˆeme, les flux T(t), D(t) et M(t) ne peuvent d´epasser les niveaux Tmax, Dmax et Mmax. On impose ´egalement `a tout moment une limite inf´erieure T Dmin sur le flux total sortant (´egal `a T(t) + D(t)). Enfin, il n'est pas possible d'ouvrir ou fermer instantan´ement une vanne : par cons´equent, on impose une contrainte de variation maximale sur les flux T(t) et D(t), qui peut s'exprimer selon |T ′ (t)| ≤ V Tmax et |D′ (t)| ≤ V Dmax `a tout instant t (ces bornes sont exprim´ees en m3/h<sup>2</sup> ).

L'optimisation est effectu´ee sur un horizon de N heures, soit t ∈ [0, tmax] (en h) avec tmax = N. Le volume d'eau initial contenu dans le barrage est fix´e `a V (0) = V0, et, dans une optique de fonctionnement cyclique, on imposera toujours la contrainte terminale V (tmax) = V0.

Toutes les constantes physiques sont disponibles dans le fichier BelgiumScenario.txt.

#### 3 Questions de mod´elisation

Question 1.1 On suppose disposer de pr´evisions exactes du flux entrant et du prix de l'´electricit´e. Plus pr´ecis´ement, pour un horizon de planification de N heures, on connaˆıt les valeurs moyennes horaires F1, . . . , F<sup>N</sup> et P1, . . . , P<sup>N</sup> .

> Formulez un mod`ele lin´eaire d´ecrivant le fonctionnement du barrage sur cet horizon. Vous pr´eciserez clairement :

- les variables de d´ecision ;
- les param`etres ;
- les contraintes ;
- les ´eventuelles hypoth`eses de mod´elisation ;
- les unit´es des diff´erentes quantit´es.

Bien que la description physique initiale soit continue en temps, votre mod`ele devra reposer sur une discr´etisation horaire afin d'obtenir un nombre fini de variables et de contraintes. Vous expliquerez en particulier comment les variables discr`etes repr´esentent les flux continus T(t) et D(t) sur l'intervalle [0, tmax], avec tmax = N.

Vous pouvez, si vous le jugez utile, accompagner votre formulation d'un sch´ema r´ecapitulatif.

Question 1.2 On introduit `a pr´esent une fonction objectif. On suppose que la puissance ´electrique produite est proportionnelle au flux turbin´e :

$$E(t) = E_T T(t),$$

o`u E<sup>T</sup> est une constante exprim´ee en MWh/m<sup>3</sup> .

On consid`ere aussi une station de pompage permettant de renvoyer de l'eau depuis l'aval vers le r´eservoir. A l'instant ` t, le flux pomp´e M(t) (en m3/h) est born´e par Mmax et cela consomme une ´energie proportionnelle au d´ebit :

$$M_E M(t),$$

o`u M<sup>E</sup> est exprim´e en MWh/m<sup>3</sup> . Cette ´energie est achet´ee au prix du march´e P(t).

Proposez une formulation du probl`eme enti`erement lin´eaire et continue permettant de d´eterminer la strat´egie de contrˆole optimale, c'est-`a-dire celle qui maximise le b´en´efice total (revenus de vente moins coˆuts d'achat d'´electricit´e) sur l'horizon consid´er´e.

## 4 Analyse exploratoire des donn´ees

Question 1.3 Analysez qualitativement les donn´ees fournies.

Vous pouvez par exemple examiner comment ´evoluent le prix de l'´electricit´e, le flux entrant, etc.

Discutez les implications pour l'exploitation du barrage : par exemple `a quels moments semble-t-il int´eressant a priori de produire, `a quels moments semble-t-il int´eressant de stocker ?

#### 5 Impl´ementation

Question 1.4 Impl´ementez en Python le mod`ele lin´eaire propos´e `a la Question 1.2, en utilisant la biblioth`eque cvxpy (<https://www.cvxpy.org/>) et le solveur HiGHS, disponible directement sur cvxpy (plus d'informations sur <https://highs.dev/>).

> Votre impl´ementation devra contenir une fonction principale hydro(data), o`u data d´esigne le fichier depuis lequel les donn´ees sont lues (BelgiumScenario1.txt, BelgiumScenario2.txt ou tout autre fichier .txt de la mˆeme forme pour tester votre impl´ementation).

Cette fonction devra r´esoudre le probl`eme d'optimisation et renvoyer un dictionnaire sol contenant :

- les volumes sol.V,
- les flux turbin´es sol.T,
- les flux d´elest´es sol.D,
- les flux pomp´es sol.M,
- la valeur optimale de la fonction objectif sol.valopt.

Vous ˆetes libres d'impl´ementer autant de fonctions auxiliaires que n´ecessaire. Toutefois, la fonction hydro(data) devra constituer le point d'entr´ee principal de votre programme et appeler, le cas ´ech´eant, ces fonctions auxiliaires.

Question 1.5 Calculez la solution optimale pour les donn´ees fournies.

Estimez le gain apport´e par l'optimisation, en comparant avec une strat´egie de r´ef´erence sans pompage dans laquelle le flux turbin´e compense exactement le flux entrant `a chaque instant. Estimez ´egalement le gain apport´e sp´ecifiquement par le pompage.

- Question 1.6 Consid´erez `a nouveau le mod`ele lin´eaire introduit `a la Question 1.2
  - (a) Comment pourrait-on ´evaluer, avec un minimum de nouveaux calculs, l'impact sur la valeur optimale de la fonction objectif :

- d'une petite variation des param`etres suivants :
  - volume maximal Vmax ;
  - d´ebit maximal de turbinage Tmax ;
  - d´ebit maximal de pompage Mmax ;
  - limite de variation du turbinage V Tmax.
- d'une petite variation ∆F<sup>k</sup> du flux entrant durant la p´eriode k ;
- d'une petite variation ∆P<sup>k</sup> du prix de l'´electricit´e durant la p´eriode k.
- (b) Calculez ces valeurs (exprim´ees dans les unit´es appropri´ees, par exemple en euros par m<sup>3</sup> , ou en euros·h/m<sup>3</sup> ) et interpr´etez ´economiquement. En particulier, estimez `a partir de quel coˆut il serait rentable d'effectuer chacun des investissements correspondants. Identifiez le ou les investissements prioritaires.
- (c) Montrez enfin, `a l'aide d'un exemple impliquant une variation plus importante d'un param`etre, que ces estimations peuvent devenir inexactes. Comparez les estimations obtenues avec les gains r´eels apr`es r´e-optimisation compl`ete du probl`eme et commentez les diff´erences observ´ees.

## 6 Consignes — Partie 1

Cette premi`ere partie est consacr´ee `a la construction du mod`ele math´ematique, `a son impl´ementation et `a une premi`ere (et courte) analyse.

- Le projet se r´ealise par groupes de deux ´etudiants.
- Le rapport de cette partie ne d´epassera pas 3 pages.
- La date limite de remise de ce rapport est fix´e au lundi 13 avril 2026 `a midi.
- Le code Python devra ˆetre fourni sous la forme d'un Notebook Jupyter, avec la fonction hydro(data) facile et rapide `a appeler, pour tester votre impl´ementation.
- Votre impl´ementation sera test´ee sur plusieurs jeux de donn´ees, dont certains ne seront pas accessibles `a l'avance.
- L'objectif principal de cette partie est la mod´elisation correcte et l'impl´ementation correcte du probl`eme initial.
- Les analyses demand´ees doivent rester br`eves.
- Une interrogation ´ecrite individuelle portant sur le projet sera organis´ee lors de S13 (apr`es la seconde partie du projet). Lors de cette interrogation, vous devrez ˆetre capables d'expliquer et de justifier les choix de mod´elisation et de r´esolution effectu´es, d'interpr´eter les r´esultats obtenus, ainsi que de mod´eliser un probl`eme diff´erent mais similaire en utilisant les mˆemes principes.