import re
import sqlite3


def get_db_connection():
    db = sqlite3.connect('../domains.db')
    return db


def get_domains(cursor) -> list[tuple]:
    cursor.execute('SELECT * FROM DOMAINS')
    return cursor.fetchall()


def extract_rules(domains: list[tuple], regexp: str) -> dict[str, str]:
    rules = {}  # project_id: regexp

    for project_id, name in domains:
        if project_id in rules:
            continue

        rules[project_id] = regexp

    return rules


def set_rules(cursor, rules: dict[str, str]):
    cursor.executemany(
        'INSERT INTO RULES (project_id, regexp) VALUES (?, ?)',
        rules.items(),
    )


def main():
    with get_db_connection() as db:
        cursor = db.cursor()
        domains = get_domains(cursor)
        regexp = r'\.(\w+\.\w+)$'
        rules = extract_rules(domains, regexp)
        set_rules(cursor, rules)
        db.commit()


if __name__ == '__main__':
    main()
