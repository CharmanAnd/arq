#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Cliente Google Gemini Pro Ultra-Robusto
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

class UltraRobustGeminiClient:
    """Cliente para integração com Google Gemini Pro"""
    
    def __init__(self):
        """Inicializa cliente Gemini"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        # Configura API
        genai.configure(api_key=self.api_key)
        
        # Modelo principal (usando o mais avançado disponível)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Configurações de geração
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 32768,  # Aumentado para análises ultra-detalhadas
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
            # Constrói prompt ultra-detalhado
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

Você é o DIRETOR SUPREMO DE ANÁLISE DE MERCADO, um especialista de elite com 25+ anos de experiência em análise de mercado, psicologia do consumidor, estratégia de negócios e marketing digital avançado.

Sua missão é gerar a ANÁLISE MAIS COMPLETA E PROFUNDA possível, implementando TODOS os sistemas avançados dos documentos fornecidos:

1. SISTEMA DE PROVAS VISUAIS INSTANTÂNEAS
2. ARQUITETO DE DRIVERS MENTAIS  
3. PRÉ-PITCH INVISÍVEL
4. ENGENHARIA ANTI-OBJEÇÃO
5. ANCORAGEM PSICOLÓGICA

IMPORTANTE: Esta análise deve ter PROFUNDIDADE EXTREMA, com insights únicos que vão muito além do óbvio. Seja ULTRA-ESPECÍFICO e ACIONÁVEL.

## DADOS DO PROJETO:
- **Segmento**: {data.get('segmento', 'Não informado')}
- **Produto/Serviço**: {data.get('produto', 'Não informado')}
- **Público-Alvo**: {data.get('publico', 'Não informado')}
- **Preço**: R$ {data.get('preco', 'Não informado')}
- **Concorrentes**: {data.get('concorrentes', 'Não informado')}
- **Objetivo de Receita**: R$ {data.get('objetivo_receita', 'Não informado')}
- **Orçamento Marketing**: R$ {data.get('orcamento_marketing', 'Não informado')}
- **Prazo de Lançamento**: {data.get('prazo_lancamento', 'Não informado')}
- **Dados Adicionais**: {data.get('dados_adicionais', 'Não informado')}
"""

        if search_context:
            prompt += f"\n## CONTEXTO DE PESQUISA:\n{search_context}\n"
        
        if attachments_context:
            prompt += f"\n## CONTEXTO DOS ANEXOS:\n{attachments_context}\n"
        
        prompt += """
## INSTRUÇÕES PARA ANÁLISE ULTRA-ROBUSTA:

Gere uma análise ULTRA-COMPLETA e estruturada em formato JSON implementando TODOS os sistemas dos documentos. A estrutura deve ser:

```json
{
  "avatar_ultra_detalhado": {
    "perfil_demografico": {
      "idade": "Faixa etária específica",
      "genero": "Distribuição por gênero",
      "renda": "Faixa de renda mensal detalhada",
      "escolaridade": "Nível educacional",
      "localizacao": "Região geográfica",
      "estado_civil": "Status relacionamento",
      "filhos": "Situação familiar"
    },
    "perfil_psicografico": {
      "personalidade": "Traços de personalidade dominantes",
      "valores": "Valores e crenças principais detalhados",
      "interesses": "Hobbies e interesses",
      "estilo_vida": "Como vive o dia a dia",
      "comportamento_compra": "Como toma decisões de compra",
      "influenciadores": "Quem influencia suas decisões"
    },
    "dores_especificas": [
      "Lista de 8-12 dores específicas e viscerais"
    ],
    "desejos_profundos": [
      "Lista de 8-12 desejos e aspirações profundas"
    ],
    "gatilhos_mentais": [
      "Lista de gatilhos psicológicos efetivos"
    ],
    "objecoes_comuns": [
      "Principais objeções e resistências detalhadas"
    ],
    "jornada_cliente": {
      "consciencia": "Como toma consciência do problema",
      "consideracao": "Como avalia soluções",
      "decisao": "Como decide pela compra",
      "pos_compra": "Experiência pós-compra"
    },
    "linguagem_interna": {
      "frases_dor": ["Frases que usa para expressar dores"],
      "frases_desejo": ["Frases que usa para expressar desejos"],
      "metaforas_comuns": ["Metáforas que usa"],
      "vocabulario_especifico": ["Palavras específicas do nicho"]
    },
    "arquetipo_psicologico": "Arquétipo dominante identificado",
    "nivel_consciencia": "Nível de consciência do problema (1-5)",
    "nivel_sofisticacao": "Nível de sofisticação do mercado (1-5)",
    "resistencias_ocultas": [
      "Resistências psicológicas não verbalizadas"
    ],
    "momento_ideal_abordagem": "Quando e como abordar este avatar"
    }
  },
  
  "drivers_mentais_customizados": [
    {
      "nome": "Nome do driver específico",
      "gatilho_central": "Emoção ou lógica core",
      "definicao_visceral": "Definição impactante",
      "roteiro_ativacao": "Como ativar este driver",
      "frases_ancoragem": ["Frases para usar"],
      "momento_ideal": "Quando usar na jornada",
      "prova_logica": "Dados que sustentam",
      "loop_reforco": "Como reativar depois"
    }
  ],
  
  "provas_visuais_sugeridas": [
    {
      "nome": "Nome da demonstração",
      "conceito_alvo": "O que quer provar",
      "experimento": "Descrição da demonstração física",
      "analogia": "Como conecta com a vida deles",
      "materiais": ["Lista de materiais necessários"],
      "roteiro_completo": "Script passo a passo",
      "variacoes": "Adaptações para diferentes formatos",
      "gestao_riscos": "Como lidar se der errado"
    }
  ],
  
  "escopo": {
    "posicionamento_mercado": "Posicionamento único no mercado",
    "proposta_valor_unica": "Proposta de valor irresistível",
    "diferenciais_competitivos": ["Lista de diferenciais únicos"],
    "mensagem_central": "Mensagem principal",
    "tom_comunicacao": "Tom de voz ideal",
    "nicho_especifico": "Nicho mais específico recomendado",
    "estrategia_oceano_azul": "Como criar mercado sem concorrência"
  },
  
  "analise_concorrencia_detalhada": {
    "concorrentes_diretos": [
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
        "vulnerabilidades": ["Pontos fracos exploráveis"],
        "preco": "Faixa de preço",
        "share_mercado": "Participação estimada"
      }
    ],
    "concorrentes_indiretos": ["Lista de concorrentes indiretos"],
    "gaps_oportunidade": ["Oportunidades não exploradas"],
    "benchmarks_setor": "Benchmarks específicos do setor",
    "estrategias_diferenciacao": ["Como se diferenciar"],
    "analise_precos": "Análise detalhada de precificação"
  },
  
  "estrategia_palavras_chave": {
    "palavras_primarias": ["8-12 palavras-chave principais"],
    "palavras_secundarias": ["15-25 palavras-chave secundárias"],
    "palavras_cauda_longa": ["20-30 palavras-chave de cauda longa"],
    "palavras_negativas": ["Palavras a evitar"],
    "intencao_busca": {
      "informacional": ["Palavras informacionais"],
      "navegacional": ["Palavras navegacionais"],
      "transacional": ["Palavras transacionais"]
    },
    "estrategia_conteudo": "Como usar as palavras-chave",
    "sazonalidade": "Variações sazonais das buscas"
  },
  
  "metricas_performance_detalhadas": {
    "kpis_principais": [
      {
        "metrica": "Nome da métrica",
        "objetivo": "Meta específica",
        "benchmark": "Benchmark do setor",
        "frequencia": "Frequência de medição",
        "formula_calculo": "Como calcular"
      }
    ],
    "kpis_secundarios": ["KPIs de apoio"],
    "metas_especificas": {
      "cpl_meta": "Custo por lead ideal",
      "cac_meta": "Custo de aquisição ideal",
      "ltv_meta": "Lifetime value esperado",
      "roi_meta": "ROI esperado"
    },
    "funil_conversao": {
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
  
  "sistema_anti_objecao": {
    "objecoes_universais": {
      "tempo": {
        "objecao": "Não tenho tempo",
        "raiz_emocional": "Medo de mais uma responsabilidade",
        "contra_ataque": "Técnica específica de neutralização",
        "drives_mentais": ["Drivers para usar"],
        "historias": ["Histórias para contar"],
        "provas": ["Provas para mostrar"]
      },
      "dinheiro": {
        "objecao": "Não tenho dinheiro",
        "raiz_emocional": "Medo de desperdício",
        "contra_ataque": "Técnica específica de neutralização",
        "drives_mentais": ["Drivers para usar"],
        "historias": ["Histórias para contar"],
        "provas": ["Provas para mostrar"]
      },
      "confianca": {
        "objecao": "Não confio",
        "raiz_emocional": "Medo de ser enganado",
        "contra_ataque": "Técnica específica de neutralização",
        "drives_mentais": ["Drivers para usar"],
        "historias": ["Histórias para contar"],
        "provas": ["Provas para mostrar"]
      }
    },
    "objecoes_ocultas": {
      "autossuficiencia": "Análise e neutralização",
      "sinal_fraqueza": "Análise e neutralização",
      "medo_novo": "Análise e neutralização",
      "prioridades_desequilibradas": "Análise e neutralização",
      "autoestima_destruida": "Análise e neutralização"
    },
    "arsenal_emergencia": ["Objeções de última hora e como lidar"]
  },
  
  "pre_pitch_invisivel": {
    "orquestracao_emocional": {
      "sequencia_psicologica": [
        {"fase": "QUEBRA", "objetivo": "Destruir ilusão", "tempo": "15%"},
        {"fase": "EXPOSICAO", "objetivo": "Revelar ferida", "tempo": "15%"},
        {"fase": "INDIGNACAO", "objetivo": "Criar revolta", "tempo": "15%"},
        {"fase": "VISLUMBRE", "objetivo": "Mostrar possível", "tempo": "15%"},
        {"fase": "TENSAO", "objetivo": "Amplificar gap", "tempo": "15%"},
        {"fase": "NECESSIDADE", "objetivo": "Tornar inevitável", "tempo": "25%"}
      ],
      "drivers_por_fase": "Mapeamento de drivers por fase",
      "narrativas_conectoras": "Como conectar as fases"
    },
    "justificacao_logica": {
      "numeros_irrefutaveis": ["Dados que não podem ser contestados"],
      "calculos_roi": "Cálculos de retorno conservadores",
      "demonstracoes": "Demonstrações passo a passo",
      "cases_metricas": "Cases com métricas específicas",
      "garantias": "Garantias que eliminam risco"
    },
    "roteiro_completo": "Script completo do pré-pitch",
    "adaptacoes_formato": {
      "webinario": "Adaptação para webinário",
      "evento_presencial": "Adaptação para evento",
      "cpl": "Adaptação para CPL",
      "lives": "Adaptação para lives"
    }
  },
  
  "inteligencia_mercado_ultra": {
    "tendencias_setor": ["Principais tendências do setor"],
    "oportunidades_emergentes": ["Oportunidades emergentes"],
    "ameacas_externas": ["Ameaças do ambiente externo"],
    "sazonalidade": "Análise de sazonalidade",
    "ciclo_vida_produto": "Estágio no ciclo de vida",
    "inovacoes_disruptivas": ["Inovações que podem impactar"],
    "regulamentacoes": "Mudanças regulatórias relevantes",
    "impacto_tecnologico": "Como a tecnologia afeta o setor",
    "mudancas_comportamentais": "Mudanças no comportamento do consumidor"
  },
  
  "plano_acao_90_dias": {
    "primeiros_30_dias": {
      "foco": "Foco principal",
      "atividades": ["Atividades específicas"],
      "entregas": ["Entregas esperadas"],
      "investimento": "Investimento necessário",
      "duracao": "Tempo estimado",
      "marcos": ["Marcos importantes"]
    },
    "dias_31_60": {
      "foco": "Foco principal",
      "atividades": ["Atividades específicas"],
      "entregas": ["Entregas esperadas"],
      "investimento": "Investimento necessário",
      "duracao": "Tempo estimado",
      "marcos": ["Marcos importantes"]
    },
    "dias_61_90": {
      "foco": "Foco principal",
      "atividades": ["Atividades específicas"],
      "entregas": ["Entregas esperadas"],
      "investimento": "Investimento necessário",
      "duracao": "Tempo estimado",
      "marcos": ["Marcos importantes"]
    },
    "cronograma_semanal": "Cronograma semana a semana",
    "recursos_necessarios": ["Recursos humanos e financeiros"],
    "riscos_mitigacao": ["Riscos e como mitigar"]
  },
  
  "insights_exclusivos_ultra": [
    "Lista de 15-20 insights únicos e ultra-valiosos baseados na análise profunda"
  ],
  
  "recomendacoes_estrategicas": [
    "Recomendações estratégicas específicas e acionáveis"
  ],
  
  "sistema_monitoramento": {
    "dashboards": ["Dashboards necessários"],
    "alertas": ["Alertas automáticos"],
    "relatorios": ["Relatórios periódicos"],
    "ajustes_otimizacao": ["Como otimizar baseado nos dados"]
  }
}
```

## DIRETRIZES ULTRA-IMPORTANTES:

1. **PROFUNDIDADE EXTREMA**: Cada seção deve ter profundidade de especialista
2. **ULTRA-ESPECÍFICO**: Use dados concretos, números, percentuais, exemplos reais
3. **IMPLEMENTAÇÃO DOS SISTEMAS**: Implemente TODOS os sistemas dos documentos
4. **ACIONABILIDADE TOTAL**: Cada insight deve ser imediatamente implementável
5. **INOVAÇÃO CONSTANTE**: Identifique oportunidades que ninguém mais viu
6. **COERÊNCIA ABSOLUTA**: Todos os dados devem ser perfeitamente consistentes
7. **LINGUAGEM DE ELITE**: Tom de consultor de R$ 50.000/hora
8. **INSIGHTS ÚNICOS**: Gere insights que só uma análise desta profundidade pode revelar
9. **SISTEMAS INTEGRADOS**: Todos os sistemas devem trabalhar em sinergia
10. **RESULTADOS GARANTIDOS**: Cada recomendação deve ter alta probabilidade de sucesso

CRÍTICO: Esta análise será usada para decisões de investimento de milhões de reais. A qualidade deve ser IMPECÁVEL.

Gere APENAS o JSON válido e ultra-completo, sem texto adicional antes ou depois.
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
            analysis['metadata_gemini'] = {
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
        fallback = {
            "avatar_ultra_detalhado": {
                "perfil_demografico": {
                    "idade": "25-45 anos",
                    "genero": "Misto",
                    "renda": "R$ 3.000 - R$ 15.000",
                    "escolaridade": "Superior",
                    "localizacao": "Centros urbanos",
                    "estado_civil": "Variado",
                    "filhos": "Variado",
                    "profissao": "Profissionais diversos"
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
                    "Falta de conhecimento especializado",
                    "Dificuldade para implementar",
                    "Resultados inconsistentes",
                    "Falta de direcionamento claro"
                ],
                "desejos_profundos": [
                    "Alcançar liberdade financeira",
                    "Ter mais tempo para família",
                    "Ser reconhecido como especialista",
                    "Fazer diferença no mundo"
                ],
                "gatilhos_mentais": [
                    "Urgência",
                    "Escassez",
                    "Prova social",
                    "Autoridade",
                    "Reciprocidade"
                ],
                "objecoes_comuns": [
                    "Preço muito alto",
                    "Falta de tempo",
                    "Dúvida sobre resultados",
                    "Já tentei antes"
                ],
                "jornada_cliente": {
                    "consciencia": "Reconhece que tem um problema",
                    "consideracao": "Pesquisa soluções disponíveis",
                    "decisao": "Avalia custo-benefício",
                    "pos_compra": "Busca implementar e obter resultados"
                }
            },
            "escopo": {
                "posicionamento_mercado": "Solução premium para resultados rápidos",
                "proposta_valor_unica": "Transforme seu negócio com estratégias comprovadas",
                "diferenciais_competitivos": ["Metodologia exclusiva", "Suporte personalizado"],
                "mensagem_central": "Resultados garantidos com método comprovado",
                "segmentacao_mercado": "Empreendedores digitais",
                "nicho_especifico": data.get('segmento', 'Produtos Digitais')
            },
            "insights_exclusivos_ultra": [
                "O mercado está em crescimento acelerado",
                "Existe demanda reprimida no segmento",
                "Oportunidade de posicionamento premium",
                "Potencial de expansão internacional",
                "Análise gerada em modo fallback - execute nova análise para resultados completos"
            ],
            "metadata_gemini": {
                "generated_at": datetime.now().isoformat(),
                "model": "fallback",
                "version": "2.0.0",
                "note": "Análise gerada em modo fallback devido a erro na IA"
            }
        }
        
        return fallback


# Instância global do cliente
try:
    gemini_client = UltraRobustGeminiClient()
    logger.info("Cliente Gemini inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar cliente Gemini: {str(e)}")
    gemini_client = None

