Yes. You have given enough information. We don't need another round of questions.

I'll take the decisions we've already made, fill only the small implementation gaps using sensible defaults, and produce the artifacts in the exact order you requested.

# Step 1 — Functional & Non-Functional Requirements

I'll use IDs so everything can be traced later:

> **Requirement → User Story → Acceptance Criteria → Test Case**

---

# A. Authentication & Authorization

| ID          | Requirement                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------------- |
| FR-AUTH-001 | The system shall authenticate users before allowing access to protected functionality.         |
| FR-AUTH-002 | The system shall support at least two roles: **Employee** and **TA**.                          |
| FR-AUTH-003 | Employees shall only access functionality permitted to employees.                              |
| FR-AUTH-004 | Employees shall only be able to view their own applications.                                   |
| FR-AUTH-005 | TA users shall be able to manage job postings and applications according to their permissions. |
| FR-AUTH-006 | Authorization shall be enforced by the backend, not only by frontend visibility.               |

---

# B. Employee Profile

| ID         | Requirement                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------------- |
| FR-EMP-001 | The system shall maintain an employee profile.                                                                      |
| FR-EMP-002 | An employee profile shall contain full name, employee code, email, department, designation, experience, and skills. |
| FR-EMP-003 | Employee experience shall be stored as a decimal/floating-point number representing years.                          |
| FR-EMP-004 | Department shall be maintained as a separate entity and referenced by the employee.                                 |
| FR-EMP-005 | Designation shall be maintained as a separate entity and referenced by the employee.                                |
| FR-EMP-006 | Employee skills shall be stored as structured JSONB data containing skill names and skill levels.                   |

---

# C. Job Posting Discovery

| ID         | Requirement                                                                              |
| ---------- | ---------------------------------------------------------------------------------------- |
| FR-JOB-001 | Employees shall be able to view open internal job postings.                              |
| FR-JOB-002 | Employees shall be able to search postings by job title.                                 |
| FR-JOB-003 | Search shall be text-based.                                                              |
| FR-JOB-004 | Employees shall be able to filter postings by department.                                |
| FR-JOB-005 | Employees shall be able to filter postings by designation/title.                         |
| FR-JOB-006 | Employees shall be able to filter postings by skills.                                    |
| FR-JOB-007 | Employees shall be able to filter postings by due date.                                  |
| FR-JOB-008 | Employees shall be able to sort postings by due date.                                    |
| FR-JOB-009 | The system shall display an appropriate empty state when no open postings are available. |
| FR-JOB-010 | Employees shall be able to view the complete details of a selected job posting.          |

---

# D. Job Posting Information

| ID          | Requirement                                              |
| ----------- | -------------------------------------------------------- |
| FR-POST-001 | A job posting shall have a title.                        |
| FR-POST-002 | A job posting shall have a department.                   |
| FR-POST-003 | A job posting shall have a designation/title.            |
| FR-POST-004 | A job posting shall have a description.                  |
| FR-POST-005 | A job posting shall have a location.                     |
| FR-POST-006 | A job posting shall have an employment type.             |
| FR-POST-007 | A job posting shall have a required experience value.    |
| FR-POST-008 | A job posting shall have required skills.                |
| FR-POST-009 | Salary shall be optional.                                |
| FR-POST-010 | If salary is provided, it shall be visible to employees. |
| FR-POST-011 | Every open posting shall have a deadline.                |
| FR-POST-012 | A job posting shall have a lifecycle status.             |

---

# E. Job Application

| ID         | Requirement                                                                                                                      |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------- |
| FR-APP-001 | An employee shall be able to apply directly from the job-posting details view.                                                   |
| FR-APP-002 | The application process shall not require redirecting the employee to another application page merely to submit the application. |
| FR-APP-003 | The system shall display a confirmation before submitting an application.                                                        |
| FR-APP-004 | An application shall use the employee's existing profile.                                                                        |
| FR-APP-005 | Customized resumes/profiles shall not be required.                                                                               |
| FR-APP-006 | Applications shall not require manager approval before submission.                                                               |
| FR-APP-007 | Applications shall be submitted immediately after confirmation.                                                                  |
| FR-APP-008 | The system shall not support draft applications in the current scope.                                                            |
| FR-APP-009 | Attachments shall not be supported in the current application flow.                                                              |
| FR-APP-010 | An employee shall not have more than one active application for the same posting.                                                |
| FR-APP-011 | An employee may reapply only after withdrawing the previous application.                                                         |
| FR-APP-012 | An employee shall have a maximum of three reapplications for the same posting.                                                   |

---

# F. Application Status

| ID            | Requirement                                                                   |
| ------------- | ----------------------------------------------------------------------------- |
| FR-STATUS-001 | New applications shall start in `APPLIED` status.                             |
| FR-STATUS-002 | The system shall support `UNDER_REVIEW`.                                      |
| FR-STATUS-003 | The system shall support `SHORTLISTED`.                                       |
| FR-STATUS-004 | The system shall support `INTERVIEW`.                                         |
| FR-STATUS-005 | The system shall support `SELECTED`.                                          |
| FR-STATUS-006 | The system shall support `REJECTED`.                                          |
| FR-STATUS-007 | The system shall support `WITHDRAWN`.                                         |
| FR-STATUS-008 | TA shall be able to update application status only through valid transitions. |
| FR-STATUS-009 | `APPLIED → SHORTLISTED` shall be allowed.                                     |
| FR-STATUS-010 | An application may be rejected from any non-terminal processing state.        |
| FR-STATUS-011 | `SHORTLISTED → UNDER_REVIEW` shall be allowed.                                |
| FR-STATUS-012 | Rejected applications shall not transition to another status.                 |
| FR-STATUS-013 | Selected applications shall not transition to another status.                 |
| FR-STATUS-014 | Withdrawn applications shall not transition to another status.                |

---

# G. Withdraw Application

| ID        | Requirement                                                                                              |
| --------- | -------------------------------------------------------------------------------------------------------- |
| FR-WD-001 | Employees shall be able to withdraw an application in `APPLIED` status.                                  |
| FR-WD-002 | Employees shall be able to withdraw an application in `UNDER_REVIEW` status.                             |
| FR-WD-003 | Employees shall be able to withdraw an application in `SHORTLISTED` status.                              |
| FR-WD-004 | Employees shall not be able to withdraw an application in `INTERVIEW`, `SELECTED`, or `REJECTED` status. |
| FR-WD-005 | Withdrawal shall require user confirmation.                                                              |
| FR-WD-006 | A withdrawn application shall remain stored as historical application data.                              |

---

# H. My Applications

| ID           | Requirement                                                                                   |
| ------------ | --------------------------------------------------------------------------------------------- |
| FR-MYAPP-001 | Employees shall be able to view their applications.                                           |
| FR-MYAPP-002 | Employees shall be able to see the associated job posting for each application.               |
| FR-MYAPP-003 | Employees shall be able to see the application status.                                        |
| FR-MYAPP-004 | Employees shall be able to see the applied date.                                              |
| FR-MYAPP-005 | Employees shall be able to see the job-posting deadline.                                      |
| FR-MYAPP-006 | The withdraw action shall only be displayed/enabled when permitted by the application status. |

---

# I. Job Templates

| ID          | Requirement                                                                  |
| ----------- | ---------------------------------------------------------------------------- |
| FR-TEMP-001 | TA shall be able to create job templates.                                    |
| FR-TEMP-002 | TA shall be able to retrieve job templates.                                  |
| FR-TEMP-003 | TA shall be able to update job templates.                                    |
| FR-TEMP-004 | TA shall be able to delete eligible job templates.                           |
| FR-TEMP-005 | TA shall be able to create a posting without using a template.               |
| FR-TEMP-006 | TA shall be able to create a posting from a template.                        |
| FR-TEMP-007 | Template data shall automatically populate the corresponding posting fields. |
| FR-TEMP-008 | TA shall be able to modify populated fields before creating the posting.     |
| FR-TEMP-009 | Multiple postings may use the same template.                                 |
| FR-TEMP-010 | Updating a template shall not automatically modify existing postings.        |

---

# J. TA Job Posting Management

| ID           | Requirement                                                                                                             |
| ------------ | ----------------------------------------------------------------------------------------------------------------------- |
| FR-TAJOB-001 | TA shall be able to create job postings.                                                                                |
| FR-TAJOB-002 | TA shall be able to retrieve job postings.                                                                              |
| FR-TAJOB-003 | TA shall be able to retrieve a specific job posting.                                                                    |
| FR-TAJOB-004 | TA shall be able to update eligible job postings.                                                                       |
| FR-TAJOB-005 | TA shall be able to delete draft postings.                                                                              |
| FR-TAJOB-006 | TA shall be able to manage posting status.                                                                              |
| FR-TAJOB-007 | TA shall be able to close an open posting manually.                                                                     |
| FR-TAJOB-008 | TA shall be able to reopen a closed posting.                                                                            |
| FR-TAJOB-009 | TA shall be able to mark a posting as completed only when all associated applications are terminal.                     |
| FR-TAJOB-010 | Multiple postings for the same role may exist simultaneously.                                                           |
| FR-TAJOB-011 | The frontend may warn TA about a highly similar existing posting.                                                       |
| FR-TAJOB-012 | Such duplicate-posting warnings shall not prevent valid posting creation unless a separate business rule is introduced. |

---

# K. Posting Lifecycle & Deadline

| ID          | Requirement                                                                                                      |
| ----------- | ---------------------------------------------------------------------------------------------------------------- |
| FR-LIFE-001 | A posting shall support `DRAFT`, `OPEN`, `CLOSED`, and `COMPLETED` statuses.                                     |
| FR-LIFE-002 | Draft postings shall not be visible to employees as open opportunities.                                          |
| FR-LIFE-003 | Open postings shall accept applications.                                                                         |
| FR-LIFE-004 | Closed postings shall not accept new applications.                                                               |
| FR-LIFE-005 | Closing a posting shall not alter its existing applications.                                                     |
| FR-LIFE-006 | A deadline shall be mandatory for an open posting.                                                               |
| FR-LIFE-007 | The system shall automatically close a posting when its deadline is reached.                                     |
| FR-LIFE-008 | TA shall be able to close a posting manually before its deadline.                                                |
| FR-LIFE-009 | TA shall be able to change the deadline of a posting.                                                            |
| FR-LIFE-010 | Existing valid applications shall remain valid if the deadline is subsequently shortened.                        |
| FR-LIFE-011 | A closed posting may be reopened by changing its deadline and reopening it.                                      |
| FR-LIFE-012 | Existing applications shall remain associated with a reopened posting.                                           |
| FR-LIFE-013 | A posting may become completed only when every associated application is `SELECTED`, `REJECTED`, or `WITHDRAWN`. |

---

# L. Notifications

| ID           | Requirement                                                                                  |
| ------------ | -------------------------------------------------------------------------------------------- |
| FR-NOTIF-001 | Employees shall be notified when an application is shortlisted.                              |
| FR-NOTIF-002 | Employees shall be notified when an application reaches interview status.                    |
| FR-NOTIF-003 | Employees shall be notified when an application is selected.                                 |
| FR-NOTIF-004 | Employees shall be notified when an application is rejected.                                 |
| FR-NOTIF-005 | TA shall receive a configurable reminder before a posting deadline.                          |
| FR-NOTIF-006 | TA shall be notified when a posting is automatically closed because its deadline has passed. |
| FR-NOTIF-007 | Notifications shall be associated with their recipient.                                      |
| FR-NOTIF-008 | Notifications shall support read/unread state.                                               |

---

# M. Compatibility & Recommendations — Phase 3

| ID           | Requirement                                                                                                     |
| ------------ | --------------------------------------------------------------------------------------------------------------- |
| FR-MATCH-001 | The system shall calculate compatibility between an employee and a job posting.                                 |
| FR-MATCH-002 | Compatibility shall be represented as an overall percentage.                                                    |
| FR-MATCH-003 | Experience shall contribute to compatibility.                                                                   |
| FR-MATCH-004 | Skills shall contribute to compatibility.                                                                       |
| FR-MATCH-005 | Employee skill levels shall be considered in TA-facing compatibility.                                           |
| FR-MATCH-006 | Skill-name matching shall be used for employee-facing matching/recommendations.                                 |
| FR-MATCH-007 | A missing requirement shall not prevent an employee from applying.                                              |
| FR-MATCH-008 | An employee may still be shortlisted even when compatibility is low.                                            |
| FR-MATCH-009 | Compatibility shall not automatically determine selection or rejection.                                         |
| FR-MATCH-010 | Recommendation shall allow employees with up to one year less experience than the requirement to be considered. |
| FR-MATCH-011 | Skill-based recommendation shall use the agreed minimum match threshold.                                        |
| FR-MATCH-012 | No AI/ML model shall be required for compatibility or recommendation.                                           |

---

# N. UX & Frontend Behavior

| ID        | Requirement                                                                            |
| --------- | -------------------------------------------------------------------------------------- |
| FR-UX-001 | State-changing actions shall provide confirmation where appropriate.                   |
| FR-UX-002 | State-changing POST/PUT/PATCH/DELETE operations shall provide toast feedback.          |
| FR-UX-003 | GET operations shall not require toast notifications.                                  |
| FR-UX-004 | Login, logout, and refresh shall not require toast notifications.                      |
| FR-UX-005 | Invalid/unavailable actions shall be disabled.                                         |
| FR-UX-006 | Disabled actions shall have a visually distinguishable state.                          |
| FR-UX-007 | Rapid repeated clicks on state-changing actions shall not create duplicate operations. |
| FR-UX-008 | Search input shall use request throttling/debouncing as appropriate.                   |
| FR-UX-009 | Search and filtering shall provide clear feedback when no results exist.               |
| FR-UX-010 | The employee shall be able to apply directly from the posting details view.            |

---

# O. Non-Functional Requirements

| ID            | Requirement                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------------ |
| NFR-PERF-001  | Normal job listing and search operations should complete within approximately 2 seconds.               |
| NFR-AVAIL-001 | The production system should target 99% availability.                                                  |
| NFR-SEC-001   | Backend APIs shall enforce role-based authorization.                                                   |
| NFR-SEC-002   | Employees shall not be able to access another employee's applications.                                 |
| NFR-SEC-003   | Sensitive state-changing operations shall be protected against unauthorized access.                    |
| NFR-AUD-001   | Important posting and application state changes shall be auditable.                                    |
| NFR-SCALE-001 | The system shall support at least 700 employees.                                                       |
| NFR-SCALE-002 | The architecture shall allow future compatibility/recommendation functionality without major redesign. |
| NFR-MAINT-001 | The codebase shall follow modular architecture and consistent coding practices.                        |
| NFR-MAINT-002 | Major modules shall be independently maintainable and testable.                                        |
| NFR-REC-001   | Successfully submitted applications shall not be silently lost.                                        |
| NFR-REC-002   | Database backups shall be maintained with restoration capability.                                      |
| NFR-COMP-001  | The frontend shall support modern browsers.                                                            |
| NFR-COMP-002  | The frontend shall provide responsive layouts for desktop and mobile devices.                          |
| NFR-RATE-001  | Backend APIs shall enforce appropriate rate limits.                                                    |

---

# P. Audit Requirements

| ID         | Requirement                                            |
| ---------- | ------------------------------------------------------ |
| FR-AUD-001 | The system shall record creation of job postings.      |
| FR-AUD-002 | The system shall record updates to job postings.       |
| FR-AUD-003 | The system shall record deletion of eligible postings. |
| FR-AUD-004 | The system shall record posting closure and reopening. |
| FR-AUD-005 | The system shall record posting completion.            |
| FR-AUD-006 | The system shall record application status changes.    |

---

# Requirement Count

We now have a substantial requirements baseline covering:

* **Employee**
* **TA**
* **Authentication**
* **Job discovery**
* **Search**
* **Filtering**
* **Sorting**
* **Job details**
* **Applications**
* **Withdrawal**
* **Reapplication**
* **Application lifecycle**
* **Job templates**
* **Posting lifecycle**
* **Deadlines**
* **Notifications**
* **UX behavior**
* **Security**
* **Audit**
* **Performance**
* **Scalability**
* **Maintainability**
* **Recovery**
* **Phase-3 compatibility**

This is enough to move forward.

---

