 # -*- coding: UTF-8 -*-
import json


def cleaned_slide_data(slide_data:str):
    cleaned_data = slide_data
    for i in range(0,len(slide_data)-1):
        if slide_data[i] == "{":
            cleaned_data = slide_data[i:]
            break

    for i in range(len(cleaned_data)-1,-1,-1):
        if cleaned_data[i] == "}":
            cleaned_data = cleaned_data[:i+1]
            break
    json_dict = json.loads(cleaned_data,strict = False)
    return json_dict
             
def get_clean_json(json_str: str) -> str:
    """
    Attempt to clean a JSON response string from the LLM by removing the trailing ```
    and any text beyond that.
    CAUTION: May not be always accurate.

    :param json_str: The input string in JSON format.
    :return: The "cleaned" JSON string.
    """

    response_cleaned = json_str

    while True:
        idx = json_str.rfind('```')  # -1 on failure

        if idx <= 0:
            break

        # In the ideal scenario, the character before the last ``` should be
        # a new line or a closing bracket }
        prev_char = json_str[idx - 1]

        if (prev_char == '}') or (prev_char == '\n' and json_str[idx - 2] == '}'):
            response_cleaned = json_str[:idx]

        json_str = json_str[:idx]

    return response_cleaned




        



    





