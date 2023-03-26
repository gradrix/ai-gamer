SELECT m.gameid, MAX(m.idx) as moves, m.playerid as winner
FROM moves m
JOIN games g ON g.id = m.gameid AND g.status = 2

GROUP BY m.gameid