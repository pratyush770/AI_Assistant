from langchain_core.tools import tool
from duckduckgo_search import DDGS
import datetime

@tool
def duckduckgosearch(input: str) -> str:
    """ Function to search user input using DuckDuckGo and return the most relevant result.
    Parameter:
        input -> user input
    """
    results = DDGS().text(input, safesearch="off", max_results=1)
    res = " ".join(r['body'] for r in results)
    return res


@tool
def get_current_day():
    """ Function to get current day details """
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")  # example: "2023-10-05 14:30:00"
    return formatted_date


@tool
def add_numbers(num1: int, num2: int):
    """ Function to add 2 numbers. """
    return num1 + num2


@tool
def subtract_numbers(num1: int, num2: int):
    """ Function to subtract 2 numbers. """
    if num1 > num2:
        return num1 - num2
    else:
        return num2 - num1


@tool
def multiply_numbers(num1: int, num2: int):
    """ Function to multiply 2 numbers. """
    return num1 * num2


@tool
def divide_numbers(num1: int, num2: int):
    """ Function to divide 2 numbers. """
    if num1 > num2:
        return num1 / num2
    else:
        return num2 / num1