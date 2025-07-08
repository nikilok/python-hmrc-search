from typing import List

from fastapi import FastAPI, HTTPException, Query
from fastapi_mcp import FastApiMCP

from app.models import CompanySearchResult
from app.services.search import search_companies

app = FastAPI()
mcp = FastApiMCP(app)
mcp.mount()


@app.get("/search", response_model=List[CompanySearchResult])
def search_company(
    company_name: str = Query(..., description="Company name to search for")
) -> List[CompanySearchResult]:
    if len(company_name.strip()) < 3:
        raise HTTPException(
            status_code=400, detail="company_name must be at least 3 characters long."
        )
    return search_companies(company_name)


mcp.setup_server()
