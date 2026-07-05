# [TEST] Rôles et permissions

### Objectif

Documenter les rôles et permissions des utilisateurs est essentiel pour garantir la clarté, la sécurité et la responsabilité au sein de la Plateforme de Gestion des Retours d'Information. Cela aidera à comprendre qui peut accéder à des sections spécifiques de la plateforme et de ses données, les modifier ou les gérer. Cela réduira le risque de mauvaise configuration, d'accès non autorisé et d'erreurs opérationnelles. Cela facilite également l'intégration, l'audit et la conformité en fournissant une référence fiable sur le comportement du système. 

Un aperçu plus détaillé de la gestion des rôles est disponible dans la [documentation officielle d'EspoCRM](https://docs.espocrm.com/administration/roles-management/). 

### Accéder à la Plateforme de Gestion des Retours d'Information

Les Sociétés Nationales ont la possibilité d'accéder à la Plateforme de Gestion des Retours d'Information. Comme il s'agit d'une plateforme partagée, chaque Société Nationale est affectée à une Équipe, ce qui lui permet d'accéder **UNIQUEMENT** à ses données de retour d'information et à ses visualisations.

Au sein de la structure d'Équipe par Société Nationale, plusieurs utilisateurs de la Société Nationale peuvent être liés à l'Équipe correspondante pour y accéder. Selon les rôles et permissions spécifiques de l'utilisateur, celui-ci peut créer, lire, modifier et/ou supprimer des données de retour d'information.

### Rôles de la Société Nationale

#### Superviseur des retours d'information

Ce rôle est désigné pour le point focal CEA de la SN au siège. Cette personne supervisera, suivra et traitera les retours d'information reçus et fournis à la communauté. Elle est la principale personne de contact pour la SN en cas de problème avec la plateforme.

Ce qu'il peut faire dans la plateforme :

- Lire, créer, modifier, supprimer des enregistrements de retour d'information
  - Exemple : supprimer des enregistrements de retour d'information après l'intégration du personnel et des volontaires, afin de retirer les entrées de test de la plateforme
  - Remarque : en dehors des entrées de test, il n'est pas recommandé de supprimer des données de retour d'information
- Créer ou supprimer des utilisateurs via l'entité "User Access Requests"
- Affecter des utilisateurs au suivi d'enregistrements de retour d'information spécifiques
- Assurer le suivi dans le flux avec d'autres collègues
- Lire les rapports
- Autorisé pour les enregistrements de retour d'information sensibles
  - Peut lire, modifier, affecter des utilisateurs et assurer le suivi des retours d'information sensibles

#### Point focal des retours d'information

Ce rôle est désigné pour les membres de la SN (par ex., CEA, PMER, IM, branches, opérateurs de hotline) qui traiteront les retours d'information saisis dans la Plateforme de Gestion des Retours d'Information. 

Ce qu'il peut faire dans la plateforme :

- Lire, créer, modifier des enregistrements de retour d'information
- Affecter des utilisateurs au suivi d'enregistrements de retour d'information spécifiques (si les utilisateurs sont connus)
- Assurer le suivi des enregistrements de retour d'information
- Assurer le suivi dans le flux avec d'autres collègues
- Lire les rapports


#### Gestionnaire des retours d'information

Ce rôle est désigné pour les membres de la SN (par ex., points focaux CVA, Santé, Abris) qui traiteront ou verront uniquement des retours d'information spécifiques.

Ce qu'il peut faire dans la plateforme :

- Lire et modifier les enregistrements de retour d'information qui lui sont attribués
- Assurer le suivi des enregistrements de retour d'information qui lui sont attribués
- Assurer le suivi dans le flux avec d'autres collègues
- Lire les rapports


#### Point focal des retours d'information sensibles

Ce rôle est désigné pour le point focal de la SN (par ex., point focal PGI) qui traitera les retours d'information sensibles. Lorsqu'un enregistrement de retour d'information est marqué comme sensible, SEULS les utilisateurs ayant ce rôle et les Superviseurs des retours d'information pourront accéder à l'enregistrement de retour d'information, le consulter et le modifier.

Ce qu'il peut faire dans la plateforme :

- Lire et modifier les enregistrements de retour d'information sensibles
- Assurer le suivi et clôturer les enregistrements de retour d'information sensibles
- Lire les rapports


#### Lecteur des rapports de retours d'information

Ce rôle est désigné pour les utilisateurs de la SN qui ont besoin d'une vue d'ensemble de haut niveau des retours d'information. Le Lecteur des rapports de retours d'information, par exemple, peut être une personne de l'équipe PMER qui a besoin de données pour les rapports ou le Secrétaire général qui souhaite avoir une vue d'ensemble du travail. Ils ne peuvent PAS voir d'informations personnellement identifiables dans l'enregistrement de retour d'information.

Ce qu'il peut faire dans la plateforme :

- Accès au tableau de bord pour le reporting
- Accès de haut niveau aux enregistrements de retour d'information sans PII