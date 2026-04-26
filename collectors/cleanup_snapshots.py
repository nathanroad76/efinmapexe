"""
Delete price_snapshots older than RETAIN_DAYS (default 30).
Run nightly via cron to keep table size bounded.
Usage: python cleanup_snapshots.py
"""
import os
from datetime import datetime
from db import get_connection

RETAIN_DAYS = int(os.getenv("SNAPSHOT_RETAIN_DAYS", "30"))


def main():
    print(f"[cleanup] {datetime.now().isoformat()} retaining last {RETAIN_DAYS} days", flush=True)
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM price_snapshots "
                "WHERE snapshot_at < NOW() - make_interval(days => %s)",
                (RETAIN_DAYS,),
            )
            deleted = cur.rowcount
        conn.commit()
        print(f"[cleanup] deleted {deleted} rows", flush=True)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
