# [TEST] Cadre de responsabilité des données
 
### Objectif
 
Ce document fournit un aperçu clair des responsabilités en matière de données pour les Sociétés nationales (NS) participant à la Plateforme régionale de gestion des retours d’information. Il définit qui est responsable des données, comment elles sont traitées et quelles obligations chaque rôle implique.
 
### Aperçu de la plateforme
 
- **Plateforme :** Plateforme régionale de gestion des retours d’information (EspoCRM) et KoboToolbox.
- **Exploitée par :** Croix-Rouge néerlandaise (NLRC).
- **NS concernées :** Toute Société nationale formellement intégrée à la Plateforme régionale de gestion des retours d’information.
- **Objectif :** Collecter, gérer et assurer le suivi des retours d’information communautaires soumis à la NS via des formulaires numériques (KoboToolbox) ou une saisie directe (EspoCRM).
- **Séparation des données :** Chaque NS est affectée à une équipe au sein de la Plateforme régionale de gestion des retours d’information, garantissant que le personnel ne peut accéder qu’aux retours d’information liés à sa propre NS.
- **Marqueur sensible :** Les retours d’information peuvent être marqués comme sensibles, limitant l’accès aux seuls rôles autorisés.

### Rôles et responsabilités relatifs aux données
 
| Role | Who | Key Responsibilities | Access in EspoCRM |
|------|-----|----------------------|-------------------|
| **Responsable du traitement** | NS participante | • Détermine la finalité et les moyens du traitement<br>• Garantit la base légale de la collecte des données<br>• Responsable des droits des personnes concernées<br>• Initie et signe un accord de partage des données avec la NLRC | Varie selon le rôle utilisateur attribué |
| **Sous-traitant** | Croix-Rouge néerlandaise (NLRC) | • Héberge et exploite l’instance EspoCRM [Azure Europe Ouest – Amsterdam]<br>• Traite les données uniquement sur instruction de la NS<br>• Met en œuvre des mesures de sécurité techniques et organisationnelles<br>• Soutient la NS dans le cadre d’une DPIA si nécessaire<br>• Notifie la NS de toute violation de données | Administrateur EspoCRM : accès à l’échelle du système uniquement pour la configuration et la maintenance |
| **Sous-traitant** | IFRC (héberge KoboToolbox) | • Héberge et exploite la plateforme KoboToolbox (sur AWS Francfort, Allemagne) pour la soumission de formulaires et la collecte de données<br>• Traite les données de retour d’information pour le compte de la NS avant leur transmission à EspoCRM<br>• Applique des mesures de sécurité aux données en transit et au repos<br>• Lié par le cadre de protection des données de l’IFRC | Les données sont transmises à EspoCRM via API lors de la soumission du formulaire |
| **Administrateur de la plateforme (KoboToolbox)** | Administrateur Kobo (NLRC) | • Gère la configuration des formulaires KoboToolbox<br>• Garantit le bon étiquetage de l’équipe (NS, marqueur sensible) lors de la soumission du formulaire | Administrateur Kobo : accès à la gestion des formulaires |
| **Utilisateur API** | Compte technique géré par la NLRC | • Facilite la transmission automatisée entre KoboToolbox et EspoCRM<br>• Géré et surveillé par le sous-traitant NLRC | • Accès au niveau système limité à l’équipe NS attribuée<br>• Utilisateur à des fins d’intégration uniquement |
| **Gestionnaire des retours d’information** | Personnel NS (supervision) | • Supervise le traitement des retours d’information au sein de la NS<br>• Attribue le suivi aux points focaux<br>• Garantit des réponses appropriées et en temps utile | • Créer, lire, modifier, archiver tous les retours d’information de la NS<br>• Attribuer des points focaux<br>• Recevoir des notifications par e-mail |
| **Éditeur/Créateur de retours d’information** | Personnel NS (opérationnel) | • Saisit directement les retours d’information dans EspoCRM<br>• Assure le suivi des retours d’information qui lui sont personnellement attribués | • Créer des retours d’information<br>• Lire et modifier uniquement les retours d’information qui lui sont attribués |
| **Collecteur de retours d’information** | Personnel NS ou volontaire | • Soumet les retours d’information communautaires au nom des individus via KoboToolbox à partir d’un lien par code QR ou de l’application mobile KoboCollect<br>• N’accède pas à EspoCRM | • Aucun accès<br>• Les données entrent automatiquement dans EspoCRM lors de la soumission via KoboToolbox |
| **Gestionnaire des retours d’information sensibles** | Personnel NS (accès restreint) | • Traite les cas de retours d’information sensibles<br>• Doit respecter des obligations strictes de confidentialité | Lire et modifier les retours d’information marqués comme sensibles |
| **Lecteur de rapports** | Personnel NS / direction | • Surveille les tendances et la performance des programmes<br>• Utilise les données pour améliorer les programmes | • Lire les rapports (uniquement)<br>• Aucun accès aux dossiers individuels |
| **Support client** | Personnel de support NLRC | • Fournit un support technique aux utilisateurs NS<br>• N’accède pas au contenu des retours d’information dans le cadre des opérations normales | Accès limité : uniquement à des fins de support |
 
### Données traitées
 
- **Nature :** Retours d’information communautaires soumis par ou au nom d’individus.
- **Peut inclure des informations personnellement identifiables (PII) :** Noms, coordonnées, localisation et descriptions d’expériences individuelles ou de plaintes.
- **Données sensibles :** Les retours d’information peuvent être signalés comme sensibles. L’accès est limité au rôle de Gestionnaire des retours d’information sensibles.
- **Flux de données :**
  - KoboToolbox (soumission de formulaire) vers EspoCRM (stockage, suivi, rapports)
  - Saisie directe par le personnel NS dans EspoCRM
  - La séparation par équipe garantit que chaque NS n’accède qu’à ses propres données
- **Transferts internationaux :** Les données sont traitées dans EspoCRM hébergé par la NLRC. Les NS situées en dehors de l’Espace économique européen (EEE) doivent noter que les garanties de transfert applicables doivent être confirmées.

### Gouvernance et base légale
 
- **Base légitime :** La Plateforme régionale de gestion des retours d’information aide les Sociétés nationales à collecter et à répondre aux retours d’information communautaires dans le cadre de leurs programmes humanitaires. Chaque NS participante, en tant que Responsable du traitement, est chargée de confirmer la base légale appropriée conformément aux normes nationales applicables et aux normes de protection des données du Mouvement de la Croix-Rouge et du Croissant-Rouge.
- **Accord de partage des données (DSA) :** Un DSA entre chaque NS participante (en tant que Responsable du traitement) et la NLRC (en tant que Sous-traitant) est requis avant l’intégration. Cet accord doit couvrir : la portée et la finalité du traitement, les obligations de sécurité, la notification des violations, les accords avec les sous-traitants ultérieurs et le soutien relatif aux droits des personnes concernées.
- **Durée de conservation :** Les données personnelles collectées via la plateforme seront conservées pendant une durée maximale de 2 ans à compter de leur collecte, après quoi elles seront supprimées ou anonymisées. Les données ne peuvent pas être conservées plus longtemps que nécessaire au regard de la finalité pour laquelle elles ont été collectées.
- **Analyse d’impact relative à la protection des données (DPIA) :** Étant donné que des PII sont collectées, les NS participantes doivent évaluer la nécessité d’une DPIA, en particulier lorsque des retours d’information sensibles sont traités ou lorsque la NS sert des populations vulnérables. La NLRC apportera son soutien avec les informations techniques pertinentes. [Exigence de DPIA à évaluer pour chaque NS].
- **Normes applicables :** La NLRC adhère aux principes du Règlement général sur la protection des données (RGPD). Les NS sont tenues de se conformer à leur propre législation nationale sur la protection des données ainsi qu’aux politiques applicables de protection des données du Mouvement de la Croix-Rouge et du Croissant-Rouge.

### Contact
 
- **Contact du sous-traitant de la Croix-Rouge néerlandaise :** Daan Gorsse (dgorsse@redcross.nl)
- **Violation de données ou préoccupations :** Informez immédiatement la NLRC. Le Responsable du traitement de la NS est chargé de notifier l’autorité de contrôle compétente dans le délai applicable.
---

*Lors du remplissage de l’accord de partage des données avec la Société nationale, veuillez utiliser le modèle joint. Quelques notes supplémentaires relatives aux sections ci-dessous dans le modèle :*
 
- *Fondements juridiques du partage des données personnelles (choisissez la base légale la plus appropriée parmi celles énumérées ci-dessous et expliquez clairement pourquoi il s’agit d’une base légale appropriée)*
- *Portée (vérifiez ce qui est applicable)*
- *Licences (à remplir uniquement si applicable)*
*Pour référence :* [Modèle d’accord de traitement des données GDPR](https://gdpr.eu/data-processing-agreement/)