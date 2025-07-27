#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - WebSailor Integration
Navegação web avançada para pesquisa profunda e extração de insights
"""

import os
import logging
import time
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus, urljoin
import json
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class WebSailorAgent:
    """Agente WebSailor para navegação web avançada"""
    
    def __init__(self):
        """Inicializa agente WebSailor"""
        self.enabled = os.getenv("WEBSAILOR_ENABLED", "false").lower() == "true"
        self.google_search_key = os.getenv("GOOGLE_SEARCH_KEY")
        self.jina_api_key = os.getenv("JINA_API_KEY")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID", "017576662512468239146:omuauf_lfve") # ID de CSE genérico ou do usuário
        
        # URLs das APIs
        self.google_search_url = "https://www.googleapis.com/customsearch/v1"
        self.jina_reader_url = "https://r.jina.ai/"
        
        # Headers para requisições
        self.headers = {
            "User-Agent": "ARQV30-Enhanced-WebSailor/2.0 (Market Research Agent)",
            "Accept": "application/json, text/html, */*",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br"
        }
        
        # Cache para evitar requisições duplicadas e otimizar
        self.cache = {}
        self.cache_ttl = 3600  # 1 hora
        
        logger.info(f"WebSailor Agent initialized - Enabled: {self.enabled}")
    
    def is_available(self) -> bool:
        """Verifica se o WebSailor está disponível"""
        return self.enabled and (self.google_search_key or self.jina_api_key)
    
    def navigate_and_research(
        self, 
        query: str, 
        context: Dict[str, Any],
        max_pages: int = 8,  # Aumentado de 5 para 8
        depth: int = 2,  # Padrão agora é profundidade 2
        aggressive_mode: bool = True  # Novo modo agressivo para pesquisa intensiva
    ) -> Dict[str, Any]:
        """Navega e pesquisa informações relevantes com profundidade"""
        
        if not self.is_available():
            logger.warning("WebSailor não está disponível")
            return self._generate_fallback_research(query, context)
        
        try:
            logger.info(f"Iniciando pesquisa WebSailor para: {query} (Profundidade: {depth}, Modo Agressivo: {aggressive_mode})")
            start_time = time.time()
            
            all_page_contents = []
            
            # 1. Busca inicial (mais páginas se modo agressivo)
            search_pages = max_pages * 2 if aggressive_mode else max_pages
            search_results = self._perform_search(query, search_pages)
            
            # 2. Navega e extrai conteúdo das páginas principais
            for result in search_results:
                content = self._extract_page_content(result["url"])
                if content:
                    all_page_contents.append({
                        "url": result["url"],
                        "title": result["title"],
                        "content": content,
                        "relevance_score": self._calculate_relevance(content, query, context),
                        "source_type": "primary_search"
                    })
            
            # 3. Pesquisa em profundidade (se depth > 1)
            if depth > 1:
                logger.info(f"Iniciando pesquisa em profundidade (nível {depth})...")
                top_pages = 5 if aggressive_mode else 3  # Mais páginas no modo agressivo
                for page in all_page_contents[:top_pages]:
                    internal_links = self._extract_internal_links(page["url"], page["content"])
                    links_to_process = 4 if aggressive_mode else 2  # Mais links internos no modo agressivo
                    for link in internal_links[:links_to_process]:
                        internal_content = self._extract_page_content(link)
                        if internal_content:
                            all_page_contents.append({
                                "url": link,
                                "title": f"Link interno de {page['title']}",
                                "content": internal_content,
                                "relevance_score": self._calculate_relevance(internal_content, query, context) * 0.8,
                                "source_type": "internal_link"
                            })
            
            # 4. Pesquisa de queries relacionadas (modo agressivo)
            if aggressive_mode:
                logger.info("Executando pesquisa de queries relacionadas (modo agressivo)...")
                related_queries = self._generate_related_queries(query, context)
                for related_query in related_queries[:3]:  # Máximo 3 queries relacionadas
                    related_results = self._perform_search(related_query, 3)  # 3 resultados por query relacionada
                    for result in related_results:
                        content = self._extract_page_content(result["url"])
                        if content:
                            all_page_contents.append({
                                "url": result["url"],
                                "title": result["title"],
                                "content": content,
                                "relevance_score": self._calculate_relevance(content, query, context) * 0.7,  # Menor relevância
                                "source_type": "related_query"
                            })
            
            # 5. Filtra e ordena por relevância (geral)
            all_page_contents.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            # 6. Consolida informações
            research_result = self._consolidate_research(all_page_contents, query, context)
            
            end_time = time.time()
            logger.info(f"Pesquisa WebSailor concluída em {end_time - start_time:.2f} segundos")
            
            return research_result
            
        except Exception as e:
            logger.error(f"Erro na pesquisa WebSailor: {str(e)}", exc_info=True)
            return self._generate_fallback_research(query, context)
    
    def _perform_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Realiza busca usando Google Custom Search ou alternativa"""
        
        cache_key = f"search_{hash(query)}"
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if time.time() - cached_result["timestamp"] < self.cache_ttl:
                logger.info("Usando resultado de busca do cache")
                return cached_result["data"]
        
        results = []
        
        if self.google_search_key:
            results = self._google_search(query, max_results)
        
        if not results:
            results = self._alternative_search(query, max_results)
        
        self.cache[cache_key] = {
            "data": results,
            "timestamp": time.time()
        }
        
        return results
    
    def _google_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca usando Google Custom Search API"""
        
        try:
            enhanced_query = self._enhance_search_query(query)
            
            params = {
                "key": self.google_search_key,
                "cx": self.google_cse_id,
                "q": enhanced_query,
                "num": min(max_results, 10),
                "lr": "lang_pt",
                "gl": "br",
                "safe": "medium",
                "dateRestrict": "y1"  # Últimos 12 meses
            }
            
            response = requests.get(
                self.google_search_url,
                params=params,
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get("items", []):
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "source": "google_cse"
                    })
                
                logger.info(f"Google Search retornou {len(results)} resultados")
                return results
            else:
                logger.warning(f"Google Search falhou: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Erro no Google Search: {str(e)}", exc_info=True)
            return []
    
    def _alternative_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca alternativa quando Google não está disponível ou falha"""
        
        logger.info("Realizando busca alternativa (simulada).")
        base_results = [
            {
                "title": f"Análise de mercado: {query}",
                "url": "https://example.com/analise-mercado",
                "snippet": f"Informações relevantes sobre {query} no mercado brasileiro.",
                "source": "alternative"
            },
            {
                "title": f"Tendências {query} 2024",
                "url": "https://example.com/tendencias-2024",
                "snippet": f"Principais tendências e oportunidades em {query}.",
                "source": "alternative"
            },
            {
                "title": f"Estratégias de marketing para {query}",
                "url": "https://example.com/marketing-estrategias",
                "snippet": f"Como desenvolver estratégias eficazes para {query}.",
                "source": "alternative"
            }
        ]
        
        return base_results[:max_results]
    
    def _enhance_search_query(self, query: str) -> str:
        """Melhora a query de busca para pesquisa de mercado"""
        
        market_terms = [
            "mercado brasileiro",
            "análise de mercado",
            "tendências 2024",
            "oportunidades negócio",
            "estratégia marketing",
            "dados",
            "estatísticas",
            "relatório"
        ]
        
        relevant_terms = []
        query_lower = query.lower()
        
        if "mercado" not in query_lower:
            relevant_terms.append("mercado")
        
        if "brasil" not in query_lower and "brasileiro" not in query_lower:
            relevant_terms.append("Brasil")
        
        if "2024" not in query_lower and "2025" not in query_lower:
            relevant_terms.append("2024") # Manter 2024 como padrão, mas pode ser 2025
        
        # Adiciona termos de mercado relevantes se a query for muito genérica
        if len(query.split()) < 3:
            relevant_terms.extend(market_terms[:2]) # Adiciona os 2 primeiros termos de mercado

        enhanced_query = query
        if relevant_terms:
            enhanced_query += " " + " ".join(relevant_terms)
        
        return enhanced_query.strip()
    
    def _extract_page_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo de uma página web"""
        
        if not url or not url.startswith("http"): # Garante que é uma URL válida
            return None
        
        cache_key = f"content_{hash(url)}"
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if time.time() - cached_result["timestamp"] < self.cache_ttl:
                return cached_result["data"]
        
        content = None
        
        if self.jina_api_key:
            content = self._extract_with_jina(url)
        
        if not content:
            content = self._extract_basic_content(url)
        
        if content:
            self.cache[cache_key] = {
                "data": content,
                "timestamp": time.time()
            }
        
        return content
    
    def _extract_with_jina(self, url: str) -> Optional[str]:
        """Extrai conteúdo usando Jina Reader API"""
        
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {self.jina_api_key}"
            }
            
            jina_url = f"{self.jina_reader_url}{url}"
            
            response = requests.get(
                jina_url,
                headers=headers,
                timeout=30 # Aumentar timeout para Jina
            )
            
            if response.status_code == 200:
                content = response.text
                
                # Limita tamanho do conteúdo, mas permite mais que antes
                if len(content) > 10000: # Aumentado para 10k caracteres
                    content = content[:10000] + "... [conteúdo truncado]"
                
                logger.info(f"Conteúdo extraído com Jina Reader: {len(content)} caracteres de {url}")
                return content
            else:
                logger.warning(f"Jina Reader falhou para {url}: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro no Jina Reader para {url}: {str(e)}", exc_info=True)
            return None
    
    def _extract_basic_content(self, url: str) -> Optional[str]:
        """Extração básica de conteúdo usando requests + BeautifulSoup"""
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=20, # Aumentar timeout para requests
                allow_redirects=True
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                for element in soup(["script", "style", "nav", "footer", "header", "form", "aside"]):
                    element.decompose()
                
                text = soup.get_text()
                
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = " ".join(chunk for chunk in chunks if chunk)
                
                if len(text) > 6000: # Aumentado para 6k caracteres
                    text = text[:6000] + "... [conteúdo truncado]"
                
                logger.info(f"Conteúdo extraído básico: {len(text)} caracteres de {url}")
                return text
            else:
                logger.warning(f"Falha ao acessar {url}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na extração básica para {url}: {str(e)}", exc_info=True)
            return None

    def _extract_internal_links(self, base_url: str, content: str) -> List[str]:
        """Extrai links internos de uma página para pesquisa em profundidade"""
        links = []
        try:
            soup = BeautifulSoup(content, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                full_url = urljoin(base_url, href)
                # Filtra apenas links que são do mesmo domínio e não são âncoras internas
                if full_url.startswith(base_url) and "#" not in full_url and full_url != base_url:
                    links.append(full_url)
            logger.info(f"Encontrados {len(links)} links internos em {base_url}")
        except Exception as e:
            logger.warning(f"Erro ao extrair links internos de {base_url}: {str(e)}")
        return list(set(links)) # Remove duplicatas
    
    def _calculate_relevance(
        self, 
        content: str, 
        query: str, 
        context: Dict[str, Any]
    ) -> float:
        """Calcula score de relevância do conteúdo"""
        
        if not content:
            return 0.0
        
        content_lower = content.lower()
        query_lower = query.lower()
        
        score = 0.0
        
        # Score baseado na query
        query_words = query_lower.split()
        for word in query_words:
            if len(word) > 2:
                score += content_lower.count(word) * 0.2 # Peso maior para palavras da query
        
        # Score baseado no contexto
        context_terms = [
            context.get("segmento", "").lower(),
            context.get("produto", "").lower(),
            context.get("publico", "").lower()
        ]
        
        for term in context_terms:
            if term and len(term) > 2:
                score += content_lower.count(term) * 0.3 # Peso ainda maior para termos do contexto
        
        # Bonus para termos de mercado
        market_terms = [
            "mercado", "análise", "tendência", "oportunidade",
            "estratégia", "marketing", "concorrência", "público",
            "crescimento", "demanda", "inovação", "tecnologia"
        ]
        
        for term in market_terms:
            score += content_lower.count(term) * 0.1
        
        # Bônus por proximidade de termos (simplificado)
        if all(word in content_lower for word in query_words) and len(query_words) > 1:
            score += 5.0 # Bônus se todos os termos da query estiverem presentes

        # Normaliza score (0-100 para facilitar visualização)
        # O score máximo pode variar muito, então uma normalização simples pode ser: 
        # dividir pelo log do tamanho do conteúdo para penalizar textos muito longos com pouca densidade
        normalized_score = score / (len(content) / 1000 + 1) # Divide por 1 para cada 1000 caracteres
        return min(normalized_score, 100.0) # Limita o score máximo
    
    def _consolidate_research(
        self, 
        page_contents: List[Dict[str, Any]], 
        query: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consolida informações da pesquisa, gerando insights mais ricos"""
        
        if not page_contents:
            return self._generate_fallback_research(query, context)
        
        # Ordena novamente por relevância, caso a profundidade tenha adicionado novos itens
        page_contents.sort(key=lambda x: x["relevance_score"], reverse=True)

        # Combina o conteúdo das páginas mais relevantes para análise da IA
        combined_content = ""
        sources_list = []
        for i, page in enumerate(page_contents):
            combined_content += f"\n--- Conteúdo da Página {i+1} ({page['url']}) ---\n"
            combined_content += page["content"]
            sources_list.append({
                "title": page["title"],
                "url": page["url"],
                "relevance_score": page["relevance_score"]
            })
            if len(combined_content) > 15000: # Limita o conteúdo combinado para não estourar o token da IA
                combined_content = combined_content[:15000] + "... [conteúdo adicional truncado]"
                break
        
        # Usar Gemini para extrair insights, tendências e oportunidades do conteúdo combinado
        # Importa o gemini_client aqui para evitar circular dependency
        from services.gemini_client import gemini_client

        if not gemini_client:
            logger.error("Gemini client não disponível para consolidação de pesquisa.")
            return self._generate_fallback_research(query, context)

        prompt_for_ai = f"""Com base no seguinte conteúdo de pesquisa web sobre '{query}' (contexto: {context}), extraia os principais insights, tendências de mercado e oportunidades. Seja detalhado e forneça exemplos quando possível. Formate a saída como um JSON com as chaves 'key_insights', 'market_trends', 'opportunities'.

Conteúdo:
```text
{combined_content}
```

JSON:
"""
        try:
            ai_response = gemini_client.generate_content(prompt_for_ai, timeout=60) # Aumentar timeout
            json_match = re.search(r"```json\n(.*?)```", ai_response, re.DOTALL)
            if not json_match:
                json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)

            if json_match:
                ai_extracted_data = json.loads(json_match.group(1) if json_match.group(1) else json_match.group(0))
                insights = ai_extracted_data.get("key_insights", [])
                trends = ai_extracted_data.get("market_trends", [])
                opportunities = ai_extracted_data.get("opportunities", [])
            else:
                logger.warning("IA não retornou JSON válido para consolidação. Usando extração básica.")
                insights, trends, opportunities = self._extract_basic_insights(combined_content)

        except Exception as e:
            logger.error(f"Erro ao usar IA para consolidar pesquisa: {str(e)}. Usando extração básica.", exc_info=True)
            insights, trends, opportunities = self._extract_basic_insights(combined_content)
        
        result = {
            "query": query,
            "context": context,
            "pages_analyzed": len(page_contents),
            "research_summary": {
                "key_insights": insights,
                "market_trends": trends,
                "opportunities": opportunities
            },
            "sources": sources_list,
            "metadata": {
                "research_date": datetime.now().isoformat(),
                "agent": "WebSailor",
                "version": "2.0.0",
                "ai_assisted_consolidation": True if gemini_client else False
            }
        }
        
        return result
    
    def _extract_basic_insights(self, text_content: str) -> tuple[List[str], List[str], List[str]]:
        """Extração básica de insights de texto sem IA (fallback)"""
        insights = []
        trends = []
        opportunities = []
        
        sentences = text_content.split(". ")
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 50:
                if "tendência" in sentence.lower() or "crescimento" in sentence.lower():
                    trends.append(sentence[:200])
                elif "oportunidade" in sentence.lower() or "novo mercado" in sentence.lower():
                    opportunities.append(sentence[:200])
                elif "insight" in sentence.lower() or "chave" in sentence.lower() or "importante" in sentence.lower():
                    insights.append(sentence[:200])
                elif any(term in sentence.lower() for term in ["mercado", "análise", "estratégia"]):
                    insights.append(sentence[:200])
        
        return list(set(insights))[:5], list(set(trends))[:3], list(set(opportunities))[:3]

    def _generate_fallback_research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gera pesquisa básica quando WebSailor não está disponível ou falha"""
        logger.warning("Gerando pesquisa de fallback.")
        return {
            "query": query,
            "context": context,
            "pages_analyzed": 0,
            "research_summary": {
                "key_insights": [
                    f"O mercado para '{query}' é dinâmico e exige adaptação.",
                    "A personalização e a automação são cruciais para o sucesso."
                ],
                "market_trends": [
                    "Crescimento contínuo do digital.",
                    "Aumento da demanda por soluções eficientes."
                ],
                "opportunities": [
                    "Identificar nichos inexplorados.",
                    "Investir em conteúdo de valor."
                ]
            },
            "sources": [],
            "metadata": {
                "research_date": datetime.now().isoformat(),
                "agent": "WebSailor_Fallback",
                "version": "2.0.0",
                "note": "WebSailor não disponível ou erro na pesquisa."
            }
        }

# Instância global do serviço
websailor_agent = WebSailorAgent()

def _generate_related_queries(self, original_query: str, context: Dict[str, Any]) -> List[str]:
        """Gera queries relacionadas para pesquisa mais abrangente"""
        
        segmento = context.get("segmento", "")
        produto = context.get("produto", "")
        
        related_queries = []
        
        # Queries baseadas em aspectos específicos
        if segmento:
            related_queries.extend([
                f"estatísticas {segmento} Brasil 2024",
                f"crescimento mercado {segmento}",
                f"principais players {segmento}",
                f"tendências futuras {segmento}",
                f"desafios {segmento} brasileiro"
            ])
        
        if produto:
            related_queries.extend([
                f"como vender {produto} online",
                f"preço médio {produto} mercado",
                f"demanda {produto} Brasil"
            ])
        
        # Queries de contexto geral
        related_queries.extend([
            f"análise SWOT {original_query}",
            f"oportunidades investimento {original_query}",
            f"cases sucesso {original_query}"
        ])
        
        # Remove duplicatas e queries muito similares à original
        unique_queries = []
        for query in related_queries:
            if query.lower() not in original_query.lower() and query not in unique_queries:
                unique_queries.append(query)
        
        return unique_queries[:5]  # Máximo 5 queries relacionadas

