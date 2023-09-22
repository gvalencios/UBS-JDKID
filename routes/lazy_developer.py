import json
import logging
from typing import Dict, List

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route("/lazy-developer", methods=["POST"])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = getNextProbableWords(data)
    # logging.info("My result :{}".format(result))
    return json.dumps(result)


def getNextProbableWords(input_value):
    # Fill in your solution here and return the correct output based on the given input
    classes = input_value["classes"]
    statements = input_value["statements"]

    def runThrough(class_dict, parts, word_starter):
        list_element = []
        # iterate through every class [Order -> allocations -> ..]
        for class_name in parts:
            # will return "" if the class name is not in the input, e.g., Order.allocations but no Allocation class can be found inside the dictionary:
            if class_name not in class_dict:
                list_element.append("")

            for key, value in class_dict.items():
                if key == class_name:
                    # if the value is dictionary
                    if isinstance(value, dict):
                        # the class has only 1 value
                        if parts[1:] == []:
                            temp = [
                                item for item in value if item.startswith(word_starter)
                            ]
                            list_element += temp
                        # it means the class is still nested, need to dig more inside
                        else:
                            parts[1] = value[parts[1]].split("<")[1].split(">")[0]
                            return runThrough(class_dict, parts[1:], word_starter)

                    # if the value is list
                    elif isinstance(value, list):
                        # no starting word -> append nothing
                        if word_starter == "":
                            list_element.append("")
                        # has a starting word
                        else:
                            temp = [
                                item for item in value if item.startswith(word_starter)
                            ]
                            list_element += temp

                    # if the value is Empty string
                    else:
                        list_element.append("")

        # sort alphabetically and only show 5 elements max
        list_element.sort()
        return list_element[:5]

    # flatten the input
    class_dict = {}
    for class_item in classes:
        for key, value in class_item.items():
            class_dict[key] = value

    answer = dict()
    for word in statements:
        parts = word.split(".")
        # to know the word_starter, either "." or a string
        word_starter = parts[-1]
        parts.pop()
        # put word as the key and the return from helper function as the value
        answer[word] = runThrough(class_dict, parts, word_starter)

    return answer
