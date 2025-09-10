# Diagramme d’Activités (UML)


## 1) Objectif et positionnement
- Le diagramme d’Activités décrit le **flux de travail** (workflow) et l’**enchaînement des traitements** d’un processus métier, d’un cas d’utilisation, d’une opération, d’un algorithme ou d’un scénario technique.
- Il est centré sur la **logique de contrôle** (ordre d’exécution) et la **circulation des données** (flux d’objets).
- Il complète:
  - le diagramme de cas d’utilisation (vue fonctionnelle haut niveau),
  - le diagramme de séquence (interactions temporelles entre objets),
  - le diagramme d’états (cycle de vie d’un objet).
- On l’utilise pour:
  - clarifier un processus complexe,
  - révéler les **décisions**, **boucles**, **parallélismes** et **exceptions**,
  - aligner des acteurs/équipes via des **couloirs (swimlanes)**.

## 2) Éléments de base (notation UML)
- Action: unité de travail atomique (verbe d’action au présent: “Valider le panier”).
- Nœud initial (Start): point de départ du flux (disque plein).
- Nœud final d’activité (Activity Final): fin globale (cible cerclée).
- Nœud final de flux (Flow Final): termine un **flux** sans arrêter toute l’activité (cercle avec croix).
- Transition/Flux de contrôle: flèche simple entre nœuds.
- Garde: condition booléenne entre crochets sur une transition: `[stock > 0]`.
- Nœud de décision: losange séparant des branches conditionnelles (une entrée, plusieurs sorties).
- Nœud de fusion: losange réunissant des branches alternatives (plusieurs entrées, une sortie).
- Nœud de bifurcation (Fork): barre épaisse 1→n (déclenche des branches en **parallèle**).
- Nœud de jonction (Join): barre épaisse n→1 (synchronise les branches parallèles).
- Donnée/Objet (Object Node): représente un artefact manipulé (commande, facture…).
- Flux d’objet (Object Flow): flèche “donnée” entre actions/objets (option: stéréotype «objectFlow»).
- Partition / Couloir (Swimlane): sous-zone qui regroupe les actions par **rôle**, **système**, **organisation**.
- Interruption/Exception: borne d’interruption sur un bord (Interruptible Activity Region) + flux d’exception.
- Signal/Événement: envoi/réception d’événements asynchrones.
- Sous-activité (Call Behavior Action): action qui appelle une activité détaillée ailleurs.

Conseil de nommage:
- Actions: verbe + complément (“Vérifier le stock”, “Calculer les frais”).
- Objets: nom substantif (“Commande”, “Panier”).
- Gardes: conditions courtes, mesurables, sans effets de bord.

## 3) Contrôle, données et états intermédiaires
- Le **flux de contrôle** impose l’ordre d’exécution (sans transporter de données).
- Le **flux d’objet** transporte des **valeurs** ou **artefacts** entre actions.
- Les **objets en sortie** peuvent être étiquetés (ex: “Commande validée”).
- Les **pré/post-conditions** peuvent être notées en commentaire ou sous forme de gardes.

## 4) Décisions, gardes et couverture des cas
- Chaque sortie d’une décision doit être étiquetée par une **garde**. Elles doivent être:
  - mutuellement exclusives (sauf usage explicite de “else”),
  - complètes (couvrir tous les cas pertinents).
- Utiliser “else” pour la branche par défaut si nécessaire.

## 5) Parallélisme, synchronisation et ressources
- Un **Fork** démarre des branches parallèles indépendantes.
- Un **Join** attend la fin de toutes (par défaut) ou d’un sous-ensemble (avec garde/notation avancée).
- Attention aux **accès concurrents** à un même objet: prévoir des sections critiques, files, verrous ou actions idempotentes côté conception.

## 6) Boucles et répétitions
- Modèle simple: décision + garde pour boucler (“[encore des éléments?]”).
- Modèle structuré: une **Activity Region** annotée “loop” avec parties init/itération/sortie (selon notation outillée).
- Toujours expliciter la condition d’arrêt.

## 7) Swimlanes (Partitions)
- Objectif: clarifier “qui fait quoi”.
- Un couloir par **acteur**, **service**, **système** ou **équipe**.
- Déplacer l’action dans le couloir du **propriétaire** de l’exécution (pas forcément l’émetteur de données).
- Limiter le nombre de couloirs pour conserver la lisibilité (4–7 typiquement).

## 8) Exceptions et interruptions
- Utiliser des **Interruptible Activity Regions** pour modéliser des annulations (ex: “Annuler la commande”).
- Les **flux d’exception** sortent de la région vers un traitement d’erreur.
- Les **timeouts** et **signaux** peuvent déclencher des branches d’exception.

## 9) Démarche de construction (pas à pas)
1. Définir le **périmètre** et le **but** de l’activité (début/fin clairs).
2. Lister les **étapes majeures** (actions) dans l’ordre approximatif.
3. Identifier les **décisions** et les **conditions** (gardes).
4. Repérer les **flux d’objets** et objets clés.
5. Déterminer les **parallélismes** nécessaires et leurs **synchronisations**.
6. Introduire les **swimlanes** (qui exécute quoi).
7. Ajouter les **exceptions** (annulation, échec, délai).
8. Vérifier les **conditions de complétude** (toutes les branches mènent à une fin).
9. Simplifier, factoriser en **sous-activités** si le diagramme devient trop dense.
10. Faire valider par les parties prenantes (lecture de bout en bout).

## 10) Bonnes pratiques
- Préférer des actions **courtes et verbales**.
- Placer **une seule entrée** et **une seule sortie** par action (sauf nécessité).
- Gardes **visibles** et **testables**.
- Parallélisme: n’introduire que s’il apporte une valeur (performance, clarté).
- Limiter la **crossing** de flèches: réorganiser spatialement, utiliser des contours.
- Cohérence avec les autres diagrammes (cas d’utilisation, séquence, états).
- Documenter les hypothèses dans des **notes** (stéréotype «note»).

## 11) Erreurs fréquentes à éviter
- Oublier le **nœud final** ou confondre “Flow Final” et “Activity Final”.
- Branches de décision sans gardes, ou gardes ambiguës.
- Join/Fork mal appariés (désynchronisation).
- Utiliser les swimlanes pour “décorer” sans signification claire.
- Mélanger action et décision dans un même nœud.
- Créer des cycles sans condition d’arrêt explicite.

## 12) Mise en page et lisibilité
- Lecture de gauche à droite, puis haut vers bas.
- Alignements et espacements réguliers; grouper par sous-domaines.
- Libellés courts, police cohérente, contraste suffisant.
- Préférer des **connecteurs orthogonaux** (moins de croisements).
- Légende minimale si vous utilisez des conventions spécifiques.

## 13) Traçabilité et niveau de détail
- Chaque action doit tracer à au moins un **exigence** (fonctionnelle/non fonctionnelle) ou un **scénario**.
- Adapter le niveau de détail au public:
  - Direction/PO: vue macro, peu de gardes techniques.
  - Équipe technique: gardes précises, flux d’objet typés, exceptions.

## 14) Exemple textuel (mini-processus)
- Démarrer
- “Saisir identifiants”
- Décision: `[identifiants valides]` → “Charger profil”, sinon → “Afficher erreur” → revenir à “Saisir identifiants”
- Fork: “Charger préférences” || “Charger notifications”
- Join → “Afficher tableau de bord”
- Fin

## 15) Exemple diagramme d’Activités 


### 1) Éléments de base

![alt text](<images/atm_activity_examples-01 - Éléments de base — DAB Retrait.drawio.png>)

- Ce que ça montre: un flux simple depuis le nœud initial jusqu’au nœud final d’activité, avec des actions comme “Insérer carte”, “Saisir PIN”, “Choisir opération”, des transitions/flux de contrôle, une garde sur une décision ([PIN valide] / [PIN invalide]) et une fusion qui ramène vers la suite.
- À retenir: différence entre Activity Final (termine toute l’activité) et Flow Final (stoppe seulement un chemin), libellés d’actions au verbe, et usage des gardes sur les flèches sortantes du losange.

### 2) Parallélisme (Fork/Join)

![alt text](<images/atm_activity_examples-02 - Parallélisme — Comptes et Journal.drawio.png>)

- Ce que ça montre: après “Sélectionner Retrait”, un fork déclenche en parallèle “Préparer billets” et “Imprimer reçu” (ou “Actualiser journal”). Un join synchronise avant “Remettre billets et reçu”.
- À retenir: le fork 1→n démarre plusieurs branches simultanées; le join n→1 attend que toutes les branches parallèles soient terminées avant de continuer.

### 3) Flux d’objet (Object Flow)

![alt text](<images/atm_activity_examples-03 - Flux d’objet — Billets & Reçu.drawio.png>)

- Ce que ça montre: des nœuds d’objet comme Carte, PIN, RequêteRetrait, Billets, Reçu circulent entre actions (“Lire carte”, “Vérifier habilitation”, “Compter billets”). Les flèches d’objet véhiculent ces artefacts.
- À retenir: distinguer flux de contrôle (ordonnancement) et flux d’objet (transport de données); possibilité d’annoter un stéréotype «objectFlow» si souhaité.

### 4) Partitions / Swimlanes

![alt text](<images/atm_activity_examples-04 - Partitions — Client _ DAB _ Banque.drawio.png>)

- Ce que ça montre: l’activité répartie en couloirs “Client”, “ATM (IHM)”, “Contrôleur ATM”, “Système bancaire”. Les actions sont placées dans le couloir du rôle/système responsable, p.ex. “Saisir PIN” (Client), “Masquer saisie” (IHM), “Valider PIN” (Contrôleur), “Autoriser retrait” (Système bancaire).
- À retenir: les swimlanes clarifient qui fait quoi; les flux traversent les couloirs pour montrer les interactions entre rôles/systèmes.

### 5) Interruption / Exception

![alt text](<images/atm_activity_examples-05 - Interruption — Carte avalée.drawio.png>)

- Ce que ça montre: une Interruptible Activity Region autour de “Attendre saisie PIN” et “Valider PIN”. Un flux d’exception part d’un événement “Timeout” ou “Retrait carte par l’utilisateur” vers un Flow Final “Annuler opération” (ou vers “Éjecter carte”).
- À retenir: les régions interruptibles permettent de briser un sous-flux en cas d’exception; l’exception n’achève pas forcément toute l’activité (Flow Final vs Activity Final).

### 6) Signaux / Événements

![alt text](<images/atm_activity_examples-06 - Signal_Événement — Maintenance.drawio.png>)

- Ce que ça montre: envoi d’un signal “AlerteMaintenance” si le stock de billets est bas et réception d’un “SignalBlocage” venu du système bancaire en cas de carte suspecte. Les actions “Envoyer signal” / “Recevoir signal” matérialisent ces événements asynchrones.
- À retenir: les signaux décorrèlent l’émetteur et le récepteur; ils modélisent des interactions asynchrones entre l’ATM, la supervision et les systèmes tiers.

### 7) Sous-activité (Call Behavior Action)

![alt text](<images/atm_activity_examples-07 - Sous-activité — Appel d’activité.drawio.png>)

- Ce que ça montre: l’action “Traiter Retrait” est un Call Behavior Action qui invoque une activité détaillée ailleurs (par exemple la page 2 ou une autre définition) contenant validation, débit et délivrance. L’action d’appel a un petit symbole indiquant qu’elle référence une activité.
- À retenir: factoriser la complexité en appelant des activités réutilisables; soigner les paramètres d’entrée/sortie (p.ex. Montant, Compte, Statut) qui se connectent via des nœuds d’objet.


## 16) Check-list
- Périmètre clair (nœud initial/final présents).
- Décisions: gardes complètes + exclusives (+ “else” si utile).
- Parallélismes justifiés + joins correspondants.
- Flux d’objets identifiés pour les données importantes.
- Exceptions/timeouts modélisés si requis.
- Swimlanes cohérentes et limitées en nombre.
- Pas de croisements inutiles; lisibilité satisfaisante.
- Noms d’actions verbaux, concis et non ambigus.
- Cohérence avec cas d’utilisation et séquences.
- Taille maîtrisée: sous-activités si besoin.

## 17) Glossaire rapide
- Action: étape exécutable.
- Garde: condition booléenne sur une transition.
- Fork/Join: séparation/synchronisation parallèle.
- Swimlane: partition par rôle/système.
- Flow Final vs Activity Final: fin d’un flux vs fin de l’activité entière.
- Flux d’objet: transport de données entre actions.

