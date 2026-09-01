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


def test_skills_update_logic():
    print("================ TESTING SKILLS UPDATE LOGIC ================")

    # 1. Login
    _, res = make_request("/auth/login", method="POST", data={"email": "ta@jobhub.com", "password": "Password@123"})
    admin_token = res["data"]["access_token"]

    _, res = make_request("/auth/login", method="POST", data={"email": "tony@jobhub.com", "password": "tony@123"})
    emp_token = res["data"]["access_token"]

    # Retrieve 3 skill IDs for testing
    _, res = make_request("/skills", method="GET", token=emp_token)
    skills_list = res["data"]
    s1_id, s2_id, s3_id = skills_list[0]["id"], skills_list[1]["id"], skills_list[2]["id"]

    # -------------------------------------------------------------
    # A. EMPLOYEE PROFILE SKILLS UPDATE TESTS
    # -------------------------------------------------------------
    print("\n--- A. Testing Employee Profile Skills Update ---")

    # Step 1: Set initial skills [s1: 2, s2: 3]
    status, res = make_request(
        "/employee/me",
        method="PUT",
        data={"skills": [{s1_id: 2}, {s2_id: 3}]},
        token=emp_token,
    )
    # Note: If initial state had skills, let's reset first with []
    status, res = make_request("/employee/me", method="PUT", data={"skills": []}, token=emp_token)
    assert status == 200 and res["data"]["skills"] == []
    print("✔ Empty array [] clears all existing employee skills")

    status, res = make_request(
        "/employee/me",
        method="PUT",
        data={"skills": [{s1_id: 2}, {s2_id: 3}]},
        token=emp_token,
    )
    assert status == 200
    emp_skills = res["data"]["skills"]
    assert len(emp_skills) == 2
    assert s1_id in emp_skills[0] and emp_skills[0][s1_id] == 2
    assert s2_id in emp_skills[1] and emp_skills[1][s2_id] == 3
    print("✔ Set initial employee skills [s1: 2, s2: 3]")

    # Step 2: Add a new skill s3: 5 (should be inserted at the end)
    status, res = make_request(
        "/employee/me",
        method="PUT",
        data={"skills": [{s3_id: 5}]},
        token=emp_token,
    )
    assert status == 200
    emp_skills = res["data"]["skills"]
    assert len(emp_skills) == 3
    assert s1_id in emp_skills[0] and emp_skills[0][s1_id] == 2
    assert s2_id in emp_skills[1] and emp_skills[1][s2_id] == 3
    assert s3_id in emp_skills[2] and emp_skills[2][s3_id] == 5
    print("✔ Added new skill s3: 5 -> inserted at the end")

    # Step 3: Update level of existing skill s1: 4 (level updated in place)
    status, res = make_request(
        "/employee/me",
        method="PUT",
        data={"skills": [{s1_id: 4}]},
        token=emp_token,
    )
    assert status == 200
    emp_skills = res["data"]["skills"]
    assert len(emp_skills) == 3
    assert s1_id in emp_skills[0] and emp_skills[0][s1_id] == 4  # Level updated in place!
    assert s2_id in emp_skills[1] and emp_skills[1][s2_id] == 3
    assert s3_id in emp_skills[2] and emp_skills[2][s3_id] == 5
    print("✔ Updated level of existing skill s1: 4 in place")

    # Step 4: Omit skills field in request body -> no changes made to skills
    status, res = make_request(
        "/employee/me",
        method="PUT",
        data={"experience_years": 7.0},
        token=emp_token,
    )
    assert status == 200
    emp_skills = res["data"]["skills"]
    assert len(emp_skills) == 3
    assert s1_id in emp_skills[0] and emp_skills[0][s1_id] == 4
    print("✔ Omitted skills field -> skills section unchanged")

    # Fetch valid department and designation IDs
    _, res = make_request("/departments", method="GET", token=emp_token)
    dept_id = res["data"][0]["id"]
    _, res = make_request("/designations", method="GET", token=emp_token)
    desig_id = res["data"][0]["id"]

    # -------------------------------------------------------------
    # B. JOB TEMPLATE SKILLS UPDATE TESTS
    # -------------------------------------------------------------
    print("\n--- B. Testing Job Template Skills Update ---")

    import time
    ts = int(time.time())

    # Create job template
    status, res = make_request(
        "/job-templates",
        method="POST",
        data={
            "name": f"Skills Test Template {ts}",
            "title": "Skills Test Engineer",
            "description": "Template for skill merging tests",
            "designation_id": desig_id,
            "employment_type": "full_time",
            "experience_years": 3.0,
            "skills": [{s1_id: 1}, {s2_id: 2}],
        },
        token=admin_token,
    )
    assert status in (200, 201), f"Create job template failed: {res}"
    tmpl_id = res["data"]["id"]
    print("✔ Created job template with initial skills [s1: 1, s2: 2]")

    # Add new skill s3: 4
    status, res = make_request(
        f"/job-templates/{tmpl_id}",
        method="PUT",
        data={"skills": [{s3_id: 4}]},
        token=admin_token,
    )
    assert status == 200
    tmpl_skills = res["data"]["skills"]
    assert len(tmpl_skills) == 3
    assert s1_id in tmpl_skills[0] and tmpl_skills[0][s1_id] == 1
    assert s2_id in tmpl_skills[1] and tmpl_skills[1][s2_id] == 2
    assert s3_id in tmpl_skills[2] and tmpl_skills[2][s3_id] == 4
    print("✔ Template: Added new skill s3: 4 -> inserted at the end")

    # Update level of s2: 5
    status, res = make_request(
        f"/job-templates/{tmpl_id}",
        method="PUT",
        data={"skills": [{s2_id: 5}]},
        token=admin_token,
    )
    assert status == 200
    tmpl_skills = res["data"]["skills"]
    assert len(tmpl_skills) == 3
    assert s2_id in tmpl_skills[1] and tmpl_skills[1][s2_id] == 5
    print("✔ Template: Updated s2: 5 in place")

    # Clear skills with []
    status, res = make_request(
        f"/job-templates/{tmpl_id}",
        method="PUT",
        data={"skills": []},
        token=admin_token,
    )
    assert status == 200
    assert res["data"]["skills"] == []
    print("✔ Template: Empty array [] cleared all skills")

    # Clean up test template
    make_request(f"/job-templates/{tmpl_id}", method="DELETE", token=admin_token)

    # -------------------------------------------------------------
    # C. JOB POSTING SKILLS UPDATE TESTS
    # -------------------------------------------------------------
    print("\n--- C. Testing Job Posting Skills Update ---")

    # Create draft posting
    status, res = make_request(
        "/job-postings",
        method="POST",
        data={
            "title": f"Skills Test Job Posting {ts}",
            "description": "Job posting for skill merging tests",
            "department_id": dept_id,
            "designation_id": desig_id,
            "employment_type": "full_time",
            "experience_years": 3.0,
            "skills": [{s1_id: 2}, {s2_id: 3}],
            "status": "draft",
            "deadline": "2026-12-31T23:59:59Z",
        },
        token=admin_token,
    )
    assert status in (200, 201), f"Create job posting failed: {res}"
    job_id = res["data"]["id"]
    print("✔ Created job posting with initial skills [s1: 2, s2: 3]")

    # Add new skill s3: 4
    status, res = make_request(
        f"/job-postings/{job_id}",
        method="PUT",
        data={"skills": [{s3_id: 4}]},
        token=admin_token,
    )
    assert status == 200
    job_skills = res["data"]["skills"]
    assert len(job_skills) == 3
    assert s1_id in job_skills[0] and job_skills[0][s1_id] == 2
    assert s2_id in job_skills[1] and job_skills[1][s2_id] == 3
    assert s3_id in job_skills[2] and job_skills[2][s3_id] == 4
    print("✔ Job Posting: Added new skill s3: 4 -> inserted at the end")

    # Update level of s1: 5
    status, res = make_request(
        f"/job-postings/{job_id}",
        method="PUT",
        data={"skills": [{s1_id: 5}]},
        token=admin_token,
    )
    assert status == 200
    job_skills = res["data"]["skills"]
    assert len(job_skills) == 3
    assert s1_id in job_skills[0] and job_skills[0][s1_id] == 5
    print("✔ Job Posting: Updated s1: 5 in place")

    # Clear skills with []
    status, res = make_request(
        f"/job-postings/{job_id}",
        method="PUT",
        data={"skills": []},
        token=admin_token,
    )
    assert status == 200
    assert res["data"]["skills"] == []
    print("✔ Job Posting: Empty array [] cleared all skills")

    # Clean up test posting
    make_request(f"/job-postings/{job_id}", method="DELETE", token=admin_token)

    print("\n================ ALL SKILLS UPDATE TESTS PASSED! ================")


if __name__ == "__main__":
    test_skills_update_logic()
