import asyncio
import logging
from typing import List

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi_mcp import FastApiMCP

from app import logging_config  # noqa: F401
from app.models import CompanySearchResult
from app.services.ai_investment import investment_agent
from app.services.search import search_companies
from app.utils import lessthan_x

logger = logging.getLogger(__name__)

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
    ticker_symbol: str = Query(
        ..., description="Stock ticker symbol to analyze for investment"
    )
):
    """
    Stream AI-powered investment analysis for a given stock ticker.
    """

    def investment_stream():
        try:
            analysis_generator = investment_agent(ticker_symbol)
            for chunk in analysis_generator:
                if chunk:
                    yield str(chunk)
        except Exception as error:
            yield f"Error during analysis: {str(error)}\n"
            yield "Please try again or contact support.\n"

    async def async_investment_stream():
        for chunk in investment_stream():
            await asyncio.sleep(0)  # Yield control to event loop
            yield chunk

    return StreamingResponse(
        async_investment_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


mcp.setup_server()
