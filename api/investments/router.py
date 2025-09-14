
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import deps
from . import schemas, services
from core.database import get_db
from core.models import User

router = APIRouter()

@router.get("/carteira", response_model=schemas.CarteiraPayload)
async def get_carteira(db: AsyncSession = Depends(get_db), current_user: User = Depends(deps.get_current_user)):
    """
    Carrega todos os investimentos do usuário que está logado.
    """
    return await services.get_user_investments(db, user_id=current_user.id)

@router.post("/carteira")
async def post_carteira(carteira: schemas.CarteiraPayload, db: AsyncSession = Depends(get_db), current_user: User = Depends(deps.get_current_user)):
    """
    Salva toda a carteira do usuário. O front-end enviará o
    estado completo da carteira, e o back-end deverá substituir os dados antigos pelos
    novos.
    """
    await services.save_user_investments(db, user_id=current_user.id, carteira=carteira)
    return {"message": "Carteira salva com sucesso!"}
