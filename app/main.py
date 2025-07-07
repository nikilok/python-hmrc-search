from fastapi import FastAPI, Query, HTTPException
from typing import List
from app.models import CompanySearchResult
from app.services.search import search_companies

app = FastAPI()

@app.get("/search", response_model=List[CompanySearchResult])
def search_company(company_name: str = Query(..., description="Company name to search for")) -> List[CompanySearchResult]:
    if len(company_name.strip()) < 3:
        raise HTTPException(status_code=400, detail="company_name must be at least 3 characters long.")
    return search_companies(company_name)
