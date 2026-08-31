from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"

class JobPostingStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"
    COMPLETED = "completed"
    
class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    INTERVIEWED = "interviewed"
    REJECTED = "rejected"
    SELECTED = "selected"
    WITHDRAWN = "withdrawn"
    
class NotificationType(str, Enum):
    APPLICATION_SHORTLISTED = "application_shortlisted"
    APPLICATION_REJECTED = "application_rejected"
    APPLICATION_SELECTED = "application_selected"
    JOB_POSTING_CLOSED = "job_posting_closed"
    DEADLINE_REMINDER = "deadline_reminder"
    
class SkillLevel(int, Enum):
    BEGINNER = 1
    ADVANCED = 2
    COMPETENT = 3
    PROFICIENT = 4
    EXPERT = 5
    
class NotificationEntityType(str, Enum):
    JOB_POSTING = "job_postings"
    APPLICATION = "applications"