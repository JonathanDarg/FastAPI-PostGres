from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/configs", response_model=schemas.SavedConfigOut)
def save_config(config: schemas.SavedConfigCreate, db: Session = Depends(get_db)):
    result = config.a + config.b
    full_name = f"{config.first_name} {config.last_name}"

    max_order = db.query(models.SavedConfig).count()

    record = models.SavedConfig(
        config_name=config.config_name,
        a=config.a,
        b=config.b,
        result=result,
        first_name=config.first_name,
        last_name=config.last_name,
        full_name=full_name,
        order_index=max_order
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get("/configs", response_model=list[schemas.SavedConfigOut])
def get_configs(db: Session = Depends(get_db)):
    return (
        db.query(models.SavedConfig)
        .order_by(models.SavedConfig.order_index.asc())
        .all()
    )


@router.post("/configs/reorder")
def reorder_config(data: schemas.ReorderConfig, db: Session = Depends(get_db)):
    current = db.query(models.SavedConfig).filter(
        models.SavedConfig.id == data.config_id
    ).first()

    if not current:
        raise HTTPException(status_code=404, detail="Config not found")

    if data.direction == "up":
        other = (
            db.query(models.SavedConfig)
            .filter(models.SavedConfig.order_index < current.order_index)
            .order_by(models.SavedConfig.order_index.desc())
            .first()
        )
    elif data.direction == "down":
        other = (
            db.query(models.SavedConfig)
            .filter(models.SavedConfig.order_index > current.order_index)
            .order_by(models.SavedConfig.order_index.asc())
            .first()
        )
    else:
        raise HTTPException(status_code=400, detail="Direction must be up or down")

    if other:
        current.order_index, other.order_index = other.order_index, current.order_index
        db.commit()

    return {"status": "ok"}