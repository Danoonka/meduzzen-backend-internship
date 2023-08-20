import json
from redis import Redis

redis_pool = None

redis_connect = Redis(host='redis-cache', port=6379)


async def add_quiz(user_id: str, company_id: str, quiz_id: str, questions: list):
    questions_json = json.dumps(questions)
    redis_connect.set(f"user:{user_id}:companies", company_id)
    redis_connect.expire(f"user:{user_id}:companies", 48 * 60 * 60)
    redis_connect.set(f"company:{company_id}:quizzes", quiz_id)
    redis_connect.expire(f"company:{company_id}:quizzes", 48 * 60 * 60)

    hash_key = f"quiz:{quiz_id}"
    redis_connect.set(hash_key, questions_json)
    redis_connect.expire(hash_key, 48 * 60 * 60)

    return {"message": "Quiz added successfully"}
