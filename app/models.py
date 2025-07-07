from pydantic import BaseModel


class CompanySearchResult(BaseModel):
    Organisation_Name: str
    Town_City: str
    County: str
    fuzzy_score: int
