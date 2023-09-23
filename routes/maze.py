import json
import logging
import http.cookiejar

from enum import Enum
from flask import Flask, make_response, request, session
from routes import app

logger = logging.getLogger(__name__)

app.secret_key = "lalalala"


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

    def check_goal():
        if Map[posX][posY + 1] == 3:
            return Direction.RIGHT
        elif Map[posX][posY - 1] == 3:
            return Direction.LEFT
        elif Map[posX - 1][posY] == 3:
            return Direction.UP
        elif Map[posX + 1][posY] == 3:
            return Direction.DOWN
        else:
            return False

    def check_next_move(lastMove):
        if check_goal():
            return check_goal()
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
                return find_way(yes_up(), yes_left(), yes_down(), yes_right())
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


previousData = None
previousMove = None


@app.route("/maze", methods=["POST"])
def maze_test():
    global previousData, previousMove
    data = request.get_json()

    logging.info("data sent for evaluation {}".format(data))

    if previousData is not None:
        logging.info("Previous map: {}".format(previousData.get("nearby")))
        logging.info("Current map: {}".format(data.get("nearby")))
        logging.info("Previous move: {}".format(previousMove))
        result = maze(previousMove, data)
        logging.info("Current move: {}".format(result["playerAction"]))
    else:
        logging.info("Previous data not found.")
        result = maze(None, data)

    previousData = data
    previousMove = result["playerAction"]

    # session["previous_position"] = data.get("nearby")
    # session["previous_move"] = result["playerAction"]
    # logging.info("Previous map: {}".format(previousMap))
    # logging.info("Current map: {}".format(session["previous_position"]))
    # logging.info("Previous move: {}".format(previousMove))
    # logging.info("Current move: {}".format(session["previous_move"]))

    # # Store the new previous move in a cookie
    # response.set_cookie("previous_move_cookie", str(maze(None, data)))
    # logging.info("tes cookie: {}".format(request.cookies.get("my_data_cookie")))

    return json.dumps(result)
