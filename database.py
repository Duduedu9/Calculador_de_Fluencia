from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔹 Criar conexão com o banco de dados SQLite
DATABASE_URL = "sqlite:///fluencia.db"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# 🔹 Criar modelo da tabela no banco de dados
class CalculoFluencia(Base):
    __tablename__ = "calculos_fluencia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lv = Column(Float)
    bw = Column(Float)
    h = Column(Float)
    fck = Column(Float)
    fyk = Column(Float)
    Es = Column(Float)
    qtotal = Column(Float)
    Mtd = Column(Float)
    Msd = Column(Float)
    xLN = Column(Float)
    hn = Column(Float)
    pdf_name = Column(String)

# 🔹 Criar a tabela no banco de dados
Base.metadata.create_all(engine)

# 🔹 Função para salvar cálculos no banco de dados
def salvar_calculo(lv, bw, h, fck, fyk, Es, qtotal, Mtd, Msd, xLN, hn, pdf_name):
    session = SessionLocal()
    novo_calculo = CalculoFluencia(
        lv=lv, bw=bw, h=h, fck=fck, fyk=fyk, Es=Es,
        qtotal=qtotal, Mtd=Mtd, Msd=Msd, xLN=xLN, hn=hn, pdf_name=pdf_name
    )
    session.add(novo_calculo)
    session.commit()
    session.close()
    print("✅ Cálculo salvo no banco de dados!")

# 🔹 Função para recuperar cálculos do banco de dados
def obter_calculos():
    session = SessionLocal()
    calculos = session.query(CalculoFluencia).all()
    session.close()
    return calculos

# 🔹 Função para excluir um cálculo do banco de dados
def excluir_calculo(calculo_id):
    session = SessionLocal()
    session.query(CalculoFluencia).filter_by(id=calculo_id).delete()
    session.commit()
    session.close()
    print(f"🗑️ Cálculo ID {calculo_id} excluído!")
