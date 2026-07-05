# [TEST] Sensitive Feedback
 
### 1. Purpose
 
To ensure that feedback classified as sensitive by the National Society (NS) is handled securely, consistently, and only by designated authorized individuals.
 
### 2. Definition
 
Sensitive feedback is a category of feedback defined by the National Society (NS), which may only be handled by specifically designated responsible individuals.
 
Sensitive feedback can be classified in different ways, but here are 2 main distinctions to be aware of since follow-up will be done differently:
 
- Breaches of code of conduct (example: corruption/fraud/GBV committed by Red Cross staff or volunteers)
- Feedback that is sensitive to someone's personal situation (example: health, stigma, domestic violence).

### 3. Roles and Responsibilities
 
- **Feedback Collector**
  - Logs feedback in Kobo.
  - Flags feedback as sensitive where applicable.
- **Feedback Manager**
  - Reviews incoming feedback.
  - Confirms whether feedback is sensitive according to NS definitions.
  - Assigns a designated Sensitive Feedback Manager.
  - Ensures follow-up takes place.
  - User account configurations: *[screenshots: role/permission settings]*
- **Feedback Creator and Editor (Authorized Individual – Sensitive Feedback Manager)**
  - Handles the case end-to-end.
  - Ensures appropriate follow-up and documentation.
  - Updates status and closes the case.
  - User account configurations: *[screenshots: role/permission settings]*
- **System (Kobo / EspoCRM)**
  - Automatically sets priority to *High* when feedback is marked as sensitive.
  - Automatically authorizes Feedback Managers for handling sensitive feedback (based on NS-defined roles/permissions).
  - Verifies that any assigned individual is authorized to handle sensitive feedback.
  - Sets case status to *In Progress* upon assignment.
  - Sends notifications and reminders.

### 4. Procedure
 
#### Step 1: Feedback Collection and Registration
 
- Feedback is collected and logged in Kobo.
- If applicable, the Feedback Collector marks the feedback as **sensitive**.
- If it is not known whether feedback is sensitive, leave empty.

#### Step 2: Automatic System Actions
 
- The system automatically:
  - Sets priority to **High**.
  - Routes the feedback for review.

#### Step 3: Review and Validation
 
- The Feedback Manager:
  - Reviews the feedback.
  - Confirms whether it meets the NS definition of sensitive feedback.
- If **not sensitive**:
  - Unmark as sensitive.
  - Reset priority.
  - Process according to standard feedback procedures.
- If **sensitive**:
  - Proceed to Step 4.

#### Step 4: Assignment
 
- The Feedback Manager assigns the case to a **designated Sensitive Feedback Manager**.
- The system sets the case status to **In Progress**.

#### Step 5: Notification and Monitoring
 
- The assigned Sensitive Feedback Manager:
  - Receives notification via email and EspoCRM.
- The system:
  - Sends daily reminders until the case is updated.

#### Step 6: Case Handling
 
- The Sensitive Feedback Manager:
  - Reviews the case.
  - Takes appropriate action.
  - Follows internal standard operating procedures on handling sensitive cases.
  - Shares feedback internally **if** required and allowed.

#### Step 7: Status Updates
 
- The Sensitive Feedback Manager updates the case status as work progresses.

#### Step 8: Closure
 
- Once the case is resolved:
  - The Sensitive Feedback Manager marks the case as **closed**.
  - Closure is confirmed in the overview system.

### 5. Key Principles
 
- The National Society defines what constitutes sensitive feedback.
- Only authorized individuals may handle sensitive feedback.
- Sensitive feedback is hidden from all other users except for authorized users.
- All sensitive feedback cases are treated as **high priority**.
- Timely follow-up is mandatory and actively monitored.

### 6. Risks
 
Failure to follow this SOP may result in:
 
- Delays in handling high-risk feedback.
- Breaches of confidentiality or safeguarding protocols.

### 7. Visual of workflow
 
![Sensitive feedback workflow](../../assets/sensitive-feedback-flow.png)
 
### 8. Validation
 
- Protocol needs review by the end of 2026 to make sure it stays effective.