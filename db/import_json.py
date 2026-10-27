import json

from db.database import get_connection


ATHLETES_FILE = "data/athletes.json"
DISCIPLINES_FILE = "data/disciplines.json"
COMPETITIONS_FILE = "data/competitions.json"
RESULTS_FILE = "data/results.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_athletes(conn):
    athletes = load_json(ATHLETES_FILE)

    conn.executemany(
        """
        INSERT INTO athletes (
            id,
            full_name,
            birth_year
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                athlete["id"],
                athlete["full_name"],
                athlete["birth_year"],
            )
            for athlete in athletes
        ],
    )


def import_disciplines(conn):
    disciplines = load_json(DISCIPLINES_FILE)

    conn.executemany(
        """
        INSERT INTO disciplines (
            id,
            name,
            unit
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                discipline["id"],
                discipline["name"],
                discipline["unit"],
            )
            for discipline in disciplines
        ],
    )


def import_competitions(conn):
    competitions = load_json(COMPETITIONS_FILE)

    conn.executemany(
        """
        INSERT INTO competitions (
            id,
            name,
            date
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                competition["id"],
                competition["name"],
                competition["date"],
            )
            for competition in competitions
        ],
    )


def import_results(conn):
    results = load_json(RESULTS_FILE)

    conn.executemany(
        """
        INSERT INTO results (
            id,
            athlete_id,
            discipline_id,
            competition_id,
            result,
            place,
            standard
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                result["id"],
                result["athlete_id"],
                result["discipline_id"],
                result["competition_id"],
                result["result"],
                result["place"],
                result["standard"],
            )
            for result in results
        ],
    )


def clear_database(conn):
    conn.execute("DELETE FROM results")
    conn.execute("DELETE FROM competitions")
    conn.execute("DELETE FROM disciplines")
    conn.execute("DELETE FROM athletes")


def main():
    conn = get_connection()

    try:
        clear_database(conn)

        import_athletes(conn)
        import_disciplines(conn)
        import_competitions(conn)
        import_results(conn)

        conn.commit()

        print("Данные успешно перенесены из JSON в SQLite.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
