import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_core.rate_limiters import InMemoryRateLimiter
from dotenv import load_dotenv

load_dotenv()
model = os.getenv("MODEL")
google_api_key = os.getenv("GEMINI_API_KEY")


def run_csv_sports_agent(csv_paths: list[str]):
    # Set up rate limiter: 1 request per 10 seconds
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.1,
        check_every_n_seconds=0.1,
        max_bucket_size=1,
    )

    # Initialize LLM with rate limiter
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=google_api_key,
        rate_limiter=rate_limiter
    ).with_retry()

    # Build CSV agent supporting multiple files
    agent = create_csv_agent(
        llm=llm,
        path=csv_paths,
        verbose=True,
        allow_dangerous_code=True # Opt into Python REPL execution
    )

    # Sample queries for exploratory analysis
    questions = [
        "Across all formats, how many innings has Virat Kohli played?",
        "What is his overall batting average and strike rate in T20Is?",
        "Which opposition team has he scored the most total runs against in Tests?",
        "Show the top 3 highest scores in ODIs."
    ]
    for q in questions:
        resp = agent.invoke({"input": q})
        print(f"\n> Q: {q}\nA: {resp['output']}")

if __name__ == "__main__":
    BASE = os.path.dirname(os.path.abspath(__file__))
    csvs = [
        os.path.join(BASE, "data", "virat_kohli_odi_innings_data.csv"),
        os.path.join(BASE, "data", "virat_kohli_t20i_innings_data.csv"),
        os.path.join(BASE, "data", "virat_kohli_test_innings_data.csv"),
    ]
    run_csv_sports_agent(csvs)