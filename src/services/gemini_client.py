#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Cliente Google Gemini Pro
Integração com IA Avançada para Análise de Mercado
"""

import os
import logging
import json
import time
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from datetime import datetime

logger = logging.getLogger(__name__)

class GeminiClient:
    """Cliente para integração com Google Gemini Pro"""
    
    def __init__(self):
        """Inicializa cliente Gemini"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        # Configura API
        genai.configure(api_key=self.api_key)
        
        # Modelo principal
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Configurações de geração
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 8192,
        }
        
        # Configurações de segurança
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    
    def test_connection(self) -> bool:
        """Testa conexão com Gemini"""
        try:
            response = self.model.generate_content(
                "Teste de conexão. Responda apenas: OK",
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return "OK" in response.text
        except Exception as e:
            logger.error(f"Erro ao testar Gemini: {str(e)}")
            return False
    
    def generate_ultra_detailed_analysis(
        self, 
        analysis_data: Dict[str, Any],
        search_context: Optional[str] = None,
        attachments_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gera análise ultra-detalhada usando Gemini Pro"""
        
        try:
            # Constrói prompt principal
            prompt = self._build_analysis_prompt(analysis_data, search_context, attachments_context)
            
            logger.info("Iniciando análise com Gemini Pro...")
            start_time = time.time()
            
            # Gera análise
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            end_time = time.time()
            logger.info(f"Análise concluída em {end_time - start_time:.2f} segundos")
            
            # Processa resposta
            if response.text:
                return self._parse_analysis_response(response.text)
            else:
                raise Exception("Resposta vazia do Gemini")
                
        except Exception as e:
            logger.error(f"Erro na análise Gemini: {str(e)}")
            return self._generate_fallback_analysis(analysis_data)
    
    def _build_analysis_prompt(
        self, 
        data: Dict[str, Any], 
        search_context: Optional[str] = None,
        attachments_context: Optional[str] = None
    ) -> str:
        """Constrói prompt detalhado para análise"""
        
        prompt = f"""
# ANÁLISE ULTRA-DETALHADA DE MERCADO - ARQV30 ENHANCED

Você é um especialista em análise de mercado e marketing digital com 20+ anos de experiência. 
Sua missão é gerar uma análise ultra-detalhada e profissional baseada nos dados fornecidos.

## DADOS DO PROJETO:
- **Segmento**: {data.get('segmento', 'Não informado')}
- **Produto/Serviço**: {data.get('produto', 'Não informado')}
- **Público-Alvo**: {data.get('publico', 'Não informado')}
- **Preço**: R$ {data.get('preco', 'Não informado')}
- **Concorrentes**: {data.get('concorrentes', 'Não informado')}
- **Objetivo de Receita**: R$ {data.get('objetivo_receita', 'Não informado')}
- **Orçamento Marketing**: R$ {data.get('orcamento_marketing', 'Não informado')}
- **Prazo de Lançamento**: {data.get('prazo_lancamento', 'Não informado')}
"""

        if search_context:
            prompt += f"\n## CONTEXTO DE PESQUISA:\n{search_context}\n"
        
        if attachments_context:
            prompt += f"\n## CONTEXTO DOS ANEXOS:\n{attachments_context}\n"
        
        prompt += """
## INSTRUÇÕES PARA ANÁLISE:

Gere uma análise completa e estruturada em formato JSON com as seguintes seções:

```json
{
  "avatar_ultra_detalhado": {
    "perfil_demografico": {
      "idade": "Faixa etária específica",
      "genero": "Distribuição por gênero",
      "renda": "Faixa de renda mensal",
      "escolaridade": "Nível educacional",
      "localizacao": "Região geográfica",
      "estado_civil": "Status relacionamento",
      "filhos": "Situação familiar"
    },
    "perfil_psicografico": {
      "personalidade": "Traços de personalidade dominantes",
      "valores": "Valores e crenças principais",
      "interesses": "Hobbies e interesses",
      "estilo_vida": "Como vive o dia a dia",
      "comportamento_compra": "Como toma decisões de compra",
      "influenciadores": "Quem influencia suas decisões"
    },
    "dores_especificas": [
      "Lista de 5-8 dores específicas e detalhadas"
    ],
    "desejos_profundos": [
      "Lista de 5-8 desejos e aspirações"
    ],
    "gatilhos_mentais": [
      "Lista de gatilhos psicológicos efetivos"
    ],
    "objecoes_comuns": [
      "Principais objeções e resistências"
    ],
    "jornada_cliente": {
      "consciencia": "Como toma consciência do problema",
      "consideracao": "Como avalia soluções",
      "decisao": "Como decide pela compra",
      "pos_compra": "Experiência pós-compra"
    }
  },
  
  "escopo": {
    "posicionamento_mercado": "Posicionamento único no mercado",
    "proposta_valor": "Proposta de valor clara e diferenciada",
    "diferenciais_competitivos": ["Lista de diferenciais únicos"],
    "segmentacao_mercado": "Como segmentar o mercado",
    "nicho_especifico": "Nicho mais específico recomendado"
  },
  
  "analise_concorrencia_detalhada": {
    "concorrentes_diretos": [
      {
        "nome": "Nome do concorrente",
        "pontos_fortes": ["Forças principais"],
        "pontos_fracos": ["Fraquezas identificadas"],
        "preco": "Faixa de preço",
        "estrategia": "Estratégia principal"
      }
    ],
    "concorrentes_indiretos": ["Lista de concorrentes indiretos"],
    "gaps_oportunidade": ["Oportunidades não exploradas"],
    "analise_precos": "Análise detalhada de precificação",
    "vantagem_competitiva": "Como se diferenciar"
  },
  
  "estrategia_palavras_chave": {
    "palavras_primarias": ["5-8 palavras-chave principais"],
    "palavras_secundarias": ["10-15 palavras-chave secundárias"],
    "long_tail": ["15-20 palavras-chave de cauda longa"],
    "intencao_busca": {
      "informacional": ["Palavras informacionais"],
      "navegacional": ["Palavras navegacionais"],
      "transacional": ["Palavras transacionais"]
    },
    "volume_estimado": "Estimativa de volume de busca",
    "dificuldade_ranking": "Análise de dificuldade SEO"
  },
  
  "metricas_performance_detalhadas": {
    "kpis_principais": [
      {
        "metrica": "Nome da métrica",
        "objetivo": "Meta específica",
        "benchmark": "Benchmark do setor",
        "frequencia": "Frequência de medição"
      }
    ],
    "funil_conversao": {
      "topo": "Métricas de awareness",
      "meio": "Métricas de consideração",
      "fundo": "Métricas de conversão"
    },
    "roi_esperado": "Retorno sobre investimento estimado",
    "lifetime_value": "Valor vitalício do cliente",
    "custo_aquisicao": "Custo de aquisição estimado"
  },
  
  "projecoes_cenarios": {
    "conservador": {
      "receita_mensal": "Receita mensal conservadora",
      "clientes_mes": "Número de clientes/mês",
      "ticket_medio": "Ticket médio",
      "margem_lucro": "Margem de lucro %"
    },
    "realista": {
      "receita_mensal": "Receita mensal realista",
      "clientes_mes": "Número de clientes/mês",
      "ticket_medio": "Ticket médio",
      "margem_lucro": "Margem de lucro %"
    },
    "otimista": {
      "receita_mensal": "Receita mensal otimista",
      "clientes_mes": "Número de clientes/mês",
      "ticket_medio": "Ticket médio",
      "margem_lucro": "Margem de lucro %"
    },
    "fatores_sucesso": ["Fatores críticos para o sucesso"],
    "riscos_principais": ["Principais riscos identificados"]
  },
  
  "inteligencia_mercado": {
    "tendencias_setor": ["Principais tendências do setor"],
    "oportunidades_emergentes": ["Oportunidades emergentes"],
    "ameacas_externas": ["Ameaças do ambiente externo"],
    "sazonalidade": "Análise de sazonalidade",
    "ciclo_vida_produto": "Estágio no ciclo de vida",
    "inovacoes_disruptivas": ["Inovações que podem impactar"]
  },
  
  "plano_acao_detalhado": {
    "fase_1_preparacao": {
      "duracao": "Tempo estimado",
      "atividades": ["Lista de atividades"],
      "recursos_necessarios": ["Recursos necessários"],
      "investimento": "Investimento estimado"
    },
    "fase_2_lancamento": {
      "duracao": "Tempo estimado",
      "atividades": ["Lista de atividades"],
      "recursos_necessarios": ["Recursos necessários"],
      "investimento": "Investimento estimado"
    },
    "fase_3_crescimento": {
      "duracao": "Tempo estimado",
      "atividades": ["Lista de atividades"],
      "recursos_necessarios": ["Recursos necessários"],
      "investimento": "Investimento estimado"
    },
    "cronograma_detalhado": "Cronograma mês a mês",
    "marcos_importantes": ["Marcos e milestones"],
    "indicadores_progresso": ["Como medir progresso"]
  },
  
  "insights_exclusivos": [
    "Lista de 8-12 insights únicos e valiosos baseados na análise"
  ]
}
```

## DIRETRIZES IMPORTANTES:

1. **Seja ULTRA-ESPECÍFICO**: Use dados concretos, números, percentuais
2. **Base-se em DADOS REAIS**: Use o contexto de pesquisa fornecido
3. **Seja PRÁTICO**: Forneça ações executáveis
4. **Seja INOVADOR**: Identifique oportunidades não óbvias
5. **Mantenha COERÊNCIA**: Todos os dados devem ser consistentes
6. **Use LINGUAGEM PROFISSIONAL**: Tom consultivo e especializado

Gere APENAS o JSON válido, sem texto adicional antes ou depois.
"""
        
        return prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Processa resposta do Gemini e extrai JSON"""
        try:
            # Remove markdown se presente
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.rfind("```")
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.rfind("```")
                response_text = response_text[start:end].strip()
            
            # Tenta parsear JSON
            analysis = json.loads(response_text)
            
            # Adiciona metadados
            analysis['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'model': 'gemini-pro',
                'version': '2.0.0'
            }
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {str(e)}")
            logger.error(f"Resposta recebida: {response_text[:500]}...")
            return self._generate_fallback_analysis({})
    
    def _generate_fallback_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera análise básica em caso de erro"""
        return {
            "avatar_ultra_detalhado": {
                "perfil_demografico": {
                    "idade": "25-45 anos",
                    "genero": "Misto",
                    "renda": "R$ 3.000 - R$ 15.000",
                    "escolaridade": "Superior",
                    "localizacao": "Centros urbanos",
                    "estado_civil": "Variado",
                    "filhos": "Variado"
                },
                "perfil_psicografico": {
                    "personalidade": "Ambiciosos e determinados",
                    "valores": "Crescimento pessoal e profissional",
                    "interesses": "Tecnologia e inovação",
                    "estilo_vida": "Dinâmico e conectado",
                    "comportamento_compra": "Pesquisa antes de comprar",
                    "influenciadores": "Especialistas e peers"
                },
                "dores_especificas": [
                    "Falta de tempo para aprender",
                    "Dificuldade para implementar",
                    "Resultados inconsistentes",
                    "Falta de direcionamento claro"
                ],
                "desejos_profundos": [
                    "Alcançar liberdade financeira",
                    "Ter mais tempo livre",
                    "Ser reconhecido como especialista",
                    "Fazer diferença no mundo"
                ],
                "gatilhos_mentais": [
                    "Urgência",
                    "Escassez",
                    "Prova social",
                    "Autoridade"
                ],
                "objecoes_comuns": [
                    "Preço muito alto",
                    "Falta de tempo",
                    "Dúvida sobre resultados",
                    "Já tentei antes"
                ],
                "jornada_cliente": {
                    "consciencia": "Percebe que precisa de ajuda",
                    "consideracao": "Pesquisa soluções disponíveis",
                    "decisao": "Avalia custo-benefício",
                    "pos_compra": "Busca implementar e obter resultados"
                }
            },
            "escopo": {
                "posicionamento_mercado": "Solução premium para resultados rápidos",
                "proposta_valor": "Transforme seu negócio com estratégias comprovadas",
                "diferenciais_competitivos": ["Metodologia exclusiva", "Suporte personalizado"],
                "segmentacao_mercado": "Empreendedores digitais",
                "nicho_especifico": data.get('segmento', 'Produtos Digitais')
            },
            "insights_exclusivos": [
                "O mercado está em crescimento acelerado",
                "Existe demanda reprimida no segmento",
                "Oportunidade de posicionamento premium",
                "Potencial de expansão internacional"
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "model": "fallback",
                "version": "2.0.0",
                "note": "Análise gerada em modo fallback devido a erro na IA"
            }
        }


# Instância global do cliente
try:
    gemini_client = GeminiClient()
    logger.info("Cliente Gemini inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar cliente Gemini: {str(e)}")
    gemini_client = None

