from typing import Any


def merge_skills(existing_skills: list | None, new_skills: list | None) -> list:
    """
    Merges incoming new_skills into existing_skills according to business rules:
    - If new_skills is an empty array `[]`, clears all existing skills and returns `[]`.
    - If a skill ID in new_skills already exists in existing_skills, updates its skill level in place.
    - If a skill ID in new_skills is new (not in existing_skills), appends it to the end of existing_skills.
    - Preserves all other existing skills and their order.
    """
    if new_skills is None:
        return existing_skills or []

    if len(new_skills) == 0:
        return []

    result: list[dict[str, Any]] = []
    if existing_skills:
        for item in existing_skills:
            if isinstance(item, dict):
                result.append({str(k): (v.value if hasattr(v, "value") else v) for k, v in item.items()})

    for new_skill_dict in new_skills:
        for raw_id, raw_level in new_skill_dict.items():
            skill_id = str(raw_id)
            level = (
                raw_level.value
                if hasattr(raw_level, "value")
                else (int(raw_level) if isinstance(raw_level, int) or (isinstance(raw_level, str) and raw_level.isdigit()) else raw_level)
            )

            found = False
            for existing_item in result:
                if skill_id in existing_item:
                    existing_item[skill_id] = level
                    found = True
                    break

            if not found:
                result.append({skill_id: level})

    return result
