# [TEST] Retour d’information sensible
 
### 1. Objectif
 
Garantir que les retours d’information classés comme sensibles par la Société nationale (SN) soient traités de manière sécurisée, cohérente et uniquement par des personnes autorisées désignées.
 
### 2. Définition
 
Le retour d’information sensible est une catégorie de retour d’information définie par la Société nationale (SN), qui ne peut être traitée que par des personnes responsables spécifiquement désignées.
 
Les retours d’information sensibles peuvent être classés de différentes manières, mais voici 2 distinctions principales à connaître, car le suivi sera effectué différemment :
 
- Violations du code de conduite (exemple : corruption/fraude/VBG commise par le personnel ou les volontaires de la Croix-Rouge)
- Retour d’information sensible à la situation personnelle de quelqu’un (exemple : santé, stigmatisation, violence domestique).

### 3. Rôles et responsabilités
 
- **Collecteur de retours d’information**
  - Enregistre les retours d’information dans Kobo.
  - Signale les retours d’information comme sensibles, le cas échéant.
- **Gestionnaire des retours d’information**
  - Examine les retours d’information entrants.
  - Confirme si le retour d’information est sensible selon les définitions de la SN.
  - Assigne un gestionnaire désigné des retours d’information sensibles.
  - Veille à ce qu’un suivi ait lieu.
  - Configurations du compte utilisateur : *[captures d’écran : paramètres de rôle/autorisation]*
- **Créateur et éditeur de retours d’information (Personne autorisée – Gestionnaire des retours d’information sensibles)**
  - Gère le cas de bout en bout.
  - Veille à un suivi et à une documentation appropriés.
  - Met à jour le statut et clôture le cas.
  - Configurations du compte utilisateur : *[captures d’écran : paramètres de rôle/autorisation]*
- **Système (Kobo / EspoCRM)**
  - Définit automatiquement la priorité sur *High* lorsque le retour d’information est marqué comme sensible.
  - Autorise automatiquement les gestionnaires des retours d’information à traiter les retours d’information sensibles (sur la base des rôles/autorisations définis par la SN).
  - Vérifie que toute personne assignée est autorisée à traiter des retours d’information sensibles.
  - Définit le statut du cas sur *In Progress* lors de l’assignation.
  - Envoie des notifications et des rappels.

### 4. Procédure
 
#### Étape 1 : Collecte et enregistrement des retours d’information
 
- Les retours d’information sont collectés et enregistrés dans Kobo.
- Le cas échéant, le collecteur de retours d’information marque le retour d’information comme **sensible**.
- S’il n’est pas connu si le retour d’information est sensible, laisser vide.

#### Étape 2 : Actions automatiques du système
 
- Le système automatiquement :
  - Définit la priorité sur **High**.
  - Achemine le retour d’information pour examen.

#### Étape 3 : Examen et validation
 
- Le gestionnaire des retours d’information :
  - Examine le retour d’information.
  - Confirme s’il répond à la définition de la SN d’un retour d’information sensible.
- Si **non sensible** :
  - Retirer le marquage sensible.
  - Réinitialiser la priorité.
  - Traiter conformément aux procédures standard de retour d’information.
- Si **sensible** :
  - Passer à l’étape 4.

#### Étape 4 : Assignation
 
- Le gestionnaire des retours d’information assigne le cas à un **gestionnaire désigné des retours d’information sensibles**.
- Le système définit le statut du cas sur **In Progress**.

#### Étape 5 : Notification et suivi
 
- Le gestionnaire des retours d’information sensibles assigné :
  - Reçoit une notification par e-mail et via EspoCRM.
- Le système :
  - Envoie des rappels quotidiens jusqu’à ce que le cas soit mis à jour.

#### Étape 6 : Traitement du cas
 
- Le gestionnaire des retours d’information sensibles :
  - Examine le cas.
  - Prend les mesures appropriées.
  - Suit les procédures opérationnelles standard internes pour le traitement des cas sensibles.
  - Partage le retour d’information en interne **si** requis et autorisé.

#### Étape 7 : Mises à jour du statut
 
- Le gestionnaire des retours d’information sensibles met à jour le statut du cas à mesure que le travail progresse.

#### Étape 8 : Clôture
 
- Une fois le cas résolu :
  - Le gestionnaire des retours d’information sensibles marque le cas comme **closed**.
  - La clôture est confirmée dans le système d’aperçu.

### 5. Principes clés
 
- La Société nationale définit ce qui constitue un retour d’information sensible.
- Seules les personnes autorisées peuvent traiter les retours d’information sensibles.
- Les retours d’information sensibles sont masqués pour tous les autres utilisateurs, sauf les utilisateurs autorisés.
- Tous les cas de retours d’information sensibles sont traités comme **high priority**.
- Un suivi en temps utile est obligatoire et activement contrôlé.

### 6. Risques
 
Le non-respect de cette SOP peut entraîner :
 
- Des retards dans le traitement des retours d’information à haut risque.
- Des violations de la confidentialité ou des protocoles de sauvegarde.

### 7. Visuel du flux de travail
 
![Flux de travail des retours d’information sensibles](../../assets/sensitive-feedback-flow.png)
 
### 8. Validation
 
- Le protocole doit être révisé d’ici la fin de 2026 pour s’assurer qu’il reste efficace.