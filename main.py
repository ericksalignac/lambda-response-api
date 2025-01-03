from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Define the FastAPI application
app = FastAPI(title="Lambda Response Receiver API", description="API to receive and process results from AWS Lambda.")

# Define the data model for incoming POST requests
class LambdaResponse(BaseModel):
    id: str
    cd_occurrence: str
    generated_response: str

@app.post("/lambda-response")
async def receive_lambda_response(response: LambdaResponse):
    """
    Endpoint to receive results from AWS Lambda.

    Args:
        response (LambdaResponse): The payload containing id, cd_occurrence, and generated_response.

    Returns:
        dict: Confirmation message with received data.
    """
    try:
        # Log or process the data here
        print("Received response:", response)

        return {
            "message": "Response received successfully.",
            "received": response.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
