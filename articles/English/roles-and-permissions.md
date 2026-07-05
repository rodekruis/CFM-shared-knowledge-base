# [TEST] Roles and permissions

### Purpose

Documenting user roles and permissions is essential for ensuring clarity, security, and accountability within the Feedback Management Platform. It will help understand who can access, modify, or manage specific sections of the platform and its data. This will reduce the risk of misconfiguration, unauthorized access, and operational errors. It also supports onboarding, auditing, and compliance by providing a reliable reference for system behavior. 

A more detailed overview of role management can be found in the [EspoCRM official documentation](https://docs.espocrm.com/administration/roles-management/). 

### Accessing the Feedback Management Platform

National Societies have the ability to access the Feedback Management Platform. Since this is a shared platform, each National Society is assigned to a Team, allowing them access to **ONLY** their feedback data and visualizations.

Within the Team structure per National Society, multiple users from the National Society can be linked to the respective Team for access. Depending on the user specific roles and permissions, the user can create, read, edit, and/or delete feedback data.

---

### National Society Roles

#### Feedback Supervisor

This role is designated for the NS CEA focal point at Headquarters. This person will oversee, monitor, and handle the feedback received and provided to the community. They are the main contact person for the NS incase of any issues with the platform.

What they can do in the platform:

- Read, create, edit, delete feedback records
  - Example: delete feedback records after onboarding staff and volunteers, to remove test entries from the platform
  - Note: besides test entries, it is not best practice to delete feedback data
- Create or remove users via the entity "User Access Requests"
- Assign users to follow-up on the specific feedback records
- Follow-up in the stream with other colleagues
- Read reports
- Authorized for sensitive feedback records
  - Can read, edit, assign users, and follow-up on sensitive feedback

#### Feedback Focal Point

This role is designated for NS members (e.g., CEA, PMER, IM, Branches, hotline operators) that will handle feedback entered into the Feedback Management Platform. 

What they can do in the platform:

- Read, create, edit feedback records
- Assign users to follow-up on the specific feedback records (if users are known)
- Follow-up on feedback records
- Follow-up in the stream with other colleagues
- Read reports


#### Feedback Handler

This role is designated for NS members (e.g., CVA, Health, Shelter focal points) that will handle or just see specific feedback.

What they can do in the platform:

- Read and edit feedback records assigned to them
- Follow-up on feedback records assigned to them
- Follow-up in the stream with other colleagues
- Read reports


#### Sensitive Feedback Focal Point

This role is designated for the NS focal point (e.g., PGI focal point) that will handle sensitive feedback. When a feedback record is marked as sensitive, ONLY users with this role and Feedback Supervisors will be able to access, view, and edit the feedback record.

What they can do in the platform:

- Read and edit feedback records that are sensitive
- Follow-up and close sensitive feedback records
- Read reports


#### Feedback Report Viewer

This role is designated for NS users that need a high level overview of the feedback. The Feedback Report Viewer, for example, could be someone from the PMER team that needs data for reporting or could be the Secretary General that would like to have an overview of the work. They CANNOT see any Personal Identifiable Information in the feedback record.

What they can do in the platform:

- Access to the dashboard for reporting
- High level access to feedback records without PII

---

### Support Roles
 
#### Client Support
 
This role is designated to the Netherlands Red Cross Data Team 510. The Client Support team will address and troubleshoot any issues faced by the NS when using the Regional Feedback Management Platform.
 
What can be expected from them:
 
- Level 1 and 2 support
  - Level 1: invite users, reset passwords, help users navigate the User Interface (UI), explain how EspoCRM is (not) meant to be used, update a field
- Troubleshooting errors
- User support

#### Administrator
 
This role is designated to the Netherlands Red Cross Data Team 510.
 
What can be expected from them:
 
- Level 1, 2, 3 support
  - Level 1: invite users, reset passwords, help users navigate the User Interface (UI), explain how EspoCRM is (not) meant to be used, update a field
  - Level 2: add a new field, create a new entity, relate 2 entities with one another, automate a task (flowcharts)
  - Level 3: setup the server on which EspoCRM is hosted, install/update EspoCRM, create/restore a backup, update network settings.
- Platform updates and configurations
- Adding National Society Teams and onboarding them into the platform
- Developing reports and maintaining the homepage dashboard
- Maintaining flowcharts and API integrations

#### Feedback Data Collector (View Kobo Form)
 
This role is not an EspoCRM role but solely a role in the KoboToolbox account of the NS feedback data collector who needs offline access to the KoboToolbox Form. This role can be requested through the NS focal point (Feedback Manager) who has access to the Form.
