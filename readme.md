# Exercice UML — Système de Gestion de Bibliothèque

## Démarche avec UML ?

- UML fournit un langage pour décrire besoins et solutions, mais ne dicte pas la démarche.
- Une méthode outillée par UML est typiquement:
  - pilotée par les cas d’utilisation (utilité pour l’utilisateur en premier),
  - centrée sur l’architecture (satisfaction des besoins, évolutivité, contraintes),
  - pragmatique (se concentrer sur le sous-ensemble UML réellement utile).
- [La démarche UML](demarche_uml.md)


## Contexte général
Vous allez modéliser un système de gestion de bibliothèque municipale afin de capturer les besoins métier et de produire un mini-dossier UML cohérent.  
Le travail s’effectue en groupes et s’étale sur deux séances. Les livrables sont des schémas réalisés avec draw.io et une courte description textuelle (en Markdown) intégrée à chaque partie.

## Livrables et format attendus

- Un fichier unique draw.io contenant plusieurs pages (onglets) :
  - `UC — Cas d’utilisation`
  - `CL — Diagramme de classes`
  - `ACT — Emprunter un livre (diagramme d’activités)`
  - `STATE — Cycle de vie Livre (diagramme d’états-transitions)`
  - `SEQ — Emprunter un livre (diagramme de séquence)`
- Le présent énoncé rempli (ce fichier Markdown) annoté par vos hypothèses majeures et les règles découvertes/choisies.
- Nommez le fichier draw.io: `bibliotheque_UML.drawio`.

## Introduction à l’exercice — Règles métier à découvrir pendant l’atelier
Votre objectif est de faire émerger (puis d’expliciter) les règles métier suivantes. Elles ne sont **pas** toutes figées : vous devez les préciser, les discuter et les justifier dans vos modèles et notes.

1) Adhésion et profils
- Un adhérent possède un identifiant, des coordonnées et un statut (ex. Étudiant, Adulte, Jeune).  
- Chaque statut peut imposer des **plafonds d’emprunt** (nombre d’ouvrages simultanés) et des **durées** (en jours) différentes.
- Un compte peut être **bloqué** en cas d’impayés, de retards répétés ou sur décision du bibliothécaire.

2) Fonds documentaire
- Un « Livre » est décrit par un ISBN, un titre, un ou plusieurs auteurs, une catégorie, et peut exister en **plusieurs exemplaires**.
- Certains ouvrages sont **non empruntables** (ex. « Référence »/consultation sur place).
- État d’un exemplaire: Disponible, Emprunté, Réservé, En réparation, Perdu.

3) Emprunts, retards et amendes
- Un emprunt est associé à un adhérent, un exemplaire, une **date de prêt** et une **date d’échéance**.
- Les retards génèrent des **pénalités** (amende/jour ou barème par palier). Les modalités exactes sont à définir.
- Les comptes **avec amende due** peuvent être temporairement bloqués pour de nouveaux emprunts.

4) Réservations et file d’attente
- Un adhérent peut **réserver** un titre indisponible.  
- Les réservations se gèrent en **file d’attente** FIFO par titre (et non par exemplaire).
- À la **disponibilité**, une **notification** est envoyée et une **fenêtre de retrait** limitée s’applique (à définir).

5) Renouvellements
- Un emprunt peut être **renouvelé** si aucune réservation en attente n’existe et si le **maximum de renouvellements** n’est pas atteint. Les limites (compteur, durée) sont à préciser.

6) Rôle du bibliothécaire
- Le bibliothécaire valide l’inscription, gère les pénalités, peut **enregistrer un retour**, **déclarer un exemplaire perdu** ou **envoyer en réparation**.
- Certains traitements peuvent être **automatisés** par le système (notifications, calcul des amendes), d’autres sont **manuels**.

7) Contraintes diverses
- Possibles **restrictions d’âge** pour certains contenus (à définir).  
- Les **rappels automatiques** (avant échéance) peuvent être envoyés.  
- Les **prêts inter-bibliothèques** sont hors périmètre, sauf si vous choisissez de les inclure en extension.

Indiquez clairement toute hypothèse ajoutée et justifiez-la.

---

## Séance 1 — Modéliser les fonctionnalités et la structure

### Partie A — Diagrammes de Cas d’Utilisation
- [Réaliser un diagramme de Cas d’Utilisation](use_case.md)
- Objectif: Identifier les acteurs et fonctions principales du système.
- Acteurs pressentis:
  - Adhérent (primaire)
  - Bibliothécaire (primaire/secondaire selon les cas)
  - Système de paiement (secondaire, optionnel)
  - Service de notification (secondaire)
- Tâches
  1. À partir des règles métier ci-dessus, **listez** les cas d’utilisation candidats (ex.: S’inscrire, Chercher un livre, Emprunter, Rendre, Réserver, Renouveler, Payer amende, Gérer catalogue, Gérer adhérents, Déclarer perdu, Envoyer en réparation).
  2. Construisez le **diagramme de cas d’utilisation** complet:
     - Utilisez les relations `<<include>>`, `<<extend>>` et la généralisation d’acteurs si pertinent.
     - Encadrez le **système** et placez les acteurs avec les bonnes associations.
  3. Pour 2 cas d’utilisation majeurs (« Emprunter un livre », « Réserver un livre »), rédigez une **description textuelle**:
     - Scénario nominal (pas-à-pas).
     - Règles/gardes (conditions), exceptions et alternatives (retard, exemplaire non disponible, compte bloqué, réservation en file d’attente, etc.).
- Livrable: Page `UC — Cas d’utilisation` dans le fichier draw.io + notes textuelles dans ce Markdown.

### Partie B — Diagramme de Classes
- [Réaliser un diagramme de Classes](class_diagram.md)
- Objectif: Modéliser le **domaine métier** (pas la conception technique).
- Concepts attendus (à adapter): Livre, Exemplaire, Auteur, Catégorie, Adhérent, Emprunt, Réservation, Pénalité/Amende, Notification, Bibliothécaire, RègleTarification (option), StatutAdhérent.
- Tâches
  1. Dérivez les **classes** à partir des cas d’utilisation et des règles: proposez les **attributs** clés (ex.: pour Emprunt: dateEmprunt, dateEcheance, nbRenouvellements).
  2. Spécifiez les **associations**, **multiplicités** et, si pertinent, **agrégations/compositions** (ex.: Livre 1..* Exemplaire).
  3. Faites figurer des **contraintes** (texte ou OCL libre) près des associations/attributs (ex.: « un exemplaire non empruntable ne peut pas être réservé » — si vous adoptez cette règle).
- Livrable: Page `CL — Diagramme de classes` dans draw.io.

---

## Séance 2 — Modélisation du comportement et des interactions

### Partie C — Diagramme d’Activités
- [Réaliser un diagramme d’Activités](activity_diagram.md)
- Mise en situation: Détailler le processus « Emprunter un livre » de bout en bout.
- Tâches
  1. Utilisez des **partitions (swimlanes)** pour « Adhérent », « Bibliothécaire », « Système ».
  2. Modélisez: recherche, vérification d’éligibilité (compte non bloqué, quotas), sélection d’un exemplaire, enregistrement de l’emprunt, mise à jour du stock, envoi d’accusé/notification.
  3. Ajoutez des **décisions/fusions** pour les alternatives: compte bloqué, aucun exemplaire disponible, réservation en attente, etc.
- Livrable: Page `ACT — Emprunter un livre`.

### Partie D — Diagramme d’États-Transitions
- [Réaliser un diagramme d’États-Transitions](state_diagram.md)
- Objet cible: l’**Exemplaire de livre** (ou « LivreExemplaire »).
- États candidats: Disponible → Réservé → Emprunté → (Retourné →) Disponible; transitions vers En réparation; transition terminale Perdu.  
- Tâches
  1. Définissez les **événements** (emprunter(), rendre(), réserver(), annulerReservation(), déclarerPerdu(), envoyerEnReparation(), réparer()).
  2. Indiquez les **gardes** (ex.: [compte éligible], [pas de réservation prioritaire]) et **actions** (ex.: incrémenter compteur d’emprunts, notifier suivant de la file).
- Livrable: Page `STATE — Cycle de vie Livre`.

### Partie E — Diagramme de Séquence
- [Réaliser un diagramme de Séquence](sequence_diagram.md)
- Scénario: « Emprunter un livre ».
- Tâches
  1. Identifiez les **lignes de vie**: Adhérent, InterfaceBibliothèque, ServiceEmprunts, RépertoireExemplaires, ServiceNotifications (adapter selon votre modèle).
  2. Tracez les **messages** synchrones/asynchrones, fragments (alt/loop) pour gérer les alternatives (compte bloqué, aucun exemplaire).
  3. Assurez la **cohérence** avec le diagramme d’activités et les règles métier.
- Livrable: Page `SEQ — Emprunter un livre`.  
- Synthèse: Vérifiez l’alignement entre:
  - Cas d’utilisation (le quoi),
  - Classes (le qui),
  - Activités/États/Séquence (le comment).

---

## Critères de qualité
- Pertinence et complétude des cas d’utilisation (+ relations)
- Qualité du diagramme de classes (attributs, multiplicités, contraintes)
- Clarté des comportements (activités, états, séquence)
- Cohérence inter-diagrammes et explicitation des hypothèses/règles
- Lisibilité, nomenclature, et respect des consignes

---

## Aide — Questions de cadrage à vous poser
- Quelles données minimales pour un Emprunt ? Quelles règles pour l’échéance et le renouvellement ?
- Quelles conditions exactes pour bloquer/débloquer un compte ?
- Une réservation porte-t-elle sur un **titre** ou un **exemplaire** ? Que se passe-t-il si la fenêtre de retrait expire ?
- Quelles notifications et à quels instants (création emprunt, rappel avant échéance, disponibilité réservation) ?
- Quels cas sont en `<<include>>` ou `<<extend>>` (ex.: « Payer amende » étend « Rendre un livre » en cas de retard) ?

