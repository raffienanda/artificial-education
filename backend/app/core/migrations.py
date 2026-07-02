from sqlalchemy import text


def ensure_runtime_columns(engine):
    statements = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'student'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS reward_points INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS current_streak INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS longest_streak INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_study_date DATE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS redeemed_rewards JSON DEFAULT '[]'",
        "ALTER TABLE modules ADD COLUMN IF NOT EXISTS course_id VARCHAR",
        "ALTER TABLE topic_prerequisites ADD COLUMN IF NOT EXISTS mastery_threshold FLOAT DEFAULT 60.0",
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
