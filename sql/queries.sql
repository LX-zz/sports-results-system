-- ==========================================
-- Sports Results: SQL-запросы ПР7
-- ==========================================


-- 1. Список всех спортсменов
SELECT
    id,
    full_name,
    birth_year
FROM athletes
ORDER BY full_name;


-- 2. Список всех соревнований
SELECT
    id,
    name,
    date
FROM competitions
ORDER BY date;


-- 3. Спортсмены, родившиеся не раньше 2006 года
SELECT
    id,
    full_name,
    birth_year
FROM athletes
WHERE birth_year >= 2006
ORDER BY birth_year, full_name;


-- 4. Результаты с первым или вторым местом
SELECT
    id,
    athlete_id,
    result,
    place
FROM results
WHERE place <= 2
ORDER BY place;


-- 5. Полная информация о спортивных результатах
SELECT
    results.id,
    athletes.full_name AS athlete_name,
    disciplines.name AS discipline_name,
    competitions.name AS competition_name,
    competitions.date AS competition_date,
    results.result,
    disciplines.unit,
    results.place,
    results.standard
FROM results
JOIN athletes
    ON results.athlete_id = athletes.id
JOIN disciplines
    ON results.discipline_id = disciplines.id
JOIN competitions
    ON results.competition_id = competitions.id
ORDER BY results.id;


-- 6. Спортсмены и соревнования, в которых они участвовали
SELECT
    athletes.full_name AS athlete_name,
    competitions.name AS competition_name,
    competitions.date
FROM results
JOIN athletes
    ON results.athlete_id = athletes.id
JOIN competitions
    ON results.competition_id = competitions.id
ORDER BY competitions.date, athletes.full_name;


-- 7. Общее количество спортсменов
SELECT
    COUNT(*) AS athletes_count
FROM athletes;


-- 8. Средний спортивный результат
SELECT
    AVG(result) AS average_result
FROM results;


-- 9. Количество результатов по дисциплинам
SELECT
    disciplines.name AS discipline_name,
    COUNT(results.id) AS results_count
FROM disciplines
LEFT JOIN results
    ON results.discipline_id = disciplines.id
GROUP BY disciplines.id, disciplines.name
ORDER BY results_count DESC;


-- 10. Количество участников по соревнованиям
SELECT
    competitions.name AS competition_name,
    COUNT(results.id) AS participants_count
FROM competitions
LEFT JOIN results
    ON results.competition_id = competitions.id
GROUP BY competitions.id, competitions.name
ORDER BY participants_count DESC;


-- 11. Дисциплины, в которых зарегистрирован хотя бы один результат
SELECT
    disciplines.name AS discipline_name,
    COUNT(results.id) AS results_count
FROM disciplines
JOIN results
    ON results.discipline_id = disciplines.id
GROUP BY disciplines.id, disciplines.name
HAVING COUNT(results.id) >= 1;


-- 12. Лучший результат по каждой дисциплине
SELECT
    disciplines.name AS discipline_name,
    MIN(results.result) AS best_result,
    disciplines.unit
FROM disciplines
JOIN results
    ON results.discipline_id = disciplines.id
GROUP BY disciplines.id, disciplines.name, disciplines.unit
ORDER BY disciplines.name;
