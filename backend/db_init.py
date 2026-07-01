import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import json
import sys

# Add backend directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "123")
DB_HOST = os.getenv("POSTGRES_SERVER", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = "artificial_education"

def create_database():
    try:
        # Connect to default postgres db to create the new one
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database {DB_NAME}...")
            cur.execute(f"CREATE DATABASE {DB_NAME}")
        else:
            print(f"Database {DB_NAME} already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

def seed_database():
    print("Seeding database...")
    from app.core.database import SessionLocal, engine, Base
    from app.models.user import User
    from app.models.module import Module, Subtopic
    from app.models.question import Question
    from app.models.progress import UserProgress
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Seed User
    if not db.query(User).filter(User.username == "student_cs").first():
        user = User(username="student_cs", xp=500, combo=0, total_score=0)
        db.add(user)
        db.commit()
    
    user = db.query(User).first()
    
    # Modules Data (from src/data/modules.js)
    # We will hardcode a subset here to seed the DB
    mod1 = db.query(Module).filter(Module.id == "mod-001").first()
    if not mod1:
        mod1 = Module(
            id="mod-001", title="Dasar & Variabel", icon="🧱", 
            description="Konsep dasar pemrograman", difficulty="Dasar",
            estimated_time="60 menit", order=1, status="in-progress"
        )
        db.add(mod1)
        db.commit()
        
        sub1 = Subtopic(
            id="sub-001-1", module_id="mod-001", title="Pengantar Algoritma",
            content={"sections": [{"type": "text", "content": "Algoritma adalah urutan langkah logis."}]}
        )
        sub2 = Subtopic(
            id="sub-001-2", module_id="mod-001", title="Variabel dan Tipe Data",
            content={"sections": [{"type": "text", "content": "Variabel adalah wadah."}]}
        )
        db.add_all([sub1, sub2])
        db.commit()

        q1 = Question(
            id="q-001", subtopic_id="sub-001-2", question_text="Deklarasi Python?",
            options=[{"id": "a", "text": "int x=1", "label": "A"}, {"id": "b", "text": "x=1", "label": "B"}],
            correct_answer="b", explanation="Python uses dynamic typing.", difficulty="mudah"
        )
        db.add(q1)
        
        p1 = UserProgress(user_id=user.id, topic_id="sub-001-1", mastery=100.0, status="proficient")
        p2 = UserProgress(user_id=user.id, topic_id="sub-001-2", mastery=75.0, status="proficient")
        db.add_all([p1, p2])
        db.commit()
        
    print("Seeding complete.")

if __name__ == "__main__":
    create_database()
    seed_database()
