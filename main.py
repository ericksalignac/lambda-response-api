import json
import xml.etree.ElementTree as ET
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Define the FastAPI application
app = FastAPI(title="Lambda Response Receiver API", description="API to receive and process results from AWS Lambda.")

def extrair_campos_e_formatar_reposta(response, retorno=False):
    """
    Recebe a resposta_do_modelo entre tags XML, extrai os campos e retorna o texto formatado adequadamente

    Argumentos: 
        resposta_do_modelo (str): texto a ser processado
        retorno (bool): Se True irá retornar os campos extraídos em formato de dicionário

    Retorna:
        resposta_do_modelo_formatada (str): Resposta formatada do modelo
        campos_da_resposta_do_modelo (dict) : se retorno == True retorna os campos extraídos da resposta

    """

    resposta_json = json.loads(response)
    resposta_do_modelo = resposta_json["generated_response"]

    # Parsear o XML
    root = ET.fromstring(resposta_do_modelo)

    # Função recursiva para extrair tags e conteúdos
    def extract_tags(element):
        campos_da_resposta_do_modelo = {}
        for child in element:
            tag_key = child.tag  # Apenas o nome da tag
            campos_da_resposta_do_modelo[tag_key] = child.text.strip() if child.text else ""
            # Adicionar conteúdo dos filhos, se houver
            campos_da_resposta_do_modelo.update(extract_tags(child))
        return campos_da_resposta_do_modelo

    # Extrair todas as tags e conteúdos
    campos_da_resposta_do_modelo = extract_tags(root)

    # Gerar a resposta_do_modelo_formatada com título e subtítulos

    resposta_do_modelo_formatada = "PARECER TÉCNICO\n\n"  # Título principal
    for chave, conteudo in campos_da_resposta_do_modelo.items():
        # Substituir "_" por espaço e capitalizar cada palavra para o subtítulo
        subtitulo = chave.replace("_", " ").title()
        resposta_do_modelo_formatada += f"{subtitulo}\n{'-' * len(subtitulo)}\n{conteudo}\n\n"

    if retorno == True:
        return resposta_do_modelo_formatada, campos_da_resposta_do_modelo 
    else:
        return resposta_do_modelo_formatada




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
        print(extrair_campos_e_formatar_reposta(response))

        return {
            "message": "Response received successfully.",
            "received": response.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
