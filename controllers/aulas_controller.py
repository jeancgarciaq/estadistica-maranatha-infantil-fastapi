from modelos.aula import Aula
from modelos.database import get_db
from sqlalchemy.orm import Session

class ControladorAula:
    def __init__(self, vista):
        self.vista = vista

    def crear_aula(self, auxiliar, capitan, colaborador, condicion, edad, maestra, ninos, ninas, subcapitan, id_salon):
        db: Session = next(get_db())
        nueva_aula = Aula(
            auxiliar=auxiliar, capitan=capitan, colaborador=colaborador, condicion=condicion,
            edad=edad, maestra=maestra, ninos=ninos, ninas=ninas, subcapitan=subcapitan,
            id_salon=id_salon
        )
        db.add(nueva_aula)
        db.commit()
        db.refresh(nueva_aula)
        self.listar_aulas()

    def actualizar_aula(self, id, auxiliar, capitan, colaborador, condicion, edad, maestra, ninos, ninas, subcapitan, id_salon):
        db: Session = next(get_db())
        aula_actualizar = db.query(Aula).filter(Aula.id == id).first()
        if aula_actualizar:
            aula_actualizar.auxiliar = auxiliar
            aula_actualizar.capitan = capitan
            aula_actualizar.colaborador = colaborador
            aula_actualizar.condicion = condicion
            aula_actualizar.edad = edad
            aula_actualizar.maestra = maestra
            aula_actualizar.ninos = ninos
            aula_actualizar.ninas = ninas
            aula_actualizar.subcapitan = subcapitan
            aula_actualizar.id_salon = id_salon
            db.commit()
            self.listar_aulas()

    def eliminar_aula(self, id):
        db: Session = next(get_db())
        aula_eliminar = db.query(Aula).filter(Aula.id == id).first()
        if aula_eliminar:
            db.delete(aula_eliminar)
            db.commit()
            self.listar_aulas()

    def listar_aulas(self):
        db: Session = next(get_db())
        aulas = db.query(Aula).all()
        self.vista.actualizar_lista_aulas(aulas)

    def obtener_aula(self, id):
        db: Session = next(get_db())
        return db.query(Aula).filter(Aula.id == id).first()