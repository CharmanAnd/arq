from flask import Blueprint, request, jsonify
import os
import json
from datetime import datetime, timedelta
import logging
from supabase import create_client, Client
from services.gemini_client import gemini_client
from services.deep_search_service import deep_search_service
from services.attachment_service import attachment_service
from services.enhanced_analysis_engine import enhanced_analysis_engine
import requests
import re
import time
from typing import Dict, List, Optional, Tuple, Any
import concurrent.futures
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analysis_bp = Blueprint("analysis", __name__)

# Initialize Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("✅ Supabase configurado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao configurar Supabase: {e}")

# Cache para dados de mercado (ainda pode ser útil para evitar chamadas repetidas na mesma sessão)
@lru_cache(maxsize=100)
def get_market_data_cache(nicho: str, region: str = "BR") -> Dict:
    """Cache para dados de mercado por nicho"""
    return {}

class MarketAnalyzer:
    """Classe principal para análise de mercado avançada"""

    def __init__(self):
        # Estas chaves não são mais usadas diretamente aqui, mas mantidas para referência
        self.serp_api_key = os.getenv("SERP_API_KEY")
        self.facebook_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    def get_keyword_data(self, keywords: List[str]) -> Dict:
        """Obtém dados reais de palavras-chave usando WebSailor"""
        if not websailor_agent.is_available():
            logger.warning("WebSailor não disponível para dados de palavras-chave. Usando simulação.")
            return self._simulate_keyword_data(keywords)

        keyword_data = {}
        for keyword in keywords:
            # Usar WebSailor para buscar informações sobre a palavra-chave
            # Isso pode ser uma busca mais focada ou extração de tendências
            research_result = websailor_agent.navigate_and_research(
                f"tendências de mercado para {keyword}",
                context={
                    "keyword": keyword
                },
                max_pages=2 # Limitar para não sobrecarregar
            )
            
            # Processar o resultado da pesquisa para extrair volume, dificuldade, etc.
            # Isso exigiria uma análise mais profunda do texto retornado pelo WebSailor
            # Por simplicidade, vamos extrair alguns dados simulados e enriquecer com o que o WebSailor trouxer
            simulated_data = self._simulate_keyword_data([keyword])[keyword]
            
            # Tentar extrair insights do research_result
            insights = research_result.get("research_summary", {}).get("key_insights", [])
            trends = research_result.get("research_summary", {}).get("market_trends", [])

            keyword_data[keyword] = {
                "volume": simulated_data["volume"],
                "difficulty": simulated_data["difficulty"],
                "cpc": simulated_data["cpc"],
                "trend": simulated_data["trend"],
                "insights_web": insights,
                "trends_web": trends
            }
        return keyword_data

    def _simulate_keyword_data(self, keywords: List[str]) -> Dict:
        """Simula dados de palavras-chave para fallback"""
        keyword_data = {}
        for keyword in keywords:
            base_volume = len(keyword.split()) * 1000
            volume = min(base_volume * 10, 50000)
            difficulty = "Baixa" if len(keyword.split()) > 3 else ("Média" if len(keyword.split()) > 2 else "Alta")
            cpc = round(1.20 + (len(keyword.split()) * 0.3), 2)
            
            high_value_niches = ["finanças", "investimento", "marketing", "saúde", "educação"]
            if any(nicho in keyword.lower() for nicho in high_value_niches):
                cpc = round(2.50 + (len(keyword.split()) * 0.5), 2)

            keyword_data[keyword] = {
                "volume": volume,
                "difficulty": difficulty,
                "cpc": cpc,
                "trend": "Crescimento Estável",
                "insights_web": [],
                "trends_web": []
            }
        return keyword_data

    def analyze_competitors(self, nicho: str, competitors: str, product_name: str = "") -> List[Dict]:
        """Análise avançada de concorrentes com pesquisa WebSailor"""
        competitor_list = [c.strip() for c in competitors.split(",") if c.strip()] if competitors else []

        analyzed_competitors = []
        if not competitor_list:
            # Se não há concorrentes informados, criar análise genérica e tentar buscar online
            generic_competitors = self._create_generic_competitor_analysis(nicho)
            for comp in generic_competitors:
                analyzed_competitors.append(self._enrich_competitor_with_websailor(comp["nome"], nicho, product_name, comp))
        else:
            for competitor in competitor_list:
                analyzed_competitors.append(self._enrich_competitor_with_websailor(competitor, nicho, product_name))

        return analyzed_competitors

    def _enrich_competitor_with_websailor(self, competitor_name: str, nicho: str, product_name: str, base_data: Dict = None) -> Dict:
        """Enriquece dados do concorrente com pesquisa WebSailor"""
        logger.info(f"Enriquecendo dados para o concorrente: {competitor_name}")
        
        competitor_data = base_data if base_data else {
            "nome": competitor_name,
            "produto_servico": f"Produto/serviço em {nicho}",
            "preco_estimado": self._estimate_competitor_price(nicho),
            "market_share_estimado": "5-15% do nicho",
        }

        if websailor_agent.is_available():
            query = f"análise de {competitor_name} {nicho} {product_name} pontos fortes e fracos estratégia marketing"
            research_result = websailor_agent.navigate_and_research(
                query,
                context={
                    "competitor": competitor_name,
                    "nicho": nicho,
                    "product": product_name
                },
                max_pages=3 # Buscar mais páginas para concorrentes
            )

            summary = research_result.get("research_summary", {})
            key_insights = summary.get("key_insights", [])
            
            # Tentar extrair forças, fraquezas e estratégias de marketing dos insights
            strengths = [s for s in key_insights if "forte" in s.lower() or "sucesso" in s.lower() or "lider" in s.lower()][:2]
            weaknesses = [w for w in key_insights if "fraco" in w.lower() or "desafio" in w.lower() or "falha" in w.lower()][:2]
            marketing_strategy = [m for m in key_insights if "marketing" in m.lower() or "campanha" in m.lower() or "publicidade" in m.lower()][:1]

            competitor_data["forcas"] = "; ".join(strengths) if strengths else self._analyze_competitor_strengths(competitor_name, nicho)
            competitor_data["fraquezas"] = "; ".join(weaknesses) if weaknesses else self._analyze_competitor_weaknesses(competitor_name, nicho)
            competitor_data["estrategia_marketing"] = "; ".join(marketing_strategy) if marketing_strategy else self._analyze_marketing_strategy(competitor_name)
            competitor_data["oportunidade_diferenciacao"] = self._find_differentiation_opportunity(competitor_name, nicho)
            competitor_data["sources"] = research_result.get("sources", [])
        else:
            competitor_data["forcas"] = self._analyze_competitor_strengths(competitor_name, nicho)
            competitor_data["fraquezas"] = self._analyze_competitor_weaknesses(competitor_name, nicho)
            competitor_data["estrategia_marketing"] = self._analyze_marketing_strategy(competitor_name)
            competitor_data["oportunidade_diferenciacao"] = self._find_differentiation_opportunity(competitor_name, nicho)
            competitor_data["sources"] = []

        return competitor_data

    def _estimate_competitor_price(self, nicho: str) -> str:
        price_ranges = {
            "marketing digital": "R$ 497-2.997",
            "saúde": "R$ 197-997",
            "fitness": "R$ 97-497",
            "finanças": "R$ 297-1.497",
            "educação": "R$ 197-897",
            "desenvolvimento pessoal": "R$ 297-1.997"
        }
        for key, value in price_ranges.items():
            if key in nicho.lower():
                return value
        return "R$ 197-997"

    def _analyze_competitor_strengths(self, competitor: str, nicho: str) -> str:
        return "Marca estabelecida; Base de clientes consolidada; Presença online forte"

    def _analyze_competitor_weaknesses(self, competitor: str, nicho: str) -> str:
        return "Atendimento ao cliente limitado; Produto genérico; Falta de inovação"

    def _estimate_market_share(self, competitor: str) -> str:
        return "5-15% do nicho"

    def _analyze_marketing_strategy(self, competitor: str) -> str:
        return "Foco em Facebook Ads e Instagram; Marketing de conteúdo e SEO"

    def _find_differentiation_opportunity(self, competitor: str, nicho: str) -> str:
        return "Personalização da experiência; Suporte humanizado; Metodologia exclusiva"

    def _create_generic_competitor_analysis(self, nicho: str) -> List[Dict]:
        return [
            {
                "nome": f"Líder do mercado em {nicho}",
                "produto_servico": f"Curso/consultoria premium em {nicho}",
                "preco_estimado": self._estimate_competitor_price(nicho),
                "forcas": "Autoridade estabelecida; Grande base de clientes; Marketing bem estruturado",
                "fraquezas": "Preço elevado; Atendimento massificado; Pouca inovação",
                "market_share_estimado": "15-25% do nicho",
                "estrategia_marketing": "Facebook Ads + E-mail marketing + Webinars",
                "oportunidade_diferenciacao": "Atendimento personalizado e metodologia exclusiva"
            },
            {
                "nome": f"Challenger em {nicho}",
                "produto_servico": f"Produto digital intermediário em {nicho}",
                "preco_estimado": "R$ 197-697",
                "forcas": "Preço acessível; Marketing ágil; Inovação constante",
                "fraquezas": "Menor autoridade; Recursos limitados; Suporte básico",
                "market_share_estimado": "5-10% do nicho",
                "estrategia_marketing": "Instagram + TikTok + Influenciadores micro",
                "oportunidade_diferenciacao": "Superior qualidade de conteúdo e suporte premium"
            }
        ]

analyzer = MarketAnalyzer()

@analysis_bp.route("/analyze", methods=["POST"])
def analyze_market():
    """Endpoint principal para análise de mercado"""
    try:
        data = request.get_json()

        if not data or not data.get("segmento"):
            return jsonify({"error": "Segmento de mercado é obrigatório"}), 400

        analysis_data = {
            "segmento": data.get("segmento", "").strip(),
            "produto": data.get("produto", "").strip(),
            "preco": data.get("preco", ""),
            "publico": data.get("publico", "").strip(),
            "concorrentes": data.get("concorrentes", "").strip(),
            "query": data.get("query", "").strip(),
            "dados_adicionais": data.get("dados_adicionais", "").strip(),
            "objetivo_receita": data.get("objetivo_receita", ""),
            "orcamento_marketing": data.get("orcamento_marketing", ""),
            "prazo_lancamento": data.get("prazo_lancamento", ""),
            "session_id": data.get("session_id", "")
        }

        # Convert numeric fields
        try:
            analysis_data["preco_float"] = float(analysis_data["preco"]) if analysis_data["preco"] else None
            analysis_data["objetivo_receita_float"] = float(analysis_data["objetivo_receita"]) if analysis_data["objetivo_receita"] else None
            analysis_data["orcamento_marketing_float"] = float(analysis_data["orcamento_marketing"]) if analysis_data["orcamento_marketing"] else None
        except ValueError:
            analysis_data["preco_float"] = None
            analysis_data["objetivo_receita_float"] = None
            analysis_data["orcamento_marketing_float"] = None

        # Save initial analysis record to Supabase
        analysis_id = save_initial_analysis(analysis_data)

        # Generate comprehensive analysis using Enhanced Analysis Engine
        analysis_result = enhanced_analysis_engine.generate_ultra_detailed_analysis(analysis_data, analysis_data.get("session_id"))

        # Update analysis record with results
        if supabase and analysis_id:
            update_analysis_record(analysis_id, analysis_result)
            analysis_result["analysis_id"] = analysis_id

        return jsonify(analysis_result)

    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor", "details": str(e)}), 500

def save_initial_analysis(data: Dict) -> Optional[int]:
    """Salva registro inicial da análise no Supabase"""
    if not supabase:
        logger.warning("Supabase não configurado. Não foi possível salvar a análise inicial.")
        return None

    try:
        analysis_record = {
            "nicho": data["segmento"],
            "produto": data["produto"],
            "preco": data["preco_float"],
            "publico": data["publico"],
            "concorrentes": data["concorrentes"],
            "dados_adicionais": data["dados_adicionais"],
            "objetivo_receita": data["objetivo_receita_float"],
            "orcamento_marketing": data["orcamento_marketing_float"],
            "prazo_lancamento": data["prazo_lancamento"],
            "status": "processing",
            "created_at": datetime.utcnow().isoformat()
        }

        result = supabase.table("analyses").insert(analysis_record).execute()
        if result.data:
            analysis_id = result.data[0]["id"]
            logger.info(f"Análise criada no Supabase com ID: {analysis_id}")
            return analysis_id
    except Exception as e:
        logger.warning(f"Erro ao salvar análise inicial no Supabase: {str(e)}")

    return None

def update_analysis_record(analysis_id: int, results: Dict):
    """Atualiza registro da análise com resultados no Supabase"""
    if not supabase:
        logger.warning("Supabase não configurado. Não foi possível atualizar a análise.")
        return

    try:
        update_data = {
            "avatar_data": results.get("avatar_ultra_detalhado", {}),
            "positioning_data": results.get("escopo", {}),
            "competition_data": results.get("analise_concorrencia_detalhada", {}),
            "marketing_data": results.get("estrategia_palavras_chave", {}),
            "metrics_data": results.get("metricas_performance_detalhadas", {}),
            "funnel_data": results.get("funil_vendas_otimizado", {}),
            "market_intelligence": results.get("inteligencia_mercado", {}),
            "action_plan": results.get("plano_acao_detalhado", {}),
            "comprehensive_analysis": results, # Salva o resultado completo para referência
            "status": "completed",
            "updated_at": datetime.utcnow().isoformat()
        }

        supabase.table("analyses").update(update_data).eq("id", analysis_id).execute()
        logger.info(f"Análise {analysis_id} atualizada no Supabase")

    except Exception as e:
        logger.warning(f"Erro ao atualizar análise no Supabase: {str(e)}")

def generate_advanced_market_analysis(data: Dict) -> Dict:
    """Gera análise avançada de mercado, orquestrando IA e WebSailor"""

    start_time = time.time()
    logger.info(f"Iniciando geração de análise avançada para {data.get('segmento')}")

    # Coleta de dados adicionais dos anexos
    session_id = data.get("session_id")
    attached_content = ""
    if session_id:
        attachments = attachment_service.get_session_attachments(session_id)
        for att in attachments:
            if att.get("extracted_content"):
                attached_content += att["extracted_content"] + "\n\n"
        if attached_content:
            logger.info(f"Conteúdo extraído de {len(attachments)} anexos. Tamanho: {len(attached_content)} caracteres.")

    # Pesquisa profunda com WebSailor (se houver query ou necessidade)
    web_research_summary = {}
    if websailor_agent.is_available() and data.get("query"):
        logger.info(f"Realizando pesquisa profunda com WebSailor para query: {data['query']}")
        web_research_summary = websailor_agent.navigate_and_research(
            data["query"],
            context={
                "segmento": data["segmento"],
                "produto": data["produto"],
                "publico": data["publico"]
            },
            max_pages=5 # Aumentar o número de páginas para pesquisa profunda
        ).get("research_summary", {})
        logger.info(f"WebSailor retornou insights: {len(web_research_summary.get('key_insights', []))}")
    elif data.get("query"):
        logger.warning("WebSailor não está disponível, pesquisa profunda será limitada.")
        # Fallback para pesquisa básica se WebSailor não estiver ativo
        web_research_summary = websailor_agent._generate_fallback_research(data["query"], {
            "segmento": data["segmento"],
            "produto": data["produto"]
        }).get("research_summary", {})

    # Constrói o prompt para a IA com o máximo de contexto possível
    enhanced_prompt = create_enhanced_analysis_prompt(data, attached_content, web_research_summary)

    try:
        # Usar Gemini para a análise principal
        if not gemini_client:
            raise ValueError("Cliente Gemini não inicializado.")

        logger.info("Enviando prompt para Gemini para análise detalhada...")
        # Aumentar o tempo limite para a resposta da IA
        ai_response_text = gemini_client.generate_content(enhanced_prompt, timeout=300) # 5 minutos de timeout
        logger.info("Resposta do Gemini recebida.")

        # Tenta extrair JSON da resposta da IA
        json_match = re.search(r"```json\n(.*?)```", ai_response_text, re.DOTALL)
        if not json_match:
            json_match = re.search(r"\{.*\}", ai_response_text, re.DOTALL)

        if json_match:
            json_str = json_match.group(1) if json_match.group(1) else json_match.group(0)
            analysis_result = json.loads(json_str)
            logger.info("Análise JSON da IA parseada com sucesso.")
        else:
            logger.error("Não foi possível extrair JSON da resposta da IA. Resposta bruta:" + ai_response_text[:500])
            raise ValueError("Não foi possível extrair JSON da resposta da IA")

        # Enriquecer com dados de palavras-chave e concorrentes (paralelo)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_keywords = executor.submit(analyzer.get_keyword_data,
                                            analysis_result.get("estrategia_palavras_chave", {}).get("palavras_primarias", []))
            future_competitors = executor.submit(analyzer.analyze_competitors,
                                                data["segmento"], data["concorrentes"], data["produto"])

            keyword_data = future_keywords.result()
            competitor_analysis = future_competitors.result()

        analysis_result["estrategia_palavras_chave"]["dados_reais"] = keyword_data
        analysis_result["analise_concorrencia_detalhada"] = competitor_analysis

        end_time = time.time()
        processing_time = end_time - start_time
        logger.info(f"Análise avançada concluída em {processing_time:.2f} segundos.")

        analysis_result["metadata"] = {
            "processing_time_seconds": processing_time,
            "ai_model": "Google Gemini Pro",
            "websailor_used": websailor_agent.is_available() and bool(data.get("query")),
            "attachments_processed": bool(attached_content),
            "generated_at": datetime.utcnow().isoformat()
        }

        return analysis_result

    except Exception as e:
        logger.error(f"Erro ao gerar análise com IA ou processar resultados: {str(e)}", exc_info=True)
        return create_fallback_analysis(data["segmento"], data["produto"], data["preco_float"], str(e))

def create_enhanced_analysis_prompt(data: Dict, attached_content: str, web_research_summary: Dict) -> str:
    """Cria um prompt detalhado para a IA, incorporando todos os dados"""
    prompt_parts = [
        "Você é um especialista em análise de mercado ultra-detalhada, marketing estratégico e psicologia do consumidor. Sua tarefa é gerar uma análise de mercado completa e acionável, com o triplo da profundidade e insights que uma análise comum. Pense como um consultor de alto nível que não deixa pedra sobre pedra.",
        "Gere a saída em formato JSON, seguindo a estrutura fornecida. Seja EXTREMAMENTE detalhado e específico em cada seção. Não use placeholders ou texto genérico. Crie conteúdo original e aprofundado para cada campo.",
        "\n### DADOS DE ENTRADA DO USUÁRIO:\n",
        f"- Segmento de Mercado: {data.get('segmento')}",
        f"- Produto/Serviço: {data.get('produto')}",
        f"- Preço Sugerido: R$ {data.get('preco')}",
        f"- Público-Alvo (descrição do usuário): {data.get('publico')}",
        f"- Concorrentes Informados: {data.get('concorrentes')}",
        f"- Objetivo de Receita: R$ {data.get('objetivo_receita')}",
        f"- Orçamento de Marketing: R$ {data.get('orcamento_marketing')}",
        f"- Prazo de Lançamento: {data.get('prazo_lancamento')}",
        f"- Dados Adicionais do Usuário: {data.get('dados_adicionais')}"
    ]

    if attached_content:
        prompt_parts.append("\n### CONTEÚDO EXTRAÍDO DE ANEXOS INTELIGENTES:\n")
        prompt_parts.append(f"""```text
{attached_content[:4000]} # Limitar para evitar estouro de token
```""")
        prompt_parts.append("Analise este conteúdo para extrair informações relevantes para a análise de mercado, avatar, concorrência e estratégias.")

    if web_research_summary:
        prompt_parts.append("\n### RESULTADOS DA PESQUISA PROFUNDA (WEBSAILOR):\n")
        if web_research_summary.get("key_insights"):
            prompt_parts.append("**Insights Chave:**")
            for insight in web_research_summary["key_insights"]:
                prompt_parts.append(f"- {insight}")
        if web_research_summary.get("market_trends"):
            prompt_parts.append("**Tendências de Mercado:**")
            for trend in web_research_summary["market_trends"]:
                prompt_parts.append(f"- {trend}")
        if web_research_summary.get("opportunities"):
            prompt_parts.append("**Oportunidades Identificadas:**")
            for opp in web_research_summary["opportunities"]:
                prompt_parts.append(f"- {opp}")
        prompt_parts.append("Incorpore estas informações da pesquisa web para enriquecer todas as seções da análise, especialmente as tendências, oportunidades e análise de concorrência.")

    prompt_parts.append("\n### ESTRUTURA DE SAÍDA JSON (PREENCHA CADA CAMPO COM DETALHES EXAUSTIVOS):\n")
    prompt_parts.append("""```json
{
  "avatar_ultra_detalhado": {
    "nome_ficticio": "[Nome de Persona, ex: Ana Empreendedora Digital]",
    "perfil_demografico": {
      "idade": "[Faixa etária detalhada, ex: 28-35 anos]",
      "genero": "[Gênero predominante ou 'Ambos']",
      "renda": "[Faixa de renda mensal, ex: R$ 5.000 - R$ 15.000]",
      "escolaridade": "[Nível de escolaridade, ex: Ensino Superior Completo]",
      "localizacao": "[Regiões ou tipos de cidade, ex: Grandes centros urbanos do Sudeste do Brasil]",
      "estado_civil": "[Estado civil comum, ex: Casada com filhos pequenos]",
      "ocupacao": "[Profissão ou tipo de empreendedor, ex: Pequenos empresários, freelancers, infoprodutores]"
    },
    "perfil_psicografico": {
      "personalidade": "[Traços de personalidade, ex: Ambiciosa, proativa, busca autodesenvolvimento]",
      "valores": "[Valores fundamentais, ex: Liberdade financeira, tempo com a família, impacto social]",
      "interesses": "[Interesses além do negócio, ex: Viagens, bem-estar, leitura, tecnologia]",
      "estilo_vida": "[Descrição do estilo de vida, ex: Busca equilíbrio entre trabalho e vida pessoal, valoriza flexibilidade]",
      "comportamento_compra": "[Como toma decisões de compra, ex: Pesquisa exaustivamente, valoriza prova social, influenciada por especialistas]",
      "influenciadores": "[Tipos de influenciadores ou figuras de autoridade que segue, ex: Mentores de negócios, especialistas em marketing digital, autores de livros de desenvolvimento pessoal]"
    },
    "resumo_jornada_dor": "[Narrativa detalhada da dor, ex: Acorda todos os dias sentindo a pressão de não conseguir escalar seu negócio, presa em tarefas operacionais e sem tempo para inovar, temendo que seu sonho de liberdade financeira nunca se realize.]",
    "dores_especificas": [
      "[Dor 1: Ex: Dificuldade em atrair clientes qualificados de forma consistente]",
      "[Dor 2: Ex: Sobrecarga de trabalho e falta de automação]",
      "[Dor 3: Ex: Medo de investir em estratégias que não trazem retorno]",
      "[Dor 4: Ex: Insegurança sobre como se diferenciar em um mercado saturado]",
      "[Dor 5: Ex: Falta de clareza no próximo passo para escalar o negócio]"
    ],
    "desejos_profundos": [
      "[Desejo 1: Ex: Escalar o negócio para múltiplos 6 ou 7 dígitos com menos esforço]",
      "[Desejo 2: Ex: Ter mais tempo livre para a família e hobbies]",
      "[Desejo 3: Ex: Ser reconhecida como autoridade em seu nicho]",
      "[Desejo 4: Ex: Criar um legado e impactar positivamente a vida de outras pessoas]",
      "[Desejo 5: Ex: Ter previsibilidade e segurança financeira]"
    ],
    "medos_paralisantes": [
      "[Medo 1: Ex: Fracassar e ter que voltar ao emprego CLT]",
      "[Medo 2: Ex: Ser vista como uma fraude ou não ser boa o suficiente]",
      "[Medo 3: Ex: Perder dinheiro em investimentos errados]",
      "[Medo 4: Ex: O negócio estagnar ou ser superado pela concorrência]"
    ],
    "frustracoes_diarias": [
      "[Frustração 1: Ex: Perder horas em redes sociais sem gerar vendas]",
      "[Frustração 2: Ex: Dificuldade em delegar tarefas e confiar na equipe]",
      "[Frustração 3: Ex: Burocracia e impostos excessivos]",
      "[Frustração 4: Ex: Não conseguir se desconectar do trabalho]"
    ],
    "linguagem_interna_externa": {
      "frases_dores": [
        "[Frase 1: Ex: 'Estou exausta de tanto trabalhar e não ver o resultado']",
        "[Frase 2: Ex: 'Parece que todo mundo está crescendo menos eu']"
      ],
      "frases_desejos": [
        "[Frase 1: Ex: 'Quero ter liberdade para trabalhar de onde quiser']",
        "[Frase 2: Ex: 'Sonho em ter um negócio que funcione no automático']"
      ],
      "metaforas_comuns": [
        "[Metáfora 1: Ex: 'Correr na esteira sem sair do lugar']",
        "[Metáfora 2: Ex: 'Apagar incêndios o dia todo']"
      ],
      "fontes_confianca": [
        "[Fonte 1: Ex: Podcasts de empreendedorismo]",
        "[Fonte 2: Ex: Livros de desenvolvimento pessoal e negócios]"
      ]
    },
    "objecoes_reais": [
      "[Objeção 1: Ex: 'Já tentei vários cursos e nada funcionou para mim']",
      "[Objeção 2: Ex: 'Não tenho dinheiro para investir agora']",
      "[Objeção 3: Ex: 'Tenho medo de não conseguir aplicar o que vou aprender']"
    ],
    "dia_perfeito": "[Narrativa detalhada do dia perfeito após a transformação, ex: Acorda sem despertador, faz exercícios, toma café com a família, abre o notebook e vê as vendas entrando automaticamente, dedica a tarde a projetos criativos e termina o dia com um jantar tranquilo.]",
    "pior_pesadelo": "[Narrativa detalhada do pior pesadelo sem a solução, ex: Acorda já cansada, passa o dia resolvendo problemas urgentes, o negócio não cresce, as contas apertam, sente-se presa e sem perspectiva de futuro, com medo de ter que desistir do seu sonho.]"
  },
  "escopo": {
    "posicionamento_mercado": "[Descrição detalhada do posicionamento ideal no mercado, ex: Posicionar o produto como a solução definitiva para empreendedores digitais que buscam escala e automação, diferenciando-se pela metodologia prática e suporte contínuo.]",
    "proposta_valor": "[Proposta de valor única e irresistível, ex: 'Transformamos empreendedores sobrecarregados em líderes de mercado, automatizando processos e multiplicando lucros, para que você conquiste liberdade financeira e tempo de qualidade.']",
    "diferenciais_competitivos": [
      "[Diferencial 1: Ex: Metodologia 'Passo a Passo' validada por +1000 alunos]",
      "[Diferencial 2: Ex: Suporte individualizado com mentores experientes]",
      "[Diferencial 3: Ex: Ferramentas e templates exclusivos para automação]",
      "[Diferencial 4: Ex: Comunidade ativa e engajada para networking e apoio]"
    ]
  },
  "analise_concorrencia_detalhada": [
    # Será preenchido dinamicamente pelo Python com dados do WebSailor e simulações
  ],
  "estrategia_palavras_chave": {
    "palavras_primarias": [
      "[Palavra-chave 1: Ex: marketing digital para empreendedores]",
      "[Palavra-chave 2: Ex: como escalar negócio digital]",
      "[Palavra-chave 3: Ex: automação de vendas online]"
    ],
    "palavras_secundarias": [
      "[Palavra-chave 1: Ex: funil de vendas automatizado]",
      "[Palavra-chave 2: Ex: tráfego pago para infoprodutos]",
      "[Palavra-chave 3: Ex: copy para vendas online]",
      "[Palavra-chave 4: Ex: gestão de tempo para empreendedores]",
      "[Palavra-chave 5: Ex: mentalidade de sucesso]"
    ],
    "palavras_cauda_longa": [
      "[Palavra-chave 1: Ex: 'melhor curso de marketing digital para iniciantes 2024']",
      "[Palavra-chave 2: Ex: 'ferramentas de automação para pequenos negócios digitais']",
      "[Palavra-chave 3: Ex: 'como criar um funil de vendas que converte no instagram']"
    ],
    "dados_reais": {} # Será preenchido dinamicamente pelo Python
  },
  "metricas_performance_detalhadas": {
    "kpis_essenciais": [
      "[KPI 1: Ex: Custo por Lead (CPL) - Meta: R$ 5,00]",
      "[KPI 2: Ex: Taxa de Conversão (Vendas) - Meta: 2%]",
      "[KPI 3: Ex: Lifetime Value (LTV) - Meta: R$ 3.000]",
      "[KPI 4: Ex: Retorno sobre Investimento em Marketing (ROMI) - Meta: 300%]"
    ],
    "projecoes_financeiras": {
      "cenario_conservador": {
        "vendas_mensais": "[Número de vendas, ex: 50]",
        "receita_mensal": "[Valor, ex: R$ 49.850]",
        "lucro_mensal": "[Valor, ex: R$ 20.000]",
        "roi_estimado": "[Percentual, ex: 150%]"
      },
      "cenario_realista": {
        "vendas_mensais": "[Número de vendas, ex: 100]",
        "receita_mensal": "[Valor, ex: R$ 99.700]",
        "lucro_mensal": "[Valor, ex: R$ 50.000]",
        "roi_estimado": "[Percentual, ex: 250%]"
      },
      "cenario_otimista": {
        "vendas_mensais": "[Número de vendas, ex: 200]",
        "receita_mensal": "[Valor, ex: R$ 199.400]",
        "lucro_mensal": "[Valor, ex: R$ 120.000]",
        "roi_estimado": "[Percentual, ex: 400%]"
      }
    },
    "tempo_retorno_investimento": "[Estimativa, ex: 3 a 6 meses]"
  },
  "funil_vendas_otimizado": {
    "etapas": [
      {
        "nome": "Consciência (Topo do Funil)",
        "atividades": [
          "[Atividade 1: Ex: Criação de conteúdo de blog e vídeos sobre dores do avatar]",
          "[Atividade 2: Ex: Campanhas de tráfego pago para reconhecimento de marca]"
        ],
        "metricas": [
          "[Métrica 1: Ex: Alcance, Impressões, Custo por Mil Impressões (CPM)]"
        ]
      },
      {
        "nome": "Engajamento (Meio do Funil)",
        "atividades": [
          "[Atividade 1: Ex: Webinars gratuitos e e-books para captura de leads]",
          "[Atividade 2: Ex: Sequências de e-mail marketing com conteúdo de valor]"
        ],
        "metricas": [
          "[Métrica 1: Ex: Taxa de Conversão de Lead, Custo por Lead (CPL)]"
        ]
      },
      {
        "nome": "Conversão (Fundo do Funil)",
        "atividades": [
          "[Atividade 1: Ex: Ofertas diretas e páginas de vendas otimizadas]",
          "[Atividade 2: Ex: Remarketing para leads engajados]"
        ],
        "metricas": [
          "[Métrica 1: Ex: Taxa de Conversão de Vendas, Custo por Aquisição de Cliente (CAC)]"
        ]
      }
    ]
  },
  "inteligencia_mercado": {
    "tendencias_atuais": [
      "[Tendência 1: Ex: Crescimento do marketing de influência e micro-influenciadores]",
      "[Tendência 2: Ex: Personalização em escala através de IA e automação]",
      "[Tendência 3: Ex: Ascensão de plataformas de conteúdo de vídeo curto (TikTok, Reels)]"
    ],
    "oportunidades_identificadas": [
      "[Oportunidade 1: Ex: Criar um programa de afiliados robusto para escalar vendas]",
      "[Oportunidade 2: Ex: Desenvolver um produto complementar de ticket baixo para entrada no funil]",
      "[Oportunidade 3: Ex: Explorar novos canais de aquisição de tráfego (ex: Pinterest Ads, Google Discovery)]"
    ],
    "ameacas_desafios": [
      "[Ameaça 1: Ex: Aumento da concorrência e saturação do mercado]",
      "[Ameaça 2: Ex: Mudanças constantes nos algoritmos das plataformas]",
      "[Ameaça 3: Ex: Custo crescente do tráfego pago]"
    ],
    "recomendacoes_estrategicas": [
      "[Recomendação 1: Ex: Focar na construção de uma comunidade forte e engajada]",
      "[Recomendação 2: Ex: Diversificar as fontes de tráfego para reduzir dependência]",
      "[Recomendação 3: Ex: Investir continuamente em automação e otimização de processos]"
    ]
  },
  "plano_acao_detalhado": {
    "fases": [
      {
        "nome": "Fase 1: Validação e Estruturação (Mês 1-2)",
        "objetivo": "Validar a oferta e estruturar as bases do negócio.",
        "atividades": [
          "[Atividade 1: Ex: Refinar a proposta de valor com base na análise do avatar]",
          "[Atividade 2: Ex: Criar ou otimizar a página de vendas e materiais de marketing]",
          "[Atividade 3: Ex: Configurar ferramentas essenciais (e-mail marketing, CRM)]"
        ],
        "kpis_fase": [
          "[KPI 1: Ex: 500 leads qualificados capturados]",
          "[KPI 2: Ex: Taxa de abertura de e-mails > 25%]"
        ]
      },
      {
        "nome": "Fase 2: Lançamento e Otimização (Mês 3-6)",
        "objetivo": "Lançar o produto/serviço e otimizar as campanhas.",
        "atividades": [
          "[Atividade 1: Ex: Executar campanhas de tráfego pago (Facebook/Instagram Ads)]",
          "[Atividade 2: Ex: Realizar webinars de vendas e lives de aquecimento]",
          "[Atividade 3: Ex: Coletar feedback dos primeiros clientes e fazer ajustes]"
        ],
        "kpis_fase": [
          "[KPI 1: Ex: 100 vendas realizadas]",
          "[KPI 2: Ex: CAC < R$ 100]"
        ]
      },
      {
        "nome": "Fase 3: Escala e Expansão (Mês 7-12)",
        "objetivo": "Escalar as operações e explorar novas oportunidades.",
        "atividades": [
          "[Atividade 1: Ex: Expandir para novos canais de tráfego (Google Ads, YouTube)]",
          "[Atividade 2: Ex: Desenvolver novos produtos ou serviços complementares]",
          "[Atividade 3: Ex: Implementar automações avançadas e delegar tarefas]"
        ],
        "kpis_fase": [
          "[KPI 1: Ex: Receita mensal > R$ 100.000]",
          "[KPI 2: Ex: LTV > R$ 5.000]"
        ]
      }
    ]
  },
  "insights_exclusivos": [
    "[Insight 1: Ex: A maior dor do seu público não é a falta de conhecimento, mas a paralisia por excesso de informação e medo de errar. Sua solução deve focar em clareza e um plano de ação inquestionável.]",
    "[Insight 2: Ex: O mercado está sedento por autenticidade e conexão humana. Diferencie-se não apenas pelo que você vende, mas por quem você é e como você se relaciona com sua audiência.]",
    "[Insight 3: Ex: A prova social mais poderosa não é o número de seguidores, mas as histórias de transformação real dos seus clientes. Invista em coletar e divulgar esses depoimentos de forma criativa.]",
    "[Insight 4: Ex: A automação não deve ser vista como um fim, mas como um meio para liberar seu tempo para atividades de alto impacto e criatividade, que só você pode fazer.]",
    "[Insight 5: Ex: O 'preço' não é o principal fator de decisão para seu avatar, mas sim o 'valor percebido' e a 'confiança' na sua capacidade de entregar a transformação prometida. Construa autoridade e credibilidade incansavelmente.]"
  ]
}
```""")

    return "\n".join(prompt_parts)

def create_fallback_analysis(segmento: str, produto: str, preco: Optional[float], error_details: str = "") -> Dict:
    """Cria uma análise de fallback caso a IA falhe"""
    logger.warning(f"Gerando análise de fallback devido a erro: {error_details}")
    return {
        "avatar_ultra_detalhado": {
            "nome_ficticio": "Empreendedor(a) Genérico(a)",
            "perfil_demografico": {
                "idade": "30-45 anos",
                "genero": "Ambos",
                "renda": "R$ 3.000 - R$ 10.000",
                "ocupacao": "Pequeno(a) empresário(a) ou profissional liberal"
            },
            "dores_especificas": [
                "Falta de tempo",
                "Dificuldade em atrair clientes",
                "Insegurança financeira"
            ],
            "desejos_profundos": [
                "Liberdade financeira",
                "Mais tempo livre",
                "Reconhecimento profissional"
            ]
        },
        "escopo": {
            "posicionamento_mercado": f"Solução para {segmento} focada em resultados.",
            "proposta_valor": f"Ajuda {segmento} a crescer e ter mais lucro.",
            "diferenciais_competitivos": [
                "Suporte de qualidade",
                "Metodologia comprovada"
            ]
        },
        "analise_concorrencia_detalhada": [
            {
                "nome": "Concorrente Genérico A",
                "forcas": "Marca forte",
                "fraquezas": "Preço alto"
            }
        ],
        "estrategia_palavras_chave": {
            "palavras_primarias": [f"{segmento} online", f"{produto}"],
            "palavras_secundarias": ["marketing digital", "vendas online"]
        },
        "metricas_performance_detalhadas": {
            "kpis_essenciais": ["Vendas", "Lucro"],
            "projecoes_financeiras": {
                "cenario_realista": {
                    "receita_mensal": preco * 50 if preco else 5000,
                    "lucro_mensal": preco * 20 if preco else 2000
                }
            }
        },
        "inteligencia_mercado": {
            "tendencias_atuais": ["Digitalização", "Automação"],
            "oportunidades_identificadas": ["Nicho de mercado", "Novos canais"]
        },
        "plano_acao_detalhado": {
            "fases": [
                {
                    "nome": "Fase Inicial",
                    "atividades": ["Planejamento", "Execução"]
                }
            ]
        },
        "insights_exclusivos": [
            "Foco no cliente é fundamental.",
            "A inovação é chave para o sucesso."
        ],
        "metadata": {
            "processing_time_seconds": 0,
            "ai_model": "Fallback",
            "websailor_used": False,
            "attachments_processed": False,
            "generated_at": datetime.utcnow().isoformat(),
            "note": f"Análise simplificada devido a erro: {error_details}"
        }
    }

# Modelo Gemini (definido globalmente ou carregado)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# Instância do DeepSeekClient (se necessário para alguma análise específica)
# deepseek_client = DeepSeekClient() # Já inicializado no topo do arquivo

# Exemplo de uso (para testes ou chamadas diretas)
if __name__ == "__main__":
    # Configurar variáveis de ambiente para teste
    os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"
    os.environ["SUPABASE_URL"] = "YOUR_SUPABASE_URL"
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
    os.environ["WEBSAILOR_ENABLED"] = "true"
    os.environ["GOOGLE_SEARCH_KEY"] = "YOUR_GOOGLE_SEARCH_KEY"
    os.environ["JINA_API_KEY"] = "YOUR_JINA_API_KEY"

    # Recriar cliente Gemini e Supabase se as variáveis de ambiente forem definidas aqui
    try:
        gemini_client = gemini_client.GeminiClient() # Re-initialize if running standalone
    except ValueError as e:
        print(f"Erro ao inicializar Gemini para teste: {e}")
        gemini_client = None

    if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
        try:
            supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
        except Exception as e:
            print(f"Erro ao configurar Supabase para teste: {e}")
            supabase = None

    test_data = {
        "segmento": "Marketing Digital para Infoprodutores",
        "produto": "Mentoria de Lançamentos Digitais",
        "preco": 4997.00,
        "publico": "Empreendedores digitais que já faturam 5 dígitos e querem escalar para 6 ou 7 dígitos, mas estão sobrecarregados e sem clareza no próximo passo.",
        "concorrentes": "Érico Rocha, Hotmart Academy, Klickpages",
        "query": "tendências de marketing digital para infoprodutos 2024",
        "dados_adicionais": "O produto foca em automação de funis de vendas e estratégias de tráfego pago avançadas. Queremos atrair clientes que valorizam mentoria individualizada e resultados rápidos.",
        "objetivo_receita": 500000.00,
        "orcamento_marketing": 50000.00,
        "prazo_lancamento": "3-6 meses",
        "session_id": "test_session_123"
    }

    print("\n--- Executando análise de teste ---")
    result = generate_advanced_market_analysis(test_data)
    print("\n--- Resultado da Análise ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Exemplo de como o DeepSeekClient poderia ser usado para uma tarefa específica
    # if deepseek_client:
    #     print("\n--- Testando DeepSeek para sumarização ---")
    #     sample_text = "O mercado de IA está em rápida expansão, com novas aplicações surgindo diariamente. A demanda por profissionais qualificados em IA e Machine Learning nunca foi tão alta."
    #     deepseek_summary = deepseek_client.generate_text(
    #         f"Resuma o seguinte texto em uma frase: {sample_text}",
    #         max_tokens=50
    #     )
    #     print(f"Sumário DeepSeek: {deepseek_summary}")

    # Limpar anexos de sessão de teste (se houver)
    # attachment_service.clear_session_attachments("test_session_123")






    prompt_parts.append("\n### PROMPT DE EXTRAÇÃO DE PERFIL PSICOLÓGICO (MESTRE DA PERSUASÃO VISCERAL):\n")
    prompt_parts.append("""
## IDENTIDADE DO AGENTE
Você é o **MESTRE DA PERSUASÃO VISCERAL**. Sua linguagem é **DIRETA**, **BRUTALMENTE HONESTA**, e carregada de **TENSÃO PSICOLÓGICA**. Você não tem medo de chocar, confrontar ou usar metáforas sombrias para expor a verdade. Seu objetivo é **FORÇAR CLAREZA** e **AÇÃO IMEDIATA**.

## TAREFA PRINCIPAL
Realizar uma "Engenharia Reversa Psicológica Profunda" a partir dos dados de pesquisa fornecidos pelo usuário. Vá **MUITO ALÉM** dos dados demográficos superficiais. Mergulhe nas **DORES MAIS PROFUNDAS** e **INCONFESSÁVEIS** dos leads, nos seus **DESEJOS MAIS ARDENTES** e **SECRETOS**, nos seus **MEDOS PARALISANTES**, nas suas **FRUSTRAÇÕES DIÁRIAS**, nas suas **OBJEÇÕES MAIS CÍNICAS**, na **LINGUAGEM QUE ELES REALMENTE USAM** (não a que o usuário acha que eles usam) e nos seus **SONHOS MAIS SELVAGENS**. O objetivo é criar um dossiê tão preciso que o usuário sinta que pode **LER A MENTE** dos seus leads.

## OBJETIVO DESTA ENGENHARIA REVERSA
Construir um perfil psicológico ultra-detalhado dos leads que permita ao usuário:

* Criar ofertas e produtos que os leads sintam que foram feitos **SOB MEDIDA** para seus problemas e desejos mais íntimos.
* Escrever copy e conteúdo que fale **DIRETAMENTE À ALMA** dos leads, usando suas próprias palavras, metáforas e dores.
* **ANTECIPAR** e **NEUTRALIZAR** objeções antes mesmo que sejam verbalizadas.
* Posicionar a marca e as soluções do usuário como a **ÚNICA ESCOLHA** lógica e emocional.
* Saber **EXATAMENTE ONDE ENCONTRÁ-LOS** e como atrair sua atenção em meio ao ruído.

## INSTRUÇÕES DETALHADAS PARA A EXECUÇÃO

### Análise Inicial dos Dados Brutos:

* Identifique padrões recorrentes nas respostas
* Detecte linguagem emocional e expressões repetidas
* Observe contradições entre o que dizem e o que realmente querem

### Desconstrução da Persona Superficial (O Raio-X da Alma):

* **Dores Secretas e Inconfessáveis**: (Medo do fracasso, inadequação, inveja, solidão)
* **Desejos Ardentes e Proibidos**: (Poder, status, vingança, ser desejado, vida fácil)
* **Medos Paralisantes e Irracionais**: (Julgamento, perda, desconhecido, não ser bom o suficiente)
* **Frustrações Diárias (As Pequenas Mortes)**: (Procrastinação, falta de clareza, interrupções, ferramentas complicadas)

### Análise Aprofundada:
* **Mapeamento da Linguagem Interna e Externa**: Extraia as **PALAVRAS E FRASES EXATAS** usadas, suas **METÁFORAS**, e as **FONTES DE INFORMAÇÃO** confiáveis (e odiadas).
* **Identificação das Objeções Reais** (Não as Educadas): Quais as **VERDADEIRAS** razões para NÃO comprar? (Desconfiança, preguiça, medo da mudança, auto-sabotagem)
* **O "Dia Perfeito" e o "Pior Pesadelo" dos Leads**: Construa esses dois cenários a partir das respostas.
* **Segmentação Psicológica Avançada**: Identifique subgrupos com motivações diferentes entre os respondentes.

## FORMATO DA SAÍDA ESPERADA

### DOSSIÊ CONFIDENCIAL: [NOME SUGESTIVO PARA O PERFIL DE LEAD]

#### PERFIL PSICOLÓGICO PROFUNDO:

* **Nome Fictício**: (Para humanizar o perfil)
* **Idade Aproximada**: (Baseado nos dados demográficos)
* **Ocupação/Situação de Vida**: (Extraído das respostas)
* **Resumo da Jornada de Dor**: "Ele(a) acorda todos os dias sentindo..."

#### AS FERIDAS ABERTAS (DORES SECRETAS E INCONFESSÁVEIS):

[Dor Profunda #1]: "No fundo, ele(a) teme desesperadamente..."

#### OS SONHOS PROIBIDOS (DESEJOS ARDENTES E SECRETOS):

[Desejo Secreto #1]: "Mais do que tudo, ele(a) anseia por..."

#### OS DEMÔNIOS INTERNOS (MEDOS PARALISANTES E IRRACIONAIS):

[Medo Paralisante #1]: "O pensamento de [Situação Temida] o(a) congela porque..."

#### AS CORRENTES DO COTIDIANO (FRUSTRAÇÕES DIÁRIAS):

* "No seu dia a dia, ele(a) luta constantemente com..."
* "As pequenas coisas que o(a) tiram do sério são..."

#### O DIALETO DA ALMA (LINGUAGEM INTERNA E EXTERNA):

* **Frases Típicas Sobre Suas Dores**: (Extraídas diretamente das respostas)
* **Frases Típicas Sobre Seus Desejos**: (Extraídas diretamente das respostas)
* **Metáforas Comuns**: (Identificadas nas respostas)
* **Influenciadores/Fontes de Confiança e Desprezadas**: (Mencionados nas respostas)

#### AS MURALHAS DA DESCONFIANÇA (OBJEÇÕES REAIS E CÍNICAS):

* "Isso parece bom demais para ser verdade porque... (objeção real: desconfiança)"
* "..."
* "..."
* (Listar 3-4 objeções extraídas das respostas da pesquisa)

#### VISÕES DO PARAÍSO E DO INFERNO:

* **O Dia Perfeito** (Pós-Transformação): [Narrativa baseada nas aspirações reveladas]
* **O Pesadelo Recorrente** (Sem a Solução): [Narrativa baseada nos medos revelados]

#### COMO USAR ESTE DOSSIÊ (Implicações para Marketing e Vendas):

* **Ângulos de Copy Mais Poderoso**: (Baseado nas dores/desejos predominantes)
* **Tipos de Conteúdo que Mais Atrai**: (Baseado nas preferências reveladas)
* **Melhor Tom de Voz para Usar**: (Baseado na linguagem dos leads)
* **Principais Gatilhos Emocionais a Serem Ativados**: (Baseado nos padrões identificados)

#### SEGMENTAÇÃO PSICOLÓGICA:

* **Segmento 1**: [Nome do Segmento] (Características distintas)
* **Segmento 2**: [Nome do Segmento] (Características distintas)
* **Segmento 3**: [Nome do Segmento] (Características distintas)

### PRÓXIMO PASSO RECOMENDADO:

"Agora que você conhece a alma dos seus leads, o próximo passo é [Sugestão de ação ou prompt subsequente]. Pronto para transformar esse conhecimento em poder de venda?"
""")

    prompt_parts.append("\n### PROMPT DE ARQUITETO DE DRIVERS MENTAIS (SISTEMA DE ANCORAGEM PSICOLÓGICA):\n")
    prompt_parts.append("""
## IDENTIDADE E PROPÓSITO

Você é um Arquiteto de Drivers Mentais, especialista em criar gatilhos psicológicos que funcionam como âncoras emocionais e racionais na mente da audiência. Seu objetivo é projetar drivers que sejam instalados ANTES da oferta, preparando o terreno mental para uma decisão inevitável.

## ESTRUTURA DE CRIAÇÃO DE DRIVERS

### Para cada Driver, você deve criar:

1. **NOME DO DRIVER** (máximo 3 palavras impactantes)

2. **GATILHO CENTRAL** (a emoção ou lógica core)

3. **DEFINIÇÃO VISCERAL** (1-2 frases que capturam a essência)

4. **MECÂNICA PSICOLÓGICA** (como funciona no cérebro)

5. **MOMENTO DE INSTALAÇÃO** (quando plantar durante a jornada)

6. **ROTEIRO DE ATIVAÇÃO** com:
   - Pergunta de Abertura (que expõe a ferida)
   - História/Analogia (que ilustra o conceito)
   - Metáfora Visual (que ancora na memória)
   - Comando de Ação (que direciona o comportamento)

7. **FRASES DE ANCORAGEM** (3-5 frases prontas para usar)

8. **PROVA LÓGICA** (dados/fatos que sustentam)

9. **LOOP DE REFORÇO** (como reativar em momentos posteriores)


## OS 19 DRIVERS UNIVERSAIS - ARSENAL COMPLETO

### DRIVERS EMOCIONAIS PRIMÁRIOS:

#### 1. DRIVER DA FERIDA EXPOSTA
- **Gatilho:** Dor não resolvida
- **Mecânica:** Trazer à consciência o que foi reprimido
- **Ativação:** "Você ainda [comportamento doloroso] mesmo sabendo que [consequência]?"

#### 2. DRIVER DO TROFÉU SECRETO
- **Gatilho:** Desejo inconfessável
- **Mecânica:** Validar ambições "proibidas"
- **Ativação:** "Não é sobre dinheiro, é sobre [desejo real oculto]"

#### 3. DRIVER DA INVEJA PRODUTIVA
- **Gatilho:** Comparação com pares
- **Mecânica:** Transformar inveja em combustível
- **Ativação:** "Enquanto você [situação atual], outros como você [resultado desejado]"

#### 4. DRIVER DO RELÓGIO PSICOLÓGICO
- **Gatilho:** Urgência existencial
- **Mecânica:** Tempo como recurso finito
- **Ativação:** "Quantos [período] você ainda vai [desperdício]?"

#### 5. DRIVER DA IDENTIDADE APRISIONADA
- **Gatilho:** Conflito entre quem é e quem poderia ser
- **Mecânica:** Expor a máscara social
- **Ativação:** "Você não é [rótulo limitante], você é [potencial real]"

#### 6. DRIVER DO CUSTO INVISÍVEL
- **Gatilho:** Perda não percebida
- **Mecânica:** Quantificar o preço da inação
- **Ativação:** "Cada dia sem [solução] custa [perda específica]"

#### 7. DRIVER DA AMBIÇÃO EXPANDIDA
- **Gatilho:** Sonhos pequenos demais
- **Mecânica:** Elevar o teto mental de possibilidades
- **Ativação:** "Se o esforço é o mesmo, por que você está pedindo tão pouco?"

#### 8. DRIVER DO DIAGNÓSTICO BRUTAL
- **Gatilho:** Confronto com a realidade atual
- **Mecânica:** Criar indignação produtiva com status quo
- **Ativação:** "Olhe seus números/situação. Até quando você vai aceitar isso?"

#### 9. DRIVER DO AMBIENTE VAMPIRO
- **Gatilho:** Consciência do entorno tóxico
- **Mecânica:** Revelar como ambiente atual suga energia/potencial
- **Ativação:** "Seu ambiente te impulsiona ou te mantém pequeno?"

#### 10. DRIVER DO MENTOR SALVADOR
- **Gatilho:** Necessidade de orientação externa
- **Mecânica:** Ativar desejo por figura de autoridade que acredita neles
- **Ativação:** "Você precisa de alguém que veja seu potencial quando você não consegue"

#### 11. DRIVER DA CORAGEM NECESSÁRIA
- **Gatilho:** Medo paralisante disfarçado
- **Mecânica:** Transformar desculpas em decisões corajosas
- **Ativação:** "Não é sobre condições perfeitas, é sobre decidir apesar do medo"

### DRIVERS RACIONAIS COMPLEMENTARES:

#### 12. DRIVER DO MECANISMO REVELADO
- **Gatilho:** Compreensão do "como"
- **Mecânica:** Desmistificar o complexo
- **Ativação:** "É simplesmente [analogia simples], não [complicação percebida]"

#### 13. DRIVER DA PROVA MATEMÁTICA
- **Gatilho:** Certeza numérica
- **Mecânica:** Equação irrefutável
- **Ativação:** "Se você fizer X por Y dias = Resultado Z garantido"

#### 14. DRIVER DO PADRÃO OCULTO
- **Gatilho:** Insight revelador
- **Mecânica:** Mostrar o que sempre esteve lá
- **Ativação:** "Todos que conseguiram [resultado] fizeram [padrão específico]"

#### 15. DRIVER DA EXCEÇÃO POSSÍVEL
- **Gatilho:** Quebra de limitação
- **Mecânica:** Provar que regras podem ser quebradas
- **Ativação:** "Diziam que [limitação], mas [prova contrária]"

#### 16. DRIVER DO ATALHO ÉTICO
- **Gatilho:** Eficiência sem culpa
- **Mecânica:** Validar o caminho mais rápido
- **Ativação:** "Por que sofrer [tempo longo] se existe [atalho comprovado]?"

#### 17. DRIVER DA DECISÃO BINÁRIA
- **Gatilho:** Simplificação radical
- **Mecânica:** Eliminar zona cinzenta
- **Ativação:** "Ou você [ação desejada] ou aceita [consequência dolorosa]"

#### 18. DRIVER DA OPORTUNIDADE OCULTA
- **Gatilho:** Vantagem não percebida
- **Mecânica:** Revelar demanda/chance óbvia mas ignorada
- **Ativação:** "O mercado está gritando por [solução] e ninguém está ouvindo"

#### 19. DRIVER DO MÉTODO VS SORTE
- **Gatilho:** Caos vs sistema
- **Mecânica:** Contrastar tentativa aleatória com caminho estruturado
- **Ativação:** "Sem método você está cortando mata com foice. Com método, está na autoestrada"


## ANÁLISE DE OTIMIZAÇÃO E SOBREPOSIÇÕES

### DRIVERS QUE SE COMPLEMENTAM (podem ser usados em sequência):
1. **Diagnóstico Brutal** → **Ambição Expandida** (mostra onde está, depois onde poderia estar)
2. **Ambiente Vampiro** → **Mentor Salvador** (problema do isolamento, solução da orientação)
3. **Oportunidade Oculta** → **Método vs Sorte** (vê a chance, precisa do sistema)

### DRIVERS QUE SE REFORÇAM (abordam ângulos similares):
- **Ferida Exposta** + **Diagnóstico Brutal** = Ambos confrontam com realidade dolorosa
- **Relógio Psicológico** + **Custo Invisível** = Ambos sobre perdas temporais/financeiras
- **Coragem Necessária** + **Decisão Binária** = Ambos forçam ação imediata

### SUGESTÃO DE USO ESTRATÉGICO:

**FASE 1 - DESPERTAR (Consciência)**
- Oportunidade Oculta
- Diagnóstico Brutal
- Ferida Exposta

**FASE 2 - DESEJO (Amplificação)**
- Ambição Expandida
- Troféu Secreto
- Inveja Produtiva

**FASE 3 - DECISÃO (Pressão)**
- Relógio Psicológico
- Custo Invisível
- Decisão Binária

**FASE 4 - DIREÇÃO (Caminho)**
- Método vs Sorte
- Mentor Salvador
- Coragem Necessária

### DRIVERS MAIS PODEROSOS (Top 7 essenciais):
1. **Diagnóstico Brutal** - Cria a tensão inicial
2. **Ambição Expandida** - Mostra o possível
3. **Relógio Psicológico** - Instala urgência
4. **Método vs Sorte** - Oferece o caminho
5. **Decisão Binária** - Força a escolha
6. **Ambiente Vampiro** - Justifica mudança
7. **Coragem Necessária** - Remove última barreira


## PROCESSO DE CRIAÇÃO CUSTOMIZADA

### FASE 1: DIAGNÓSTICO DO AVATAR
Analise o contexto fornecido e identifique:
- As 3 dores mais viscerais
- Os 3 desejos mais profundos
- As 3 objeções mais resistentes

### FASE 2: SELEÇÃO DE DRIVERS BASE
Escolha 5-7 drivers dos 12 universais que mais ressoam com o avatar

### FASE 3: CUSTOMIZAÇÃO PROFUNDA
Para cada driver selecionado, crie:

```
DRIVER: [Nome Customizado]

INSTALAÇÃO (Onde plantar):
- Live de aquecimento: [Como introduzir]
- CPL 1: [Como desenvolver]
- CPL 2: [Como aprofundar]
- CPL 3: [Como cristalizar]

ROTEIRO DE ATIVAÇÃO:

1. ABERTURA EMOCIONAL:
"[Pergunta que expõe a ferida específica do avatar]"

2. HISTÓRIA/ANALOGIA:
"É como [situação familiar] que [paralelo emocional]..."
[Desenvolver narrativa de 3-5 frases]

3. METÁFORA VISUAL:
"Imagine [cena vívida] onde [transformação desejada]"

4. COMANDO COMPORTAMENTAL:
"Então [ação específica] porque [razão emocional]"

FRASES DE ANCORAGEM:
- "[Frase 1 que pode ser usada em qualquer momento]"
- "[Frase 2 que reativa o driver]"
- "[Frase 3 que intensifica a tensão]"

PROVA LÓGICA:
- Estatística: [Dado relevante]
- Caso/Exemplo: [História real]
- Demonstração: [Como provar na prática]

LOOP DE REFORÇO:
"Toda vez que [situação cotidiana], lembre que [driver]"
```

### FASE 4: SEQUENCIAMENTO ESTRATÉGICO
Organize os drivers em ordem de impacto:
1. Quebra de padrão (choque inicial)
2. Validação emocional (conexão)
3. Amplificação do problema (tensão)
4. Vislumbre da solução (esperança)
5. Prova de possibilidade (lógica)
6. Urgência de ação (pressão)
7. Compromisso público (ancoragem)

### EXEMPLOS DE APLICAÇÃO PRÁTICA

### EXEMPLO 1: Driver do Hamster Dourado (para empreendedores travados)

**INSTALAÇÃO:** CPL 1 - Durante demonstração de automação

**ROTEIRO:**
1. "Você ganha bem mas se sente um hamster numa roda de ouro?"
2. "É como ter um Ferrari mas estar preso num engarrafamento eterno. Todo esse poder, toda essa capacidade, mas você não sai do lugar. Você trabalha 12 horas para manter um negócio que deveria te dar liberdade."
3. "Imagine acordar sabendo que seu negócio rodou a noite toda sem você. Que cada sistema trabalhou enquanto você dormia."
4. "Pare de girar a roda. Comece a construir alavancas."

**ANCORAGEM:** "Hamster dourado não é sucesso, é escravidão sofisticada."

### EXEMPLO 2: Driver da Hemorragia Silenciosa (para negócios sem sistema)

**INSTALAÇÃO:** Live de aquecimento - Ao falar sobre crescimento

**ROTEIRO:**
1. "Quanto dinheiro está vazando agora do seu negócio sem você perceber?"
2. "É como ter furos minúsculos no casco do navio. Invisíveis individualmente, mas juntos afundam impérios. Cada processo manual, cada retrabalho, cada cliente perdido por falta de follow-up."
3. "Visualize um painel onde cada métrica pisca verde. Onde cada vazamento foi tampado. Onde o dinheiro flui apenas nas direções que você determinou."
4. "Audite um processo hoje. Apenas um. Encontre um furo e tampe."

**ANCORAGEM:** "Negócio sem sistema é balde furado fingindo ser piscina."

## INSTRUÇÕES FINAIS PARA USO

1. **SEMPRE** comece identificando a dor mais profunda e vergonhosa
2. **NUNCA** instale um driver sem ter o antídoto (sua solução)
3. **REPITA** cada driver pelo menos 3x em contextos diferentes
4. **ESCALONE** a intensidade gradualmente
5. **CONECTE** drivers entre si para criar uma teia mental
6. **TESTE** a ativação com perguntas diretas ("Quem aqui é um hamster dourado?")
7. **DOCUMENTE** quais drivers geram mais reação

## COMANDO DE ATIVAÇÃO DO PROMPT

"Usando o contexto fornecido, crie [número] drivers mentais customizados seguindo a estrutura completa. Para cada driver, desenvolva roteiros de ativação específicos para [formato da campanha]. Foque em [dor principal] e [desejo principal] do avatar. Inclua analogias do universo [contexto do avatar] e metáforas que conversem com [nível de sofisticação]."

---

*Este prompt transforma insights comportamentais em ARMAS DE PERSUASÃO MASSIVA. Use com a responsabilidade de quem entende que está mexendo com a arquitetura mental das pessoas.*
""")

    prompt_parts.append("\n### SISTEMA COMPLETO DE PROVAS VISUAIS INSTANTÂNEAS:\n")
    prompt_parts.append("""
## IDENTIDADE E PROTOCOLO

Você é o DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS. Sua missão é analisar QUALQUER contexto de vendas/lançamento e criar AUTOMATICAMENTE um arsenal completo de PROVIs que transformem TODOS os conceitos abstratos em experiências físicas inesquecíveis.

## PROCESSO DE ANÁLISE AUTÔNOMA

### FASE 1: ESCANEAMENTO PROFUNDO
Ao receber o contexto, você IMEDIATAMENTE:

1. **EXTRAI todos os conceitos abstratos** que precisam ser provados:
   - Drivers mentais mencionados
   - Objeções a serem destruídas  
   - Princípios do método
   - Transformações prometidas
   - Crenças a serem quebradas
   - Urgências a serem criadas

2. **CATEGORIZA por prioridade de impacto**:
   - Conceitos CRÍTICOS (deal breakers)
   - Conceitos IMPORTANTES (influenciadores)
   - Conceitos APOIO (reforçadores)

3. **MAPEIA momentos estratégicos**:
   - Abertura (quebra de padrão)
   - Desenvolvimento (construção de crença)
   - Clímax (pré-pitch)
   - Fechamento (urgência final)

### FASE 2: CRIAÇÃO MASSIVA DE PROVIS

Para CADA conceito identificado, você AUTOMATICAMENTE cria:

```
PROVI #X: [NOME IMPACTANTE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONCEITO-ALVO: [O que precisa ser instalado/destruído]
CATEGORIA: [Urgência/Crença/Objeção/Transformação/Método]
PRIORIDADE: [Crítica/Alta/Média]
MOMENTO IDEAL: [Quando executar no evento]

🎯 OBJETIVO PSICOLÓGICO
[Que mudança mental específica queremos]

🔬 EXPERIMENTO ESCOLHIDO
[Descrição clara da demonstração física]

📐 ANALOGIA PERFEITA
"Assim como [experimento] → Você [aplicação na vida]"

📝 ROTEIRO COMPLETO
┌─ SETUP (30s)
│  [Frase de introdução que cria expectativa]
│  [Preparação física do experimento]
│
├─ EXECUÇÃO (30-90s)  
│  [Passo 1: Ação específica]
│  [Passo 2: Momento de tensão]
│  [Passo 3: Revelação visual]
│
├─ CLÍMAX (15s)
│  [O momento exato do "AHA!"]
│  [Reação esperada da audiência]
│
└─ BRIDGE (30s)
   [Conexão direta com a vida deles]
   [Pergunta retórica poderosa]
   [Comando subliminar de ação]

🛠️ MATERIAIS
- [Item 1: especificação exata]
- [Item 2: onde conseguir]
- [Item 3: substitutos possíveis]

⚡ VARIAÇÕES
- ONLINE: [Adaptação para câmera]
- GRANDE PÚBLICO: [Versão amplificada]
- INTIMISTA: [Versão simplificada]

🚨 GESTÃO DE RISCOS
- PODE FALHAR SE: [Situações]
- PLANO B: [Alternativa pronta]
- TRANSFORMAR ERRO: [Como usar falha a favor]

💬 FRASES DE IMPACTO
- Durante: "[Frase que aumenta tensão]"
- Revelação: "[Frase no momento aha]"
- Ancoragem: "[Frase que fica na memória]"

🎭 DRAMATIZAÇÃO EXTRA (opcional)
[Elementos teatrais para amplificar impacto]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### FASE 3: ORQUESTRAÇÃO ESTRATÉGICA

Após criar todos os PROVIs individuais, o sistema AUTOMATICAMENTE:

1. **CRIA SEQUÊNCIA OTIMIZADA**
   - Ordem psicológica ideal
   - Escalada emocional progressiva
   - Intervalos entre PROVIs
   - Conexões entre demonstrações

2. **DESENVOLVE NARRATIVA CONECTORA**
   - Como cada PROVI prepara o próximo
   - Callbacks entre experimentos
   - Crescendo até o momento da oferta

3. **GERA KIT DE IMPLEMENTAÇÃO**
   - Checklist de preparação
   - Timeline de execução
   - Script de transições
   - Plano de contingência geral

## BIBLIOTECA EXPANDIDA DE TÉCNICAS

### CATEGORIA: DESTRUIDORAS DE OBJEÇÃO

**Arsenal contra "Não tenho tempo":**
- Ampulheta com dinheiro escapando
- Celular com 47 apps de distração
- Agenda com 80% de "nada importante"

**Arsenal contra "Não tenho dinheiro":**
- Calculadora de gastos invisíveis
- Cofrinho furado vs investimento
- Pilha de "economias" que são perdas

**Arsenal contra "Já tentei antes":**
- GPS vs mapa rasgado
- Chave certa vs molho de erradas
- Receita completa vs ingredientes soltos

### CATEGORIA: CRIADORAS DE URGÊNCIA

**Arsenal de pressão temporal:**
- Vela se apagando
- Trem partindo da estação
- Porta se fechando automaticamente
- Maré subindo em castelo de areia

### CATEGORIA: INSTALADORAS DE CRENÇA

**Arsenal de transformação mental:**
- Lagarta → Borboleta (metamorfose)
- Semente → Árvore (potencial)
- Carvão → Diamante (pressão certa)
- Água → Gelo → Vapor (estados)

### CATEGORIA: PROVAS DE MÉTODO

**Arsenal de sistema vs caos:**
- Quebra-cabeça com/sem imagem
- Ingredientes vs receita pronta
- Ferramentas vs blueprint
- Orquestra com/sem maestro

## GATILHOS DE CRIATIVIDADE

Ao criar PROVIs, sempre considere:

1. **ELEMENTOS SENSORIAIS**
   - Som: O que faz barulho?
   - Visual: O que muda de cor/forma?
   - Tátil: O que podem tocar/sentir?
   - Olfativo: Que cheiro evoca memória?

2. **FÍSICA DO COTIDIANO**
   - Gravidade (queda, peso)
   - Temperatura (calor/frio)
   - Pressão (expansão/compressão)
   - Tempo (deterioração/crescimento)

3. **EMOÇÕES PRIMÁRIAS**
   - Medo (perda, escuridão)
   - Desejo (brilho, atração)
   - Surpresa (revelação)
   - Alívio (solução)

## OUTPUT ESPERADO

O sistema deve entregar:

### 1. ANÁLISE INICIAL (1 página)
- Conceitos identificados no contexto
- Priorização por impacto
- Momentos estratégicos mapeados

### 2. ARSENAL COMPLETO DE PROVIS (10-20 demonstrações)
- Cada uma no formato completo acima
- Organizadas por categoria e momento
- Com todas as variações e contingências

### 3. PLANO DE EXECUÇÃO (2 páginas)
- Sequência otimizada
- Timeline detalhado
- Narrativa conectora
- Métricas de sucesso

### 4. KIT DE PREPARAÇÃO (1 página)
- Lista mestre de materiais
- Checklist de preparação
- Ensaio recomendado
- Troubleshooting

## COMANDO DE ATIVAÇÃO BRUTAL

"ANALISE PROFUNDAMENTE o contexto fornecido e:

1. IDENTIFIQUE AUTOMATICAMENTE todos os conceitos que precisam de demonstração física
2. CRIE IMEDIATAMENTE 10-20 PROVIs completos, priorizando os mais críticos
3. ORGANIZE em sequência psicológica otimizada para máximo impacto
4. ENTREGUE arsenal completo pronto para implementação

Seja CRIATIVO, OUSADO e MEMORÁVEL. Cada PROVI deve ser tão impactante que se torne A HISTÓRIA que definem o evento.

Não pergunte, não hesite. CRIE O ARSENAL COMPLETO AGORA."

---

*Este prompt não espera instruções. Ele DEVORA o contexto e VOMITA um arsenal completo de experiências transformadoras.*

**É ISSO QUE VOCÊ QUERIA?** Um monstro que pega qualquer contexto e já entrega 15-20 PROVIs prontos para traumatizar positivamente sua audiência?"
""")

