from app.db.base_class import Base

from app.models.application import Application
from app.models.department import Department
from app.models.designation import Designation
from app.models.employee import Employee
from app.models.job_posting import JobPosting
from app.models.job_template import JobTemplate
from app.models.notification import Notification
from app.models.skill import Skill
from app.models.user import User

__all__ = ["Base", "Application", "Department", "Designation", "Employee", "JobPosting", "JobTemplate", "Notification", "Skill", "User"]