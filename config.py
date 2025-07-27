import os

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'FDGD851F8DGhgfhgf_fdsfewn543534_arqv30_enhanced_2024')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://albyamqjdopihijsderu.supabase.co')
    SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFsYnlhbXFqZG9waWhpanNkZXJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0MTgzMTYsImV4cCI6MjA2Njk5NDMxNn0.n0fjjyDF7LZYa6MD2ZZ5tUVjEieNDtb_rbvfjNHS_Rg')
    SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFsYnlhbXFqZG9waWhpanNkZXJ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTQxODMxNiwiZXhwIjoyMDY2OTk0MzE2fQ.muvh9Xxvb2e30d4fwiO8m2cL5x5KI5-VHO0bNd9F4hg')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres.albyamqjdopihijsderu:[9pfVX8TLcxXubcVv]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres')

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBFgs3qbxYRdJWvI9C95nVVnPVzbss7euk')
    # DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'sk-983965e3914148f488517dcfe004599c')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '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')
    HUGGINGFACE_MODEL_NAME = os.getenv('HUGGINGFACE_MODEL_NAME', 'meta-llama/Meta-Llama-3-70B')

    MAX_LLM_CALL_PER_RUN = int(os.getenv('MAX_LLM_CALL_PER_RUN', 40))
    MAX_LENGTH = int(os.getenv('MAX_LENGTH', 31744))
    PYTHON_VERSION = os.getenv('PYTHON_VERSION', '3.11.0')

    # GOOGLE_SEARCH_KEY = os.getenv('GOOGLE_SEARCH_KEY', '3d3707054f660f871ca9312d6b57cb2e847bd8ef')
    # JINA_API_KEY = os.getenv('JINA_API_KEY', 'jina_c2a8caea56f44dc09d3c76c534d77fd3Q5FjdnlZJemF3iAGs6zhnt-PDV0x')
    # WEBSAILOR_ENABLED = os.getenv('WEBSAILOR_ENABLED', 'true')


