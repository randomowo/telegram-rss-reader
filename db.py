import sqlite3
import time
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE = os.getenv('FEED_DATABASE')


def add_feed_source(userId, source, source_alias):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    dt_date = int(time.strftime("%Y%m%d%H%M%S"))
    cur.execute("INSERT INTO sources VALUES (?, ?, ?, ? )",
                (userId, source, source_alias, dt_date))
    con.commit()
    con.close()


def is_already_present(userId, source_alias):
    results = []
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM sources WHERE (URL=:source_or_alias OR ALIAS=:source_or_alias) AND USERID=:userid",
        {
            "userid": userId,
            'source_or_alias': source_alias,
        }
    )
    for row in cur:
        results.append(row)
    con.close()
    if len(results):
        return True
    return False


def remove_feed_source(userId, source_or_alias):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(
        "DELETE FROM sources WHERE (URL=:source_or_alias OR ALIAS=:source_or_alias) AND USERID=:userid",
        {
            "userid": userId,
            "source_or_alias": source_or_alias
        }
    )
    con.commit()
    con.close()


def get_sources(userId):
    results = []
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(
        "SELECT ALIAS, URL FROM sources WHERE USERID=:userid",
        {
            "userid": userId
        }
    )
    for row in cur:
        results.append(f'{row[0]} <{row[1]}>')
    con.close()
    return results


def get_all_sources():
    results = []
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM sources")
    for row in cur:
        results.append({
            "userId": row[0],
            "url": row[1],
            'alias': row[2],
            "last_updated": row[3]
        })
    con.close()
    return results


def update_source_timestamp(userId, source, time):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("UPDATE sources SET last_updated=:dt_date WHERE URL=:source AND USERID=:userid", {
                "userid": userId, "source": source, "dt_date": time})
    con.commit()
    con.close()

