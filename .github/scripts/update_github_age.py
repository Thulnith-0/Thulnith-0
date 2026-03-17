from datetime import datetime, timezone
from pathlib import Path

README_PATH = Path("README.md")

# Your GitHub account creation date from the API
CREATED_AT = datetime(2024, 11, 30, 14, 57, 6, tzinfo=timezone.utc)

def diff_ymd(start: datetime, end: datetime):
    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day

    if days < 0:
        # borrow days from previous month
        if end.month == 1:
            prev_month = 12
            prev_year = end.year - 1
        else:
            prev_month = end.month - 1
            prev_year = end.year

        if prev_month in {1, 3, 5, 7, 8, 10, 12}:
            days_in_prev_month = 31
        elif prev_month in {4, 6, 9, 11}:
            days_in_prev_month = 30
        else:
            # February
            is_leap = (prev_year % 4 == 0 and prev_year % 100 != 0) or (prev_year % 400 == 0)
            days_in_prev_month = 29 if is_leap else 28

        days += days_in_prev_month
        months -= 1

    if months < 0:
        months += 12
        years -= 1

    return years, months, days

def format_age(years: int, months: int, days: int) -> str:
    parts = []

    if years == 1:
        parts.append("1 year")
    elif years != 0:
        parts.append(f"{years} years")

    if months == 1:
        parts.append("1 month")
    elif months != 0:
        parts.append(f"{months} months")

    if days == 1:
        parts.append("1 day")
    elif days != 0:
        parts.append(f"{days} days")

    if not parts:
        return "0 days"

    return ", ".join(parts)

def main():
    now = datetime.now(timezone.utc)
    years, months, days = diff_ymd(CREATED_AT, now)
    age_text = format_age(years, months, days)

    content = README_PATH.read_text(encoding="utf-8")
    updated = content.replace(
        "📅 GitHub Age: **AUTO_GITHUB_AGE**",
        f"📅 GitHub Age: **{age_text}**"
    )

    # Also update existing generated line if it already exists
    import re
    updated = re.sub(
        r"📅 GitHub Age: \*\*.*?\*\*",
        f"📅 GitHub Age: **{age_text}**",
        updated
    )

    README_PATH.write_text(updated, encoding="utf-8")
    print(f"Updated GitHub age to: {age_text}")

if __name__ == "__main__":
    main()
