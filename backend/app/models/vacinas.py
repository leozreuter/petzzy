from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infra.erros import ValidationError
from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .pets import Pet
from .usuarios import Usuario

class Vacina(db.Model):
    __tablename__ = "vacinas"
    __table_args__ = {'schema': 'public'}
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nome_vacina = db.Column(db.String(100), nullable=False)
    data_aplicacao = db.Column(Date, nullable=False)
    data_proxima_dose = db.Column(Date)
    lote = db.Column(db.String(50))
    id_pet = db.Column(UUID(as_uuid=True), ForeignKey("public.pets.id"), nullable=False)
    id_veterinario = db.Column(UUID(as_uuid=True), ForeignKey("public.usuarios.id"), nullable=False)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)

    veterinario_fk  = relationship("Usuario", back_populates="vacinas")
    pet_fk          = relationship("Pet", back_populates="vacinas")

    @classmethod
    def procuraPeloID(cls, id):
        vacina = cls.query.filter_by(id=id).first()
        if not vacina:
            raise ValidationError(message=f"Registro de vacina com ID '{id}' não encontrado.")
        return vacina

    @classmethod
    def criarVacina(cls, props):
        id_pet = props.get("id_pet")
        id_veterinario = props.get("id_veterinario")
        
        if not all([id_pet, id_veterinario, props.get("nome_vacina"), props.get("data_aplicacao")]):
            raise ValidationError(message="Campos obrigatórios ausentes para registrar a vacina.")

        Pet.procuraPeloID(id_pet)
        Usuario.procuraPeloID(id_veterinario)

        nova_vacina = cls(
            id_pet=id_pet,
            id_veterinario=id_veterinario,
            nome_vacina=props.get("nome_vacina").strip(),
            data_aplicacao=props.get("data_aplicacao"),
            data_proxima_dose=props.get("data_proxima_dose"),
            lote=props.get("lote")
        )
        db.session.add(nova_vacina)
        db.session.commit()
        return nova_vacina

    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "id_pet": str(self.id_pet),
            "id_veterinario": str(self.id_veterinario),
            "nome_vacina": self.nome_vacina,
            "data_aplicacao": self.data_aplicacao.isoformat() if self.data_aplicacao else None,
            "data_proxima_dose": self.data_proxima_dose.isoformat() if self.data_proxima_dose else None,
            "lote": self.lote
        }

    @staticmethod
    def listaVacinas():
        vacinas = Vacina.query.all()
        return [v.retornaDicionario() for v in vacinas]