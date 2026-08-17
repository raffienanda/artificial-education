import argparse

from app.api.endpoints.quiz import _calibrate_finished_assessment_mastery
from app.core.database import SessionLocal
from app.models.assessment import AssessmentAttempt


def main() -> None:
    parser = argparse.ArgumentParser(description="Recalibrate stored mastery from finished passed assessments.")
    parser.add_argument("--user-id", type=int, default=None, help="Optional user id to recalibrate.")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        query = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.assessment_type.in_(["quiz", "post_test"]),
            AssessmentAttempt.finished_at.isnot(None),
            AssessmentAttempt.passed.is_(True),
        )
        if args.user_id is not None:
            query = query.filter(AssessmentAttempt.user_id == args.user_id)

        attempts = query.order_by(
            AssessmentAttempt.user_id,
            AssessmentAttempt.finished_at,
            AssessmentAttempt.id,
        ).all()

        updated_count = 0
        for attempt in attempts:
            calibrated = _calibrate_finished_assessment_mastery(
                db=db,
                user_id=attempt.user_id,
                attempt=attempt,
            )
            updated_count += len(calibrated)

        db.commit()
        target = f"user {args.user_id}" if args.user_id is not None else "all users"
        print(f"Recalibrated {updated_count} subtopic mastery values for {target}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
