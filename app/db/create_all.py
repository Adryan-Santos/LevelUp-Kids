from app.db.session import engine
from app.db.base import Base
from app.models import parent, kid, mission, reward, kid_mission, kid_reward

print("🔧 Criando todas as tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
