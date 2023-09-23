import json
import logging
from enum import Enum

from flask import request, session

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

app.secret_key = "your-secret-key"


def maze(last_move, data):
    # Define the possible directions
    class Direction(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    Map = data.get("nearby")
    if last_move == "right":
        direction = Direction.RIGHT
    elif last_move == "left":
        direction = Direction.LEFT
    elif last_move == "up":
        direction = Direction.UP
    elif last_move == "down":
        direction = Direction.DOWN
    posX, posY = 1, 1

    def yes_right():
        if Map[posX][posY + 1] == 1:
            return Direction.RIGHT
        else:
            return False

    def yes_left():
        if Map[posX][posY - 1] == 1:
            return Direction.LEFT
        else:
            return False

    def yes_up():
        if Map[posX - 1][posY] == 1:
            return Direction.UP
        else:
            return False

    def yes_down():
        if Map[posX + 1][posY] == 1:
            return Direction.DOWN
        else:
            return False

    def find_way(f1, f2, f3, f4):
        for result in (f1, f2, f3, f4):
            if result:
                return result

    def check_next_move(lastMove):
        if last_move == None:
            if Map[posX][posY + 1] == 1:
                return Direction.RIGHT
            elif Map[posX][posY - 1] == 1:
                return Direction.LEFT
            elif Map[posX - 1][posY] == 1:
                return Direction.UP
            elif Map[posX + 1][posY] == 1:
                return Direction.DOWN
        else:
            if last_move == "right":
                return find_way(yes_down(), yes_right(), yes_up(), yes_left())
            elif last_move == "left":
                return find_way(yes_down(), yes_left(), yes_up(), yes_right())
            elif last_move == "up":
                return find_way(yes_right(), yes_up(), yes_left(), yes_down())
            elif last_move == "down":
                return find_way(yes_left(), yes_down(), yes_right(), yes_up())

    if Map[posX][posY] == 2:
        last_move = None

    direction = check_next_move(last_move)

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
    previousMap = session.get("previous_position")
    previousMove = session.get("previous_move")
    result = maze(previousMove, data)
    session["previous_position"] = data.get("nearby")
    session["previous_move"] = result["playerAction"]
    logging.info("Previous map: {}".format(previousMap))
    logging.info("Current map: {}".format(session["previous_position"]))
    logging.info("Previous move: {}".format(previousMove))
    logging.info("Current move: {}".format(session["previous_move"]))
    return json.dumps(result)
