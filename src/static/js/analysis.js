// ARQV30 Enhanced v2.0 - Análise JavaScript Aprimorado
// Sistema de feedback em tempo real e exibição de resultados ultra-detalhados

class AnalysisManager {
    constructor() {
        this.isAnalyzing = false;
        this.currentStep = 0;
        this.totalSteps = 8; // Aumentado para mais etapas
        this.analysisStartTime = null;
        this.progressInterval = null;
        this.setupEventListeners();
    }

    setupEventListeners() {
        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.startAnalysis());
        }
    }

    async startAnalysis() {
        if (this.isAnalyzing) return;

        // Validação do formulário
        if (!this.validateForm()) {
            this.showError('Por favor, preencha pelo menos o segmento de mercado.');
            return;
        }

        this.isAnalyzing = true;
        this.analysisStartTime = Date.now();
        this.currentStep = 0;

        // Mostra área de progresso
        this.showProgressArea();
        
        // Inicia animação de progresso
        this.startProgressAnimation();

        try {
            // Coleta dados do formulário
            const formData = this.collectFormData();
            
            // Envia requisição para análise
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`Erro na análise: ${response.status}`);
            }

            const result = await response.json();
            
            // Finaliza progresso
            this.completeProgress();
            
            // Exibe resultados
            setTimeout(() => {
                this.displayResults(result);
            }, 1000);

        } catch (error) {
            console.error('Erro na análise:', error);
            this.showError(`Erro na análise: ${error.message}`);
        } finally {
            this.isAnalyzing = false;
            this.stopProgressAnimation();
        }
    }

    validateForm() {
        const segmento = document.getElementById('segmento')?.value?.trim();
        return segmento && segmento.length > 0;
    }

    collectFormData() {
        return {
            segmento: document.getElementById('segmento')?.value?.trim() || '',
            produto: document.getElementById('produto')?.value?.trim() || '',
            preco: document.getElementById('preco')?.value || '',
            publico: document.getElementById('publico')?.value?.trim() || '',
            concorrentes: document.getElementById('concorrentes')?.value?.trim() || '',
            query: document.getElementById('query')?.value?.trim() || '',
            dados_adicionais: document.getElementById('dados_adicionais')?.value?.trim() || '',
            objetivo_receita: document.getElementById('objetivo_receita')?.value || '',
            orcamento_marketing: document.getElementById('orcamento_marketing')?.value || '',
            prazo_lancamento: document.getElementById('prazo_lancamento')?.value || '',
            session_id: this.getSessionId()
        };
    }

    getSessionId() {
        let sessionId = localStorage.getItem('arqv30_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('arqv30_session_id', sessionId);
        }
        return sessionId;
    }

    showProgressArea() {
        const progressArea = document.getElementById('progressArea');
        if (progressArea) {
            progressArea.style.display = 'block';
            progressArea.scrollIntoView({ behavior: 'smooth' });
        }

        // Esconde resultados anteriores
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.style.display = 'none';
        }
    }

    startProgressAnimation() {
        const steps = [
            { text: '🔍 Coletando dados do formulário...', duration: 2000 },
            { text: '📊 Processando anexos inteligentes...', duration: 3000 },
            { text: '🌐 Realizando pesquisa profunda na web...', duration: 8000 },
            { text: '🧠 Analisando com Inteligência Artificial...', duration: 12000 },
            { text: '🎯 Criando avatar ultra-detalhado...', duration: 5000 },
            { text: '⚔️ Mapeando concorrência e oportunidades...', duration: 4000 },
            { text: '📈 Calculando métricas e projeções...', duration: 3000 },
            { text: '✨ Finalizando insights exclusivos...', duration: 2000 }
        ];

        let currentStepIndex = 0;
        
        const updateStep = () => {
            if (currentStepIndex < steps.length && this.isAnalyzing) {
                const step = steps[currentStepIndex];
                this.updateProgressStep(currentStepIndex + 1, step.text);
                
                setTimeout(() => {
                    currentStepIndex++;
                    updateStep();
                }, step.duration);
            }
        };

        updateStep();
    }

    updateProgressStep(step, text) {
        this.currentStep = step;
        
        // Atualiza barra de progresso
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            const percentage = (step / this.totalSteps) * 100;
            progressBar.style.width = `${percentage}%`;
        }

        // Atualiza texto do passo
        const stepText = document.getElementById('currentStep');
        if (stepText) {
            stepText.textContent = text;
        }

        // Atualiza contador
        const stepCounter = document.getElementById('stepCounter');
        if (stepCounter) {
            stepCounter.textContent = `${step}/${this.totalSteps}`;
        }

        // Atualiza tempo estimado
        this.updateEstimatedTime();
    }

    updateEstimatedTime() {
        if (!this.analysisStartTime) return;

        const elapsed = Date.now() - this.analysisStartTime;
        const estimatedTotal = (elapsed / this.currentStep) * this.totalSteps;
        const remaining = Math.max(0, estimatedTotal - elapsed);

        const timeElement = document.getElementById('estimatedTime');
        if (timeElement) {
            const minutes = Math.floor(remaining / 60000);
            const seconds = Math.floor((remaining % 60000) / 1000);
            timeElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    completeProgress() {
        this.updateProgressStep(this.totalSteps, '🎉 Análise concluída! Preparando resultados...');
        
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = '100%';
            progressBar.classList.add('progress-complete');
        }
    }

    stopProgressAnimation() {
        this.progressInterval = null;
    }

    displayResults(result) {
        console.log('Resultado da análise:', result);

        // Mostra área de resultados
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.style.display = 'block';
            resultsArea.scrollIntoView({ behavior: 'smooth' });
        }

        // Esconde área de progresso
        const progressArea = document.getElementById('progressArea');
        if (progressArea) {
            progressArea.style.display = 'none';
        }

        // Exibe seções dos resultados
        this.displayAvatarSection(result.avatar_ultra_detalhado);
        this.displayDriversSection(result.drivers_mentais_customizados);
        this.displayCompetitionSection(result.analise_concorrencia_profunda);
        this.displayPositioningSection(result.estrategia_posicionamento);
        this.displayKeywordsSection(result.estrategia_palavras_chave);
        this.displayMetricsSection(result.metricas_performance);
        this.displayFunnelSection(result.funil_vendas_detalhado);
        this.displayActionPlanSection(result.plano_acao_90_dias);
        this.displayInsightsSection(result.insights_exclusivos);
        this.displayMetadataSection(result.metadata);

        // Habilita botão de download PDF
        this.enablePdfDownload(result);
    }

    displayAvatarSection(avatar) {
        if (!avatar) return;

        const container = document.getElementById('avatarResults');
        if (!container) return;

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">🎯 Avatar Ultra-Detalhado</h3>
                <div class="avatar-card">
                    <div class="avatar-header">
                        <h4>${avatar.nome_ficticio || 'Avatar Personalizado'}</h4>
                    </div>
                    
                    <div class="avatar-content">
                        <div class="avatar-demographic">
                            <h5>📊 Perfil Demográfico</h5>
                            ${this.renderObjectAsCards(avatar.perfil_demografico)}
                        </div>
                        
                        <div class="avatar-psychographic">
                            <h5>🧠 Perfil Psicográfico</h5>
                            ${this.renderObjectAsCards(avatar.perfil_psicografico)}
                        </div>
                        
                        <div class="avatar-pains">
                            <h5>💔 Dores Viscerais</h5>
                            ${this.renderObjectAsCards(avatar.dores_viscerais)}
                        </div>
                        
                        <div class="avatar-desires">
                            <h5>✨ Desejos Secretos</h5>
                            ${this.renderObjectAsCards(avatar.desejos_secretos)}
                        </div>
                        
                        <div class="avatar-language">
                            <h5>💬 Linguagem Interna</h5>
                            ${this.renderObjectAsCards(avatar.linguagem_interna)}
                        </div>
                        
                        <div class="avatar-objections">
                            <h5>🚫 Objeções Reais</h5>
                            ${this.renderObjectAsCards(avatar.objecoes_reais)}
                        </div>
                        
                        <div class="avatar-journey">
                            <h5>🌟 Jornada Emocional</h5>
                            ${this.renderObjectAsCards(avatar.jornada_emocional)}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    displayDriversSection(drivers) {
        if (!drivers || !Array.isArray(drivers)) return;

        const container = document.getElementById('driversResults');
        if (!container) return;

        const driversHtml = drivers.map(driver => `
            <div class="driver-card">
                <h4>${driver.nome || 'Driver Mental'}</h4>
                <div class="driver-content">
                    <p><strong>Gatilho Central:</strong> ${driver.gatilho_central || 'N/A'}</p>
                    <p><strong>Definição:</strong> ${driver.definicao_visceral || 'N/A'}</p>
                    <p><strong>Roteiro de Ativação:</strong> ${driver.roteiro_ativacao || 'N/A'}</p>
                    <p><strong>Momento Ideal:</strong> ${driver.momento_ideal || 'N/A'}</p>
                    ${driver.frases_ancoragem ? `
                        <div class="anchor-phrases">
                            <strong>Frases de Ancoragem:</strong>
                            <ul>
                                ${driver.frases_ancoragem.map(frase => `<li>"${frase}"</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">🧠 Drivers Mentais Customizados</h3>
                <div class="drivers-grid">
                    ${driversHtml}
                </div>
            </div>
        `;
    }

    displayCompetitionSection(competition) {
        if (!competition || !Array.isArray(competition)) return;

        const container = document.getElementById('competitionResults');
        if (!container) return;

        const competitionHtml = competition.map(comp => `
            <div class="competitor-card">
                <h4>${comp.nome || 'Concorrente'}</h4>
                <div class="competitor-content">
                    ${comp.analise_swot ? `
                        <div class="swot-analysis">
                            <div class="swot-item">
                                <strong>💪 Forças:</strong>
                                <ul>${comp.analise_swot.forcas?.map(f => `<li>${f}</li>`).join('') || '<li>Não informado</li>'}</ul>
                            </div>
                            <div class="swot-item">
                                <strong>⚠️ Fraquezas:</strong>
                                <ul>${comp.analise_swot.fraquezas?.map(f => `<li>${f}</li>`).join('') || '<li>Não informado</li>'}</ul>
                            </div>
                            <div class="swot-item">
                                <strong>🎯 Oportunidades:</strong>
                                <ul>${comp.analise_swot.oportunidades?.map(o => `<li>${o}</li>`).join('') || '<li>Não informado</li>'}</ul>
                            </div>
                            <div class="swot-item">
                                <strong>🚨 Ameaças:</strong>
                                <ul>${comp.analise_swot.ameacas?.map(a => `<li>${a}</li>`).join('') || '<li>Não informado</li>'}</ul>
                            </div>
                        </div>
                    ` : `
                        <p><strong>Forças:</strong> ${comp.forcas || 'Não informado'}</p>
                        <p><strong>Fraquezas:</strong> ${comp.fraquezas || 'Não informado'}</p>
                    `}
                    <p><strong>Estratégia de Marketing:</strong> ${comp.estrategia_marketing || 'Não informado'}</p>
                    <p><strong>Posicionamento:</strong> ${comp.posicionamento || 'Não informado'}</p>
                    ${comp.vulnerabilidades ? `
                        <div class="vulnerabilities">
                            <strong>Vulnerabilidades Exploráveis:</strong>
                            <ul>${comp.vulnerabilidades.map(v => `<li>${v}</li>`).join('')}</ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">⚔️ Análise de Concorrência Profunda</h3>
                <div class="competition-grid">
                    ${competitionHtml}
                </div>
            </div>
        `;
    }

    displayPositioningSection(positioning) {
        if (!positioning) return;

        const container = document.getElementById('positioningResults');
        if (!container) return;

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">🎯 Estratégia de Posicionamento</h3>
                <div class="positioning-content">
                    <div class="positioning-card">
                        <h4>💎 Proposta de Valor Única</h4>
                        <p>${positioning.proposta_valor_unica || 'Não informado'}</p>
                    </div>
                    
                    <div class="positioning-card">
                        <h4>📍 Posicionamento no Mercado</h4>
                        <p>${positioning.posicionamento_mercado || 'Não informado'}</p>
                    </div>
                    
                    <div class="positioning-card">
                        <h4>🏆 Diferenciais Competitivos</h4>
                        ${positioning.diferenciais_competitivos ? `
                            <ul>
                                ${positioning.diferenciais_competitivos.map(d => `<li>${d}</li>`).join('')}
                            </ul>
                        ` : '<p>Não informado</p>'}
                    </div>
                    
                    <div class="positioning-card">
                        <h4>📢 Mensagem Central</h4>
                        <p>${positioning.mensagem_central || 'Não informado'}</p>
                    </div>
                    
                    <div class="positioning-card">
                        <h4>🎵 Tom de Comunicação</h4>
                        <p>${positioning.tom_comunicacao || 'Não informado'}</p>
                    </div>
                </div>
            </div>
        `;
    }

    displayKeywordsSection(keywords) {
        if (!keywords) return;

        const container = document.getElementById('keywordsResults');
        if (!container) return;

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">🔍 Estratégia de Palavras-Chave</h3>
                <div class="keywords-content">
                    <div class="keywords-group">
                        <h4>🎯 Palavras Primárias</h4>
                        <div class="keywords-list">
                            ${keywords.palavras_primarias?.map(kw => `<span class="keyword primary">${kw}</span>`).join('') || '<p>Não informado</p>'}
                        </div>
                    </div>
                    
                    <div class="keywords-group">
                        <h4>📊 Palavras Secundárias</h4>
                        <div class="keywords-list">
                            ${keywords.palavras_secundarias?.map(kw => `<span class="keyword secondary">${kw}</span>`).join('') || '<p>Não informado</p>'}
                        </div>
                    </div>
                    
                    <div class="keywords-group">
                        <h4>🎣 Palavras Cauda Longa</h4>
                        <div class="keywords-list">
                            ${keywords.palavras_cauda_longa?.map(kw => `<span class="keyword long-tail">${kw}</span>`).join('') || '<p>Não informado</p>'}
                        </div>
                    </div>
                    
                    ${keywords.estrategia_conteudo ? `
                        <div class="keywords-strategy">
                            <h4>📝 Estratégia de Conteúdo</h4>
                            <p>${keywords.estrategia_conteudo}</p>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    displayMetricsSection(metrics) {
        if (!metrics) return;

        const container = document.getElementById('metricsResults');
        if (!container) return;

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">📈 Métricas de Performance</h3>
                <div class="metrics-content">
                    ${metrics.kpis_primarios ? `
                        <div class="kpis-section">
                            <h4>🎯 KPIs Primários</h4>
                            <div class="kpis-grid">
                                ${metrics.kpis_primarios.map(kpi => `<div class="kpi-card">${kpi}</div>`).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${metrics.projecoes_financeiras ? `
                        <div class="projections-section">
                            <h4>💰 Projeções Financeiras</h4>
                            <div class="projections-grid">
                                ${this.renderFinancialProjections(metrics.projecoes_financeiras)}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${metrics.metas_especificas ? `
                        <div class="goals-section">
                            <h4>🎯 Metas Específicas</h4>
                            <div class="goals-grid">
                                ${this.renderObjectAsCards(metrics.metas_especificas)}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    displayFunnelSection(funnel) {
        if (!funnel) return;

        const container = document.getElementById('funnelResults');
        if (!container) return;

        const funnelStages = ['topo_funil', 'meio_funil', 'fundo_funil'];
        const stageNames = {
            'topo_funil': '🔝 Topo do Funil',
            'meio_funil': '🎯 Meio do Funil',
            'fundo_funil': '💰 Fundo do Funil'
        };

        const funnelHtml = funnelStages.map(stage => {
            const stageData = funnel[stage];
            if (!stageData) return '';

            return `
                <div class="funnel-stage">
                    <h4>${stageNames[stage]}</h4>
                    <div class="stage-content">
                        <p><strong>Objetivo:</strong> ${stageData.objetivo || 'Não informado'}</p>
                        
                        ${stageData.estrategias ? `
                            <div class="strategies">
                                <strong>Estratégias:</strong>
                                <ul>${stageData.estrategias.map(e => `<li>${e}</li>`).join('')}</ul>
                            </div>
                        ` : ''}
                        
                        ${stageData.conteudos ? `
                            <div class="contents">
                                <strong>Conteúdos:</strong>
                                <ul>${stageData.conteudos.map(c => `<li>${c}</li>`).join('')}</ul>
                            </div>
                        ` : ''}
                        
                        ${stageData.metricas ? `
                            <div class="metrics">
                                <strong>Métricas:</strong>
                                <ul>${stageData.metricas.map(m => `<li>${m}</li>`).join('')}</ul>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">🎯 Funil de Vendas Detalhado</h3>
                <div class="funnel-content">
                    ${funnelHtml}
                </div>
            </div>
        `;
    }

    displayActionPlanSection(actionPlan) {
        if (!actionPlan) return;

        const container = document.getElementById('actionPlanResults');
        if (!container) return;

        const phases = ['primeiros_30_dias', 'dias_31_60', 'dias_61_90'];
        const phaseNames = {
            'primeiros_30_dias': '📅 Primeiros 30 Dias',
            'dias_31_60': '📅 Dias 31-60',
            'dias_61_90': '📅 Dias 61-90'
        };

        const phasesHtml = phases.map(phase => {
            const phaseData = actionPlan[phase];
            if (!phaseData) return '';

            return `
                <div class="action-phase">
                    <h4>${phaseNames[phase]}</h4>
                    <div class="phase-content">
                        <p><strong>Foco:</strong> ${phaseData.foco || 'Não informado'}</p>
                        <p><strong>Investimento:</strong> ${phaseData.investimento || 'Não informado'}</p>
                        
                        ${phaseData.atividades ? `
                            <div class="activities">
                                <strong>Atividades:</strong>
                                <ul>${phaseData.atividades.map(a => `<li>${a}</li>`).join('')}</ul>
                            </div>
                        ` : ''}
                        
                        ${phaseData.entregas ? `
                            <div class="deliverables">
                                <strong>Entregas:</strong>
                                <ul>${phaseData.entregas.map(e => `<li>${e}</li>`).join('')}</ul>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">📋 Plano de Ação 90 Dias</h3>
                <div class="action-plan-content">
                    ${phasesHtml}
                </div>
            </div>
        `;
    }

    displayInsightsSection(insights) {
        if (!insights || !Array.isArray(insights)) return;

        const container = document.getElementById('insightsResults');
        if (!container) return;

        const insightsHtml = insights.map((insight, index) => `
            <div class="insight-card">
                <div class="insight-number">${index + 1}</div>
                <div class="insight-content">${insight}</div>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="result-section">
                <h3 class="section-title">✨ Insights Exclusivos</h3>
                <div class="insights-content">
                    ${insightsHtml}
                </div>
            </div>
        `;
    }

    displayMetadataSection(metadata) {
        if (!metadata) return;

        const container = document.getElementById('metadataResults');
        if (!container) return;

        const processingTime = metadata.processing_time_seconds ? 
            `${Math.floor(metadata.processing_time_seconds / 60)}:${(metadata.processing_time_seconds % 60).toFixed(0).padStart(2, '0')}` : 
            'N/A';

        container.innerHTML = `
            <div class="result-section metadata-section">
                <h3 class="section-title">📊 Informações da Análise</h3>
                <div class="metadata-content">
                    <div class="metadata-item">
                        <span class="metadata-label">⏱️ Tempo de Processamento:</span>
                        <span class="metadata-value">${processingTime}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">🤖 Motor de Análise:</span>
                        <span class="metadata-value">${metadata.analysis_engine || 'N/A'}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">📈 Score de Qualidade:</span>
                        <span class="metadata-value">${metadata.quality_score || 'N/A'}%</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">🌐 Fontes de Dados:</span>
                        <span class="metadata-value">${metadata.data_sources_used || 0}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">🧠 IAs Utilizadas:</span>
                        <span class="metadata-value">${metadata.ai_models_used || 1}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">📅 Gerado em:</span>
                        <span class="metadata-value">${new Date(metadata.generated_at).toLocaleString('pt-BR')}</span>
                    </div>
                </div>
            </div>
        `;
    }

    renderObjectAsCards(obj) {
        if (!obj || typeof obj !== 'object') return '<p>Não informado</p>';

        return Object.entries(obj).map(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            if (Array.isArray(value)) {
                return `
                    <div class="info-card">
                        <strong>${label}:</strong>
                        <ul>${value.map(item => `<li>${item}</li>`).join('')}</ul>
                    </div>
                `;
            } else {
                return `
                    <div class="info-card">
                        <strong>${label}:</strong>
                        <span>${value}</span>
                    </div>
                `;
            }
        }).join('');
    }

    renderFinancialProjections(projections) {
        const scenarios = ['cenario_conservador', 'cenario_realista', 'cenario_otimista'];
        const scenarioNames = {
            'cenario_conservador': '🛡️ Conservador',
            'cenario_realista': '🎯 Realista',
            'cenario_otimista': '🚀 Otimista'
        };

        return scenarios.map(scenario => {
            const data = projections[scenario];
            if (!data) return '';

            return `
                <div class="projection-card">
                    <h5>${scenarioNames[scenario]}</h5>
                    <div class="projection-data">
                        <div class="projection-item">
                            <span class="label">Vendas Mensais:</span>
                            <span class="value">${data.vendas_mensais || 'N/A'}</span>
                        </div>
                        <div class="projection-item">
                            <span class="label">Receita Mensal:</span>
                            <span class="value">${data.receita_mensal || 'N/A'}</span>
                        </div>
                        <div class="projection-item">
                            <span class="label">Lucro Mensal:</span>
                            <span class="value">${data.lucro_mensal || 'N/A'}</span>
                        </div>
                        <div class="projection-item">
                            <span class="label">ROI:</span>
                            <span class="value">${data.roi || 'N/A'}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    enablePdfDownload(result) {
        const downloadBtn = document.getElementById('downloadPdfBtn');
        if (downloadBtn) {
            downloadBtn.style.display = 'inline-block';
            downloadBtn.onclick = () => this.downloadPdf(result);
        }
    }

    async downloadPdf(result) {
        try {
            const response = await fetch('/generate-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(result)
            });

            if (!response.ok) {
                throw new Error('Erro ao gerar PDF');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analise-mercado-${Date.now()}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            console.error('Erro no download do PDF:', error);
            this.showError('Erro ao gerar PDF. Tente novamente.');
        }
    }

    showError(message) {
        // Remove alertas anteriores
        const existingAlert = document.querySelector('.alert-error');
        if (existingAlert) {
            existingAlert.remove();
        }

        // Cria novo alerta
        const alert = document.createElement('div');
        alert.className = 'alert alert-error';
        alert.innerHTML = `
            <span class="alert-icon">⚠️</span>
            <span class="alert-message">${message}</span>
            <button class="alert-close" onclick="this.parentElement.remove()">×</button>
        `;

        // Insere no topo da página
        document.body.insertBefore(alert, document.body.firstChild);

        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 5000);
    }
}

// Inicializa o gerenciador quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
    window.analysisManager = new AnalysisManager();
});

