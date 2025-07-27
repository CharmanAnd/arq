@echo off
REM ARQV30 Enhanced v2.0 ULTRA-ROBUSTO - Script de Execução Windows
REM Execute este arquivo para iniciar a aplicação

echo ========================================
echo ARQV30 Enhanced v2.0 ULTRA-ROBUSTO
echo Análise Ultra-Detalhada de Mercado
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo Por favor, instale Python 3.11+ de https://python.org
    pause
    exit /b 1
)

REM Verifica se está no diretório correto
if not exist "src\run.py" (
    echo ❌ ERRO: Arquivo run.py não encontrado!
    echo Certifique-se de estar no diretório correto do projeto.
    pause
    exit /b 1
)

REM Ativa ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo 🔄 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ AVISO: Ambiente virtual não encontrado.
    echo Recomendamos executar install.bat primeiro.
    echo.
)

REM Verifica se arquivo .env existe
if not exist ".env" (
    echo ⚠️ AVISO: Arquivo .env não encontrado!
    echo Copie o arquivo .env.example para .env e configure suas chaves de API.
    echo.
)

REM Navega para o diretório src
cd src

REM Inicia a aplicação
echo 🚀 Iniciando ARQV30 Enhanced v2.0 ULTRA-ROBUSTO...
echo.
echo Acesse: http://localhost:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

REM Verifica se todas as dependências estão instaladas
python -c "import flask, requests, google.generativeai" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ AVISO: Algumas dependências podem estar faltando. Execute install.bat
)

python run.py

REM Volta para o diretório raiz
cd ..

echo.
echo ========================================
echo ✅ Aplicação ULTRA-ROBUSTA encerrada.
echo ========================================
pause

