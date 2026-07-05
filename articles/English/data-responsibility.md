# [TEST] Data Responsibility Framework
 
### Purpose
 
This document provides a clear overview of data responsibilities for National Societies (NS) participating in the Feedback Management Platform. It defines who is accountable for data, how it is processed, and what obligations each role carries.
 
### Platform Overview
 
- **Platform:** Feedback Management Platform (EspoCRM) and KoboToolbox.
- **Operated by:** Netherlands Red Cross (NLRC).
- **NS in scope:** Any National Society formally onboarded to the Feedback Management Platform.
- **Purpose:** Collect, manage, and follow-up community feedback submitted to the NS through digital forms (KoboToolbox) or direct entry (EspoCRM).
- **Data segregation:** Each NS is assigned to a team within the Feedback Management Platform, ensuring that staff can only access feedback related to their own NS.
- **Sensitive flag:** Feedback can be marked as sensitive, restricting access to authorized roles only.

### Data Roles and Responsibilities
 
| Role | Who | Key Responsibilities | Access in EspoCRM |
|------|-----|----------------------|-------------------|
| **Data Controller** | Participating NS | • Determines purpose and means of processing<br>• Ensures legal basis for data collection<br>• Responsible for data subject rights<br>• Initiates and signs a Data Sharing Agreement with NLRC | Varies depending on assigned user role |
| **Data Processor** | Netherlands Red Cross (NLRC) | • Hosts and operates EspoCRM instance [Azure West Europe – Amsterdam]<br>• Processes data only on NS instructions<br>• Implements technical and organizational security measures<br>• Supports NS in DPIA if required<br>• Notifies NS of any data breach | EspoCRM Admin: system wide access for configuration and maintenance only |
| **Data Processor** | IFRC (hosts KoboToolbox) | • Hosts and operates the KoboToolbox platform (on AWS Frankfurt, Germany) for form submission and data collection<br>• Processes feedback data on behalf of the NS before transmission to EspoCRM<br>• Applies security measures to data in transit and at rest<br>• Bound by IFRC's data protection framework | Data is transmitted to EspoCRM via API upon form submission |
| **Platform Admin (KoboToolbox)** | Kobo Admin (NLRC) | • Manages KoboToolbox form configuration<br>• Ensures correct team tagging (NS, sensitive flag) on form submission | Kobo Admin: form management access |
| **API User** | Technical account managed by NLRC | • Facilitates automated transmission between KoboToolbox and EspoCRM<br>• Managed and monitored by NLRC Data Processor | • System-level access scoped to assigned NS team<br>• User for integration purposes only |
| **Feedback Manager** | NS staff (supervisory) | • Oversees feedback handling within the NS<br>• Assigns follow-up to focal points<br>• Ensures timely and appropriate responses | • Create, read, edit, archive all NS feedback<br>• Assign focal points<br>• Receive email notifications |
| **Feedback Editor/Creator** | NS staff (operational) | • Enters feedback directly in EspoCRM<br>• Follows up on personally assigned feedback | • Create feedback<br>• Read and edit own assigned feedback only |
| **Feedback Collector** | NS staff or volunteer | • Submits community feedback on behalf of individuals via KoboToolbox from QR code link or KoboCollect mobile app<br>• Does not access EspoCRM | • No access<br>• Data enters EspoCRM automatically upon submission via KoboToolbox |
| **Sensitive Feedback Manager** | NS staff (restricted access) | • Handles sensitive feedback cases<br>• Must adhere to strict confidentiality obligations | Read and edit feedback marked as sensitive |
| **Report Viewer** | NS staff / management | • Monitors trends and program performance<br>• Uses data for program improvement | • Read reports (only)<br>• No individual record access |
| **Client Support** | NLRC support staff | • Provides technical support to NS users<br>• Does not access feedback content in normal operations | Limited access: For support purposes only |

### Data Processed
 
- **Nature:** Community feedback submitted by or on behalf of individuals.
- **May include Personally Identifiable Information (PII):** Names, contact details, location, and descriptions of individual experiences or complaints.
- **Sensitive data:** Feedback may be flagged as sensitive. Access is restricted to the Sensitive Feedback Manager role.
- **Data flow:**
  - KoboToolbox (form submission) to EspoCRM (storage, follow-up, reporting)
  - Direct entry by NS staff into EspoCRM
  - Team based segregation ensures each NS only accesses its own data
- **International transfers:** Data is processed within EspoCRM hosted by NLRC. NS outside the European Economic Area (EEA) should note that applicable transfer safeguards must be confirmed.

### Governance and Legal Basis
 
- **Legitimate basis:** The Feedback Management Platform supports National Societies in collecting and responding to community feedback as part of their humanitarian programs. Each participating NS, as Data Controller, is responsible for confirming the appropriate legal basis under applicable national and Red Cross Red Crescent data protection standards.
- **Data Sharing Agreement (DSA):** A DSA between each participating NS (as Data Controller) and NLRC (as Data Processor) is required before onboarding. This agreement should cover: scope and purpose of processing, security obligations, breach notification, sub-processor agreements, and data subject rights support.
- **Retention period:** Personal data collected through the platform will be retained for a maximum of 2 years from the data collection, after which it will be deleted or anonymized. Data may not be stored longer than necessary for the purpose for which it was collected.
- **Data Protection Impact Assessment (DPIA):** Given that PII is collected, participating NS should assess the need for a DPIA, particularly where sensitive feedback is processed or the NS serves vulnerable populations. NLRC will support with relevant technical information. [DPIA requirement to be assessed per NS].
- **Applicable standards:** NLRC adheres to General Data Protection Regulation (GDPR) principles. NS are expected to comply with their own national data protection legislation and applicable Red Cross Red Crescent data protection policies.

### Contact
 
- **Data Processor contact from the Netherlands Red Cross:** Daan Gorsse (dgorsse@redcross.nl)
- **Data breach or concerns:** Notify NLRC immediately. NS Data Controller is responsible for notifying relevant supervisory authority within an applicable timeframe.
---

*When filling in the Data Sharing Agreement with the National Society, please use the template attached. Some additional notes related to below sections in the template:*
 
- *Legal grounds for sharing personal data (choose the most appropriate legal basis from the ones listed below and clearly explain why it is a suitable legal basis)*
- *Scope (Check what is applicable)*
- *Licenses (only fill in if applicable)*
*For reference:* [GDPR Data Processing Agreement Template](https://gdpr.eu/data-processing-agreement/)
