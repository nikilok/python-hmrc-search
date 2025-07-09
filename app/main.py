from typing import List

from fastapi import FastAPI, Query
from fastapi_mcp import FastApiMCP

from app.models import CompanySearchResult
from app.services.search import search_companies
from app.utils import lessthan_x

app = FastAPI()
mcp = FastApiMCP(app)
mcp.mount()


@app.get("/search", response_model=List[CompanySearchResult])
@lessthan_x(
    3,
    arg_name="company_name",
    message="company_name must be at least 3 characters long.",
)
def search_company(
    company_name: str = Query(..., description="Company name to search for")
) -> List[CompanySearchResult]:
    return search_companies(company_name)


mcp.setup_server()
