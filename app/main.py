from typing import List

from fastapi import FastAPI, Query
from fastapi_mcp import FastApiMCP
from fastapi.responses import StreamingResponse

from app.models import CompanySearchResult
from app.services.search import search_companies
from app.services.ai_investment import investment_agent
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
    print("company_name", company_name)
    return search_companies(company_name)


@app.get("/investment-analysis")
async def get_investment_analysis(
    company_name: str = Query(..., description="Company name to analyze for investment")
):
    """
    Stream AI-powered investment analysis for a given company.
    """
    # Validate input length (similar to @lessthan_x decorator)
    if len(company_name) < 3:
        return {"error": "company_name must be at least 3 characters long."}

    async def async_investment_stream():
        """Async wrapper for the investment analysis generator"""
        try:
            # Use the investment_agent function which returns a proper generator
            from app.services.ai_investment import investment_agent
            analysis_generator = investment_agent(company_name)
            
            # Yield from the generator
            for chunk in analysis_generator:
                if chunk:  # Only yield non-empty chunks
                    yield str(chunk)
                    
        except Exception as error:
            yield f"Error during analysis: {str(error)}\n"
            yield "Please try again or contact support.\n"
    
    # Return StreamingResponse
    return StreamingResponse(
        async_investment_stream(), 
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

mcp.setup_server()