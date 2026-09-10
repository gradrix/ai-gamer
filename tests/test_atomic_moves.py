import os
import sqlite3
from sqlite3 import Error
import tempfile
import pytest

import game_server.state.recorderdb as recorderdb
from game_server.state.recorderdb import RecorderDb
from common.models.move import Move


@pytest.fixture
def tmp_db_path():
    """Return a temporary database path and set RECORDER_DB."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    old = recorderdb.RECORDER_DB
    recorderdb.RECORDER_DB = path
    yield path
    recorderdb.RECORDER_DB = old
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def db(tmp_db_path):
    """Create a real RecorderDb backed by a temporary SQLite database."""
    return RecorderDb()


def _make_move(gameid, playerid, idx, move, date):
    return Move(id=0, gameid=gameid, playerid=playerid, idx=idx, move=move, date=date)


def _insert_player(db, name):
    """Insert a player row and return its id."""
    with db.lock:
        cur = db.conn.cursor()
        cur.execute(
            "INSERT INTO players(name, createddate, lastonline, is_ai) VALUES(?,?,?,?)",
            (name, 1000, 1000, False),
        )
        db.conn.commit()
        return cur.lastrowid


def _insert_game(db, date=2000):
    """Insert a game row and return its id."""
    with db.lock:
        cur = db.conn.cursor()
        cur.execute(
            "INSERT INTO games(date, status, board_size, game_type) VALUES(?,?,?,?)",
            (date, 0, 3, "tick_tack_toe"),
        )
        db.conn.commit()
        return cur.lastrowid


def _count_moves(db, gameid=None):
    """Return the number of rows in the moves table, optionally filtered by gameid."""
    with db.lock:
        cur = db.conn.cursor()
        if gameid is None:
            cur.execute("SELECT COUNT(*) FROM moves")
        else:
            cur.execute("SELECT COUNT(*) FROM moves WHERE gameid=?", (gameid,))
        return cur.fetchone()[0]


def _get_moves(db, gameid=None):
    """Return all move rows, optionally filtered by gameid."""
    with db.lock:
        cur = db.conn.cursor()
        if gameid is None:
            cur.execute("SELECT gameid, playerid, idx, move, date FROM moves ORDER BY id")
        else:
            cur.execute(
                "SELECT gameid, playerid, idx, move, date FROM moves WHERE gameid=? ORDER BY id",
                (gameid,),
            )
        return cur.fetchall()


# ---------------------------------------------------------------------------
# Test 1: successful batch commit with correct enumerated indices and dates
# ---------------------------------------------------------------------------
def test_successful_batch_commit(db):
    pid = _insert_player(db, "alice")
    gid = _insert_game(db)
    moves = [
        _make_move(gid, pid, 0, "A1", 100),
        _make_move(gid, pid, 0, "B2", 200),
        _make_move(gid, pid, 0, "C3", 300),
    ]
    result = db.addMoves(moves)
    assert result is True
    rows = _get_moves(db, gid)
    assert len(rows) == 3
    # idx must be enumerate order (0,1,2), not Move.idx
    assert rows[0][2] == 0
    assert rows[1][2] == 1
    assert rows[2][2] == 2
    # move and date preserved
    assert rows[0][3] == "A1"
    assert rows[0][4] == 100
    assert rows[1][3] == "B2"
    assert rows[1][4] == 200
    assert rows[2][3] == "C3"
    assert rows[2][4] == 300


# ---------------------------------------------------------------------------
# Test 2: empty batch commits and returns True
# ---------------------------------------------------------------------------
def test_empty_batch(db):
    result = db.addMoves([])
    assert result is True
    assert _count_moves(db) == 0


# ---------------------------------------------------------------------------
# Test 3: first row constraint failure rolls back the entire batch
# ---------------------------------------------------------------------------
def test_first_row_constraint_failure_rolls_back(db):
    pid = _insert_player(db, "bob")
    gid = _insert_game(db)
    # Insert a valid move first so we can verify it survives
    valid_move = _make_move(gid, pid, 0, "valid", 500)
    assert db.addMoves([valid_move]) is True
    assert _count_moves(db, gid) == 1

    # Now try a batch where the first row violates a constraint (duplicate idx
    # is not a constraint, but we can use a non-existent gameid to trigger FK
    # if enforced, or use a NULL move to trigger NOT NULL).  We'll use a move
    # with an empty string for 'move' which is NOT NULL but empty string is
    # allowed.  Instead, let's trigger a constraint by inserting a row with
    # a gameid that doesn't exist (FK violation if enforced) or by using
    # a duplicate primary key.  The simplest reliable approach: insert a row
    # with a NULL date to trigger NOT NULL constraint.
    bad_move = _make_move(gid, pid, 0, "bad", None)  # date is None -> NOT NULL violation
    # We need to pass a list; the bad move will cause the executemany to fail
    moves = [bad_move, _make_move(gid, pid, 0, "should_not_appear", 600)]
    result = db.addMoves(moves)
    assert result == -1
    # The valid move from before must still be there
    assert _count_moves(db, gid) == 1
    # No new rows from the failed batch
    rows = _get_moves(db, gid)
    assert len(rows) == 1
    assert rows[0][3] == "valid"


# ---------------------------------------------------------------------------
# Test 4: later row constraint failure rolls back the entire batch
# ---------------------------------------------------------------------------
def test_later_row_constraint_failure_rolls_back(db):
    pid = _insert_player(db, "carol")
    gid = _insert_game(db)
    # First commit a valid batch
    first_batch = [_make_move(gid, pid, 0, "first", 700)]
    assert db.addMoves(first_batch) is True
    assert _count_moves(db, gid) == 1

    # Second batch: first row is valid, second row has NULL date (NOT NULL violation)
    good = _make_move(gid, pid, 0, "good", 800)
    bad = _make_move(gid, pid, 0, "bad", None)
    result = db.addMoves([good, bad])
    assert result == -1
    # Only the first batch's row should remain
    assert _count_moves(db, gid) == 1
    rows = _get_moves(db, gid)
    assert len(rows) == 1
    assert rows[0][3] == "first"


# ---------------------------------------------------------------------------
# Test 5: recovery – after a failed batch, a later unrelated write succeeds
# ---------------------------------------------------------------------------
def test_recovery_after_failed_batch(db):
    pid = _insert_player(db, "dave")
    gid = _insert_game(db)

    # Commit a valid batch
    assert db.addMoves([_make_move(gid, pid, 0, "ok1", 900)]) is True
    assert _count_moves(db, gid) == 1

    # Attempt a batch that will fail (NULL date)
    bad = _make_move(gid, pid, 0, "fail", None)
    assert db.addMoves([bad]) == -1
    assert _count_moves(db, gid) == 1

    # A subsequent successful write must work
    assert db.addMoves([_make_move(gid, pid, 0, "ok2", 1000)]) is True
    assert _count_moves(db, gid) == 2
    rows = _get_moves(db, gid)
    assert len(rows) == 2
    assert rows[0][3] == "ok1"
    assert rows[1][3] == "ok2"

    # Also verify that a completely unrelated write (e.g., another game's moves)
    # works after the failure
    gid2 = _insert_game(db)
    assert db.addMoves([_make_move(gid2, pid, 0, "unrelated", 1100)]) is True
    assert _count_moves(db, gid2) == 1
    assert _count_moves(db, gid) == 2
