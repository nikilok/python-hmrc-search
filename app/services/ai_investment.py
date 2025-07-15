import os

from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
from app.utils import validate_env_variables

# Load environment variables from .env file
load_dotenv()

# Validate all required environment variables
_, xai_model_s, xai_model_m, xai_model_l, xai_model_xl = validate_env_variables([
    "OPENAI_API_KEY",
    "XAI_MODEL_S",
    "XAI_MODEL_M",
    "XAI_MODEL_L",
    "XAI_MODEL_XL"
])

# Agent 1: Market Research Agent - Uses web search to gather market news and trends
market_research_agent = Agent(
    name="Market Research Agent",
    role="Gather latest market news, trends, and qualitative information from the web",
    model=xAI(id=xai_model_s),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Always cite sources and provide summaries of key articles or reports",
        "Keep tool calls simple and avoid complex JSON structures",
        "Be precise with search queries",
        "If tool calls fail, provide analysis based on general knowledge",
    ],
    markdown=True,
    show_tool_calls=False,
)

# Agent 2: Financial Data Agent - Retrieves quantitative financial data using YFinance
financial_data_agent = Agent(
    name="Financial Data Agent",
    role="Fetch stock prices, analyst recommendations, company info, and financial metrics",
    model=xAI(id=xai_model_m),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            historical_prices=True,
        )
    ],
    instructions=[
        "Present financial data in tables for clarity and include historical trends where relevant",
        "Use precise stock symbols and avoid ambiguous queries",
        "Keep tool calls simple and properly formatted",
        "If tool calls fail, provide analysis based on general knowledge",
    ],
    markdown=True,
    show_tool_calls=False,
)

# Agent 3: Investment Analysis Agent - Analyzes data from other
# agents to provide insights and recommendations
investment_analysis_agent = Agent(
    name="Investment Analysis Agent",
    role="Analyze market research and financial data to provide investment insights,"
    " risks, and recommendations",
    model=xAI(id=xai_model_xl),
    instructions="Synthesize information from team members, evaluate risks, and "
    "suggest buy/sell/hold recommendations with reasoning",
    markdown=True,
)

# Create the main Investment Team Agent that coordinates the specialized agents
investment_team = Agent(
    team=[market_research_agent, financial_data_agent, investment_analysis_agent],
    model=xAI(id=xai_model_l),
    instructions=[
        "Coordinate between agents to gather comprehensive data",
        "Ensure responses are well-structured with sections for research, data, and analysis",
        "Always include sources and use tables for data",
        "Keep tool calls simple and avoid complex JSON structures",
    ],
    markdown=True,
    show_tool_calls=False,
)


def investment_agent(ticker_symbol: str):
    """
    Investment analysis using multi-agent approach.
    Returns a generator for streaming responses.
    """

    def generate_streaming_analysis():
        """Generate streaming analysis using the investment team"""
        try:
            yield f"🔍 Starting comprehensive investment analysis for {ticker_symbol}...\n\n"

            # Use the run method to get the complete response
            response = investment_team.run(
                f"Provide a detailed investment analysis for {ticker_symbol} stock, including market outlook, financial performance, and recommendations."  # noqa: E501
            )

            # Extract and stream the content
            if hasattr(response, "content") and response.content:
                content = response.content
                # Stream in chunks for better user experience
                chunk_size = 150
                for i in range(0, len(content), chunk_size):
                    chunk = content[i : i + chunk_size]  # noqa : E203
                    yield chunk
            else:
                yield f"Analysis completed for {ticker_symbol}"

        except Exception as e:
            yield f"❌ Error during analysis: {str(e)}\n"
            yield "🔄 Attempting simplified analysis...\n"

            try:
                # Fallback to simple analysis
                simplified_response = investment_analysis_agent.run(
                    f"Provide a basic investment analysis for {ticker_symbol} based on general knowledge."  # noqa: E501
                )
                if (
                    hasattr(simplified_response, "content")
                    and simplified_response.content
                ):
                    yield simplified_response.content
                else:
                    yield f"Basic analysis completed for {ticker_symbol}"
            except Exception as fallback_error:
                yield f"Unable to complete analysis: {fallback_error}\n"

    return generate_streaming_analysis()


# To test the code through the command line instead of FastAPI
if __name__ == "__main__":
    import sys
    import os
    
    # Add the project root to Python path for imports
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, project_root)
    import sys

    # Check if company name is provided as command line argument
    if len(sys.argv) < 2:
        print("Usage: python ai_investment.py <company_name>")
        print("Example: python ai_investment.py Tesla")
        print("Example: python ai_investment.py TSLA")
        sys.exit(1)

    company_name = " ".join(
        sys.argv[1:]
    )  # Join all arguments in case company name has spaces
    print(f"Starting investment analysis for: {company_name}")
    print("=" * 50)
    print("Note: Using simplified approach to avoid JSON parsing issues")
    print("=" * 50)

    try:
        # Run the investment analysis
        analysis_gen = investment_agent(company_name)
        for chunk in analysis_gen:
            print(chunk, end="")
        print("\n" + "=" * 50)
        print("Analysis completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        print("Try using the stock symbol instead (e.g., TSLA instead of Tesla)")
        sys.exit(1)
