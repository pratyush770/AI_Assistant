from langchain_core.tools import tool
import datetime
from ddgs import DDGS

@tool
def duckduckgosearch(input: str) -> str:
    """ Function to search user's input using DDGS and return the result.
    Parameter:
        input -> user input
    """
    result = DDGS().text(query=input, num_results=1, backend=["bing", "brave", "duckduckgo", "google", "yandex", "yahoo", "wikipedia"])
    snippet = next((r["body"] for r in result if "body" in r), None)
    return snippet


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


if __name__ == "__main__":
    query = "Who is the captain for india in the ongoing india vs england test series?"
    print(duckduckgosearch(query))
