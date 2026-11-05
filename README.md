# Description du projet

Développer une application en mode console permettant à un atelier de réparation de gérer ses clients, les appareils déposés, les réparations effectuées ainsi que les pièces détachées utilisées.

## Fonctionnalités

- Enregistrer de nouveaux clients.
- Enregistrer les appareils déposés par les clients.
- Créer des fiches de réparation.
- Affecter une réparation à un technicien.
- Modifier le statut d'une réparation.
- Ajouter les pièces détachées utilisées lors d'une réparation.
- Calculer automatiquement le coût total d'une réparation.
- Consulter les réparations terminées ou en attente.

## Structure de la base de données

| Table | Rôle |
|---|---|
| clients | Informations relatives aux clients |
| appareils | Informations sur les appareils déposés |
| techniciens | Informations sur les techniciens |
| reparations | Fiches de réparation |
| pieces | Catalogue des pièces détachées |
| pieces_reparation | Pièces utilisées lors des réparations |

### Rôle des différentes tables

- `reparations` = ce qu'il faut réparer.
- `pieces` = les pièces disponibles dans l'atelier.
- `pieces_reparation` = les pièces réellement utilisées pour chaque réparation.

---

## Table reparations

Cette table contient les informations générales sur chaque réparation.

Elle représente la fiche de réparation créée lorsqu'un client dépose un appareil.

### Exemple

| id | appareil_id | technicien_id | description | statut | main_oeuvre |
|---|---|---|---|---|---|
| 1 | 3 | 2 | Remplacement écran | En cours | 45 € |
| 2 | 5 | 1 | Problème batterie | Terminée | 30 € |

### Elle permet de savoir :

- Quel appareil doit être réparé.
- Quel technicien s'en occupe.
- Quel est le problème rencontré.
- Où en est la réparation.
- Combien coûte la main-d'œuvre.

**En résumé :** c'est la fiche qui décrit le travail à effectuer.

---

## Table pieces

Cette table contient le catalogue des pièces détachées disponibles dans l'atelier.

### Exemple

| id | nom | prix_unitaire | quantite_stock |
|---|---|---|---|
| 1 | Écran ordinateur 15 pouces | 120 € | 5 |
| 2 | Batterie ordinateur | 65 € | 10 |
| 3 | Disque SSD 500 Go | 55 € | 8 |
| 4 | Clavier ordinateur | 40 € | 3 |

### Elle permet de :

- Répertorier les pièces disponibles.
- Connaître leur prix.
- Connaître les quantités en stock.
- Modifier les informations d'une pièce.

---

## Table pieces_reparation

C'est probablement la table la moins évidente à comprendre.

Elle sert à faire le lien entre les réparations et les pièces utilisées.

La table `pieces_reparation` permet d'enregistrer quelles pièces ont été utilisées pour quelle réparation, et en quelle quantité.

### Exemple

| id | reparation_id | piece_id | quantite |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 1 | 4 | 1 |
| 3 | 2 | 2 | 1 |
| 4 | 2 | 3 | 1 |

### Cela signifie :

- Réparation 1 : un écran et un clavier ont été utilisés.
- Réparation 2 : une batterie et un disque SSD ont été utilisés.

---

## Exemple de calcul du coût d'une réparation

Prenons la réparation numéro 1 :

| Élément | Prix |
|---|---:|
| Main-d'œuvre | 45 € |
| Écran | 120 € |
| Clavier | 40 € |
| **Total** | **205 €** |

Le coût total est calculé automatiquement en additionnant :

- Le coût de la main-d'œuvre.
- Le prix de chaque pièce utilisée, multiplié par sa quantité.

**Formule :**

```text
Coût total = Main-d'œuvre + Somme(prix des pièces × quantités utilisées)

Coût total = 45 + (120 × 1) + (40 × 1)
Coût total = 205 €