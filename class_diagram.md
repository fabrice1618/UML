# Diagramme de classes (UML)

## Objectifs du cours
- Comprendre le rôle du diagramme de classes dans la modélisation orientée objet.
- Savoir lire, concevoir et documenter un diagramme de classes conforme à l’UML.
- Maîtriser les principaux éléments (classes, attributs, opérations) et relations (association, agrégation, composition, héritage, dépendance, réalisation).
- Appliquer les bonnes pratiques de nommage, de structuration et de présentation.

---

## 1) Rappel: où s’inscrit le diagramme de classes dans l’UML ?
Le diagramme de classes fait partie des diagrammes structurels de l’UML. Il décrit la structure statique du système:
- Concepts métier (classes), caractéristiques (attributs), comportements (opérations/méthodes).
- Relations entre concepts (associations, généralisations, compositions, etc.).
- Contrats (interfaces), types simples (énumérations, types primitifs).
Il sert de base à l’implémentation (modèle de domaine, modèles objets) et complète les diagrammes comportementaux (cas d’utilisation, séquences, états, activités).

---

## 2) Éléments de base

### 2.1 Classe
Représentée par un rectangle en 1 à 3 compartiments:
- Nom de la classe (obligatoire).
- Attributs (facultatif).
- Opérations (facultatif).

Exemple (notation textuelle):
- Classe: `Client`
- Attributs: `+id: UUID`, `+nom: String`, `+email: String [0..1]`
- Opérations: `+changerEmail(nouveau: String): void`

### 2.2 Visibilité
- `+` public: accessible partout.
- `#` protégé: accessible par la classe et ses sous-classes.
- `-` privé: accessible uniquement par la classe.
- `~` package: accessible au sein du même paquetage.

### 2.3 Attributs
- Syntaxe: `visibilité nom: Type multiplicité = valeurParDéfaut {propriétés}`
- Propriétés fréquentes: `{readOnly}`, `{static}`, `{derived}`.
- Attribut dérivé: précédé d’un `/`, p.ex. `/age: int`.

### 2.4 Opérations (méthodes)
- Syntaxe: `visibilité nom(param1: Type, param2: Type = défaut): TypeRetour {propriétés}`
- Modificateurs fréquents: `{abstract}`, `{static}`, `{query}`.

### 2.5 Types et stéréotypes
- Types primitifs (String, int, boolean...), types valeur (Money, Date), énumérations, classes, interfaces.
- Stéréotypes (entre guillemets français « » ou anglais « »): p.ex. «entity», «service», «valueObject».

---

## 3) Relations entre classes

### 3.1 Association
- Lien structurel entre classes; peut être nommée et orientée.
- Multiplicités aux extrémités: `0..1`, `1`, `0..*`, `1..*`, `1..5`, `*` (non borné).
- Rôles: nom des extrémités (p.ex. `client`, `commandes`).
- Navigabilité: flèche ouverte vers la cible si unidirectionnelle.

Exemple: `Client 1 ---- 0..* Commande` (rôle côté Commande: `commandes`)

### 3.2 Agrégation (losange vide)
- Relation «partie-tout» faible (les parties peuvent exister sans le tout).
- Notation: losange blanc côté agrégat.

### 3.3 Composition (losange plein)
- Relation «partie-tout» forte (cycle de vie des parties lié au tout).
- Notation: losange noir côté composite.
- Règle: une partie n’a qu’un composite à la fois et n’existe pas sans lui.

### 3.4 Généralisation / Héritage
- Flèche triangle blanc vers la super-classe.
- Une sous-classe hérite attributs/opérations et peut ajouter/affiner.

### 3.5 Réalisation (classe -> interface)
- Triangle blanc en pointillé, de la classe concrète vers l’interface.

### 3.6 Dépendance
- Lien ponctillé avec flèche ouverte: une modification de la cible peut impacter la source (utilisation, paramètre, retour, création).

---

## 4) Multiplicités et contraintes

### Multiplicités courantes
- `0..1` (optionnel), `1` (obligatoire et unique), `0..*` ou `*` (liste), `1..*` (au moins un).

### Contraintes OCL (en option)
- Exemples: `{ordered}`, `{unique}`, `{subset}`, `{redefines}`, `{xor}`.
- OCL (Object Constraint Language) permet d’exprimer des invariants: `context Panier inv totalPositif: self.total >= 0`.

---

## 5) Interfaces, classes abstraites, énumérations

- Interface: nom en italique ou stéréotype «interface»; ne contient que des opérations.
- Classe abstraite: nom en italique; opérations éventuellement abstraites.
- Énumération: mot-clé `enumeration` ou stéréotype «enumeration»; liste de littéraux.

Exemple (texte):
- `<<interface>> MoyenPaiement` avec `payer(montant: Money): Reçu`
- `CarteBancaire` réalise `MoyenPaiement`
- `enumeration StatutCommande { Brouillon, Validée, Expédiée, Livrée }`

---

## 6) Nommage et style

- Noms de classes: singulier, PascalCase (ex: `AdressePostale`).
- Attributs/paramètres: camelCase (ex: `dateLivraison`).
- Opérations: verbe à l’infinitif (ex: `valider()`, `calculerTotal()`).
- Rôles d’association clairs (ex: `lignes`, `client`).
- Éviter les abréviations obscures; préférer des noms du domaine.

---

## 7) Démarche de conception (pas à pas)

1. Recueillir le vocabulaire métier (glossaire).
2. Identifier les concepts candidats (classes) à partir des cas d’utilisation et récits utilisateurs.
3. Définir attributs essentiels (types, nullabilité, dérivés).
4. Poser les relations et multiplicités; choisir composition vs agrégation selon le cycle de vie.
5. Factoriser via héritage où cela apporte une véritable généralisation.
6. Introduire des interfaces pour séparer contrat et implémentations.
7. Ajouter contraintes (unicité, ordre, invariants) si utile.
8. Vérifier cohérence avec scénarios (diagrammes de séquence) et règles métier.
9. Soigner la lisibilité (paquetages, alignements, noms, éviter les croisements).
10. Revue avec les parties prenantes; itérations courtes.

---

## 8) Bonnes pratiques

- Privilégier la composition pour représenter la possession forte (cycle de vie lié).
- Limiter l’héritage profond; préférer la délégation si la hiérarchie n’est pas stable.
- Éviter les classes «dieu» (trop de responsabilités); appliquer SOLID (SRP surtout).
- Une association doit avoir un sens dans le domaine; éviter les liens superflus.
- Définir explicitement les multiplicités et navigabilités.
- Documenter les attributs sensibles (unités, devise, timezone).
- Isoler les types valeur (Money, Quantité, Pourcentage) pour clarifier l’API.

---

## 9) Erreurs fréquentes

- Oublier les multiplicités (suppositions implicites).
- Confondre agrégation et association simple (l’agrégation n’ajoute souvent rien de plus — à utiliser avec parcimonie).
- Abuser de l’héritage pour du simple partage de code (préférer composition).
- Mélanger modèle de persistance et modèle métier (laisser la technique hors du diagramme conceptuel).
- Noms ambigus, incohérents ou pluriels pour des classes.
- Relations non navigables là où l’implémentation le nécessite (ou l’inverse).

---

## 10) Mise en page et lisibilité

- Grouper par paquetage (rectangles englobants) pour des sous-domaines.
- Placer les classes au centre de gravité de leurs relations.
- Minimiser les croisements de liens; utiliser des orthogonales si besoin.
- Éviter les polices trop petites; rester cohérent sur les icônes et stéréotypes.
- Ajouter des notes UML (coin replié) pour préciser des règles.

---

## 11) Exemple illustratif (notation textuelle + Mermaid)

Exemple textuel (simplifié — e-commerce):
- `Client` 1 — 0..* `Commande`
- `Commande` 1 — 1..* `LigneDeCommande` (composition)
- `Commande` — 1 `AdresseLivraison`
- `Commande` — 1 `AdresseFacturation`
- `MoyenPaiement` (interface) réalisée par `CarteBancaire`, `Portefeuille`
- `StatutCommande` (énumération): Brouillon, Validée, Expédiée, Livrée

Exemple Mermaid (rendu Markdown possible dans certains outils):

```mermaid
classDiagram
    class Client {
      +id: UUID
      +nom: String
      +email: String [0..1]
      +changerEmail(nouveau: String): void
    }

    class Commande {
      +numero: String
      +dateCreation: Date
      +total: Money
      +valider(): void
      +calculerTotal(): Money
    }

    class LigneDeCommande {
      +libelle: String
      +quantite: int
      +prixUnitaire: Money
      +sousTotal(): Money
    }

    class Adresse {
      +rue: String
      +ville: String
      +codePostal: String
      +pays: String
    }

    class AdresseLivraison
    class AdresseFacturation
    AdresseLivraison --|> Adresse
    AdresseFacturation --|> Adresse

    class MoyenPaiement
    <<interface>> MoyenPaiement
    class CarteBancaire
    class Portefeuille
    CarteBancaire ..|> MoyenPaiement
    Portefeuille ..|> MoyenPaiement

    class StatutCommande {
      <<enumeration>>
      Brouillon
      Validee
      Expediee
      Livree
    }

    Client "1" -- "0..*" Commande : commandes
    Commande "1" *-- "1..*" LigneDeCommande : lignes
    Commande "1" -- "1" AdresseLivraison : livraison
    Commande "1" -- "1" AdresseFacturation : facturation
```

---

## 12) Check-list de relecture

- Chaque classe a-t-elle un nom métier clair et singulier ?
- Les attributs critiques ont-ils type, nullabilité et unités précisés ?
- Les multiplicités et navigabilités sont-elles explicites sur chaque association ?
- Les compositions sont-elles justifiées par le cycle de vie ?
- Les interfaces expriment-elles des contrats stables ?
- Le diagramme est-il lisible (peu de croisements, regroupement par paquetages) ?
- Concordance avec cas d’utilisation et scénarios ?

---

## 13) Glossaire rapide

- Association: lien structurel entre classes.
- Agrégation: relation partie-tout faible (losange vide).
- Composition: relation partie-tout forte (losange plein, cycle de vie lié).
- Généralisation: héritage (triangle blanc).
- Réalisation: implémentation d’interface (lien en pointillé).
- Multiplicité: cardinalité à une extrémité d’association (ex: `0..*`).
- Navigabilité: direction de lecture/utilisation de l’association.

---

## 14) Pour approfondir
- Spécification UML (OMG): structure et sémantique des diagrammes.
- OCL (Object Constraint Language) pour exprimer des invariants.
- Bonnes pratiques DDD (Domain-Driven Design) pour structurer le modèle.
