# [TEST] Retour d'information sensible
 
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
- **Gestionnaire de retour d'information**
  - Examine les retours d'information entrants.
  - Confirme si le retour d'information est sensible selon les définitions de la SN.
  - Assigne un gestionnaire désigné du retour d'information sensible.
  - Veille à ce que le suivi ait lieu.
  - Configurations du compte utilisateur : *[captures d'écran : paramètres de rôle/autorisation]*
- **Créateur et éditeur de retour d'information (Personne autorisée – Gestionnaire du retour d'information sensible)**
  - Gère le cas de bout en bout.
  - Veille à un suivi et à une documentation appropriés.
  - Met à jour le statut et clôture le cas.
  - Configurations du compte utilisateur : *[captures d'écran : paramètres de rôle/autorisation]*
- **Système (Kobo / EspoCRM)**
  - Définit automatiquement la priorité sur *Élevée* lorsque le retour d'information est marqué comme sensible.
  - Autorise automatiquement les gestionnaires de retour d'information à traiter les retours d'information sensibles (sur la base des rôles/autorisations définis par la SN).
  - Vérifie que toute personne assignée est autorisée à traiter les retours d'information sensibles.
  - Définit le statut du cas sur *En cours* lors de l'assignation.
  - Envoie des notifications et des rappels.

### 4. Procédure
 
#### Étape 1 : Collecte et enregistrement du retour d'information
 
- Le retour d'information est collecté et enregistré dans Kobo.
- Le cas échéant, le collecteur de retour d'information marque le retour d'information comme **sensible**.
- S'il n'est pas connu si le retour d'information est sensible, laisser vide.

#### Étape 2 : Actions automatiques du système
 
- Le système :
  - Définit la priorité sur **Élevée**.
  - Achemine le retour d'information pour examen.

#### Étape 3 : Examen et validation
 
- Le gestionnaire de retour d'information :
  - Examine le retour d'information.
  - Confirme s'il répond à la définition de la SN d'un retour d'information sensible.
- Si **non sensible** :
  - Retirer le marquage sensible.
  - Réinitialiser la priorité.
  - Traiter selon les procédures standard de retour d'information.
- Si **sensible** :
  - Passer à l'étape 4.

#### Étape 4 : Assignation
 
- Le gestionnaire de retour d'information assigne le cas à un **gestionnaire désigné du retour d'information sensible**.
- Le système définit le statut du cas sur **En cours**.

#### Étape 5 : Notification et suivi
 
- Le gestionnaire du retour d'information sensible assigné :
  - Reçoit une notification par e-mail et dans EspoCRM.
- Le système :
  - Envoie des rappels quotidiens jusqu'à ce que le cas soit mis à jour.

#### Étape 6 : Traitement du cas
 
- Le gestionnaire du retour d'information sensible :
  - Examine le cas.
  - Prend les mesures appropriées.
  - Suit les procédures opérationnelles standard internes pour le traitement des cas sensibles.
  - Partage le retour d'information en interne **si** nécessaire et autorisé.

#### Étape 7 : Mises à jour du statut
 
- Le gestionnaire du retour d'information sensible met à jour le statut du cas à mesure que le travail progresse.

#### Étape 8 : Clôture
 
- Une fois le cas résolu :
  - Le gestionnaire du retour d'information sensible marque le cas comme **clôturé**.
  - La clôture est confirmée dans le système d'aperçu.

### 5. Principes clés
 
- La Société Nationale définit ce qui constitue un retour d'information sensible.
- Seules les personnes autorisées peuvent traiter les retours d'information sensibles.
- Le retour d'information sensible est masqué pour tous les autres utilisateurs, sauf pour les utilisateurs autorisés.
- Tous les cas de retour d'information sensible sont traités comme **haute priorité**.
- Un suivi en temps utile est obligatoire et activement surveillé.

### 6. Risques
 
Le non-respect de cette POS peut entraîner :
 
- Des retards dans le traitement des retours d'information à haut risque.
- Des violations de la confidentialité ou des protocoles de sauvegarde.

### 7. Visuel du flux de travail
 
![Flux de travail du retour d'information sensible](../../assets/sensitive-feedback-flow.png)
 
### 8. Validation
 
- Le protocole doit être révisé d'ici la fin de 2026 pour s'assurer qu'il reste efficace.