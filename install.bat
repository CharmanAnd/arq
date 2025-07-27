@echo off
REM ARQV30 Enhanced v2.0 - Script de Instalação Windows
REM Execute este arquivo para instalar todas as dependências

echo ========================================
echo ARQV30 Enhanced v2.0 - Instalação
echo Análise Ultra-Detalhada de Mercado
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.11+ de https://python.org
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

REM Verifica versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Versão do Python: %PYTHON_VERSION%
echo.

REM Cria ambiente virtual
echo Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ERRO: Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

REM Ativa ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

REM Atualiza pip
echo Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instala dependências
echo Instalando dependências...
echo Isso pode levar alguns minutos...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependências!
    echo Verifique sua conexão com a internet e tente novamente.
    pause
    exit /b 1
)

REM Cria arquivo .env se não existir
if not exist ".env" (
    echo Criando arquivo de configuração...
    copy .env.example .env >nul 2>&1
    if not errorlevel 1 (
        echo Arquivo .env criado com sucesso!
        echo IMPORTANTE: Edite o arquivo .env e configure suas chaves de API.
    ) else (
        echo AVISO: Não foi possível criar o arquivo .env automaticamente.
        echo Por favor, copie manualmente .env.example para .env
    )
    echo.
)

REM Cria diretórios necessários
echo Criando estrutura de diretórios...
if not exist "src\uploads" mkdir src\uploads
if not exist "src\static\images" mkdir src\static\images
echo.

REM Testa a instalação
echo Testando instalação...
cd src
python -c "import flask, requests, google.generativeai; print('✓ Dependências principais OK')"
if errorlevel 1 (
    echo AVISO: Algumas dependências podem não estar funcionando corretamente.
) else (
    echo ✓ Teste de dependências passou!
)
cd ..
echo.

echo ========================================
echo INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ========================================
echo.
echo Próximos passos:
echo.
echo 1. Edite o arquivo .env e configure suas chaves de API:
echo    - GEMINI_API_KEY (obrigatório)
echo    - SUPABASE_URL e SUPABASE_ANON_KEY (obrigatório)
echo    - DEEPSEEK_API_KEY (opcional)
echo    - GOOGLE_SEARCH_KEY e JINA_API_KEY (opcional)
echo.
echo 2. Execute run.bat para iniciar a aplicação
echo.
echo 3. Acesse http://localhost:5000 no seu navegador
echo.
echo ========================================
echo.
echo Documentação completa disponível em:
echo https://github.com/seu-usuario/arqv30_enhanced
echo.
pause

