import datetime
import json
from redis import Redis

from app.models.models_quiz import RedisResults


class RedisTools:
    redis_connect = Redis(host='redis-cache', port=6379)

    def set_results(self, user_id: str, result: RedisResults):
        serialized_result = json.dumps(result.dict())
        self.redis_connect.set(user_id, serialized_result)

    def get_results_for_user(self, user_id: str):
        results = self.redis_connect.lrange(user_id, 0, -1)
        deserialized_results = [json.loads(result) for result in results]
        return deserialized_results

    def get_keys(self):
        return self.redis_connect.keys(pattern='*')
