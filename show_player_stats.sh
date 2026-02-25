#!/bin/bash

sqlite3 -readonly data/db/game_records.db -header -table '
SELECT
    p.name,
    COALESCE(stats.played, 0) as played,
    COALESCE(stats.won, 0) as won,
    COALESCE(stats.lost, 0) as lost,
    COALESCE(stats.draw, 0) as draw,
    CASE
        WHEN COALESCE(stats.played, 0) > 0 THEN
            ROUND(CAST(COALESCE(stats.won, 0) AS FLOAT) * 100.0 / CAST(COALESCE(stats.played, 0) AS FLOAT), 3)
        ELSE 0
    END AS "rate %",
    0 as "avg moves"  -- Placeholder, calculating average moves would require more complex query
FROM players p
LEFT JOIN (
    SELECT
        playerid,
        COUNT(*) as played,
        SUM(CASE WHEN result = 1 THEN 1 ELSE 0 END) as won,
        SUM(CASE WHEN result = 2 THEN 1 ELSE 0 END) as lost,
        SUM(CASE WHEN result = 3 THEN 1 ELSE 0 END) as draw
    FROM game_results
    GROUP BY playerid
) stats ON p.id = stats.playerid
WHERE stats.played > 0  -- Only show players with recorded games
ORDER BY stats.played DESC;
'