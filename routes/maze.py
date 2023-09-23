import json
import logging
from enum import Enum

from flask import request

from routes import app

logger = logging.getLogger(__name__)


# {
#     "mazeId": "30d9caf8",
#     "nearby": [[0, 0, 0], [0, 2, 1], [0, 0, 1]],
#     "mazeWidth": 6,
#     "step": 0,
#     "remainingAccumulatedStep": 216,
#     "isPreviousMovementValid": False,
#     "message": "invalid movement",
#     "remainingEvaluationTimeInSec": 353,
# }


def maze(data):
    # Define the possible directions
    class Direction(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    Map = data.get("nearby")

    # Find the starting position
    def find_start_position():
        for y in range(len(Map)):
            for x in range(len(Map[y])):
                if Map[y][x] == 2:
                    return x, y

    direction = Direction.UP
    posX, posY = find_start_position()

    if Map[posX][posY + 1] == 1:
        direction = Direction.RIGHT
    elif Map[posX][posY - 1] == 1:
        direction = Direction.LEFT
    elif Map[posX - 1][posY] == 1:
        direction = Direction.UP
    elif Map[posX + 1][posY] == 1:
        direction = Direction.DOWN

    playerAction = None
    if direction == Direction.UP:
        playerAction = "up"
    elif direction == Direction.RIGHT:
        playerAction = "right"
    elif direction == Direction.DOWN:
        playerAction = "down"
    elif direction == Direction.LEFT:
        playerAction = "left"

    return {"playerAction": playerAction}


@app.route("/maze", methods=["POST"])
def maze_test():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = maze(data)
    return json.dumps(result)
