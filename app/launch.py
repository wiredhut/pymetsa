import uvicorn


if __name__ == "__main__":
    # For development purposes
    uvicorn.run("main:app", log_level="info")
