# Step 3 — Acceptance Criteria

We don't need to write dozens of repetitive criteria manually. We can make them precise and testable.

I'll demonstrate the structure and then establish criteria for the core stories.

---

## US-004 — Browse Jobs

### Acceptance Criteria

**AC-004-01 — Happy Path**

```gherkin
Given an authenticated employee
And open job postings exist
When the employee opens the job postings page
Then the system displays the open job postings
And each posting displays its relevant summary information
```

**AC-004-02 — No Jobs**

```gherkin
Given an authenticated employee
And no open job postings exist
When the employee opens the job postings page
Then the system displays an appropriate "no open postings" message
```

**AC-004-03 — Closed Jobs**

```gherkin
Given a job posting is closed
When an employee views the open job postings
Then the closed posting is not available for new application
```

---

# US-005 — Search Jobs

```gherkin
Given an authenticated employee
And open job postings exist
When the employee enters a job title search
Then the system displays matching open postings
```

### Unhappy path

```gherkin
Given an authenticated employee
When the employee searches for a title with no matching postings
Then the system displays an appropriate no-results state
```

---

# US-006 — Filter Jobs

```gherkin
Given open job postings exist
When the employee selects a department filter
Then only matching postings are displayed
```

```gherkin
Given open job postings exist
When the employee selects multiple filters
Then the system applies the selected filters together
And displays only postings satisfying the active filter conditions
```

---

# US-007 — Sort Jobs

```gherkin
Given multiple open job postings exist
When the employee sorts by deadline
Then the postings are ordered according to their deadline
```

---

# US-008 — View Job Details

```gherkin
Given an open job posting exists
When the employee opens the posting
Then the system displays all available job-posting details
And the employee can see the Apply action
```

```gherkin
Given salary was not provided by TA
When the employee views the posting
Then the system does not display a salary value
```

---

# US-009 — Apply Directly

```gherkin
Given an employee is viewing an open posting
And the employee does not have an active application for that posting
When the employee selects Apply
Then the system displays an application confirmation
```

```gherkin
Given the employee confirms the application
When the application request succeeds
Then a new application is created
And its status is APPLIED
And the employee receives success feedback
```

---

# US-011 — Duplicate Application

```gherkin
Given an employee already has an active application for a posting
When the employee views that posting
Then the Apply action is disabled
```

### Backend protection

```gherkin
Given an employee already has an active application
When the employee sends another application request
Then the backend rejects the request
And no duplicate active application is created
```

---

# US-012 — Withdraw

```gherkin
Given an employee has an application with status APPLIED
When the employee selects Withdraw
Then the system asks for confirmation
```

```gherkin
Given the employee confirms withdrawal
When the withdrawal succeeds
Then the application's status becomes WITHDRAWN
And the application remains in application history
```

### Invalid case

```gherkin
Given an application has status SELECTED
When the employee attempts to withdraw it
Then the withdrawal is rejected
And the application remains SELECTED
```

---

# US-013 — Reapply

```gherkin
Given an employee previously withdrew an application
And the employee has not reached the three-reapplication limit
When the employee applies again
Then a new application is created
And its status is APPLIED
```

### Limit

```gherkin
Given an employee has already used three reapplications for a posting
When the employee attempts another application
Then the system rejects the application
And no new application is created
```

---

# US-014 — My Applications

```gherkin
Given an authenticated employee
When the employee opens My Applications
Then the system displays only that employee's applications
And displays each application's status
And displays the associated posting information
And displays the applied date
And displays the posting deadline
```

---

# US-016 — Create Posting

```gherkin
Given an authenticated TA
When the TA provides all required job-posting information
And submits the posting
Then the system creates the posting successfully
And displays success feedback
```

### Validation

```gherkin
Given an authenticated TA
When the TA attempts to create an open posting without a deadline
Then the system rejects the request
And identifies the missing deadline
```

---

# US-017 — Create From Template

```gherkin
Given an authenticated TA
And a job template exists
When the TA selects the template while creating a posting
Then the template information populates the posting form
```

```gherkin
Given template information has populated the posting
When the TA modifies one or more fields
And saves the posting
Then the modified values are stored on the posting
```

---

# US-019 — Manage Postings

```gherkin
Given an authenticated TA
When the TA requests job postings
Then the system returns postings accessible to the TA
```

```gherkin
Given a draft posting exists
When the TA deletes it
Then the draft posting is removed
```

---

# US-022 — Automatic Closure

```gherkin
Given an open posting has reached its deadline
When the deadline-processing mechanism executes
Then the posting status becomes CLOSED
And employees can no longer submit new applications
And existing applications remain associated with the posting
And TA receives a closure notification
```

---

# US-023 — Reopen

```gherkin
Given a posting is CLOSED
When an authorized TA provides a new valid deadline
And reopens the posting
Then the posting status becomes OPEN
And employees can apply again
And existing applications remain associated with the posting
```

---

# US-024 — Complete

```gherkin
Given a posting is CLOSED
And every associated application is SELECTED, REJECTED, or WITHDRAWN
When TA marks the posting completed
Then the posting status becomes COMPLETED
```

### Unhappy path

```gherkin
Given a posting has an application in UNDER_REVIEW
When TA attempts to mark the posting COMPLETED
Then the system rejects the operation
And the posting remains CLOSED
```

---

# US-026 — Update Application Status

```gherkin
Given an authenticated TA
And an application is APPLIED
When TA changes the status to SHORTLISTED
Then the application status becomes SHORTLISTED
And the employee receives a notification
```

### Invalid transition

```gherkin
Given an application is REJECTED
When TA attempts to change it to SHORTLISTED
Then the system rejects the transition
And the application remains REJECTED
```

---

# US-028 — Employee Notifications

```gherkin
Given an employee's application becomes SHORTLISTED
When the status change is successfully processed
Then the employee receives a notification
```

Equivalent behavior applies to:

* Interview
* Selected
* Rejected

---

# US-029 — Deadline Reminder

```gherkin
Given an open posting has a configured deadline reminder
When the configured reminder time is reached
Then the TA receives a deadline reminder
```

---

# US-032 — Employee Profile

```gherkin
Given an employee profile exists
When the system retrieves the employee profile
Then it contains the employee's required professional information
And skills are stored with their associated levels
And experience is represented as a decimal number
```

---

