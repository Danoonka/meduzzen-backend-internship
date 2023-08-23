import json
from fastapi import Depends
from app.db.db_postgres_handler import get_redis_connection


async def add_quiz(user_id: str, company_id: str, quiz_id: str, questions: list,
                   redis_connect=Depends(get_redis_connection)):
    questions_json = json.dumps(questions)
    hash_key = f"user:{user_id}:company:{company_id}:quiz:{quiz_id}"
    redis_connect.set(hash_key, questions_json)
    redis_connect.expire(hash_key, 48 * 60 * 60)

    return {"message": "Quiz added successfully"}
