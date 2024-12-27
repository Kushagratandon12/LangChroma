from fastapi import FastAPI, Request
from app.routes.route import insert_data

# Initialize FastAPI app
app = FastAPI(
    title="LangChroma",
    description="FastAPI-based client integrating LangChain and ChromaDB",
    version="1.0.0"
)

@app.get("/")
def application_health():
    """
    This view returns application healthy status
    """
    return {"message": "Welcome to FastAPI!", "status": 200, "error": None}



@app.post("/vectordb/insert_data")
async def add_data_to_vectordb(request: Request):
    """
    This view helps to add data to vectordb setup locally
    """
    try:
        user_input_data = await request.json()
        insert_data(user_input_data=user_input_data)
        return {"message":"Data added to vectordb successfully", "status": 200, "error": None}
    
    except Exception as err:
        return {"message":"Data added to vectordb failed", "status": 400, "error": err}
