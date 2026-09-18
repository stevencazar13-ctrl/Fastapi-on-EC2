from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional

class Auto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    placa: str
    anio: int

class Reserva(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_nombre: str
    fecha_inicio: str
    fecha_fin: str
    auto_id: Optional[int] = Field(default=None, foreign_key="auto.id")

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(title="API Autos y Reservas")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/autos/", response_model=Auto)
def crear_auto(auto: Auto, session: Session = Depends(get_session)):
    session.add(auto)
    session.commit()
    session.refresh(auto)
    return auto

@app.get("/autos/", response_model=List[Auto])
def leer_autos(session: Session = Depends(get_session)):
    return session.exec(select(Auto)).all()

@app.post("/reservas/", response_model=Reserva)
def crear_reserva(reserva: Reserva, session: Session = Depends(get_session)):
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva

@app.get("/reservas/", response_model=List[Reserva])
def leer_reservas(session: Session = Depends(get_session)):
    return session.exec(select(Reserva)).all()
#yupi####