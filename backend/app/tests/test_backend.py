import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Job Hub API is running"


def test_auth_login():
    # Admin login
    res_admin = client.post("/v1/auth/login", json={"email": "ta@jobhub.com", "password": "Password@123"})
    assert res_admin.status_code == 200
    admin_token = res_admin.json()["data"]["access_token"]
    assert admin_token is not None

    # Employee login
    res_emp = client.post("/v1/auth/login", json={"email": "tony@jobhub.com", "password": "tony@123"})
    assert res_emp.status_code == 200
    emp_token = res_emp.json()["data"]["access_token"]
    assert emp_token is not None

    return admin_token, emp_token


def test_skills_crud():
    admin_token, emp_token = test_auth_login()
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_emp = {"Authorization": f"Bearer {emp_token}"}

    # GET skills
    res = client.get("/v1/skills", headers=headers_emp)
    assert res.status_code == 200
    skills = res.json()["data"]
    assert isinstance(skills, list)

    # POST skill as Admin
    res_create = client.post("/v1/skills", json={"name": "Kubernetes"}, headers=headers_admin)
    assert res_create.status_code in (201, 409)
    if res_create.status_code == 201:
        skill_id = res_create.json()["data"]["id"]

        # GET skill by ID
        res_get = client.get(f"/v1/skills/{skill_id}", headers=headers_emp)
        assert res_get.status_code == 200

        # PUT skill as Admin
        res_put = client.put(f"/v1/skills/{skill_id}", json={"name": "K8s & Cloud Native"}, headers=headers_admin)
        assert res_put.status_code == 200
        assert res_put.json()["data"]["name"] == "K8s & Cloud Native"

        # DELETE skill as Admin
        res_del = client.delete(f"/v1/skills/{skill_id}", headers=headers_admin)
        assert res_del.status_code == 204

    # POST skill as Employee should be forbidden
    res_forb = client.post("/v1/skills", json={"name": "Hacking"}, headers=headers_emp)
    assert res_forb.status_code == 403


def test_employee_profile():
    admin_token, emp_token = test_auth_login()
    headers_emp = {"Authorization": f"Bearer {emp_token}"}

    # GET profile
    res = client.get("/v1/employee/me", headers=headers_emp)
    assert res.status_code == 200
    profile = res.json()["data"]
    assert profile["full_name"] == "Tony Stark"
    assert profile["employee_code"] == "EMP001"

    # PUT profile
    res_update = client.put(
        "/v1/employee/me",
        json={"experience_years": 6.0},
        headers=headers_emp,
    )
    assert res_update.status_code == 200


def test_job_posting_discovery_and_rules():
    admin_token, emp_token = test_auth_login()
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_emp = {"Authorization": f"Bearer {emp_token}"}

    # Employee GET job postings (only open active postings)
    res_emp = client.get("/v1/job-postings", headers=headers_emp)
    assert res_emp.status_code == 200
    data = res_emp.json()["data"]["data"]
    for posting in data:
        assert posting["status"] == "open"

    # Search job postings
    res_search = client.get("/v1/job-postings?q=Backend", headers=headers_emp)
    assert res_search.status_code == 200

    # TA create open posting without deadline (should fail)
    res_no_deadline = client.post(
        "/v1/job-postings",
        json={
            "title": "Invalid Open Job",
            "description": "No deadline open job testing validation rule",
            "department_id": data[0]["department_id"],
            "designation_id": data[0]["designation_id"],
            "employment_type": "full_time",
            "experience_years": 3.0,
            "skills": [],
            "status": "open",
            "deadline": None,
        },
        headers=headers_admin,
    )
    assert res_no_deadline.status_code in (400, 422)

    # TA create draft posting
    res_draft = client.post(
        "/v1/job-postings",
        json={
            "title": "Draft QA Tester Role",
            "description": "Temporary draft posting for automated test validation.",
            "department_id": data[0]["department_id"],
            "designation_id": data[0]["designation_id"],
            "employment_type": "full_time",
            "experience_years": 2.0,
            "skills": [],
            "status": "draft",
            "deadline": "2026-12-31T23:59:59Z",
        },
        headers=headers_admin,
    )
    assert res_draft.status_code == 201
    draft_id = res_draft.json()["data"]["id"]

    # TA delete draft posting (should succeed)
    res_del_draft = client.delete(f"/v1/job-postings/{draft_id}", headers=headers_admin)
    assert res_del_draft.status_code == 204


def test_application_workflow_and_notifications():
    admin_token, emp_token = test_auth_login()
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_emp = {"Authorization": f"Bearer {emp_token}"}

    # Get open job posting
    res_jobs = client.get("/v1/job-postings", headers=headers_emp)
    open_jobs = res_jobs.json()["data"]["data"]
    assert len(open_jobs) > 0
    target_job_id = open_jobs[0]["id"]

    # Employee GET my applications
    res_my_apps = client.get("/v1/applications/my-applications", headers=headers_emp)
    assert res_my_apps.status_code == 200

    # TA GET applications for job posting
    res_job_apps = client.get(f"/v1/job-postings/{target_job_id}/applications", headers=headers_admin)
    assert res_job_apps.status_code == 200
    apps = res_job_apps.json()["data"]["data"]

    if len(apps) > 0:
        app_id = apps[0]["id"]

        # TA status transition: Shortlisted -> Interviewed
        res_transition = client.patch(
            f"/v1/applications/{app_id}/status",
            json={"status": "shortlisted"},
            headers=headers_admin,
        )
        assert res_transition.status_code in (200, 400)

    # Check notifications endpoint
    res_notif = client.get("/v1/notifications", headers=headers_emp)
    assert res_notif.status_code == 200

    # Check audit logs endpoint (Admin only)
    res_audit = client.get("/v1/audit-logs", headers=headers_admin)
    assert res_audit.status_code == 200
