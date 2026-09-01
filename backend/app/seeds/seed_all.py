import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import app.db.base
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.application import Application
from app.models.department import Department
from app.models.designation import Designation
from app.models.employee import Employee
from app.models.enums import ApplicationStatus, EmploymentType, JobPostingStatus, SkillLevel, UserRole
from app.models.job_posting import JobPosting
from app.models.job_template import JobTemplate
from app.models.skill import Skill
from app.models.user import User


def run_seeds():
    db: Session = SessionLocal()
    try:
        print("--- Starting database seeding ---")

        # 1. Departments
        departments_data = ["Engineering", "Product", "Marketing", "HR", "Finance", "Data Science"]
        dept_map = {}
        for name in departments_data:
            dept = db.query(Department).filter(Department.name == name).first()
            if not dept:
                dept = Department(name=name)
                db.add(dept)
                db.flush()
                print(f"Created Department: {name}")
            dept_map[name] = dept

        # 2. Designations
        designations_data = [
            "Software Engineer",
            "Senior Software Engineer",
            "Tech Lead",
            "Product Manager",
            "Data Analyst",
            "HR Specialist",
        ]
        desig_map = {}
        for name in designations_data:
            desig = db.query(Designation).filter(Designation.name == name).first()
            if not desig:
                desig = Designation(name=name)
                db.add(desig)
                db.flush()
                print(f"Created Designation: {name}")
            desig_map[name] = desig

        # 3. Skills
        skills_data = [
            "Python",
            "FastAPI",
            "React",
            "PostgreSQL",
            "Docker",
            "Machine Learning",
            "System Design",
            "Communication",
        ]
        skill_map = {}
        for name in skills_data:
            skill = db.query(Skill).filter(Skill.name == name, Skill.deleted_at.is_(None)).first()
            if not skill:
                skill = Skill(name=name)
                db.add(skill)
                db.flush()
                print(f"Created Skill: {name}")
            skill_map[name] = skill

        # Commit foundation lookup data
        db.commit()

        # 4. TA / Admin User
        admin_email = "ta@jobhub.com"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_user = User(
                email=admin_email,
                password_hash=get_password_hash("Password@123"),
                role=UserRole.ADMIN,
            )
            db.add(admin_user)
            db.flush()
            print(f"Created TA Admin: {admin_email}")

        # 5. Employees
        employees_data = [
            {
                "email": "tony@jobhub.com",
                "password": "tony@123",
                "full_name": "Tony Stark",
                "code": "EMP001",
                "dept": "Engineering",
                "desig": "Senior Software Engineer",
                "exp": Decimal("5.5"),
                "skills": [
                    {str(skill_map["Python"].id): 5},
                    {str(skill_map["FastAPI"].id): 4},
                    {str(skill_map["PostgreSQL"].id): 4},
                    {str(skill_map["System Design"].id): 4},
                ],
            },
            {
                "email": "sarah@jobhub.com",
                "password": "sarah@123",
                "full_name": "Sarah Connor",
                "code": "EMP002",
                "dept": "Engineering",
                "desig": "Tech Lead",
                "exp": Decimal("8.0"),
                "skills": [
                    {str(skill_map["System Design"].id): 5},
                    {str(skill_map["Docker"].id): 4},
                    {str(skill_map["Python"].id): 4},
                ],
            },
            {
                "email": "alex@jobhub.com",
                "password": "alex@123",
                "full_name": "Alex Mercer",
                "code": "EMP003",
                "dept": "Product",
                "desig": "Product Manager",
                "exp": Decimal("4.0"),
                "skills": [
                    {str(skill_map["Communication"].id): 5},
                ],
            },
        ]

        employee_user_map = {}
        for emp in employees_data:
            user = db.query(User).filter(User.email == emp["email"]).first()
            if not user:
                user = User(
                    email=emp["email"],
                    password_hash=get_password_hash(emp["password"]),
                    role=UserRole.USER,
                )
                db.add(user)
                db.flush()

                employee_record = Employee(
                    id=user.id,
                    full_name=emp["full_name"],
                    employee_code=emp["code"],
                    department_id=dept_map[emp["dept"]].id,
                    designation_id=desig_map[emp["desig"]].id,
                    experience_years=emp["exp"],
                    skills=emp["skills"],
                )
                db.add(employee_record)
                db.flush()
                print(f"Created Employee: {emp['full_name']} ({emp['email']})")
            employee_user_map[emp["email"]] = user

        db.commit()

        # 6. Job Templates
        templates_data = [
            {
                "name": "Senior Backend Template",
                "title": "Senior Backend Engineer",
                "description": "Template for recruiting Senior Backend Engineers with Python & PostgreSQL expertise.",
                "desig": "Senior Software Engineer",
                "emp_type": EmploymentType.FULL_TIME,
                "exp": Decimal("5.0"),
                "salary": Decimal("120000.00"),
                "skills": [
                    {str(skill_map["Python"].id): 4},
                    {str(skill_map["FastAPI"].id): 4},
                    {str(skill_map["PostgreSQL"].id): 4},
                ],
            },
            {
                "name": "Frontend Specialist Template",
                "title": "Frontend Specialist",
                "description": "Template for hiring skilled Frontend Developers.",
                "desig": "Software Engineer",
                "emp_type": EmploymentType.FULL_TIME,
                "exp": Decimal("3.0"),
                "salary": Decimal("95000.00"),
                "skills": [
                    {str(skill_map["React"].id): 4},
                ],
            },
        ]

        for t in templates_data:
            tmpl = db.query(JobTemplate).filter(JobTemplate.name == t["name"]).first()
            if not tmpl:
                tmpl = JobTemplate(
                    name=t["name"],
                    title=t["title"],
                    description=t["description"],
                    designation_id=desig_map[t["desig"]].id,
                    employment_type=t["emp_type"],
                    experience_years=t["exp"],
                    skills=t["skills"],
                    salary=t["salary"],
                    created_by=admin_user.id,
                )
                db.add(tmpl)
                print(f"Created Job Template: {t['name']}")

        db.commit()

        # 7. Job Postings
        now = datetime.now(timezone.utc)
        postings_data = [
            {
                "title": "Senior Backend Engineer",
                "description": "We are seeking an experienced Senior Backend Engineer to lead cloud API development.",
                "dept": "Engineering",
                "desig": "Senior Software Engineer",
                "location": "Remote / New York",
                "emp_type": EmploymentType.FULL_TIME,
                "exp": Decimal("5.0"),
                "salary": Decimal("130000.00"),
                "deadline": now + timedelta(days=14),
                "deadline_reminder_at": now + timedelta(days=13),
                "status": JobPostingStatus.OPEN,
                "skills": [
                    {str(skill_map["Python"].id): 4},
                    {str(skill_map["FastAPI"].id): 4},
                    {str(skill_map["PostgreSQL"].id): 4},
                ],
            },
            {
                "title": "Frontend React Developer",
                "description": "Join our product team to build interactive UI components using React and modern CSS.",
                "dept": "Engineering",
                "desig": "Software Engineer",
                "location": "San Francisco, CA",
                "emp_type": EmploymentType.FULL_TIME,
                "exp": Decimal("2.5"),
                "salary": Decimal("100000.00"),
                "deadline": now + timedelta(days=7),
                "deadline_reminder_at": now + timedelta(days=6),
                "status": JobPostingStatus.OPEN,
                "skills": [
                    {str(skill_map["React"].id): 4},
                ],
            },
            {
                "title": "Data Platform Architect",
                "description": "Draft posting for upcoming Data Platform Architect role.",
                "dept": "Data Science",
                "desig": "Tech Lead",
                "location": "Remote",
                "emp_type": EmploymentType.FULL_TIME,
                "exp": Decimal("7.0"),
                "salary": Decimal("150000.00"),
                "deadline": now + timedelta(days=30),
                "deadline_reminder_at": now + timedelta(days=29),
                "status": JobPostingStatus.DRAFT,
                "skills": [
                    {str(skill_map["Python"].id): 5},
                    {str(skill_map["Machine Learning"].id): 4},
                ],
            },
        ]

        created_postings = {}
        for p in postings_data:
            posting = db.query(JobPosting).filter(JobPosting.title == p["title"]).first()
            if not posting:
                posting = JobPosting(
                    title=p["title"],
                    description=p["description"],
                    department_id=dept_map[p["dept"]].id,
                    designation_id=desig_map[p["desig"]].id,
                    location=p["location"],
                    employment_type=p["emp_type"],
                    experience_years=p["exp"],
                    skills=p["skills"],
                    salary=p["salary"],
                    deadline=p["deadline"],
                    deadline_reminder_at=p["deadline_reminder_at"],
                    status=p["status"],
                    created_by=admin_user.id,
                )
                db.add(posting)
                db.flush()
                print(f"Created Job Posting: {p['title']} [{p['status'].value}]")
            created_postings[p["title"]] = posting

        db.commit()

        # 8. Applications
        backend_job = created_postings.get("Senior Backend Engineer")
        frontend_job = created_postings.get("Frontend React Developer")

        if backend_job:
            # Tony applied
            tony_user = employee_user_map["tony@jobhub.com"]
            app1 = (
                db.query(Application)
                .filter(
                    Application.employee_id == tony_user.id,
                    Application.job_posting_id == backend_job.id,
                )
                .first()
            )
            if not app1:
                app1 = Application(
                    employee_id=tony_user.id,
                    job_posting_id=backend_job.id,
                    status=ApplicationStatus.APPLIED,
                )
                db.add(app1)
                print("Created Application: Tony Stark -> Senior Backend Engineer (APPLIED)")

        if frontend_job:
            # Sarah shortlisted
            sarah_user = employee_user_map["sarah@jobhub.com"]
            app2 = (
                db.query(Application)
                .filter(
                    Application.employee_id == sarah_user.id,
                    Application.job_posting_id == frontend_job.id,
                )
                .first()
            )
            if not app2:
                app2 = Application(
                    employee_id=sarah_user.id,
                    job_posting_id=frontend_job.id,
                    status=ApplicationStatus.SHORTLISTED,
                )
                db.add(app2)
                print("Created Application: Sarah Connor -> Frontend React Developer (SHORTLISTED)")

        db.commit()
        print("--- Database seeding completed successfully! ---")

    except Exception as exc:
        db.rollback()
        print(f"Error during seeding: {exc}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
