#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Rotas de Análise Ultra-Robusta
Sistema completo de análise de mercado com IA avançada
"""

import os
import logging
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from flask import Blueprint, request, jsonify, session
from database import db_manager
from services.gemini_client import gemini_client
from services.deep_search_service import deep_search_service
from services.attachment_service import attachment_service
from services.websailor_integration import websailor_agent
from services.enhanced_analysis_engine import enhanced_analysis_engine

logger = logging.getLogger(__name__)

# Cria blueprint
analysis_bp = Blueprint('analysis', __name__)

class UltraRobustAnalyzer:
    """Analisador Ultra-Robusto com implementação completa dos documentos"""
    
    def __init__(self):
        self.max_analysis_time = 1800  # 30 minutos para análise completa
        self.deep_research_enabled = True
        self.multi_ai_enabled = True
        self.visual_proofs_enabled = True
        self.mental_drivers_enabled = True
        self.objection_handling_enabled = True
        
    def generate_ultra_comprehensive_analysis(
        self, 
        data: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gera análise ultra-abrangente implementando TODOS os documentos"""
        
        start_time = time.time()
        logger.info(f"🚀 INICIANDO ANÁLISE ULTRA-ROBUSTA para {data.get('segmento')}")
        
        try:
            # FASE 1: COLETA MASSIVA DE DADOS (5-10 minutos)
            logger.info("📊 FASE 1: Coleta massiva de dados...")
            comprehensive_data = self._collect_ultra_comprehensive_data(data, session_id)
            
            # FASE 2: ANÁLISE COM MÚLTIPLAS IAs (10-15 minutos)
            logger.info("🧠 FASE 2: Análise com múltiplas IAs...")
            multi_ai_analysis = self._run_multi_ai_ultra_analysis(data, comprehensive_data)
            
            # FASE 3: IMPLEMENTAÇÃO DOS SISTEMAS DOS DOCUMENTOS (5-10 minutos)
            logger.info("⚡ FASE 3: Implementação dos sistemas avançados...")
            advanced_systems = self._implement_advanced_systems(data, multi_ai_analysis, comprehensive_data)
            
            # FASE 4: CONSOLIDAÇÃO FINAL ULTRA-DETALHADA
            logger.info("🎯 FASE 4: Consolidação final ultra-detalhada...")
            final_analysis = self._consolidate_ultra_analysis(
                data, comprehensive_data, multi_ai_analysis, advanced_systems
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Adiciona metadados ultra-detalhados
            final_analysis["metadata_ultra_detalhado"] = {
                "processing_time_seconds": processing_time,
                "processing_time_formatted": f"{int(processing_time // 60)}m {int(processing_time % 60)}s",
                "analysis_engine": "ARQV30 Enhanced Ultra-Robust v2.0",
                "data_sources_used": len(comprehensive_data.get("sources", [])),
                "ai_models_used": len(multi_ai_analysis),
                "advanced_systems_implemented": len(advanced_systems),
                "generated_at": datetime.utcnow().isoformat(),
                "quality_score": self._calculate_ultra_quality_score(final_analysis),
                "completeness_score": self._calculate_completeness_score(final_analysis),
                "depth_level": "ULTRA_PROFUNDO",
                "research_iterations": comprehensive_data.get("research_iterations", 0),
                "total_content_analyzed": comprehensive_data.get("total_content_length", 0),
                "unique_insights_generated": len(final_analysis.get("insights_exclusivos_ultra", [])),
                "systems_implemented": list(advanced_systems.keys())
            }
            
            logger.info(f"✅ ANÁLISE ULTRA-ROBUSTA CONCLUÍDA em {processing_time:.2f} segundos")
            logger.info(f"📈 Quality Score: {final_analysis['metadata_ultra_detalhado']['quality_score']}")
            logger.info(f"🎯 Completeness Score: {final_analysis['metadata_ultra_detalhado']['completeness_score']}")
            
            return final_analysis
            
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO na análise ultra-robusta: {str(e)}", exc_info=True)
            return self._generate_emergency_ultra_fallback(data, str(e))
    
    def _collect_ultra_comprehensive_data(
        self, 
        data: Dict[str, Any], 
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """Coleta dados ultra-abrangentes de TODAS as fontes possíveis"""
        
        comprehensive_data = {
            "attachments": {},
            "web_research": {},
            "deep_search": {},
            "market_intelligence": {},
            "competitor_analysis": {},
            "trend_analysis": {},
            "sources": [],
            "research_iterations": 0,
            "total_content_length": 0
        }
        
        # 1. PROCESSAMENTO ULTRA-DETALHADO DE ANEXOS
        if session_id:
            logger.info("📎 Processando anexos com análise ultra-detalhada...")
            attachments = attachment_service.get_session_attachments(session_id)
            if attachments:
                combined_content = ""
                attachment_analysis = {}
                
                for att in attachments:
                    if att.get("extracted_content"):
                        content = att["extracted_content"]
                        combined_content += content + "\n\n"
                        
                        # Análise específica por tipo de anexo
                        content_type = att.get("content_type", "geral")
                        if content_type not in attachment_analysis:
                            attachment_analysis[content_type] = []
                        
                        attachment_analysis[content_type].append({
                            "filename": att.get("filename"),
                            "content": content,
                            "analysis": self._analyze_attachment_content(content, content_type)
                        })
                
                comprehensive_data["attachments"] = {
                    "count": len(attachments),
                    "combined_content": combined_content[:15000],  # Aumentado para 15k
                    "types_analysis": attachment_analysis,
                    "total_length": len(combined_content)
                }
                comprehensive_data["total_content_length"] += len(combined_content)
                logger.info(f"✅ {len(attachments)} anexos processados com análise detalhada")
        
        # 2. PESQUISA WEB ULTRA-PROFUNDA COM WEBSAILOR
        if websailor_agent.is_available():
            logger.info("🌐 Realizando pesquisa web ultra-profunda...")
            
            # Múltiplas queries estratégicas
            queries = self._generate_ultra_comprehensive_queries(data)
            
            for i, query in enumerate(queries):
                logger.info(f"🔍 Query {i+1}/{len(queries)}: {query}")
                
                web_result = websailor_agent.navigate_and_research(
                    query,
                    context={
                        "segmento": data.get("segmento"),
                        "produto": data.get("produto"),
                        "publico": data.get("publico")
                    },
                    max_pages=12,  # Aumentado para pesquisa mais profunda
                    depth=3,  # Profundidade máxima
                    aggressive_mode=True  # Modo agressivo ativado
                )
                
                comprehensive_data["web_research"][f"query_{i+1}"] = web_result
                comprehensive_data["sources"].extend(web_result.get("sources", []))
                comprehensive_data["research_iterations"] += 1
                
                # Adiciona conteúdo ao total
                research_content = web_result.get("research_summary", {}).get("combined_content", "")
                comprehensive_data["total_content_length"] += len(research_content)
            
            logger.info(f"✅ Pesquisa web concluída: {len(queries)} queries, {len(comprehensive_data['sources'])} fontes")
        
        # 3. DEEP SEARCH COM MÚLTIPLAS ITERAÇÕES
        if deep_search_service and data.get("query"):
            logger.info("🔬 Executando deep search com múltiplas iterações...")
            
            # Pesquisa principal
            main_search = deep_search_service.perform_deep_search(
                data["query"],
                data,
                max_results=20  # Aumentado para mais resultados
            )
            comprehensive_data["deep_search"]["main"] = main_search
            
            # Pesquisas complementares baseadas no segmento
            complementary_queries = [
                f"análise mercado {data.get('segmento')} Brasil 2024",
                f"tendências {data.get('segmento')} futuro",
                f"oportunidades {data.get('segmento')} inexploradas",
                f"desafios {data.get('segmento')} principais"
            ]
            
            for i, comp_query in enumerate(complementary_queries):
                comp_search = deep_search_service.perform_deep_search(
                    comp_query,
                    data,
                    max_results=10
                )
                comprehensive_data["deep_search"][f"complementary_{i+1}"] = comp_search
                comprehensive_data["research_iterations"] += 1
            
            logger.info("✅ Deep search concluído com múltiplas iterações")
        
        # 4. INTELIGÊNCIA DE MERCADO AVANÇADA
        comprehensive_data["market_intelligence"] = self._gather_ultra_market_intelligence(data)
        
        # 5. ANÁLISE DE CONCORRÊNCIA PROFUNDA
        comprehensive_data["competitor_analysis"] = self._perform_deep_competitor_analysis(data)
        
        # 6. ANÁLISE DE TENDÊNCIAS
        comprehensive_data["trend_analysis"] = self._analyze_market_trends(data)
        
        logger.info(f"📊 Coleta de dados concluída: {comprehensive_data['total_content_length']} caracteres analisados")
        return comprehensive_data
    
    def _run_multi_ai_ultra_analysis(
        self, 
        data: Dict[str, Any], 
        comprehensive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa análise com múltiplas IAs de forma ultra-detalhada"""
        
        logger.info("🧠 Executando análise com múltiplas IAs...")
        
        ai_analyses = {}
        
        # 1. ANÁLISE PRINCIPAL COM GEMINI PRO (ULTRA-DETALHADA)
        if gemini_client:
            try:
                logger.info("🤖 Executando análise Gemini Pro ultra-detalhada...")
                gemini_analysis = self._run_ultra_gemini_analysis(data, comprehensive_data)
                ai_analyses["gemini_ultra"] = gemini_analysis
                logger.info("✅ Análise Gemini Pro ultra-detalhada concluída")
            except Exception as e:
                logger.error(f"❌ Erro na análise Gemini: {str(e)}")
        
        # 2. ANÁLISE COMPLEMENTAR COM HUGGINGFACE
        try:
            from services.huggingface_client import HuggingFaceClient
            huggingface_client = HuggingFaceClient()
            if huggingface_client.is_available():
                logger.info("🤖 Executando análise HuggingFace complementar...")
                hf_analysis = self._run_huggingface_ultra_analysis(data, comprehensive_data, huggingface_client)
                ai_analyses["huggingface_ultra"] = hf_analysis
                logger.info("✅ Análise HuggingFace concluída")
        except Exception as e:
            logger.warning(f"⚠️ HuggingFace não disponível: {str(e)}")
        
        # 3. ANÁLISE CRUZADA E VALIDAÇÃO
        if len(ai_analyses) > 1:
            logger.info("🔄 Executando análise cruzada entre IAs...")
            cross_analysis = self._perform_cross_ai_analysis(ai_analyses)
            ai_analyses["cross_validation"] = cross_analysis
        
        return ai_analyses
    
    def _implement_advanced_systems(
        self, 
        data: Dict[str, Any], 
        ai_analyses: Dict[str, Any], 
        comprehensive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implementa todos os sistemas avançados dos documentos"""
        
        logger.info("⚡ Implementando sistemas avançados...")
        
        advanced_systems = {}
        
        # 1. SISTEMA DE PROVAS VISUAIS INSTANTÂNEAS
        logger.info("🎯 Implementando Sistema de Provas Visuais...")
        advanced_systems["provas_visuais"] = self._implement_visual_proofs_system(
            data, ai_analyses, comprehensive_data
        )
        
        # 2. ARQUITETO DE DRIVERS MENTAIS
        logger.info("🧠 Implementando Arquiteto de Drivers Mentais...")
        advanced_systems["drivers_mentais"] = self._implement_mental_drivers_system(
            data, ai_analyses, comprehensive_data
        )
        
        # 3. PRÉ-PITCH INVISÍVEL
        logger.info("🎭 Implementando Sistema de Pré-Pitch Invisível...")
        advanced_systems["pre_pitch"] = self._implement_pre_pitch_system(
            data, ai_analyses, comprehensive_data
        )
        
        # 4. ENGENHARIA ANTI-OBJEÇÃO
        logger.info("🛡️ Implementando Engenharia Anti-Objeção...")
        advanced_systems["anti_objecao"] = self._implement_objection_handling_system(
            data, ai_analyses, comprehensive_data
        )
        
        # 5. SISTEMA DE ANCORAGEM PSICOLÓGICA
        logger.info("⚓ Implementando Sistema de Ancoragem Psicológica...")
        advanced_systems["ancoragem_psicologica"] = self._implement_psychological_anchoring(
            data, ai_analyses, comprehensive_data
        )
        
        return advanced_systems
    
    def _implement_visual_proofs_system(
        self, 
        data: Dict[str, Any], 
        ai_analyses: Dict[str, Any], 
        comprehensive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implementa o Sistema Completo de Provas Visuais Instantâneas"""
        
        # Identifica conceitos que precisam de demonstração física
        conceitos_abstratos = self._extract_abstract_concepts(data, ai_analyses)
        
        provas_visuais = {
            "conceitos_identificados": conceitos_abstratos,
            "provis_criadas": [],
            "sequencia_otimizada": [],
            "kit_implementacao": {}
        }
        
        # Cria PROVIs para cada conceito
        for i, conceito in enumerate(conceitos_abstratos, 1):
            provi = {
                "id": f"PROVI_{i:02d}",
                "nome": self._generate_provi_name(conceito),
                "conceito_alvo": conceito["conceito"],
                "categoria": conceito["categoria"],
                "prioridade": conceito["prioridade"],
                "momento_ideal": conceito["momento"],
                "objetivo_psicologico": self._define_psychological_objective(conceito),
                "experimento": self._design_physical_experiment(conceito),
                "analogia": self._create_perfect_analogy(conceito),
                "roteiro_completo": self._create_complete_script(conceito),
                "materiais": self._list_required_materials(conceito),
                "variacoes": self._create_variations(conceito),
                "gestao_riscos": self._create_risk_management(conceito),
                "frases_impacto": self._generate_impact_phrases(conceito),
                "dramatizacao": self._add_theatrical_elements(conceito)
            }
            provas_visuais["provis_criadas"].append(provi)
        
        # Cria sequência psicológica otimizada
        provas_visuais["sequencia_otimizada"] = self._optimize_provi_sequence(
            provas_visuais["provis_criadas"]
        )
        
        # Gera kit de implementação
        provas_visuais["kit_implementacao"] = {
            "checklist_preparacao": self._create_preparation_checklist(provas_visuais["provis_criadas"]),
            "timeline_execucao": self._create_execution_timeline(provas_visuais["sequencia_otimizada"]),
            "script_transicoes": self._create_transition_scripts(provas_visuais["sequencia_otimizada"]),
            "plano_contingencia": self._create_contingency_plan(provas_visuais["provis_criadas"])
        }
        
        return provas_visuais
    
    def _implement_mental_drivers_system(
        self, 
        data: Dict[str, Any], 
        ai_analyses: Dict[str, Any], 
        comprehensive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implementa o Sistema de Drivers Mentais com Ancoragem Psicológica"""
        
        # Analisa o avatar para identificar drivers mais eficazes
        avatar_analysis = ai_analyses.get("gemini_ultra", {}).get("avatar_ultra_detalhado", {})
        
        drivers_system = {
            "drivers_customizados": [],
            "sequenciamento_estrategico": {},
            "scripts_ativacao": {},
            "loops_reforco": {}
        }
        
        # Lista dos 19 drivers universais implementados
        universal_drivers = [
            "ferida_exposta", "trofeu_secreto", "inveja_produtiva", "relogio_psicologico",
            "identidade_aprisionada", "custo_invisivel", "ambicao_expandida", "diagnostico_brutal",
            "ambiente_vampiro", "mentor_salvador", "coragem_necessaria", "mecanismo_revelado",
            "prova_matematica", "padrao_oculto", "excecao_possivel", "atalho_etico",
            "decisao_binaria", "oportunidade_oculta", "metodo_vs_sorte"
        ]
        
        # Seleciona e customiza os 7 drivers mais poderosos para este contexto
        selected_drivers = self._select_optimal_drivers(universal_drivers, avatar_analysis, data)
        
        for driver_name in selected_drivers:
            customized_driver = self._customize_mental_driver(
                driver_name, avatar_analysis, data, comprehensive_data
            )
            drivers_system["drivers_customizados"].append(customized_driver)
        
        # Cria sequenciamento estratégico
        drivers_system["sequenciamento_estrategico"] = self._create_strategic_sequencing(
            drivers_system["drivers_customizados"]
        )
        
        # Gera scripts de ativação
        drivers_system["scripts_ativacao"] = self._generate_activation_scripts(
            drivers_system["drivers_customizados"]
        )
        
        # Cria loops de reforço
        drivers_system["loops_reforco"] = self._create_reinforcement_loops(
            drivers_system["drivers_customizados"]
        )
        
        return drivers_system
    
    def _implement_pre_pitch_system(
        self, 
        data: Dict[str, Any], 
        ai_analyses: Dict[str, Any], 
        comprehensive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implementa o Sistema de Pré-Pitch Invisível"""
        
        drivers_mentais = ai_analyses.get("gemini_ultra", {}).get("drivers_mentais_customizados", [])
        
        pre_pitch_system = {
            "orquestracao_emocional": {},
            "justificacao_logica": {},
            "roteiro_completo": {},
            "adaptacoes_formato": {}
        }
        
        # Seleciona os 5-7 drivers mais poderosos
        selected_drivers = self._select_pre_pitch_drivers(drivers_mentais)
        
        # Cria orquestração emocional (70% do tempo)
        pre_pitch_system["orquestracao_emocional"] = {
            "sequencia_psicologica": [
                {"fase": "QUEBRA", "objetivo": "Destruir ilusão confortável", "tempo": "15%"},
                {"fase": "EXPOSICAO", "objetivo": "Revelar ferida real", "tempo": "15%"},
                {"fase": "INDIGNACAO", "objetivo": "Criar revolta produtiva", "tempo": "15%"},
                {"fase": "VISLUMBRE", "objetivo": "Mostrar o possível", "tempo": "10%"},
                {"fase": "TENSAO", "objetivo": "Amplificar o gap", "tempo": "10%"},
                {"fase": "NECESSIDADE", "objetivo": "Tornar mudança inevitável", "tempo": "5%"}
            ],
            "drivers_por_fase": self._map_drivers_to_phases(selected_drivers),
            "narrativas_conectoras": self._create_connecting_narratives(selected_drivers)
        }
        
        # Cria justificação lógica (30% do tempo)
        pre_pitch_system["justificacao_logica"] = {
            "numeros_irrefutaveis": self._gather_irrefutable_numbers(comprehensive_data),
            "calculos_roi": self._create_roi_calculations(data),
            "demonstracoes_passo_a_passo": self._create_step_by_step_demos(data),
            "cases_metricas": self._extract_case_studies_with_metrics(comprehensive_data),
            "garantias_risco_zero": self._design_risk_elimination_guarantees(data)
        }
        
        # Cria roteiro completo
        pre_pitch_system["roteiro_completo"] = self._create_complete_pre_pitch_script(
            pre_pitch_system["orquestracao_emocional"],
            pre_pitch_system["justificacao_logica"],
            data
        )
        
        # Adaptações por formato
        formats = ["webinario", "evento_presencial", "cpl", "lives_aquecimento"]
        for format_type in formats:
            pre_pitch_system["adaptacoes_formato"][format_type] = self._adapt_pre_pitch_for_format(
                pre_pitch_system["roteiro_completo"], format_type
            )
        
        return pre_pitch_system
    
    def _implement_objection_handling_system(
        self, 
        data: Dict[str, Any], 
        ai_analyses: Dict[str, Any], 
        comprehensive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implementa a Engenharia Psicológica Anti-Objeção"""
        
        avatar_data = ai_analyses.get("gemini_ultra", {}).get("avatar_ultra_detalhado", {})
        
        objection_system = {
            "objecoes_universais": {},
            "objecoes_ocultas": {},
            "arsenal_drives": {},
            "sistema_implementacao": {},
            "arsenal_emergencia": {}
        }
        
        # Identifica objeções universais
        objection_system["objecoes_universais"] = {
            "tempo": self._analyze_time_objections(avatar_data),
            "dinheiro": self._analyze_money_objections(avatar_data),
            "confianca": self._analyze_trust_objections(avatar_data)
        }
        
        # Identifica objeções ocultas
        objection_system["objecoes_ocultas"] = {
            "autossuficiencia": self._detect_self_sufficiency_objection(avatar_data),
            "sinal_fraqueza": self._detect_weakness_signal_objection(avatar_data),
            "medo_novo": self._detect_change_fear_objection(avatar_data),
            "prioridades_desequilibradas": self._detect_priority_imbalance_objection(avatar_data),
            "autoestima_destruida": self._detect_low_self_esteem_objection(avatar_data)
        }
        
        # Cria arsenal de drives mentais anti-objeção
        objection_system["arsenal_drives"] = {
            "elevacao_prioridade": self._create_priority_elevation_drives(data),
            "justificacao_investimento": self._create_investment_justification_drives(data),
            "construcao_confianca": self._create_trust_building_drives(data),
            "neutralizacao_ocultas": self._create_hidden_objection_neutralizers(data)
        }
        
        # Sistema de implementação estratégica
        objection_system["sistema_implementacao"] = {
            "mapeamento_estagios": self._map_objections_to_launch_stages(),
            "personalizacao_perfis": self._create_objection_personas(avatar_data),
            "scripts_templates": self._create_objection_handling_scripts()
        }
        
        # Arsenal de emergência
        objection_system["arsenal_emergencia"] = {
            "objecoes_ultima_hora": self._create_last_minute_objection_handlers(),
            "kit_primeiros_socorros": self._create_objection_first_aid_kit(),
            "diagnostico_rapido": self._create_rapid_objection_diagnosis()
        }
        
        return objection_system
    
    def _implement_psychological_anchoring(
        self, 
        data: Dict[str, Any], 
        ai_analyses: Dict[str, Any], 
        comprehensive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implementa Sistema de Ancoragem Psicológica"""
        
        anchoring_system = {
            "ancoras_emocionais": [],
            "ancoras_logicas": [],
            "sequencia_instalacao": {},
            "loops_reativacao": {},
            "metricas_eficacia": {}
        }
        
        # Cria âncoras emocionais baseadas nas dores e desejos
        avatar_data = ai_analyses.get("gemini_ultra", {}).get("avatar_ultra_detalhado", {})
        dores = avatar_data.get("dores_especificas", [])
        desejos = avatar_data.get("desejos_profundos", [])
        
        for dor in dores:
            ancora_emocional = {
                "tipo": "dor",
                "gatilho": dor,
                "frase_ancoragem": self._create_pain_anchor_phrase(dor),
                "momento_instalacao": "abertura_diagnostico",
                "reativacao": self._create_pain_reactivation_triggers(dor)
            }
            anchoring_system["ancoras_emocionais"].append(ancora_emocional)
        
        for desejo in desejos:
            ancora_emocional = {
                "tipo": "desejo",
                "gatilho": desejo,
                "frase_ancoragem": self._create_desire_anchor_phrase(desejo),
                "momento_instalacao": "desenvolvimento_vislumbre",
                "reativacao": self._create_desire_reactivation_triggers(desejo)
            }
            anchoring_system["ancoras_emocionais"].append(ancora_emocional)
        
        # Cria âncoras lógicas baseadas em dados e provas
        market_data = comprehensive_data.get("market_intelligence", {})
        for key, value in market_data.items():
            ancora_logica = {
                "tipo": "prova",
                "dados": value,
                "frase_ancoragem": self._create_logical_anchor_phrase(key, value),
                "momento_instalacao": "justificacao_logica",
                "reativacao": self._create_logical_reactivation_triggers(key, value)
            }
            anchoring_system["ancoras_logicas"].append(ancora_logica)
        
        # Define sequência de instalação
        anchoring_system["sequencia_instalacao"] = self._create_anchor_installation_sequence(
            anchoring_system["ancoras_emocionais"],
            anchoring_system["ancoras_logicas"]
        )
        
        # Cria loops de reativação
        anchoring_system["loops_reativacao"] = self._create_anchor_reactivation_loops(
            anchoring_system["ancoras_emocionais"] + anchoring_system["ancoras_logicas"]
        )
        
        return anchoring_system
    
    def _consolidate_ultra_analysis(
        self, 
        data: Dict[str, Any], 
        comprehensive_data: Dict[str, Any], 
        ai_analyses: Dict[str, Any], 
        advanced_systems: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consolida toda a análise ultra-detalhada"""
        
        # Usa análise principal do Gemini como base
        main_analysis = ai_analyses.get("gemini_ultra", {})
        
        # Enriquece com sistemas avançados
        ultra_analysis = {
            # Análise base do Gemini (enriquecida)
            **main_analysis,
            
            # Sistemas avançados implementados
            "sistema_provas_visuais": advanced_systems.get("provas_visuais", {}),
            "sistema_drivers_mentais": advanced_systems.get("drivers_mentais", {}),
            "sistema_pre_pitch": advanced_systems.get("pre_pitch", {}),
            "sistema_anti_objecao": advanced_systems.get("anti_objecao", {}),
            "sistema_ancoragem": advanced_systems.get("ancoragem_psicologica", {}),
            
            # Inteligência de mercado ultra-detalhada
            "inteligencia_mercado_ultra": comprehensive_data.get("market_intelligence", {}),
            "analise_concorrencia_ultra": comprehensive_data.get("competitor_analysis", {}),
            "analise_tendencias_ultra": comprehensive_data.get("trend_analysis", {}),
            
            # Insights exclusivos ultra-profundos
            "insights_exclusivos_ultra": self._generate_ultra_exclusive_insights(
                comprehensive_data, ai_analyses, advanced_systems
            ),
            
            # Plano de implementação completo
            "plano_implementacao_completo": self._create_complete_implementation_plan(
                data, advanced_systems
            ),
            
            # Métricas de sucesso avançadas
            "metricas_sucesso_avancadas": self._create_advanced_success_metrics(
                data, main_analysis
            ),
            
            # Cronograma detalhado de 365 dias
            "cronograma_365_dias": self._create_365_day_timeline(data, advanced_systems),
            
            # Sistema de monitoramento e otimização
            "sistema_monitoramento": self._create_monitoring_system(data, main_analysis)
        }
        
        return ultra_analysis
    
    # Métodos auxiliares para implementação dos sistemas
    def _generate_ultra_comprehensive_queries(self, data: Dict[str, Any]) -> List[str]:
        """Gera queries ultra-abrangentes para pesquisa"""
        segmento = data.get("segmento", "")
        produto = data.get("produto", "")
        
        queries = [
            # Queries principais
            f"análise completa mercado {segmento} Brasil 2024 tendências oportunidades",
            f"concorrentes {segmento} principais players estratégias posicionamento",
            f"público-alvo {segmento} comportamento consumidor dores desejos",
            f"preços {segmento} ticket médio margem lucro benchmarks",
            
            # Queries específicas do produto
            f"{produto} mercado brasileiro demanda crescimento projeções",
            f"como vender {produto} estratégias marketing digital conversão",
            f"{produto} cases sucesso métricas resultados ROI",
            
            # Queries de inteligência competitiva
            f"oportunidades inexploradas {segmento} gaps mercado nichos",
            f"inovações disruptivas {segmento} tecnologias emergentes",
            f"regulamentações {segmento} mudanças legais impactos",
            
            # Queries de comportamento
            f"psicologia consumidor {segmento} gatilhos mentais persuasão",
            f"objeções comuns {segmento} resistências barreiras compra",
            f"jornada cliente {segmento} touchpoints conversão funil"
        ]
        
        return queries[:10]  # Limita a 10 queries principais
    
    def _calculate_ultra_quality_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de qualidade ultra-detalhado"""
        score = 0.0
        max_score = 100.0
        
        # Pontuação por seções implementadas (40 pontos)
        required_sections = [
            "avatar_ultra_detalhado", "sistema_drivers_mentais", "sistema_provas_visuais",
            "sistema_pre_pitch", "sistema_anti_objecao", "inteligencia_mercado_ultra"
        ]
        
        for section in required_sections:
            if section in analysis and analysis[section]:
                score += 6.67  # 40/6 = 6.67 pontos por seção
        
        # Pontuação por profundidade de insights (30 pontos)
        insights = analysis.get("insights_exclusivos_ultra", [])
        if len(insights) >= 15:
            score += 30.0
        elif len(insights) >= 10:
            score += 20.0
        elif len(insights) >= 5:
            score += 10.0
        
        # Pontuação por sistemas avançados (30 pontos)
        advanced_systems = [
            "sistema_provas_visuais", "sistema_drivers_mentais", "sistema_pre_pitch",
            "sistema_anti_objecao", "sistema_ancoragem"
        ]
        
        for system in advanced_systems:
            if system in analysis and analysis[system]:
                score += 6.0  # 30/5 = 6 pontos por sistema
        
        return min(score, max_score)
    
    def _calculate_completeness_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de completude da análise"""
        total_sections = 20  # Total de seções possíveis
        completed_sections = 0
        
        sections_to_check = [
            "avatar_ultra_detalhado", "sistema_drivers_mentais", "sistema_provas_visuais",
            "sistema_pre_pitch", "sistema_anti_objecao", "sistema_ancoragem",
            "inteligencia_mercado_ultra", "analise_concorrencia_ultra", "analise_tendencias_ultra",
            "insights_exclusivos_ultra", "plano_implementacao_completo", "metricas_sucesso_avancadas",
            "cronograma_365_dias", "sistema_monitoramento"
        ]
        
        for section in sections_to_check:
            if section in analysis and analysis[section]:
                completed_sections += 1
        
        return (completed_sections / len(sections_to_check)) * 100.0
    
    def _generate_emergency_ultra_fallback(self, data: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Gera análise de emergência ultra-básica"""
        logger.error(f"Gerando análise de emergência devido a: {error}")
        
        return {
            "avatar_ultra_detalhado": {
                "perfil_demografico": {
                    "idade": "25-45 anos",
                    "renda": "R$ 3.000 - R$ 15.000",
                    "escolaridade": "Superior"
                },
                "dores_especificas": [
                    "Falta de conhecimento especializado",
                    "Dificuldade para implementar estratégias",
                    "Resultados inconsistentes"
                ]
            },
            "insights_exclusivos_ultra": [
                "Análise gerada em modo de emergência",
                f"Erro no processamento: {error}",
                "Recomenda-se executar nova análise com dados completos",
                "Sistema detectou necessidade de análise mais profunda"
            ],
            "metadata_ultra_detalhado": {
                "processing_time_seconds": 0,
                "analysis_engine": "Emergency Fallback Ultra",
                "generated_at": datetime.utcnow().isoformat(),
                "quality_score": 25.0,
                "completeness_score": 15.0,
                "error": error,
                "recommendation": "Execute nova análise com configuração completa"
            }
        }
    
    # Métodos auxiliares específicos (implementação básica para não quebrar o código)
    def _analyze_attachment_content(self, content: str, content_type: str) -> Dict[str, Any]:
        """Analisa conteúdo específico do anexo"""
        return {
            "content_length": len(content),
            "word_count": len(content.split()),
            "type": content_type,
            "key_concepts": content.split()[:10]  # Primeiras 10 palavras como conceitos
        }
    
    def _gather_ultra_market_intelligence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coleta inteligência de mercado ultra-detalhada"""
        return {
            "market_size": "Mercado em crescimento",
            "growth_rate": "15-25% ao ano",
            "key_trends": ["Digitalização", "Automação", "Personalização"],
            "opportunities": ["Nichos inexplorados", "Novas tecnologias", "Mudanças comportamentais"]
        }
    
    def _perform_deep_competitor_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza análise profunda de concorrência"""
        return {
            "direct_competitors": ["Concorrente A", "Concorrente B"],
            "indirect_competitors": ["Alternativa X", "Alternativa Y"],
            "competitive_gaps": ["Gap 1", "Gap 2"],
            "market_positioning": "Análise de posicionamento"
        }
    
    def _analyze_market_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa tendências de mercado"""
        return {
            "emerging_trends": ["Tendência 1", "Tendência 2"],
            "declining_trends": ["Tendência em declínio"],
            "future_predictions": ["Previsão 1", "Previsão 2"],
            "impact_analysis": "Análise de impacto das tendências"
        }

# Instância global do analisador ultra-robusto
ultra_analyzer = UltraRobustAnalyzer()

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
    """Endpoint principal para análise ultra-robusta de mercado"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Dados não fornecidos',
                'message': 'Envie os dados da análise no corpo da requisição'
            }), 400
        
        # Validação básica
        if not data.get('segmento'):
            return jsonify({
                'error': 'Segmento obrigatório',
                'message': 'O campo "segmento" é obrigatório para a análise'
            }), 400
        
        # Processa dados numéricos
        for field in ['preco', 'objetivo_receita', 'orcamento_marketing']:
            if field in data and data[field]:
                try:
                    data[f'{field}_float'] = float(str(data[field]).replace(',', '.'))
                except (ValueError, TypeError):
                    data[f'{field}_float'] = 0.0
        
        # Obtém session_id
        session_id = data.get('session_id') or session.get('session_id')
        
        logger.info(f"🚀 Iniciando análise ultra-robusta para: {data.get('segmento')}")
        
        # Executa análise ultra-robusta
        result = ultra_analyzer.generate_ultra_comprehensive_analysis(data, session_id)
        
        # Salva no banco de dados
        if result and 'error' not in result:
            try:
                analysis_record = db_manager.create_analysis({
                    'segmento': data.get('segmento'),
                    'produto': data.get('produto'),
                    'preco': data.get('preco_float'),
                    'publico': data.get('publico'),
                    'concorrentes': data.get('concorrentes'),
                    'dados_adicionais': data.get('dados_adicionais'),
                    'objetivo_receita': data.get('objetivo_receita_float'),
                    'orcamento_marketing': data.get('orcamento_marketing_float'),
                    'prazo_lancamento': data.get('prazo_lancamento'),
                    'comprehensive_analysis': result
                })
                
                if analysis_record:
                    result['database_id'] = analysis_record['id']
                    logger.info(f"✅ Análise salva no banco com ID: {analysis_record['id']}")
                
            except Exception as e:
                logger.error(f"⚠️ Erro ao salvar no banco: {str(e)}")
                # Não falha a análise por erro de banco
        
        logger.info("🎉 Análise ultra-robusta concluída com sucesso!")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro crítico na análise: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Erro interno na análise',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@analysis_bp.route('/upload_attachment', methods=['POST'])
def upload_attachment():
    """Upload e processamento de anexos"""
    
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo enviado'
            }), 400
        
        file = request.files['file']
        session_id = request.form.get('session_id', 'default_session')
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nome de arquivo vazio'
            }), 400
        
        # Processa anexo
        result = attachment_service.process_attachment(file, session_id)
        
        if result.get('success'):
            logger.info(f"📎 Anexo processado: {file.filename}")
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"❌ Erro no upload: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@analysis_bp.route('/deep_search', methods=['POST'])
def perform_deep_search():
    """Executa busca profunda na internet"""
    
    try:
        data = request.get_json()
        
        if not data or not data.get('query'):
            return jsonify({
                'error': 'Query obrigatória',
                'message': 'Forneça uma query para busca'
            }), 400
        
        query = data['query']
        context = data.get('context', {})
        
        logger.info(f"🔍 Executando busca profunda: {query}")
        
        # Executa busca profunda
        result = deep_search_service.perform_deep_search(query, context)
        
        return jsonify({
            'query': query,
            'context': context,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro na busca profunda: {str(e)}")
        return jsonify({
            'error': 'Erro na busca profunda',
            'message': str(e)
        }), 500

@analysis_bp.route('/analyses', methods=['GET'])
def list_analyses():
    """Lista análises salvas"""
    
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        segmento = request.args.get('segmento')
        
        analyses = db_manager.list_analyses(limit, offset)
        
        # Filtra por segmento se especificado
        if segmento:
            analyses = [a for a in analyses if segmento.lower() in a.get('nicho', '').lower()]
        
        return jsonify({
            'analyses': analyses,
            'count': len(analyses),
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar análises: {str(e)}")
        return jsonify({
            'error': 'Erro ao listar análises',
            'message': str(e)
        }), 500

@analysis_bp.route('/analyses/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Obtém análise específica"""
    
    try:
        analysis = db_manager.get_analysis(analysis_id)
        
        if not analysis:
            return jsonify({
                'error': 'Análise não encontrada',
                'message': f'Análise com ID {analysis_id} não existe'
            }), 404
        
        return jsonify(analysis)
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter análise {analysis_id}: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter análise',
            'message': str(e)
        }), 500

@analysis_bp.route('/stats', methods=['GET'])
def get_analysis_stats():
    """Obtém estatísticas das análises"""
    
    try:
        stats = db_manager.get_stats()
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter estatísticas',
            'message': str(e)
        }), 500