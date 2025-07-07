import pandas as pd
from fuzzywuzzy import fuzz
import os
from typing import List
from app.models import CompanySearchResult

# Load CSV into memory at startup
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),"..", "csv", "2025-07-03-Worker.csv")
skilled_worker_data_current = pd.read_csv(CSV_PATH)

def get_fuzzy_score(company_name: str, company: str) -> int:
    """
    Calculate the fuzzy matching score between the search query and a company name using token set ratio.
    Args:
        company_name (str): The company name to search for (user input).
        company (str): The company name from the dataset.
    Returns:
        int: Fuzzy matching score (0-100).
    """
    return fuzz.token_set_ratio(company_name.lower(), str(company).lower())

def safe_str(val):
    """
    Convert a value to a string, returning an empty string if the value is NaN.
    Args:
        val: The value to convert.
    Returns:
        str: The value as a string, or an empty string if NaN.
    """
    return "" if pd.isna(val) else str(val)

def search_companies(company_name: str, threshold: int = 70) -> List[CompanySearchResult]:
    """
    Search for companies in the loaded CSV whose names closely match the given company_name using fuzzy matching.
    Args:
        company_name (str): The company name to search for.
        threshold (int, optional): Minimum fuzzy score to consider a match. Defaults to 70.
    Returns:
        List[CompanySearchResult]: List of matching companies as Pydantic models.
    """
    scores = skilled_worker_data_current['Organisation Name'].apply(lambda company: get_fuzzy_score(company_name, company))
    matching_mask = scores >= threshold
    results: List[CompanySearchResult] = []
    for idx, is_match in matching_mask.items():
        if is_match:
            row = skilled_worker_data_current.loc[idx]
            results.append(CompanySearchResult(
                Organisation_Name=safe_str(row["Organisation Name"]),
                Town_City=safe_str(row["Town/City"]),
                County=safe_str(row["County"]),
                fuzzy_score=int(scores[idx])
            ))
    return results
