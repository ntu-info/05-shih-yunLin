import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("DB_URL")
if not db_url:
    raise RuntimeError("請先設定 DB_URL 環境變數")

engine = create_engine(db_url)

with engine.connect() as conn:
    conn.execute(text("SET search_path TO ns, public;"))

    print("\n--- posterior_cingulate 有但沒有 ventromedial_prefrontal ---")
    rows = conn.execute(text("""
        SELECT DISTINCT at1.study_id
        FROM ns.annotations_terms at1
        WHERE at1.term = 'posterior_cingulate'
          AND NOT EXISTS (
            SELECT 1 FROM ns.annotations_terms at2
            WHERE at2.study_id = at1.study_id AND at2.term = 'ventromedial_prefrontal'
          )
        LIMIT 10
    """)).fetchall()
    print([r[0] for r in rows])

    print("\n--- ventromedial_prefrontal 有但沒有 posterior_cingulate ---")
    rows = conn.execute(text("""
        SELECT DISTINCT at1.study_id
        FROM ns.annotations_terms at1
        WHERE at1.term = 'ventromedial_prefrontal'
          AND NOT EXISTS (
            SELECT 1 FROM ns.annotations_terms at2
            WHERE at2.study_id = at1.study_id AND at2.term = 'posterior_cingulate'
          )
        LIMIT 10
    """)).fetchall()
    print([r[0] for r in rows])

    print("\n--- 0_-52_26 有但沒有 -2_50_-6 ---")
    rows = conn.execute(text("""
        SELECT DISTINCT c1.study_id
        FROM ns.coordinates c1
        WHERE ST_X(c1.geom) = 0 AND ST_Y(c1.geom) = -52 AND ST_Z(c1.geom) = 26
          AND NOT EXISTS (
            SELECT 1 FROM ns.coordinates c2
            WHERE c2.study_id = c1.study_id
              AND ST_X(c2.geom) = -2 AND ST_Y(c2.geom) = 50 AND ST_Z(c2.geom) = -6
          )
        LIMIT 10
    """)).fetchall()
    print([r[0] for r in rows])

    print("\n--- -2_50_-6 有但沒有 0_-52_26 ---")
    rows = conn.execute(text("""
        SELECT DISTINCT c1.study_id
        FROM ns.coordinates c1
        WHERE ST_X(c1.geom) = -2 AND ST_Y(c1.geom) = 50 AND ST_Z(c1.geom) = -6
          AND NOT EXISTS (
            SELECT 1 FROM ns.coordinates c2
            WHERE c2.study_id = c1.study_id
              AND ST_X(c2.geom) = 0 AND ST_Y(c2.geom) = -52 AND ST_Z(c2.geom) = 26
          )
        LIMIT 10
    """)).fetchall()
    print([r[0] for r in rows])