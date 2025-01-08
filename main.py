from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi.responses import JSONResponse

# Define the FastAPI application
app = FastAPI(title="Lambda Response Receiver API", description="API to receive and process results from AWS Lambda.")

# Define the data model for incoming POST requests
class LambdaResponse(BaseModel):
    id: str
    cd_occurrence: str
    prompt: str  # Novo campo 'prompt' que será enviado pela Lambda
    status: str  # Campo status, que será enviado pela Lambda
    generated_response: str  # Campo generated_response, que será enviado pela Lambda
    generated_response_formatted: Optional[str] = None  # Campo opcional generated_response_formatted
    error: Optional[str] = None  # Campo opcional para erro, que pode ser enviado pela Lambda

    class Config:
        # Permite que qualquer chave adicional seja aceita no JSON
        extra = "allow"

@app.post("/lambda-response")
async def receive_lambda_response(response: LambdaResponse):
    """
    Endpoint to receive results from AWS Lambda.
    Args:
        response (LambdaResponse): The payload containing id, cd_occurrence, prompt, generated_response, and status.
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

# Caso haja algum erro no corpo da requisição, a resposta mostrará os detalhes
@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc: ValidationError):
    print("Validation error details:", exc.errors())  # Logando os detalhes do erro de validação
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Erro de validação", "detail": exc.errors()},
    )

