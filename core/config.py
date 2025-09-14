import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    """
    Configurações da aplicação, lidas a partir de variáveis de ambiente.
    """
    # Ambiente da aplicação (dev, prod, test)
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")

    # Configurações do banco de dados de produção (Supabase)
    PROD_DB_USER: str = os.getenv("PROD_DB_USER")
    PROD_DB_PASSWORD: str = os.getenv("PROD_DB_PASSWORD")
    PROD_DB_HOST: str = os.getenv("PROD_DB_HOST")
    PROD_DB_PORT: str = os.getenv("PROD_DB_PORT")
    PROD_DB_NAME: str = os.getenv("PROD_DB_NAME")

    # URL de conexão do banco de dados
    DATABASE_URL: str | None = None

    def __init__(self, **values):
        super().__init__(**values)
        if self.ENVIRONMENT == "prod":
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.PROD_DB_USER}:{self.PROD_DB_PASSWORD}@"
                f"{self.PROD_DB_HOST}:{self.PROD_DB_PORT}/{self.PROD_DB_NAME}?sslmode=disable"
            )
        else:
            # Mantém o banco de dados local para desenvolvimento
            self.DATABASE_URL = "postgresql+asyncpg://finance_user:finance_password@localhost/finance_db"

# Instância única das configurações
settings = Settings()