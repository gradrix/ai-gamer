#!/bin/bash

sqlite3 -readonly db/game_records.db -header -table '
SELECT 
    name,
    played,
    won,
    lost,
    draw,
    ROUND(CAST(won AS DECIMAL) * 100.0 / CAST(played AS DECIMAL), 3) AS "rate %",
    moves as "avg moves"
FROM (
    SELECT 
        p.name,
        COUNT(DISTINCT pg.gameid) AS played,
        SUM(CASE WHEN g.status = 2 AND last_moves.playerid = p.id THEN 1 ELSE 0 END) AS won,
        SUM(CASE WHEN g.status = 2 AND last_moves.playerid != p.id THEN 1 ELSE 0 END) AS lost,
        SUM(CASE WHEN g.status = 3 THEN 1 ELSE 0 END) AS draw,
        ROUND(AVG(steps), 2) AS moves
    FROM players p
    JOIN (
        SELECT m.gameid, m.playerid, COUNT(m.playerid) steps
        FROM moves m
        GROUP BY m.gameid, m.playerid
    ) pg ON pg.playerid = p.id 
    LEFT JOIN (
        SELECT m.gameid, m.playerid, MAX(m.idx) AS max_date
        FROM moves m
        GROUP BY m.gameid
    ) last_moves ON last_moves.gameid = pg.gameid
    LEFT JOIN games g ON g.id = last_moves.gameid
    WHERE 1 = 1
    GROUP BY p.id
) s;
'