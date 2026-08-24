# Step 4 — Test Cases

Now we convert acceptance criteria into executable test scenarios.

## Core Employee Tests

| Test ID    | Test                                      | Expected Result                 |
| ---------- | ----------------------------------------- | ------------------------------- |
| TC-EMP-001 | Employee opens job list                   | Open postings displayed         |
| TC-EMP-002 | No open postings                          | Empty state displayed           |
| TC-EMP-003 | Search valid title                        | Matching postings displayed     |
| TC-EMP-004 | Search nonexistent title                  | No-results state                |
| TC-EMP-005 | Filter by department                      | Correct postings returned       |
| TC-EMP-006 | Filter by designation                     | Correct postings returned       |
| TC-EMP-007 | Filter by skill                           | Correct postings returned       |
| TC-EMP-008 | Filter by deadline                        | Correct postings returned       |
| TC-EMP-009 | Sort by deadline                          | Correct ordering                |
| TC-EMP-010 | Open job details                          | All available details displayed |
| TC-EMP-011 | Salary exists                             | Salary displayed                |
| TC-EMP-012 | Salary absent                             | Salary omitted                  |
| TC-EMP-013 | Apply to open posting                     | Application created             |
| TC-EMP-014 | Confirm application                       | Status = APPLIED                |
| TC-EMP-015 | Cancel application confirmation           | Application not created         |
| TC-EMP-016 | Apply to already-applied posting          | Action disabled/rejected        |
| TC-EMP-017 | Withdraw APPLIED application              | Status = WITHDRAWN              |
| TC-EMP-018 | Withdraw UNDER_REVIEW                     | Status = WITHDRAWN              |
| TC-EMP-019 | Withdraw SHORTLISTED                      | Status = WITHDRAWN              |
| TC-EMP-020 | Withdraw SELECTED                         | Operation rejected              |
| TC-EMP-021 | Withdraw REJECTED                         | Operation rejected              |
| TC-EMP-022 | Reapply after withdrawal                  | New application created         |
| TC-EMP-023 | Fourth application after 3 reapplications | Rejected                        |
| TC-EMP-024 | Open My Applications                      | Own applications displayed      |
| TC-EMP-025 | Attempt another employee's application    | Access denied                   |

---

# TA Tests

| Test ID   | Test                                     | Expected Result                      |
| --------- | ---------------------------------------- | ------------------------------------ |
| TC-TA-001 | Create draft posting                     | Posting created                      |
| TC-TA-002 | Create open posting                      | Posting created                      |
| TC-TA-003 | Create open posting without deadline     | Validation error                     |
| TC-TA-004 | Get all postings                         | Postings returned                    |
| TC-TA-005 | Get specific posting                     | Correct posting returned             |
| TC-TA-006 | Update posting                           | Updated values persisted             |
| TC-TA-007 | Delete draft                             | Draft deleted                        |
| TC-TA-008 | Create posting from template             | Template values populated            |
| TC-TA-009 | Modify template values                   | Modified posting saved               |
| TC-TA-010 | Create without template                  | Posting created                      |
| TC-TA-011 | Close posting                            | Status = CLOSED                      |
| TC-TA-012 | Reopen posting                           | Status = OPEN                        |
| TC-TA-013 | Complete eligible posting                | Status = COMPLETED                   |
| TC-TA-014 | Complete posting with active application | Operation rejected                   |
| TC-TA-015 | Change deadline                          | New deadline persisted               |
| TC-TA-016 | Shorten deadline after applications      | Existing applications retained       |
| TC-TA-017 | Auto-close at deadline                   | Status = CLOSED                      |
| TC-TA-018 | Closed posting accepts application       | Rejected                             |
| TC-TA-019 | Reopened posting accepts applications    | Application accepted                 |
| TC-TA-020 | Multiple similar postings                | Creation allowed, warning may appear |

---

# Application Workflow Tests

| Test ID   | Scenario                   | Expected |
| --------- | -------------------------- | -------- |
| TC-WF-001 | Applied → Under Review     | Allowed  |
| TC-WF-002 | Applied → Shortlisted      | Allowed  |
| TC-WF-003 | Applied → Rejected         | Allowed  |
| TC-WF-004 | Under Review → Shortlisted | Allowed  |
| TC-WF-005 | Shortlisted → Under Review | Allowed  |
| TC-WF-006 | Shortlisted → Interview    | Allowed  |
| TC-WF-007 | Interview → Selected       | Allowed  |
| TC-WF-008 | Interview → Rejected       | Allowed  |
| TC-WF-009 | Rejected → Shortlisted     | Rejected |
| TC-WF-010 | Rejected → Selected        | Rejected |
| TC-WF-011 | Selected → Interview       | Rejected |
| TC-WF-012 | Withdrawn → Applied        | Rejected |

---

# Notification Tests

| Test ID    | Scenario                       | Expected          |
| ---------- | ------------------------------ | ----------------- |
| TC-NOT-001 | Application shortlisted        | Employee notified |
| TC-NOT-002 | Application reaches interview  | Employee notified |
| TC-NOT-003 | Application selected           | Employee notified |
| TC-NOT-004 | Application rejected           | Employee notified |
| TC-NOT-005 | Deadline reminder time reached | TA notified       |
| TC-NOT-006 | Deadline reached               | Posting closes    |
| TC-NOT-007 | Posting auto-closed            | TA notified       |

---

# UX / Robustness Tests

| Test ID   | Scenario                 | Expected                         |
| --------- | ------------------------ | -------------------------------- |
| TC-UX-001 | Apply clicked            | Confirmation shown               |
| TC-UX-002 | Withdraw clicked         | Confirmation shown               |
| TC-UX-003 | Delete clicked           | Confirmation shown               |
| TC-UX-004 | Successful POST          | Success toast                    |
| TC-UX-005 | Failed POST              | Error toast                      |
| TC-UX-006 | Successful GET           | No toast                         |
| TC-UX-007 | Rapid Apply clicks       | Only one application created     |
| TC-UX-008 | Invalid action           | Button disabled                  |
| TC-UX-009 | Rapid search typing      | Requests appropriately debounced |
| TC-UX-010 | Unauthorized API request | Request rejected                 |

---

# NFR Test Cases

| Test ID    | NFR                | Test                                                  |
| ---------- | ------------------ | ----------------------------------------------------- |
| TC-NFR-001 | Performance        | Measure normal job-list response time                 |
| TC-NFR-002 | Search performance | Measure search response time                          |
| TC-NFR-003 | Authorization      | Attempt employee access to TA endpoint                |
| TC-NFR-004 | Data isolation     | Attempt employee A to access employee B's application |
| TC-NFR-005 | Audit              | Verify posting changes create audit records           |
| TC-NFR-006 | Audit              | Verify application status changes are logged          |
| TC-NFR-007 | Rate limiting      | Send requests above configured threshold              |
| TC-NFR-008 | Scalability        | Test system with representative 700-employee dataset  |
| TC-NFR-009 | Backup             | Restore database from backup                          |
| TC-NFR-010 | Responsive UI      | Test supported desktop/mobile layouts                 |

---

# One Important Thing Before We Start Coding

We now have the complete chain:

```text
                    PRODUCT REQUIREMENTS
                           │
                           ▼
                    USER STORIES
                           │
                           ▼
                  ACCEPTANCE CRITERIA
                           │
                           ▼
                      TEST CASES
                           │
                           ▼
                     IMPLEMENTATION
```

And we have enough detail to stop requirements discovery.

## What I recommend next

**Do not write the entire application from these 34 stories at once.**

Our immediate next task should be to **slice these stories into the four-day implementation backlog**.

For example:

### Day 1

**Backend foundation + employee side**

* authentication
* employee profile
* departments/designations
* job postings
* search/filter/sort
* job details
* applications

### Day 2

**Application lifecycle + TA backend**

* application status transitions
* withdrawal/reapplication
* job templates
* TA posting management
* deadlines
* automatic closure

### Day 3

**Frontend integration**

* employee UI
* TA UI
* My Applications
* notifications
* UX states/toasts/confirmations

### Day 4

**Testing + polish + Phase 3 compatibility**

* integration testing
* edge cases
* security checks
* compatibility
* recommendation
* documentation/demo preparation

That is the point where **requirements stop and engineering begins**. We shouldn't spend another day trying to make the requirements document prettier.
