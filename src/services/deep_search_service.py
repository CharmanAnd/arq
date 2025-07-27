#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Serviço de Busca Profunda
Pesquisa avançada na internet com múltiplas fontes
"""

import os
import logging
import time
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DeepSearchService:
    """Serviço de busca profunda na internet"""
    
    def __init__(self):
        """Inicializa serviço de busca"""
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.google_search_key = os.getenv('GOOGLE_SEARCH_KEY')
        self.jina_api_key = os.getenv('JINA_API_KEY')
        
        # URLs das APIs
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
        self.google_search_url = "https://www.googleapis.com/customsearch/v1"
        self.jina_reader_url = "https://r.jina.ai/"
        
        # Headers para requisições
        self.headers = {
            'User-Agent': 'ARQV30-Enhanced/2.0 (Market Research Bot)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def perform_deep_search(
        self, 
        query: str, 
        context_data: Dict[str, Any],
        max_results: int = 10
    ) -> str:
        """Realiza busca profunda com múltiplas fontes"""
        
        try:
            logger.info(f"Iniciando busca profunda para: {query}")
            start_time = time.time()
            
            # Resultados consolidados
            search_results = []
            
            # 1. Busca com Google Custom Search (se disponível)
            if self.google_search_key:
                google_results = self._google_search(query, max_results // 2)
                search_results.extend(google_results)
            
            # 2. Busca alternativa com DuckDuckGo
            ddg_results = self._duckduckgo_search(query, max_results // 2)
            search_results.extend(ddg_results)
            
            # 3. Extrai conteúdo das páginas encontradas
            content_results = []
            for result in search_results[:5]:  # Limita a 5 páginas
                content = self._extract_page_content(result.get('url', ''))
                if content:
                    content_results.append({
                        'title': result.get('title', ''),
                        'url': result.get('url', ''),
                        'content': content[:2000]  # Limita conteúdo
                    })
            
            # 4. Processa com DeepSeek (se disponível)
            if self.deepseek_api_key and content_results:
                processed_content = self._process_with_deepseek(
                    query, context_data, content_results
                )
            else:
                processed_content = self._process_basic_content(content_results)
            
            end_time = time.time()
            logger.info(f"Busca profunda concluída em {end_time - start_time:.2f} segundos")
            
            return processed_content
            
        except Exception as e:
            logger.error(f"Erro na busca profunda: {str(e)}")
            return self._generate_fallback_search(query, context_data)
    
    def _google_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca usando Google Custom Search API"""
        try:
            if not self.google_search_key:
                return []
            
            params = {
                'key': self.google_search_key,
                'cx': '017576662512468239146:omuauf_lfve',  # CSE ID genérico
                'q': query,
                'num': min(max_results, 10),
                'lr': 'lang_pt',
                'gl': 'br'
            }
            
            response = requests.get(
                self.google_search_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('items', []):
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'google'
                    })
                
                logger.info(f"Google Search: {len(results)} resultados")
                return results
            else:
                logger.warning(f"Google Search falhou: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Erro no Google Search: {str(e)}")
            return []
    
    def _duckduckgo_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca usando DuckDuckGo (método alternativo)"""
        try:
            # Simula busca DuckDuckGo via scraping básico
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            
            response = requests.get(
                search_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                # Parse básico do HTML (implementação simplificada)
                results = []
                
                # Para demonstração, retorna resultados simulados
                sample_results = [
                    {
                        'title': f'Resultado sobre {query} - Fonte 1',
                        'url': 'https://example.com/1',
                        'snippet': f'Informações relevantes sobre {query}...',
                        'source': 'duckduckgo'
                    },
                    {
                        'title': f'Análise de mercado - {query}',
                        'url': 'https://example.com/2',
                        'snippet': f'Dados e estatísticas sobre {query}...',
                        'source': 'duckduckgo'
                    }
                ]
                
                logger.info(f"DuckDuckGo Search: {len(sample_results)} resultados simulados")
                return sample_results[:max_results]
            
            return []
            
        except Exception as e:
            logger.error(f"Erro no DuckDuckGo Search: {str(e)}")
            return []
    
    def _extract_page_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo de uma página web"""
        try:
            if not url or not url.startswith('http'):
                return None
            
            # Usa Jina Reader se disponível
            if self.jina_api_key:
                return self._extract_with_jina(url)
            else:
                return self._extract_basic(url)
                
        except Exception as e:
            logger.error(f"Erro ao extrair conteúdo de {url}: {str(e)}")
            return None
    
    def _extract_with_jina(self, url: str) -> Optional[str]:
        """Extrai conteúdo usando Jina Reader"""
        try:
            headers = {
                'Authorization': f'Bearer {self.jina_api_key}',
                'Accept': 'application/json'
            }
            
            response = requests.get(
                f"{self.jina_reader_url}{url}",
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                return response.text[:3000]  # Limita tamanho
            
            return None
            
        except Exception as e:
            logger.error(f"Erro no Jina Reader: {str(e)}")
            return None
    
    def _extract_basic(self, url: str) -> Optional[str]:
        """Extração básica de conteúdo"""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                # Parse básico do HTML
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove scripts e styles
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Extrai texto
                text = soup.get_text()
                
                # Limpa e limita
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text[:3000]  # Limita a 3000 caracteres
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na extração básica: {str(e)}")
            return None
    
    def _process_with_deepseek(
        self, 
        query: str, 
        context: Dict[str, Any], 
        content_results: List[Dict[str, Any]]
    ) -> str:
        """Processa resultados usando DeepSeek"""
        try:
            # Prepara prompt para DeepSeek
            prompt = f"""
Analise os seguintes resultados de pesquisa sobre "{query}" e extraia insights relevantes para análise de mercado:

CONTEXTO DO PROJETO:
- Segmento: {context.get('segmento', 'N/A')}
- Produto: {context.get('produto', 'N/A')}
- Público: {context.get('publico', 'N/A')}

RESULTADOS DA PESQUISA:
"""
            
            for i, result in enumerate(content_results, 1):
                prompt += f"\n{i}. {result['title']}\n{result['content']}\n"
            
            prompt += """
Forneça um resumo estruturado com:
1. Principais tendências identificadas
2. Dados de mercado relevantes
3. Oportunidades identificadas
4. Insights para estratégia de marketing
5. Informações sobre concorrência

Seja conciso e focado nos dados mais relevantes.
"""
            
            # Chama DeepSeek API
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                self.deepseek_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                logger.warning(f"DeepSeek API falhou: {response.status_code}")
                return self._process_basic_content(content_results)
                
        except Exception as e:
            logger.error(f"Erro no processamento DeepSeek: {str(e)}")
            return self._process_basic_content(content_results)
    
    def _process_basic_content(self, content_results: List[Dict[str, Any]]) -> str:
        """Processamento básico dos resultados"""
        if not content_results:
            return "Nenhum resultado de pesquisa encontrado."
        
        summary = "RESUMO DA PESQUISA:\n\n"
        
        for i, result in enumerate(content_results, 1):
            summary += f"{i}. {result['title']}\n"
            summary += f"   {result['content'][:200]}...\n\n"
        
        summary += f"\nTotal de {len(content_results)} fontes analisadas."
        
        return summary
    
    def _generate_fallback_search(self, query: str, context: Dict[str, Any]) -> str:
        """Gera resultado de busca básico em caso de erro"""
        return f"""
PESQUISA SIMULADA PARA: {query}

TENDÊNCIAS IDENTIFICADAS:
- Crescimento do mercado digital no Brasil
- Aumento da demanda por soluções online
- Competição crescente no segmento {context.get('segmento', 'digital')}

OPORTUNIDADES:
- Mercado em expansão
- Demanda por soluções inovadoras
- Potencial de diferenciação

INSIGHTS:
- Foco na experiência do cliente
- Importância do marketing digital
- Necessidade de posicionamento claro

Nota: Esta é uma análise básica. Para resultados mais precisos, configure as APIs de pesquisa.
"""

# Instância global do serviço
deep_search_service = DeepSearchService()

