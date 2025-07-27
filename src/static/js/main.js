// ARQV30 Enhanced v2.0 - Main JavaScript

class ARQV30App {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.uploadedFiles = [];
        this.currentAnalysis = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.checkAppStatus();
        this.initializeComponents();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    setupEventListeners() {
        // Form submission
        const form = document.getElementById('analysisForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
        
        // File upload
        const fileInput = document.getElementById('fileInput');
        const uploadArea = document.getElementById('uploadArea');
        
        if (fileInput && uploadArea) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
            
            // Drag and drop
            uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
            uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
            uploadArea.addEventListener('drop', (e) => this.handleFileDrop(e));
        }
        
        // New analysis button
        const newAnalysisBtn = document.getElementById('newAnalysisBtn');
        if (newAnalysisBtn) {
            newAnalysisBtn.addEventListener('click', () => this.startNewAnalysis());
        }
        
        // Download PDF button
        const downloadPdfBtn = document.getElementById('downloadPdfBtn');
        if (downloadPdfBtn) {
            downloadPdfBtn.addEventListener('click', () => this.downloadPDF());
        }
    }
    
    async checkAppStatus() {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (!statusIndicator || !statusText) return;
        
        try {
            statusIndicator.className = 'status-indicator loading';
            statusText.textContent = 'Verificando...';
            
            const response = await fetch('/api/app_status');
            const data = await response.json();
            
            if (response.ok && data.status === 'running') {
                statusIndicator.className = 'status-indicator online';
                statusText.textContent = 'Sistema Online';
                
                // Show service status details
                this.updateServiceStatus(data.services);
            } else {
                throw new Error('Sistema indisponível');
            }
        } catch (error) {
            console.error('Erro ao verificar status:', error);
            statusIndicator.className = 'status-indicator offline';
            statusText.textContent = 'Sistema Offline';
        }
    }
    
    updateServiceStatus(services) {
        // Could be used to show detailed service status
        console.log('Services status:', services);
    }
    
    initializeComponents() {
        // Initialize any additional components
        this.initializeTooltips();
        this.initializeExpandableSections();
    }
    
    initializeTooltips() {
        // Add tooltip functionality if needed
        const tooltips = document.querySelectorAll('.tooltip');
        tooltips.forEach(tooltip => {
            // Tooltip logic here
        });
    }
    
    initializeExpandableSections() {
        const expandableSections = document.querySelectorAll('.expandable-section');
        expandableSections.forEach(section => {
            const header = section.querySelector('.expandable-header');
            if (header) {
                header.addEventListener('click', () => {
                    section.classList.toggle('expanded');
                });
            }
        });
    }
    
    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = this.collectFormData();
        if (!this.validateFormData(formData)) {
            return;
        }
        
        await this.performAnalysis(formData);
    }
    
    collectFormData() {
        const form = document.getElementById('analysisForm');
        const formData = new FormData(form);
        
        const data = {
            session_id: this.sessionId,
            segmento: formData.get('segmento'),
            produto: formData.get('produto'),
            preco: formData.get('preco') ? parseFloat(formData.get('preco')) : null,
            publico: formData.get('publico'),
            objetivo_receita: formData.get('objetivo_receita') ? parseFloat(formData.get('objetivo_receita')) : null,
            orcamento_marketing: formData.get('orcamento_marketing') ? parseFloat(formData.get('orcamento_marketing')) : null,
            prazo_lancamento: formData.get('prazo_lancamento'),
            concorrentes: formData.get('concorrentes'),
            query: formData.get('query'),
            dados_adicionais: formData.get('dados_adicionais')
        };
        
        // Remove empty values
        Object.keys(data).forEach(key => {
            if (data[key] === '' || data[key] === null) {
                delete data[key];
            }
        });
        
        return data;
    }
    
    validateFormData(data) {
        if (!data.segmento) {
            this.showError('O campo "Segmento de Mercado" é obrigatório.');
            return false;
        }
        
        return true;
    }
    
    async performAnalysis(data) {
        try {
            this.showLoading();
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erro na análise');
            }
            
            const result = await response.json();
            this.currentAnalysis = result;
            
            this.hideLoading();
            this.displayResults(result);
            
        } catch (error) {
            console.error('Erro na análise:', error);
            this.hideLoading();
            this.showError('Erro ao realizar análise: ' + error.message);
        }
    }
    
    showLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'flex';
            this.startLoadingProgress();
        }
    }
    
    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }
    
    startLoadingProgress() {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const loadingText = document.getElementById('loadingText');
        
        if (!progressFill || !progressText || !loadingText) return;
        
        const steps = [
            { progress: 10, text: 'Validando dados...' },
            { progress: 25, text: 'Processando anexos...' },
            { progress: 40, text: 'Realizando pesquisa profunda...' },
            { progress: 60, text: 'Analisando com IA...' },
            { progress: 80, text: 'Gerando insights...' },
            { progress: 95, text: 'Finalizando análise...' },
            { progress: 100, text: 'Análise concluída!' }
        ];
        
        let currentStep = 0;
        
        const updateProgress = () => {
            if (currentStep < steps.length) {
                const step = steps[currentStep];
                progressFill.style.width = step.progress + '%';
                progressText.textContent = step.progress + '%';
                loadingText.textContent = step.text;
                currentStep++;
                
                setTimeout(updateProgress, 2000);
            }
        };
        
        updateProgress();
    }
    
    displayResults(result) {
        const resultsSection = document.getElementById('resultsSection');
        const resultsContent = document.getElementById('resultsContent');
        
        if (!resultsSection || !resultsContent) return;
        
        // Clear previous results
        resultsContent.innerHTML = '';
        
        // Build results HTML
        const html = this.buildResultsHTML(result);
        resultsContent.innerHTML = html;
        
        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        // Initialize result components
        this.initializeResultComponents();
    }
    
    buildResultsHTML(result) {
        let html = '';
        
        // Avatar section
        if (result.avatar_ultra_detalhado) {
            html += this.buildAvatarSection(result.avatar_ultra_detalhado);
        }
        
        // Positioning section
        if (result.escopo) {
            html += this.buildPositioningSection(result.escopo);
        }
        
        // Competition section
        if (result.analise_concorrencia_detalhada) {
            html += this.buildCompetitionSection(result.analise_concorrencia_detalhada);
        }
        
        // Marketing section
        if (result.estrategia_palavras_chave) {
            html += this.buildMarketingSection(result.estrategia_palavras_chave);
        }
        
        // Metrics section
        if (result.metricas_performance_detalhadas) {
            html += this.buildMetricsSection(result.metricas_performance_detalhadas);
        }
        
        // Projections section
        if (result.projecoes_cenarios) {
            html += this.buildProjectionsSection(result.projecoes_cenarios);
        }
        
        // Action plan section
        if (result.plano_acao_detalhado) {
            html += this.buildActionPlanSection(result.plano_acao_detalhado);
        }
        
        // Insights section
        if (result.insights_exclusivos) {
            html += this.buildInsightsSection(result.insights_exclusivos);
        }
        
        return html;
    }
    
    buildAvatarSection(avatar) {
        let html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-user-circle"></i>
                    <h4>Avatar Ultra-Detalhado</h4>
                </div>
                <div class="result-section-content">
                    <div class="avatar-grid">
        `;
        
        // Demographic profile
        if (avatar.perfil_demografico) {
            html += `
                <div class="avatar-card">
                    <h5><i class="fas fa-chart-pie"></i> Perfil Demográfico</h5>
            `;
            
            Object.entries(avatar.perfil_demografico).forEach(([key, value]) => {
                html += `
                    <div class="avatar-item">
                        <span class="avatar-label">${this.formatLabel(key)}:</span>
                        <span class="avatar-value">${value}</span>
                    </div>
                `;
            });
            
            html += `</div>`;
        }
        
        // Psychographic profile
        if (avatar.perfil_psicografico) {
            html += `
                <div class="avatar-card">
                    <h5><i class="fas fa-brain"></i> Perfil Psicográfico</h5>
            `;
            
            Object.entries(avatar.perfil_psicografico).forEach(([key, value]) => {
                html += `
                    <div class="avatar-item">
                        <span class="avatar-label">${this.formatLabel(key)}:</span>
                        <span class="avatar-value">${value}</span>
                    </div>
                `;
            });
            
            html += `</div>`;
        }
        
        html += `</div>`;
        
        // Pain points
        if (avatar.dores_especificas && avatar.dores_especificas.length > 0) {
            html += `
                <div class="expandable-section">
                    <div class="expandable-header">
                        <div class="expandable-title">
                            <i class="fas fa-exclamation-triangle"></i>
                            Dores Específicas
                        </div>
                        <i class="fas fa-chevron-down expandable-icon"></i>
                    </div>
                    <div class="expandable-content">
                        <ul class="insight-list">
            `;
            
            avatar.dores_especificas.forEach(dor => {
                html += `
                    <li class="insight-item">
                        <i class="fas fa-minus-circle"></i>
                        <span class="insight-text">${dor}</span>
                    </li>
                `;
            });
            
            html += `
                        </ul>
                    </div>
                </div>
            `;
        }
        
        // Desires
        if (avatar.desejos_profundos && avatar.desejos_profundos.length > 0) {
            html += `
                <div class="expandable-section">
                    <div class="expandable-header">
                        <div class="expandable-title">
                            <i class="fas fa-heart"></i>
                            Desejos Profundos
                        </div>
                        <i class="fas fa-chevron-down expandable-icon"></i>
                    </div>
                    <div class="expandable-content">
                        <ul class="insight-list">
            `;
            
            avatar.desejos_profundos.forEach(desejo => {
                html += `
                    <li class="insight-item">
                        <i class="fas fa-plus-circle"></i>
                        <span class="insight-text">${desejo}</span>
                    </li>
                `;
            });
            
            html += `
                        </ul>
                    </div>
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
        
        return html;
    }
    
    buildPositioningSection(escopo) {
        return `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-bullseye"></i>
                    <h4>Escopo e Posicionamento</h4>
                </div>
                <div class="result-section-content">
                    ${escopo.posicionamento_mercado ? `
                        <div class="expandable-section expanded">
                            <div class="expandable-header">
                                <div class="expandable-title">
                                    <i class="fas fa-map-marker-alt"></i>
                                    Posicionamento no Mercado
                                </div>
                                <i class="fas fa-chevron-down expandable-icon"></i>
                            </div>
                            <div class="expandable-content">
                                <p>${escopo.posicionamento_mercado}</p>
                            </div>
                        </div>
                    ` : ''}
                    
                    ${escopo.proposta_valor ? `
                        <div class="expandable-section">
                            <div class="expandable-header">
                                <div class="expandable-title">
                                    <i class="fas fa-gem"></i>
                                    Proposta de Valor
                                </div>
                                <i class="fas fa-chevron-down expandable-icon"></i>
                            </div>
                            <div class="expandable-content">
                                <p>${escopo.proposta_valor}</p>
                            </div>
                        </div>
                    ` : ''}
                    
                    ${escopo.diferenciais_competitivos && escopo.diferenciais_competitivos.length > 0 ? `
                        <div class="expandable-section">
                            <div class="expandable-header">
                                <div class="expandable-title">
                                    <i class="fas fa-star"></i>
                                    Diferenciais Competitivos
                                </div>
                                <i class="fas fa-chevron-down expandable-icon"></i>
                            </div>
                            <div class="expandable-content">
                                <ul class="feature-list">
                                    ${escopo.diferenciais_competitivos.map(diferencial => `
                                        <li class="feature-item">
                                            <i class="fas fa-check-circle"></i>
                                            <span class="feature-text">${diferencial}</span>
                                        </li>
                                    `).join('')}
                                </ul>
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    buildInsightsSection(insights) {
        return `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-lightbulb"></i>
                    <h4>Insights Exclusivos</h4>
                </div>
                <div class="result-section-content">
                    <div class="insights-showcase">
                        ${insights.map((insight, index) => `
                            <div class="insight-card">
                                <div class="insight-number">${index + 1}</div>
                                <div class="insight-content">${insight}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }
    
    buildCompetitionSection(competition) {
        // Simplified competition section
        return `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-chess"></i>
                    <h4>Análise de Concorrência</h4>
                </div>
                <div class="result-section-content">
                    <p>Análise detalhada da concorrência disponível no relatório PDF.</p>
                </div>
            </div>
        `;
    }
    
    buildMarketingSection(marketing) {
        let html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-bullhorn"></i>
                    <h4>Estratégia de Marketing</h4>
                </div>
                <div class="result-section-content">
        `;
        
        if (marketing.palavras_primarias && marketing.palavras_primarias.length > 0) {
            html += `
                <div class="expandable-section expanded">
                    <div class="expandable-header">
                        <div class="expandable-title">
                            <i class="fas fa-key"></i>
                            Palavras-Chave Primárias
                        </div>
                        <i class="fas fa-chevron-down expandable-icon"></i>
                    </div>
                    <div class="expandable-content">
                        <div class="keyword-tags">
                            ${marketing.palavras_primarias.map(keyword => `
                                <span class="keyword-tag">${keyword}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }
        
        if (marketing.palavras_secundarias && marketing.palavras_secundarias.length > 0) {
            html += `
                <div class="expandable-section">
                    <div class="expandable-header">
                        <div class="expandable-title">
                            <i class="fas fa-tags"></i>
                            Palavras-Chave Secundárias
                        </div>
                        <i class="fas fa-chevron-down expandable-icon"></i>
                    </div>
                    <div class="expandable-content">
                        <div class="keyword-tags">
                            ${marketing.palavras_secundarias.slice(0, 10).map(keyword => `
                                <span class="keyword-tag secondary">${keyword}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
        
        return html;
    }
    
    buildMetricsSection(metrics) {
        return `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-chart-line"></i>
                    <h4>Métricas de Performance</h4>
                </div>
                <div class="result-section-content">
                    <p>Métricas detalhadas e KPIs disponíveis no relatório PDF completo.</p>
                </div>
            </div>
        `;
    }
    
    buildProjectionsSection(projections) {
        return `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-chart-bar"></i>
                    <h4>Projeções e Cenários</h4>
                </div>
                <div class="result-section-content">
                    <p>Projeções financeiras detalhadas disponíveis no relatório PDF.</p>
                </div>
            </div>
        `;
    }
    
    buildActionPlanSection(actionPlan) {
        return `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-tasks"></i>
                    <h4>Plano de Ação</h4>
                </div>
                <div class="result-section-content">
                    <p>Plano de ação detalhado com cronograma disponível no relatório PDF.</p>
                </div>
            </div>
        `;
    }
    
    initializeResultComponents() {
        // Re-initialize expandable sections for results
        this.initializeExpandableSections();
    }
    
    formatLabel(key) {
        const labels = {
            'idade': 'Idade',
            'genero': 'Gênero',
            'renda': 'Renda',
            'escolaridade': 'Escolaridade',
            'localizacao': 'Localização',
            'estado_civil': 'Estado Civil',
            'filhos': 'Filhos',
            'personalidade': 'Personalidade',
            'valores': 'Valores',
            'interesses': 'Interesses',
            'estilo_vida': 'Estilo de Vida',
            'comportamento_compra': 'Comportamento de Compra',
            'influenciadores': 'Influenciadores'
        };
        
        return labels[key] || key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    async downloadPDF() {
        if (!this.currentAnalysis) {
            this.showError('Nenhuma análise disponível para download.');
            return;
        }
        
        try {
            const response = await fetch('/api/generate_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentAnalysis)
            });
            
            if (!response.ok) {
                throw new Error('Erro ao gerar PDF');
            }
            
            // Download file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `analise_mercado_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
        } catch (error) {
            console.error('Erro ao baixar PDF:', error);
            this.showError('Erro ao gerar PDF: ' + error.message);
        }
    }
    
    startNewAnalysis() {
        // Reset form
        const form = document.getElementById('analysisForm');
        if (form) {
            form.reset();
        }
        
        // Clear uploaded files
        this.uploadedFiles = [];
        this.updateUploadedFilesList();
        
        // Hide results
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection) {
            resultsSection.style.display = 'none';
        }
        
        // Generate new session ID
        this.sessionId = this.generateSessionId();
        this.currentAnalysis = null;
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.processFiles(files);
    }
    
    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.add('dragover');
    }
    
    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.remove('dragover');
    }
    
    handleFileDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.remove('dragover');
        
        const files = Array.from(e.dataTransfer.files);
        this.processFiles(files);
    }
    
    async processFiles(files) {
        for (const file of files) {
            await this.uploadFile(file);
        }
    }
    
    async uploadFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('session_id', this.sessionId);
            
            const response = await fetch('/api/upload_attachment', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.uploadedFiles.push({
                    name: file.name,
                    size: file.size,
                    type: result.content_type,
                    id: result.attachment_id || Date.now()
                });
                
                this.updateUploadedFilesList();
                this.showSuccess(`Arquivo "${file.name}" processado com sucesso!`);
            } else {
                throw new Error(result.error || 'Erro ao processar arquivo');
            }
            
        } catch (error) {
            console.error('Erro no upload:', error);
            this.showError(`Erro ao processar "${file.name}": ${error.message}`);
        }
    }
    
    updateUploadedFilesList() {
        const container = document.getElementById('uploadedFiles');
        if (!container) return;
        
        if (this.uploadedFiles.length === 0) {
            container.innerHTML = '';
            return;
        }
        
        const html = this.uploadedFiles.map(file => `
            <div class="file-item" data-file-id="${file.id}">
                <div class="file-info">
                    <i class="fas fa-file-alt"></i>
                    <div>
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${this.formatFileSize(file.size)} • ${file.type}</div>
                    </div>
                </div>
                <button class="file-remove" onclick="app.removeFile('${file.id}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    removeFile(fileId) {
        this.uploadedFiles = this.uploadedFiles.filter(file => file.id !== fileId);
        this.updateUploadedFilesList();
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    showError(message) {
        this.showNotification(message, 'error');
    }
    
    showSuccess(message) {
        this.showNotification(message, 'success');
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Add styles if not already added
        if (!document.querySelector('#notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    padding: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    min-width: 300px;
                    z-index: 10000;
                    animation: slideInRight 0.3s ease-out;
                }
                
                .notification-error {
                    border-left: 4px solid #f56565;
                }
                
                .notification-success {
                    border-left: 4px solid #48bb78;
                }
                
                .notification-info {
                    border-left: 4px solid #4299e1;
                }
                
                .notification-content {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                
                .notification-error .notification-content i {
                    color: #f56565;
                }
                
                .notification-success .notification-content i {
                    color: #48bb78;
                }
                
                .notification-info .notification-content i {
                    color: #4299e1;
                }
                
                .notification-close {
                    background: none;
                    border: none;
                    cursor: pointer;
                    color: #a0aec0;
                    padding: 4px;
                }
                
                .notification-close:hover {
                    color: #718096;
                }
                
                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
            `;
            document.head.appendChild(styles);
        }
        
        // Add to page
        document.body.appendChild(notification);
        
        // Close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.remove();
        });
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ARQV30App();
});

