# Retour d'information sensible
 
### 1. Objectif
 
Garantir que le retour d'information classé comme sensible par la Société Nationale (SN) soit traité de manière sécurisée, cohérente et uniquement par des personnes autorisées désignées.
 
### 2. Définition
 
Le retour d'information sensible est une catégorie de retour d'information définie par la Société Nationale (SN), qui ne peut être traitée que par des personnes responsables spécifiquement désignées.
 
Le retour d'information sensible peut être classé de différentes manières, mais voici 2 distinctions principales à connaître, car le suivi sera effectué différemment :
 
- Violations du code de conduite (exemple : corruption/fraude/VBG commise par le personnel ou les volontaires de la Croix-Rouge)
- Retour d'information sensible lié à la situation personnelle de quelqu'un (exemple : santé, stigmatisation, violence domestique).

### 3. Rôles et responsabilités
 
- **Collecteur de retour d'information**
  - Enregistre le retour d'information dans Kobo.
  - Marque le retour d'information comme sensible, le cas échéant.
- **Superviseur du retour d'information**
  - Examine les retours d'information entrants.
  - Confirme si le retour d'information est sensible selon les définitions de la SN.
  - Assigne un point focal du retour d'information sensible désigné (voir ci-dessous).
  - Veille à ce que le suivi ait lieu.
  - Configurations du compte utilisateur.
- **Point focal du retour d'information sensible**
  - Gère le cas de bout en bout.
  - Veille à un suivi et à une documentation appropriés.
  - Met à jour le statut et clôture le cas.
  - Configurations du compte utilisateur.
- **Système (Kobo / EspoCRM)**
  - Définit automatiquement la priorité sur *Élevée* lorsque le retour d'information est marqué comme sensible.
  - Autorise automatiquement le superviseur du retour d'information à traiter les retours d'information sensibles (sur la base des rôles/autorisations définis par la SN).
  - Vérifie que toute personne assignée est autorisée à traiter les retours d'information sensibles.
  - Définit le statut du cas sur *En cours* lors de l'assignation.
  - Envoie des notifications et des rappels.

### 4. Procédure
 
#### Étape 1 : Collecte et enregistrement du retour d'information
 
- Le retour d'information est collecté et enregistré dans Kobo.
- Le cas échéant, le collecteur de retour d'information marque le retour d'information comme **sensible**.
- Si le retour d'information est marqué comme sensible, la plateforme automatiquement :
  - Définit sa priorité sur **Élevée**.
  - L'assigne au superviseur du retour d'information pour examen.

#### Étape 2 : Examen et validation
 
- Le superviseur du retour d'information :
  - Examine le retour d'information.
  - Confirme s'il répond à la définition de la SN d'un retour d'information sensible.
- Si **non sensible** :
  - Retirer le marquage sensible.
  - Réinitialiser la priorité.
  - Traiter selon les procédures standard de retour d'information.
- Si **sensible** :
  - Passer à l'étape 3.

#### Étape 3 : Assignation
 
- Le superviseur du retour d'information assigne le cas à un **point focal du retour d'information sensible** désigné.
- Le système définit le statut du cas sur **En cours**.

#### Étape 4 : Notification et suivi
 
- Le point focal du retour d'information sensible reçoit une notification par e-mail et via la Plateforme Régionale de Gestion des Retours d'Information.
- La plateforme lui envoie des rappels jusqu'à ce que le cas soit mis à jour.

#### Étape 5 : Traitement du cas
 
- Le point focal du retour d'information sensible :
  - Examine le cas.
  - Prend les mesures appropriées.
  - Suit les procédures opérationnelles standard internes pour le traitement des cas sensibles.
  - Partage le retour d'information en interne **si** nécessaire et autorisé.

#### Étape 6 : Mises à jour du statut
 
- Le point focal du retour d'information sensible met à jour le statut du cas à mesure que le travail progresse.

#### Étape 7 : Clôture
 
- Une fois le cas résolu :
  - Le point focal du retour d'information sensible marque le cas comme **clôturé**.
  - La clôture est confirmée dans l'aperçu de la plateforme.

### 5. Principes clés
 
- La Société Nationale définit ce qui constitue un retour d'information sensible.
- Seules les personnes autorisées peuvent traiter les retours d'information sensibles.
- Le retour d'information sensible est masqué pour tous les autres utilisateurs, sauf pour les utilisateurs autorisés.
- Tous les cas de retour d'information sensible sont traités comme **haute priorité**.
- Un suivi en temps utile est obligatoire et activement surveillé.

### 6. Risques
 
Le non-respect de cette POS peut entraîner :
 
- Des retards dans le traitement des retours d'information à haut risque.
- Des violations de la confidentialité ou des protocoles de protection.
 
### 7. Validation
 
- Le protocole doit être révisé d'ici la fin de 2026 pour s'assurer qu'il reste efficace.