#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - HuggingFace Client
Cliente para integração com HuggingFace API para análise complementar
"""

import os
import logging
import requests
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class HuggingFaceClient:
    """Cliente para integração com HuggingFace API"""
    
    def __init__(self):
        """Inicializa cliente HuggingFace"""
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.model_name = os.getenv("HUGGINGFACE_MODEL_NAME", "meta-llama/Meta-Llama-3-70B")
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.available = bool(self.api_key)
        
        if self.available:
            logger.info("HuggingFace client inicializado com sucesso")
        else:
            logger.warning("HuggingFace API key não encontrada")
    
    def is_available(self) -> bool:
        """Verifica se o cliente está disponível"""
        return self.available
    
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        timeout: int = 60
    ) -> Optional[str]:
        """Gera texto usando HuggingFace"""
        
        if not self.available:
            logger.warning("HuggingFace não está disponível")
            return None
        
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                    content = data[0]["generated_text"]
                    # Hugging Face often returns the prompt as part of the generated text
                    # We need to remove it if it's present at the beginning
                    if content.startswith(prompt):
                        content = content[len(prompt):].strip()
                    logger.info(f"HuggingFace gerou {len(content)} caracteres")
                    return content
                else:
                    logger.error(f"Resposta inesperada do HuggingFace: {data}")
                    return None
            else:
                logger.error(f"Erro HuggingFace: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na requisição HuggingFace: {str(e)}", exc_info=True)
            return None
    
    def analyze_market_strategy(self, context: Dict[str, Any]) -> Optional[str]:
        """Análise estratégica específica de mercado"""
        
        prompt = f"""
        Como especialista em estratégia de mercado, analise o seguinte contexto e forneça 5 insights estratégicos únicos:
        
        Segmento: {context.get(\'segmento\', \'Não especificado\')}
        Produto: {context.get(\'produto\', \'Não especificado\')}
        Público: {context.get(\'publico\', \'Não especificado\')}
        Preço: {context.get(\'preco\', \'Não especificado\')}
        
        Foque em:
        1. Oportunidades ocultas no mercado
        2. Riscos não percebidos pela maioria
        3. Estratégias de diferenciação inovadoras
        4. Tendências emergentes relevantes
        5. Recomendações táticas específicas
        
        Seja específico e evite generalidades. Cada insight deve ser acionável.
        """
        
        return self.generate_text(prompt, max_tokens=1500, temperature=0.8)

# Instância global (opcional)
try:
    huggingface_client = HuggingFaceClient()
except Exception as e:
    logger.error(f"Erro ao inicializar HuggingFace client: {str(e)}")
    huggingface_client = None


