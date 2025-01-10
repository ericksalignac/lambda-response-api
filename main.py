from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Define the FastAPI application
app = FastAPI(title="Lambda Response Receiver API", description="API to receive and print results from AWS Lambda.")

# Define the data model for incoming POST requests
class LambdaResponse(BaseModel):
    id: str
    cd_occurrence: str
    prompt: Optional[str] = None  # Agora é opcional
    status: str
    generated_response: Optional[str] = None  # Agora é opcional
    generated_response_formatted: Optional[str] = None  # Agora é opcional
    error: str = ""  # Definindo valor padrão de string vazia

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
        # Print the received data
        print("Received response:", response.dict())

        # Return the exact data sent by the Lambda
        return response.dict()  # Return the response as is
    except Exception as e:
        print(f"Error processing the request: {str(e)}")
        return {"error": "An error occurred while processing the request."}


class DlqLambdaResponse(BaseModel):
    id: str
    cd_occurrence: str
    message: str

@app.post("/lambda-dlq-response")
async def receive_lambda_response(response: DlqLambdaResponse):
    """
    Endpoint to receive results from AWS Lambda and print them.
    Args:
        response (LambdaResponse): The payload containing id, cd_occurrence, prompt, generated_response, and status.
    Returns:
        dict: Confirmation message with received data.
    """
    try:
        # Print the received data
        print("Received response:", response.dict())

        # Return the exact data sent by the Lambda
        return response.dict()  # Return the response as is
    except Exception as e:
        print(f"Error processing the request: {str(e)}")
        return {"error": "An error occurred while processing the request."}


