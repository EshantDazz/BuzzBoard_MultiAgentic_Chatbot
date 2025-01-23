from typing import Any
from langchain_core.tools import tool
import json


@tool
def calculator(data_list, operation) -> None | Any | int | float:
    """
    Performs calculations on a list of numbers based on a given operation.

    Args:
        data_list: A list of numbers.
        operation: A string specifying the operation to perform.
                   Supported operations: "multiply", "add", "divide", "subtract",
                   "percentage", "average", "power".

    Returns:
        The result of the operation, or an error message if the input is invalid
        or the operation is not supported. Returns None if the list is empty.
    """

    if not data_list:
        return None  # Handle empty list case

    if not all(isinstance(x, (int, float)) for x in data_list):
        return "Error: List must contain only numbers."

    operation = operation.lower()  # Case-insensitive operation matching

    if operation == "multiply":
        result = 1
        for num in data_list:
            result *= num
        return result

    elif operation == "add":
        return sum(data_list)

    elif operation == "subtract":
        result = data_list[0]
        for num in data_list[1:]:
            result -= num
        return result

    elif operation == "divide":
        if 0 in data_list[1:]:
            return "Error: Division by zero."
        result = data_list[0]
        for num in data_list[1:]:
            result /= num
        return result

    elif operation == "percentage":
        if len(data_list) != 2:
            return "Error: Percentage operation requires exactly two numbers (value, total)."
        if data_list[1] == 0:
            return "Error: Division by zero."
        return (data_list[0] / data_list[1]) * 100

    elif operation == "average":
        return sum(data_list) / len(data_list)

    elif operation == "power":
        if len(data_list) != 2:
            return (
                "Error: Power operation requires exactly two numbers (base, exponent)."
            )
        return data_list[0] ** data_list[1]

    else:
        return "Error: Invalid operation."


@tool
def get_huge_corpus_for_all_companies(query: str) -> list[dict]:
    """
    Retrieve a large JSON data corpus based on the provided query.

    This function fetches a large dataset (corpus) in JSON format, which can be used
    for data analysis, processing, or other operations. The dataset is imported from
    a module named `big_data` and is structured as a list of dictionaries.

    Returns:
        list[dict]: A list of dictionaries containing the large JSON data corpus.

    """
    from big_data import big_data

    return big_data


@tool
def get_specific_company_details(company_name: str) -> dict:
    """
    Retrieve details about a specific company from the large JSON data corpus.

    This function searches the corpus returned by `get_huge_corpus` for a company
    matching the provided name. If a company with a matching business name (in lowercase)
    is found, it returns the entire company data dictionary.

    **Note:** If you're interested in general information about companies based on a query,
    use `get_huge_corpus` instead. This function is specifically designed to retrieve
    details about a single company by name.

    Args:
        company_name (str): The name of the company to retrieve details for.

    Returns:
        dict: The company data dictionary if found, otherwise None.

    """
    from big_data import big_data

    for entry in big_data:
        for key, value in entry.items():
            if isinstance(value, str):
                try:
                    json_data = json.loads(value)
                    for company in json_data:
                        if (
                            company["BUSINESS INFO"]["Business Name"].lower()
                            == company_name.lower()
                        ):
                            return company
                except json.JSONDecodeError:
                    continue
    return None
