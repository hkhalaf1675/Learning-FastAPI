from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return { "success": True, "message": "Welcome FastAPI P03"}

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    import os

    load_dotenv()
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    uvicorn.run(app, host=host, port=port)