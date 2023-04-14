def join_game() -> dict:
    return {
        "inline_keyboard": [
            [
                {
                    "text": "Присоединиться", "callback_data": "join"
                }
            ],
        ]
    }


def game_round() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "Статистика", "callback_data": "stat"},
                {"text": "Завершить игру", "callback_data": "stop"},
            ],
        ],
    }
