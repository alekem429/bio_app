from .db_context import db, Genes, Deaths, DeathGenes, Factors, DeathFactors, DeathTypes


def get_death_types():
    death_types = DeathTypes.query.all()
    return death_types


def add_death_type(death_type: dict):
    _death_type = DeathTypes(name=death_type['name'])
    db.session.add(_death_type)
    db.session.commit()


def delete_death_type(id: int):
    return None
