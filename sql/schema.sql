-- ==========================================
-- Sports Results: структура базы данных
-- ==========================================

CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS disciplines (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    unit TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS competitions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY,
    athlete_id INTEGER NOT NULL,
    discipline_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    result REAL NOT NULL,
    place INTEGER NOT NULL,
    standard REAL NOT NULL,
    FOREIGN KEY (athlete_id) REFERENCES athletes(id),
    FOREIGN KEY (discipline_id) REFERENCES disciplines(id),
    FOREIGN KEY (competition_id) REFERENCES competitions(id)
);
