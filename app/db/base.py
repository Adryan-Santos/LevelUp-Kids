from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 👇 Importa todos os modelos (para registrar no metadata)
from app.models import parent, kid, mission, reward, kid_mission, kid_reward  # noqa
