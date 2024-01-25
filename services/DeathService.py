from .db_context import db, Genes, Deaths, DeathGenes, Factors, DeathFactors, DeathTypes

def get_deaths_for_death_type_id(death_type_id: int):
    deaths_query = Deaths.query.filter_by(death_type_id=death_type_id)
    deaths = deaths_query.all()



    return deaths


def add_death(death: dict):
    _death = Deaths(description=death['description'], death_type_id=death['death_type_id'])
    db.session.add(_death)
    db.session.commit()



def update_death(death: dict):
    return None


def delete_death(id: int):
    return None

