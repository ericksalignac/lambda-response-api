from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Define the FastAPI application
app = FastAPI(title="Lambda Response Receiver API", description="API to receive and process results from AWS Lambda.")

# Define the data model for incoming POST requests
class LambdaResponse(BaseModel):
    id: str
    cd_occurrence: str
    status: str  # Adicionando o campo status, que será enviado pela Lambda
    generated_response: str  # Adicionando o campo generated_response
    generated_response_formatted: Optional[str] = None  # Se necessário, adicione como opcional

@app.post("/lambda-response")
async def receive_lambda_response(response: LambdaResponse):
    """
    Endpoint to receive results from AWS Lambda.
    Args:
        response (LambdaResponse): The payload containing id, cd_occurrence, generated_response, and status.
    Returns:
        dict: Confirmation message with received data.
    """
    try:
        # Log the received data to console (if necessary)
        print("Received response:", response)

        # Return the exact data sent by the Lambda
        return response.dict()  # Retorna a resposta sem alterações
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
