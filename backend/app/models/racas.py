from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.infra.erros import ValidationError

STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"
# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Raca(db.Model):
    __tablename__ = "racas"
    __table_args__ = {'schema': 'public'}
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    id_especie = db.Column(UUID(as_uuid=True), ForeignKey("especies.id"), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativo")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    especie_fk = relationship("Especie", back_populates="racas")
    pets = relationship("Pet", back_populates="raca_fk")
    
    @classmethod
    def procuraPeloID(cls, id):
        raca = cls.query.filter_by(id=id).first()
        if not raca:
            raise ValidationError(
                message=f"Raça com ID '{id}' não encontrada.",
                action="Verifique o ID fornecido e tente novamente."
            )
        return raca
        
    @classmethod
    def verificaNomeUnico(cls, nome, id_especie):
        return cls.query.filter_by(nome=nome, id_especie=id_especie).first()

    @classmethod
    def criarRaca(cls, props):
        nome = props.get("nome")
        especie = props.get("id_especie")

        if not nome or not especie:
            raise ValidationError(
                message="Campos obrigatórios ausentes.",
                action="Forneça 'nome' e 'id_especie' para criar a raça."
            )
        
        nome_tratado = nome.strip()
        especie_tratada = especie.strip()

        if cls.verificaNomeUnico(nome_tratado, especie_tratada):
            raise ValidationError(
                message=f"A raça '{nome_tratado}' já está cadastrada para a espécie '{especie_tratada}'.",
                action="Utilize outro nome ou verifique os dados."
            )

        nova_raca = cls(
            nome=nome_tratado,
            id_especie=especie_tratada
        )
        
        db.session.add(nova_raca)
        db.session.commit()
        return nova_raca

    def atualizarRaca(self, props):
        nome_novo = props.get('nome', self.nome).strip()
        especie_nova = props.get('especie', self.id_especie).strip()
        
        # Verifica se a nova combinação de nome e espécie já existe em outro registro
        raca_existente = self.verificaNomeUnico(nome_novo, especie_nova)
        if raca_existente and raca_existente.id != self.id:
            raise ValidationError(
                message=f"A raça '{nome_novo}' já existe para a espécie '{especie_nova}'.",
                action="Escolha outra combinação de nome e espécie."
            )

        self.nome = nome_novo
        self.id_especie = especie_nova
        self.dthr_alt = datetime.now()
        db.session.commit()
        return self

    def ativarRaca(self):
        if self.status == STATUS_ATIVO:
            raise ValidationError(message="A raça já está ativa.", action="Nenhuma ação necessária.")
        self.status = STATUS_ATIVO
        db.session.commit()

    def inativarRaca(self):
        if self.status == STATUS_INATIVO:
            raise ValidationError(message="A raça já está inativa.", action="Nenhuma ação necessária.")
        self.status = STATUS_INATIVO
        db.session.commit()
        
    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "id_especie": self.id_especie,
            "status": self.status,
            "dthr_alt": self.dthr_alt.isoformat(),
            "dthr_ins": self.dthr_ins.isoformat()
        }

    @staticmethod
    def listaRacas():
        racas = Raca.query.all()
        return [raca.retornaDicionario() for raca in racas]

    @staticmethod
    def listaRacasPorEspecie(especieFilterId):
        racas = Raca.query.filter_by(id_especie=especieFilterId).all()
        print(racas)
        return [raca.retornaDicionario() for raca in racas]
