# [TEST] Rôles et permissions

### Objectif

Documenter les rôles et permissions des utilisateurs est essentiel pour garantir la clarté, la sécurité et la responsabilité au sein de la plateforme de gestion des retours d’information. Cela aidera à comprendre qui peut accéder, modifier ou gérer des sections spécifiques de la plateforme et de ses données. Cela réduira le risque de mauvaise configuration, d’accès non autorisé et d’erreurs opérationnelles. Cela soutient également l’intégration, l’audit et la conformité en fournissant une référence fiable sur le comportement du système. 

Un aperçu plus détaillé de la gestion des rôles est disponible dans la [documentation officielle d’EspoCRM](https://docs.espocrm.com/administration/roles-management/). 

### Accéder à la plateforme de gestion des retours d’information

Les Sociétés nationales ont la possibilité d’accéder à la plateforme de gestion des retours d’information. Comme il s’agit d’une plateforme partagée, chaque Société nationale est affectée à une équipe, ce qui lui permet d’accéder **UNIQUEMENT** à ses propres données de retour d’information et visualisations.

Au sein de la structure d’équipe par Société nationale, plusieurs utilisateurs de la Société nationale peuvent être liés à l’équipe correspondante pour y accéder. Selon les rôles et permissions spécifiques de l’utilisateur, celui-ci peut créer, lire, modifier et/ou supprimer des données de retour d’information.

### Rôles des Sociétés nationales

#### Superviseur des retours d’information

Ce rôle est désigné pour le point focal CEA de la SN au siège. Cette personne supervisera, suivra et traitera les retours d’information reçus et fournis à la communauté. Elle est la principale personne de contact pour la SN en cas de problème avec la plateforme.

Ce qu’elle peut faire sur la plateforme :

- Lire, créer, modifier, supprimer des enregistrements de retour d’information
  - Exemple : supprimer des enregistrements de retour d’information après l’intégration du personnel et des volontaires, afin de retirer les entrées de test de la plateforme
  - Remarque : en dehors des entrées de test, il n’est pas recommandé de supprimer des données de retour d’information
- Créer ou supprimer des utilisateurs via l’entité "User Access Requests"
- Affecter des utilisateurs au suivi d’enregistrements spécifiques de retour d’information
- Assurer le suivi dans le flux avec d’autres collègues
- Lire les rapports
- Autorisé pour les enregistrements de retour d’information sensibles
  - Peut lire, modifier, affecter des utilisateurs et assurer le suivi des retours d’information sensibles

#### Point focal des retours d’information

Ce rôle est désigné pour les membres de la SN (par ex., CEA, PMER, IM, branches, opérateurs de hotline) qui traiteront les retours d’information saisis dans la plateforme de gestion des retours d’information. 

Ce qu’ils peuvent faire sur la plateforme :

- Lire, créer, modifier des enregistrements de retour d’information
- Affecter des utilisateurs au suivi d’enregistrements spécifiques de retour d’information (si les utilisateurs sont connus)
- Assurer le suivi des enregistrements de retour d’information
- Assurer le suivi dans le flux avec d’autres collègues
- Lire les rapports


#### Gestionnaire des retours d’information

Ce rôle est désigné pour les membres de la SN (par ex., points focaux CVA, Santé, Abris) qui traiteront ou verront uniquement des retours d’information spécifiques.

Ce qu’ils peuvent faire sur la plateforme :

- Lire et modifier les enregistrements de retour d’information qui leur sont attribués
- Assurer le suivi des enregistrements de retour d’information qui leur sont attribués
- Assurer le suivi dans le flux avec d’autres collègues
- Lire les rapports


#### Point focal des retours d’information sensibles

Ce rôle est désigné pour le point focal de la SN (par ex., point focal PGI) qui traitera les retours d’information sensibles. Lorsqu’un enregistrement de retour d’information est marqué comme sensible, SEULS les utilisateurs ayant ce rôle et les superviseurs des retours d’information pourront accéder à l’enregistrement, le consulter et le modifier.

Ce qu’ils peuvent faire sur la plateforme :

- Lire et modifier les enregistrements de retour d’information sensibles
- Assurer le suivi et clôturer les enregistrements de retour d’information sensibles
- Lire les rapports


#### Lecteur de rapports sur les retours d’information

Ce rôle est désigné pour les utilisateurs de la SN qui ont besoin d’une vue d’ensemble de haut niveau des retours d’information. Le lecteur de rapports sur les retours d’information, par exemple, pourrait être une personne de l’équipe PMER ayant besoin de données pour les rapports, ou le Secrétaire général souhaitant avoir une vue d’ensemble du travail. Ils ne peuvent PAS voir d’informations personnellement identifiables dans l’enregistrement de retour d’information.

Ce qu’ils peuvent faire sur la plateforme :

- Accès au tableau de bord pour le reporting
- Accès de haut niveau aux enregistrements de retour d’information sans PII