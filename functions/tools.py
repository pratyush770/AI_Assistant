from langchain_core.tools import tool
import datetime
from langchain_community.tools import DuckDuckGoSearchRun


@tool
def duckduckgosearch(input: str) -> str:
    """ Function to search user's input using DuckDuckGoSearchRun and return the most relevant result.
    Parameter:
        input -> user input
    """
    search = DuckDuckGoSearchRun()
    result = search.invoke(input)
    return result


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
