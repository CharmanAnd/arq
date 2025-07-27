#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Motor de Análise Aprimorado
Sistema de análise ultra-detalhada com múltiplas IAs e pesquisa profunda
"""

import os
import logging
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import concurrent.futures
from services.gemini_client import gemini_client
from services.websailor_integration import websailor_agent
from services.attachment_service import attachment_service

logger = logging.getLogger(__name__)

class EnhancedAnalysisEngine:
    """Motor de análise aprimorado com múltiplas fontes de dados e IAs"""
    
    def __init__(self):
        """Inicializa o motor de análise"""
        self.max_analysis_time = 600  # 10 minutos máximo
        self.deep_research_enabled = True
        self.multi_ai_enabled = True
        
        logger.info("Enhanced Analysis Engine inicializado")
    
    def generate_ultra_detailed_analysis(
        self, 
        data: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gera análise ultra-detalhada com múltiplas fontes"""
        
        start_time = time.time()
        logger.info(f"Iniciando análise ultra-detalhada para {data.get('segmento')}")
        
        try:
            # 1. Coleta de dados de múltiplas fontes
            research_data = self._collect_comprehensive_data(data, session_id)
            
            # 2. Análise com múltiplas IAs em paralelo
            ai_analyses = self._run_multi_ai_analysis(data, research_data)
            
            # 3. Consolidação e síntese final
            final_analysis = self._consolidate_analyses(data, research_data, ai_analyses)
            
            # 4. Enriquecimento com dados específicos
            enriched_analysis = self._enrich_with_specific_data(final_analysis, data)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            enriched_analysis["metadata"] = {
                "processing_time_seconds": processing_time,
                "analysis_engine": "Enhanced v2.0",
                "data_sources_used": len(research_data.get("sources", [])),
                "ai_models_used": len(ai_analyses),
                "generated_at": datetime.utcnow().isoformat(),
                "quality_score": self._calculate_quality_score(enriched_analysis)
            }
            
            logger.info(f"Análise ultra-detalhada concluída em {processing_time:.2f} segundos")
            return enriched_analysis
            
        except Exception as e:
            logger.error(f"Erro na análise ultra-detalhada: {str(e)}", exc_info=True)
            return self._generate_emergency_fallback(data, str(e))
    
    def _collect_comprehensive_data(
        self, 
        data: Dict[str, Any], 
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """Coleta dados abrangentes de múltiplas fontes"""
        
        logger.info("Coletando dados abrangentes...")
        research_data = {
            "attachments": {},
            "web_research": {},
            "market_intelligence": {},
            "sources": []
        }
        
        # Coleta dados de anexos
        if session_id:
            attachments = attachment_service.get_session_attachments(session_id)
            if attachments:
                combined_content = ""
                for att in attachments:
                    if att.get("extracted_content"):
                        combined_content += att["extracted_content"] + "\n\n"
                
                research_data["attachments"] = {
                    "count": len(attachments),
                    "content": combined_content[:8000],  # Limita para não estourar tokens
                    "types": [att.get("file_type", "unknown") for att in attachments]
                }
                logger.info(f"Dados de {len(attachments)} anexos coletados")
        
        # Pesquisa web profunda com WebSailor
        if websailor_agent.is_available() and data.get("query"):
            logger.info("Realizando pesquisa web profunda...")
            
            # Múltiplas queries para pesquisa abrangente
            queries = self._generate_research_queries(data)
            
            for query in queries:
                web_result = websailor_agent.navigate_and_research(
                    query,
                    context={
                        "segmento": data["segmento"],
                        "produto": data["produto"],
                        "publico": data["publico"]
                    },
                    max_pages=7,  # Aumentado para pesquisa mais profunda
                    depth=2  # Pesquisa em profundidade
                )
                
                research_data["web_research"][query] = web_result
                research_data["sources"].extend(web_result.get("sources", []))
            
            logger.info(f"Pesquisa web concluída com {len(queries)} queries")
        
        # Inteligência de mercado adicional
        research_data["market_intelligence"] = self._gather_market_intelligence(data)
        
        return research_data
    
    def _generate_research_queries(self, data: Dict[str, Any]) -> List[str]:
        """Gera múltiplas queries para pesquisa abrangente"""
        
        segmento = data["segmento"]
        produto = data.get("produto", "")
        publico = data.get("publico", "")
        
        queries = [
            # Query principal do usuário
            data.get("query", f"análise de mercado {segmento}"),
            
            # Queries específicas de mercado
            f"mercado {segmento} Brasil 2024 tendências",
            f"oportunidades negócio {segmento} brasileiro",
            f"concorrência {segmento} análise competitiva",
            f"público-alvo {segmento} comportamento consumidor",
            f"estratégias marketing {segmento} digital",
            f"preços {segmento} ticket médio Brasil",
            f"crescimento {segmento} projeções futuro"
        ]
        
        # Adiciona queries específicas do produto se informado
        if produto:
            queries.extend([
                f"{produto} mercado brasileiro análise",
                f"como vender {produto} online Brasil",
                f"{produto} concorrentes principais"
            ])
        
        # Remove duplicatas e limita quantidade
        unique_queries = list(set(queries))
        return unique_queries[:8]  # Máximo 8 queries para não sobrecarregar
    
    def _gather_market_intelligence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coleta inteligência de mercado adicional"""
        
        intelligence = {
            "segment_analysis": self._analyze_segment_characteristics(data["segmento"]),
            "pricing_intelligence": self._analyze_pricing_patterns(data),
            "competition_landscape": self._map_competition_landscape(data),
            "growth_indicators": self._identify_growth_indicators(data["segmento"])
        }
        
        return intelligence
    
    def _analyze_segment_characteristics(self, segmento: str) -> Dict[str, Any]:
        """Analisa características específicas do segmento"""
        
        # Base de conhecimento de segmentos
        segment_db = {
            "marketing digital": {
                "maturity": "Alto",
                "competition": "Muito Alta",
                "growth_rate": "15-25% ao ano",
                "key_players": ["Hotmart", "Monetizze", "Eduzz"],
                "avg_ticket": "R$ 297-2.997",
                "main_channels": ["Facebook Ads", "Instagram", "YouTube"]
            },
            "saúde": {
                "maturity": "Médio",
                "competition": "Alta",
                "growth_rate": "10-20% ao ano",
                "key_players": ["Drogarias", "Planos de Saúde", "Clínicas"],
                "avg_ticket": "R$ 97-497",
                "main_channels": ["Google Ads", "SEO", "Indicações"]
            },
            "educação": {
                "maturity": "Alto",
                "competition": "Alta",
                "growth_rate": "20-30% ao ano",
                "key_players": ["Coursera", "Udemy", "Alura"],
                "avg_ticket": "R$ 197-997",
                "main_channels": ["Google Ads", "YouTube", "Parcerias"]
            }
        }
        
        # Busca características do segmento
        for key, characteristics in segment_db.items():
            if key.lower() in segmento.lower():
                return characteristics
        
        # Características genéricas se não encontrar
        return {
            "maturity": "Médio",
            "competition": "Média",
            "growth_rate": "10-15% ao ano",
            "key_players": ["Diversos players regionais"],
            "avg_ticket": "R$ 197-997",
            "main_channels": ["Digital", "Tradicional"]
        }
    
    def _analyze_pricing_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa padrões de precificação"""
        
        preco = data.get("preco_float")
        segmento = data["segmento"]
        
        analysis = {
            "price_positioning": "Não informado",
            "market_comparison": "Análise indisponível",
            "optimization_suggestions": []
        }
        
        if preco:
            if preco < 100:
                analysis["price_positioning"] = "Baixo (Entrada)"
                analysis["optimization_suggestions"].append("Considere adicionar valor para justificar preço premium")
            elif preco < 500:
                analysis["price_positioning"] = "Médio (Competitivo)"
                analysis["optimization_suggestions"].append("Posição boa para escala, foque em volume")
            elif preco < 2000:
                analysis["price_positioning"] = "Alto (Premium)"
                analysis["optimization_suggestions"].append("Justifique valor com diferenciais únicos")
            else:
                analysis["price_positioning"] = "Premium (Exclusivo)"
                analysis["optimization_suggestions"].append("Foque em transformação e resultados excepcionais")
        
        return analysis
    
    def _map_competition_landscape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mapeia panorama competitivo"""
        
        return {
            "competition_level": "Média a Alta",
            "market_saturation": "Parcialmente saturado",
            "differentiation_opportunities": [
                "Atendimento personalizado",
                "Metodologia exclusiva",
                "Garantias diferenciadas",
                "Comunidade engajada"
            ],
            "competitive_advantages": [
                "Inovação constante",
                "Relacionamento próximo",
                "Resultados comprovados"
            ]
        }
    
    def _identify_growth_indicators(self, segmento: str) -> Dict[str, Any]:
        """Identifica indicadores de crescimento"""
        
        return {
            "market_trends": [
                "Digitalização acelerada",
                "Busca por automação",
                "Personalização em escala"
            ],
            "growth_drivers": [
                "Aumento da demanda online",
                "Necessidade de eficiência",
                "Busca por resultados rápidos"
            ],
            "future_outlook": "Positivo com crescimento sustentado"
        }
    
    def _run_multi_ai_analysis(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa análise com múltiplas IAs em paralelo"""
        
        logger.info("Executando análise com múltiplas IAs...")
        
        ai_analyses = {}
        
        # Análise principal com Gemini
        if gemini_client:
            try:
                gemini_analysis = self._run_gemini_analysis(data, research_data)
                ai_analyses["gemini"] = gemini_analysis
                logger.info("Análise Gemini concluída")
            except Exception as e:
                logger.error(f"Erro na análise Gemini: {str(e)}")
        
        # Análise complementar com DeepSeek (se disponível)
        try:
            from services.huggingface_client import HuggingFaceClient
            huggingface_client = HuggingFaceClient()
            huggingface_analysis = self._run_huggingface_analysis(data, research_data, huggingface_client)
            ai_analyses["huggingface"] = huggingface_analysis
            logger.info("Análise HuggingFace concluída")
        except Exception as e:
            logger.warning(f"DeepSeek não disponível ou erro: {str(e)}")
        
        return ai_analyses
    
    def _run_gemini_analysis(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa análise principal com Gemini"""
        
        prompt = self._create_ultra_detailed_prompt(data, research_data)
        
        response = gemini_client.generate_ultra_detailed_analysis(
            analysis_data=data,
            search_context=research_data.get("web_research"),
            attachments_context=research_data.get("attachments", {}).get("content")
        )
        
        return response
    
    def _run_huggingface_analysis(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any],
        huggingface_client: Any
    ) -> Dict[str, Any]:
        """Executa análise complementar com DeepSeek"""
        
        # Prompt específico para DeepSeek focado em insights estratégicos
        prompt = f"""
        Analise estrategicamente o seguinte contexto de negócio e forneça insights únicos:
        
        Segmento: {data['segmento']}
        Produto: {data.get('produto', 'Não especificado')}
        Público: {data.get('publico', 'Não especificado')}
        
        Dados de pesquisa disponíveis: {len(research_data.get('sources', []))} fontes
        
        Forneça 5 insights estratégicos únicos que não são óbvios, focando em:
        1. Oportunidades ocultas no mercado
        2. Riscos não percebidos
        3. Estratégias de diferenciação inovadoras
        4. Tendências emergentes
        5. Recomendações táticas específicas
        
        Formato: Lista numerada com explicação detalhada de cada insight.
        """
        
        response = huggingface_client.generate_text(prompt, max_tokens=1000)
        
        return {
            "strategic_insights": response,
            "model": "DeepSeek",
            "focus": "Strategic Analysis"
        }
    
    def _create_ultra_detailed_prompt(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any]
    ) -> str:
        """Cria prompt ultra-detalhado para análise"""
        
        prompt_parts = [
            "Você é um consultor de mercado de elite, especialista em análise ultra-detalhada e estratégia de negócios. Sua tarefa é gerar a análise de mercado mais completa e acionável possível, com insights profundos que vão muito além do óbvio.",
            "",
            "IMPORTANTE: Esta análise deve ter o TRIPLO da profundidade de uma análise comum. Seja extremamente específico, detalhado e forneça insights únicos que demonstrem expertise de alto nível.",
            "",
            "### DADOS DE ENTRADA:",
            f"- Segmento: {data.get('segmento')}",
            f"- Produto/Serviço: {data.get('produto')}",
            f"- Preço: R$ {data.get('preco')}",
            f"- Público-Alvo: {data.get('publico')}",
            f"- Concorrentes: {data.get('concorrentes')}",
            f"- Objetivo de Receita: R$ {data.get('objetivo_receita')}",
            f"- Orçamento Marketing: R$ {data.get('orcamento_marketing')}",
            f"- Dados Adicionais: {data.get('dados_adicionais')}",
            ""
        ]
        
        # Adiciona dados de anexos se disponíveis
        if research_data.get("attachments", {}).get("content"):
            prompt_parts.extend([
                "### DADOS EXTRAÍDOS DE ANEXOS:",
                research_data["attachments"]["content"][:3000],
                ""
            ])
        
        # Adiciona dados de pesquisa web
        if research_data.get("web_research"):
            prompt_parts.append("### DADOS DE PESQUISA WEB PROFUNDA:")
            for query, result in research_data["web_research"].items():
                summary = result.get("research_summary", {})
                if summary.get("key_insights"):
                    prompt_parts.append(f"**Query: {query}**")
                    prompt_parts.extend([f"- {insight}" for insight in summary["key_insights"][:3]])
            prompt_parts.append("")
        
        # Adiciona inteligência de mercado
        if research_data.get("market_intelligence"):
            prompt_parts.append("### INTELIGÊNCIA DE MERCADO:")
            intelligence = research_data["market_intelligence"]
            for key, value in intelligence.items():
                prompt_parts.append(f"**{key.replace('_', ' ').title()}:** {value}")
            prompt_parts.append("")
        
        # Adiciona prompts especializados dos arquivos carregados
        prompt_parts.extend([
            "### INSTRUÇÕES ESPECIALIZADAS:",
            "",
            "Aplique as técnicas do MESTRE DA PERSUASÃO VISCERAL para criar um avatar ultra-detalhado que vai muito além dos dados demográficos. Mergulhe nas dores mais profundas, desejos secretos, medos paralisantes e frustrações diárias.",
            "",
            "Use os DRIVERS MENTAIS para identificar gatilhos psicológicos específicos que podem ser ativados. Crie pelo menos 5 drivers customizados para este avatar específico.",
            "",
            "Desenvolva PROVAS VISUAIS (PROVIs) que transformem conceitos abstratos em experiências físicas memoráveis. Sugira pelo menos 3 demonstrações práticas.",
            "",
            "### ESTRUTURA DE SAÍDA JSON (ULTRA-DETALHADA):",
            ""
        ])
        
        # Estrutura JSON expandida
        json_structure = {
            "avatar_ultra_detalhado": {
                "nome_ficticio": "Nome de persona específico",
                "perfil_demografico": {
                    "idade": "Faixa etária específica",
                    "genero": "Gênero predominante",
                    "renda": "Faixa de renda detalhada",
                    "escolaridade": "Nível educacional",
                    "localizacao": "Localização geográfica",
                    "estado_civil": "Estado civil típico",
                    "ocupacao": "Profissão específica"
                },
                "perfil_psicografico": {
                    "personalidade": "Traços de personalidade detalhados",
                    "valores": "Valores fundamentais",
                    "interesses": "Interesses e hobbies",
                    "estilo_vida": "Estilo de vida detalhado",
                    "comportamento_compra": "Como toma decisões",
                    "influenciadores": "Quem influencia suas decisões"
                },
                "dores_viscerais": {
                    "dor_primaria": "A dor mais profunda e inconfessável",
                    "dor_secundaria": "Segunda maior dor",
                    "dor_terciaria": "Terceira dor significativa",
                    "frustracao_diaria": "O que mais irrita no dia a dia",
                    "medo_paralisante": "O que mais teme"
                },
                "desejos_secretos": {
                    "desejo_primario": "O que mais deseja secretamente",
                    "desejo_status": "Como quer ser visto",
                    "desejo_liberdade": "Que tipo de liberdade busca",
                    "desejo_reconhecimento": "Como quer ser reconhecido",
                    "desejo_transformacao": "Como quer se transformar"
                },
                "linguagem_interna": {
                    "frases_dor": ["Frases que usa para expressar dores"],
                    "frases_desejo": ["Frases que usa para expressar desejos"],
                    "metaforas_comuns": ["Metáforas que usa"],
                    "vocabulario_especifico": ["Palavras específicas do nicho"]
                },
                "objecoes_reais": {
                    "objecao_dinheiro": "Verdadeira objeção sobre preço",
                    "objecao_tempo": "Verdadeira objeção sobre tempo",
                    "objecao_credibilidade": "Objeção sobre confiança",
                    "objecao_capacidade": "Objeção sobre própria capacidade"
                },
                "jornada_emocional": {
                    "dia_perfeito": "Narrativa detalhada do dia ideal",
                    "pior_pesadelo": "Narrativa do pior cenário",
                    "momento_decisao": "O que o faria decidir comprar",
                    "pos_compra": "Como se sentiria após comprar"
                }
            },
            "drivers_mentais_customizados": [
                {
                    "nome": "Nome do driver",
                    "gatilho_central": "Emoção ou lógica core",
                    "definicao_visceral": "Definição impactante",
                    "roteiro_ativacao": "Como ativar este driver",
                    "frases_ancoragem": ["Frases para usar"],
                    "momento_ideal": "Quando usar na jornada"
                }
            ],
            "provas_visuais_sugeridas": [
                {
                    "nome": "Nome da demonstração",
                    "conceito_alvo": "O que quer provar",
                    "experimento": "Descrição da demonstração",
                    "analogia": "Como conecta com a vida deles",
                    "materiais": ["Lista de materiais necessários"]
                }
            ],
            "analise_concorrencia_profunda": [
                {
                    "nome": "Nome do concorrente",
                    "analise_swot": {
                        "forcas": ["Principais forças"],
                        "fraquezas": ["Principais fraquezas"],
                        "oportunidades": ["Oportunidades identificadas"],
                        "ameacas": ["Ameaças que representa"]
                    },
                    "estrategia_marketing": "Estratégia principal",
                    "posicionamento": "Como se posiciona",
                    "diferenciais": ["Principais diferenciais"],
                    "vulnerabilidades": ["Pontos fracos exploráveis"]
                }
            ],
            "estrategia_posicionamento": {
                "proposta_valor_unica": "Proposta de valor irresistível",
                "posicionamento_mercado": "Como se posicionar",
                "diferenciais_competitivos": ["Diferenciais únicos"],
                "mensagem_central": "Mensagem principal",
                "tom_comunicacao": "Tom de voz ideal"
            },
            "estrategia_palavras_chave": {
                "palavras_primarias": ["Palavras-chave principais"],
                "palavras_secundarias": ["Palavras-chave secundárias"],
                "palavras_cauda_longa": ["Long tail keywords"],
                "palavras_negativas": ["Palavras a evitar"],
                "estrategia_conteudo": "Como usar as palavras-chave"
            },
            "funil_vendas_detalhado": {
                "topo_funil": {
                    "objetivo": "Objetivo desta etapa",
                    "estrategias": ["Estratégias específicas"],
                    "conteudos": ["Tipos de conteúdo"],
                    "metricas": ["Métricas a acompanhar"]
                },
                "meio_funil": {
                    "objetivo": "Objetivo desta etapa",
                    "estrategias": ["Estratégias específicas"],
                    "conteudos": ["Tipos de conteúdo"],
                    "metricas": ["Métricas a acompanhar"]
                },
                "fundo_funil": {
                    "objetivo": "Objetivo desta etapa",
                    "estrategias": ["Estratégias específicas"],
                    "conteudos": ["Tipos de conteúdo"],
                    "metricas": ["Métricas a acompanhar"]
                }
            },
            "metricas_performance": {
                "kpis_primarios": ["KPIs mais importantes"],
                "kpis_secundarios": ["KPIs de apoio"],
                "metas_especificas": {
                    "cpl_meta": "Custo por lead ideal",
                    "cac_meta": "Custo de aquisição ideal",
                    "ltv_meta": "Lifetime value esperado",
                    "roi_meta": "ROI esperado"
                },
                "projecoes_financeiras": {
                    "cenario_conservador": {
                        "vendas_mensais": "Número de vendas",
                        "receita_mensal": "Receita esperada",
                        "lucro_mensal": "Lucro esperado",
                        "roi": "ROI esperado"
                    },
                    "cenario_realista": {
                        "vendas_mensais": "Número de vendas",
                        "receita_mensal": "Receita esperada",
                        "lucro_mensal": "Lucro esperado",
                        "roi": "ROI esperado"
                    },
                    "cenario_otimista": {
                        "vendas_mensais": "Número de vendas",
                        "receita_mensal": "Receita esperada",
                        "lucro_mensal": "Lucro esperado",
                        "roi": "ROI esperado"
                    }
                }
            },
            "plano_acao_90_dias": {
                "primeiros_30_dias": {
                    "foco": "Foco principal",
                    "atividades": ["Atividades específicas"],
                    "entregas": ["Entregas esperadas"],
                    "investimento": "Investimento necessário"
                },
                "dias_31_60": {
                    "foco": "Foco principal",
                    "atividades": ["Atividades específicas"],
                    "entregas": ["Entregas esperadas"],
                    "investimento": "Investimento necessário"
                },
                "dias_61_90": {
                    "foco": "Foco principal",
                    "atividades": ["Atividades específicas"],
                    "entregas": ["Entregas esperadas"],
                    "investimento": "Investimento necessário"
                }
            },
            "insights_exclusivos": [
                "Insight único 1 que ninguém mais pensou",
                "Insight único 2 baseado nos dados coletados",
                "Insight único 3 sobre oportunidades ocultas",
                "Insight único 4 sobre riscos não óbvios",
                "Insight único 5 sobre estratégias inovadoras"
            ],
            "recomendacoes_estrategicas": [
                "Recomendação estratégica específica 1",
                "Recomendação estratégica específica 2",
                "Recomendação estratégica específica 3"
            ]
        }
        
        prompt_parts.append("```json")
        prompt_parts.append(json.dumps(json_structure, indent=2, ensure_ascii=False))
        prompt_parts.append("```")
        
        prompt_parts.extend([
            "",
            "IMPORTANTE: Preencha TODOS os campos com informações específicas, detalhadas e acionáveis. Não use placeholders genéricos. Cada campo deve conter insights únicos baseados nos dados fornecidos.",
            "",
            "A qualidade desta análise será medida pela especificidade, profundidade e aplicabilidade dos insights fornecidos."
        ])
        
        return "\n".join(prompt_parts)
    
    def _consolidate_analyses(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any], 
        ai_analyses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consolida análises de múltiplas IAs"""
        
        logger.info("Consolidando análises de múltiplas IAs...")
        
        # Usa análise principal do Gemini como base
        main_analysis = ai_analyses.get("gemini", {})
        
        # Adiciona insights do DeepSeek se disponível
        if "deepseek" in ai_analyses:
            deepseek_insights = ai_analyses["deepseek"].get("strategic_insights", "")
            if "insights_exclusivos" not in main_analysis:
                main_analysis["insights_exclusivos"] = []
            
            main_analysis["insights_exclusivos"].append(f"Insight DeepSeek: {deepseek_insights}")
        
        # Adiciona dados de pesquisa web aos insights
        if research_data.get("web_research"):
            web_insights = []
            for query, result in research_data["web_research"].items():
                summary = result.get("research_summary", {})
                web_insights.extend(summary.get("key_insights", []))
            
            if web_insights:
                if "insights_exclusivos" not in main_analysis:
                    main_analysis["insights_exclusivos"] = []
                main_analysis["insights_exclusivos"].extend([f"Web Research: {insight}" for insight in web_insights[:3]])
        
        return main_analysis
    
    def _enrich_with_specific_data(
        self, 
        analysis: Dict[str, Any], 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enriquece análise com dados específicos calculados"""
        
        logger.info("Enriquecendo análise com dados específicos...")
        
        # Adiciona cálculos financeiros específicos
        if data.get("preco_float") and data.get("objetivo_receita_float"):
            vendas_necessarias = data["objetivo_receita_float"] / data["preco_float"]
            
            if "metricas_performance" not in analysis:
                analysis["metricas_performance"] = {}
            
            analysis["metricas_performance"]["vendas_necessarias_meta"] = int(vendas_necessarias)
            analysis["metricas_performance"]["vendas_mensais_meta"] = int(vendas_necessarias / 12)
        
        # Adiciona análise de viabilidade orçamentária
        if data.get("orcamento_marketing_float") and data.get("preco_float"):
            cac_maximo = data["preco_float"] * 0.3  # 30% do preço como CAC máximo
            leads_possiveis = data["orcamento_marketing_float"] / 10  # R$ 10 por lead
            
            analysis["viabilidade_orcamentaria"] = {
                "cac_maximo_recomendado": cac_maximo,
                "leads_possiveis_orcamento": int(leads_possiveis),
                "conversao_necessaria": f"{(100 / (leads_possiveis / (data['objetivo_receita_float'] / data['preco_float'] / 12))):.1f}%" if leads_possiveis > 0 else "Orçamento insuficiente"
            }
        
        # Adiciona timestamp e versão
        analysis["analise_metadata"] = {
            "versao_engine": "Enhanced v2.0",
            "data_analise": datetime.utcnow().isoformat(),
            "qualidade_dados": "Alta" if len(data.get("dados_adicionais", "")) > 100 else "Média",
            "confiabilidade": "95%" if analysis.get("insights_exclusivos") else "85%"
        }
        
        return analysis
    
    def _calculate_quality_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de qualidade da análise"""
        
        score = 0.0
        
        # Pontuação por seções preenchidas
        sections = [
            "avatar_ultra_detalhado",
            "drivers_mentais_customizados", 
            "analise_concorrencia_profunda",
            "estrategia_posicionamento",
            "metricas_performance",
            "insights_exclusivos"
        ]
        
        for section in sections:
            if section in analysis and analysis[section]:
                score += 15.0
        
        # Bônus por profundidade
        if analysis.get("insights_exclusivos") and len(analysis["insights_exclusivos"]) >= 5:
            score += 10.0
        
        return min(score, 100.0)
    
    def _generate_emergency_fallback(self, data: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Gera análise de emergência em caso de falha total"""
        
        logger.error(f"Gerando análise de emergência devido a: {error}")
        
        return {
            "avatar_ultra_detalhado": {
                "nome_ficticio": f"Empreendedor {data['segmento']}",
                "perfil_demografico": {
                    "idade": "30-45 anos",
                    "ocupacao": f"Profissional de {data['segmento']}"
                },
                "dores_viscerais": {
                    "dor_primaria": "Falta de resultados consistentes",
                    "frustracao_diaria": "Dificuldade em escalar o negócio"
                }
            },
            "insights_exclusivos": [
                "Análise gerada em modo de emergência",
                f"Erro no processamento: {error}",
                "Recomenda-se executar nova análise com dados completos"
            ],
            "metadata": {
                "processing_time_seconds": 0,
                "analysis_engine": "Emergency Fallback",
                "generated_at": datetime.utcnow().isoformat(),
                "quality_score": 20.0,
                "error": error
            }
        }

# Instância global do motor
enhanced_analysis_engine = EnhancedAnalysisEngine()

