import json
import urllib.error
import urllib.request

BASE_URL = "http://localhost:8000/v1"


def make_request(url, method="GET", data=None, token=None):
    full_url = f"{BASE_URL}{url}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(full_url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            resp_body = resp.read().decode("utf-8")
            return resp.status, json.loads(resp_body) if resp_body else None
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        return e.code, json.loads(err_body) if err_body else None


def run_all_tests():
    print("================ LIVE API ENDPOINT E2E TESTS ================")

    # 1. Login Admin / TA
    status, res = make_request("/auth/login", method="POST", data={"email": "ta@jobhub.com", "password": "Password@123"})
    assert status == 200, f"Admin login failed: {res}"
    admin_token = res["data"]["access_token"]
    print("✔ 1. TA Admin Login successful")

    # 2. Login Employee
    status, res = make_request("/auth/login", method="POST", data={"email": "tony@jobhub.com", "password": "tony@123"})
    assert status == 200, f"Employee login failed: {res}"
    emp_token = res["data"]["access_token"]
    print("✔ 2. Employee Login successful")

    # 3. Employee Profile
    status, res = make_request("/employee/me", method="GET", token=emp_token)
    assert status == 200, f"Get employee profile failed: {res}"
    assert res["data"]["full_name"] == "Tony Stark"
    print(f"✔ 3. Employee Profile retrieved: {res['data']['full_name']} ({res['data']['employee_code']})")

    # Update Employee Profile
    status, res = make_request("/employee/me", method="PUT", data={"experience_years": 6.5}, token=emp_token)
    assert status == 200, f"Update employee profile failed: {res}"
    assert float(res["data"]["experience_years"]) == 6.5
    print("✔ 4. Employee Profile experience updated to 6.5 years")

    # 4. Departments & Designations & Skills
    status, res = make_request("/departments", method="GET", token=emp_token)
    assert status == 200 and len(res["data"]) > 0
    print(f"✔ 5. Departments list retrieved ({len(res['data'])} departments)")

    status, res = make_request("/designations", method="GET", token=emp_token)
    assert status == 200 and len(res["data"]) > 0
    print(f"✔ 6. Designations list retrieved ({len(res['data'])} designations)")

    status, res = make_request("/skills", method="GET", token=emp_token)
    assert status == 200 and len(res["data"]) > 0
    skills = res["data"]
    print(f"✔ 7. Skills list retrieved ({len(skills)} skills)")

    # 5. Skill CRUD (Admin only)
    status, res = make_request("/skills", method="POST", data={"name": "GraphQL"}, token=admin_token)
    assert status in (201, 409), f"Skill creation failed: {res}"
    if status == 201:
        skill_id = res["data"]["id"]
        print(f"✔ 8. Admin created new skill: GraphQL (ID: {skill_id})")

        status, res = make_request(f"/skills/{skill_id}", method="PUT", data={"name": "GraphQL & Subscriptions"}, token=admin_token)
        assert status == 200
        print("✔ 9. Admin updated skill name")

        status, res = make_request(f"/skills/{skill_id}", method="DELETE", token=admin_token)
        assert status in (200, 204)
        print("✔ 10. Admin soft-deleted skill")

    # 6. Job Posting Discovery & Search & Filter
    status, res = make_request("/job-postings", method="GET", token=emp_token)
    assert status == 200, f"GET /job-postings failed: {res}"
    open_jobs = res["data"]["data"]
    print(f"✔ 11. Employee job discovery returned {len(open_jobs)} open postings")

    status, res = make_request("/job-postings?q=Backend", method="GET", token=emp_token)
    assert status == 200
    print(f"✔ 12. Text search for 'Backend' returned {len(res['data']['data'])} matching postings")

    # TA create open posting without deadline (validation check)
    dept_id = open_jobs[0]["department_id"]
    desig_id = open_jobs[0]["designation_id"]
    status, res = make_request(
        "/job-postings",
        method="POST",
        data={
            "title": "Invalid Open Job",
            "description": "Validation test for mandatory deadline on open job posting",
            "department_id": dept_id,
            "designation_id": desig_id,
            "employment_type": "full_time",
            "experience_years": 3.0,
            "skills": [],
            "status": "open",
            "deadline": None,
        },
        token=admin_token,
    )
    assert status in (400, 422), f"Expected validation failure for open job without deadline, got status {status}"
    print("✔ 13. System rejected open posting without deadline (Validation rule enforced)")

    # TA create draft posting
    status, res = make_request(
        "/job-postings",
        method="POST",
        data={
            "title": "Temporary Test Draft Posting",
            "description": "Draft posting for testing soft deletion rule",
            "department_id": dept_id,
            "designation_id": desig_id,
            "employment_type": "full_time",
            "experience_years": 2.0,
            "skills": [],
            "status": "draft",
            "deadline": "2026-12-31T23:59:59Z",
        },
        token=admin_token,
    )
    assert status == 201, f"Create draft posting failed: {res}"
    draft_id = res["data"]["id"]
    print(f"✔ 14. TA created draft job posting (ID: {draft_id})")

    # TA delete draft posting
    status, res = make_request(f"/job-postings/{draft_id}", method="DELETE", token=admin_token)
    assert status == 204
    print("✔ 15. TA successfully soft-deleted draft job posting")

    # 7. Job Application Workflow
    status, res = make_request("/applications/my-applications", method="GET", token=emp_token)
    assert status == 200
    print(f"✔ 16. Employee retrieved 'My Applications' ({len(res['data']['data'])} applications)")

    # TA view job applications
    target_job_id = open_jobs[0]["id"]
    status, res = make_request(f"/job-postings/{target_job_id}/applications", method="GET", token=admin_token)
    assert status == 200
    job_apps = res["data"]["data"]
    print(f"✔ 17. TA retrieved candidate applications for job posting ({len(job_apps)} candidates)")

    if len(job_apps) > 0:
        app_id = job_apps[0]["id"]
        curr_status = job_apps[0]["status"]
        if curr_status == "applied":
            status, res = make_request(
                f"/applications/{app_id}/status",
                method="PATCH",
                data={"status": "under_review"},
                token=admin_token,
            )
            assert status == 200
            print("✔ 18. TA updated application status: APPLIED -> UNDER_REVIEW")

            # Try invalid state transition (UNDER_REVIEW -> SELECTED)
            status, res = make_request(
                f"/applications/{app_id}/status",
                method="PATCH",
                data={"status": "selected"},
                token=admin_token,
            )
            assert status == 400
            print("✔ 19. System rejected invalid status transition (UNDER_REVIEW -> SELECTED)")

    # 8. Notifications & Audit Logs
    status, res = make_request("/notifications", method="GET", token=emp_token)
    assert status == 200
    print(f"✔ 20. Employee retrieved notifications ({len(res['data']['data'])} notifications)")

    status, res = make_request("/audit-logs", method="GET", token=admin_token)
    assert status == 200
    print(f"✔ 21. TA Admin retrieved audit logs ({len(res['data']['data'])} audit trail events)")

    print("================ ALL LIVE E2E TESTS PASSED 100%! ================")


if __name__ == "__main__":
    run_all_tests()
