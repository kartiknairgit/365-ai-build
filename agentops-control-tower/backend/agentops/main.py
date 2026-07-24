from fastapi import FastAPI

app = FastAPI(
    title="AgentOps Control Tower API",
    description="Local-only multi-agent trace observability and evaluation.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "agentops-control-tower"}
