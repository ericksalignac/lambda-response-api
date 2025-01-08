from fastapi import FastAPI
import logging
from pydantic import BaseModel
from typing import Optional  # Adicionando a importação de Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the FastAPI application
app = FastAPI(title="Lambda Response Receiver API", description="API to receive and print results from AWS Lambda.")

# Define the data model for incoming POST requests
class LambdaResponse(BaseModel):
    id: str
    cd_occurrence: str
    prompt: str
    status: str
    generated_response: str
    generated_response_formatted: Optional[str] = None  # Campo opcional
    error: Optional[str] = None  # Campo opcional

@app.post("/lambda-response")
async def receive_lambda_response(response: LambdaResponse):
    """
    Endpoint to receive results from AWS Lambda and print them.
    Args:
        response (LambdaResponse): The payload containing id, cd_occurrence, prompt, generated_response, and status.
    Returns:
        dict: Confirmation message with received data.
    """
    try:
        # Log the received data to console (or use logger)
        logger.info("Received response: %s", response.dict())

        # Optionally, you can print the response
        print("Received response:", response.dict())

        # Return the exact data sent by the Lambda
        return response.dict()  # Return the response as is
    except Exception as e:
        logger.error("Error processing the request: %s", str(e))
        return {"error": "An error occurred while processing the request."}
