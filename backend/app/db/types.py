from sqlalchemy import String, Text

from app.core.constants import NAME_MAX_LENGTH, SHORT_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH, EMAIL_MAX_LENGTH, EMPLOYEE_CODE_MAX_LENGTH, TOKEN_HASH_MAX_LENGTH

NameType = String(NAME_MAX_LENGTH)
ShortTextType = String(SHORT_TEXT_MAX_LENGTH)
LongTextType = Text(LONG_TEXT_MAX_LENGTH)

EmailType = String(EMAIL_MAX_LENGTH)
EmployeeCodeType = String(EMPLOYEE_CODE_MAX_LENGTH)
TokenHashType = String(TOKEN_HASH_MAX_LENGTH)

LongText = Text