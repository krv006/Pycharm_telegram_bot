import json
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class UserAddMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = {
            "id": event.message.chat.id,
            "full_name": event.message.chat.full_name,
        }
        with open('data_json/users.json', 'r') as f:
            json_object = json.load(f)
        if not(user['id'] in [item.get('id') for item in json_object]):
            json_object.append(user)
            with open('data_json/users.json', 'w') as f:
                json.dump(json_object, f, indent=3)
        return await handler(event, data)
