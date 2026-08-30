from fastapi import FastAPI

app = FastAPI(
    title="Job Hub API",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Job Hub API is running"}