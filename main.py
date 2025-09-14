
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.users import router as users_router
from api.tickers import router as tickers_router # Import the new ticker router
from core.database import Base, engine
from core.config import settings # Import settings

# --- App Initialization ---
app = FastAPI(
    title="Finance API",
    description="API para obter dados financeiros e gerenciar investimentos.",
    version="2.0.0",
)

# --- CORS Configuration ---
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Table Creation ---
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    # Diagnostic print
    print(f"[DIAGNOSTIC] Running in ENVIRONMENT: '{settings.ENVIRONMENT}'")
    print(f"[DIAGNOSTIC] DB USER: '{settings.PROD_DB_USER}'")
    print(f"[DIAGNOSTIC] DB HOST: '{settings.PROD_DB_HOST}'")
    print(f"[DIAGNOSTIC] DB PORT: '{settings.PROD_DB_PORT}'")
    print(f"[DIAGNOSTIC] DB NAME: '{settings.PROD_DB_NAME}'")
    print(f"[DIAGNOSTIC] DB URL: '{settings.DATABASE_URL}'")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- API Routers ---
app.include_router(users_router.router, prefix="/api")
app.include_router(tickers_router.router) # Include the tickers router


# --- Server Execution ---
if __name__ == "__main__":
    print("Para executar a API, rode o comando no terminal:")
    print("uvicorn main:app --reload")
