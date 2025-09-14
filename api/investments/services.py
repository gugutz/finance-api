
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from . import schemas
from core import models

async def get_user_investments(db: AsyncSession, user_id: int) -> schemas.CarteiraPayload:
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(
            selectinload(models.User.renda_fixa),
            selectinload(models.User.acoes),
            selectinload(models.User.fiis),
            selectinload(models.User.tesouro_direto)
        )
    )
    user = result.scalars().first()

    if not user:
        return schemas.CarteiraPayload(rendaFixa=[], acoes=[], fiis=[], tesouroDireto=[])

    return schemas.CarteiraPayload(
        rendaFixa=[schemas.RendaFixaInvestment.from_orm(i) for i in user.renda_fixa],
        acoes=[schemas.AcaoInvestment.from_orm(i) for i in user.acoes],
        fiis=[schemas.FIIInvestment.from_orm(i) for i in user.fiis],
        tesouroDireto=[schemas.TesouroDiretoInvestment.from_orm(i) for i in user.tesouro_direto],
    )

async def save_user_investments(db: AsyncSession, user_id: int, carteira: schemas.CarteiraPayload):
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(
            selectinload(models.User.renda_fixa),
            selectinload(models.User.acoes),
            selectinload(models.User.fiis),
            selectinload(models.User.tesouro_direto)
        )
    )
    user = result.scalars().first()
    if not user:
        return

    # Delete old investments
    for rel in [user.renda_fixa, user.acoes, user.fiis, user.tesouro_direto]:
        for item in rel:
            await db.delete(item)

    # Add new investments
    for item in carteira.rendaFixa:
        db_item = models.RendaFixaInvestment(**item.dict(), user_id=user_id)
        db.add(db_item)

    for item in carteira.acoes:
        db_item = models.AcaoInvestment(**item.dict(), user_id=user_id)
        db.add(db_item)

    for item in carteira.fiis:
        db_item = models.FIIInvestment(**item.dict(), user_id=user_id)
        db.add(db_item)

    for item in carteira.tesouroDireto:
        db_item = models.TesouroDiretoInvestment(**item.dict(), user_id=user_id)
        db.add(db_item)

    await db.commit()
