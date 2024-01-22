from .db_context import db, Genes, Deaths, DeathGenes, Factors, DeathFactors, DeathTypes
import dto_models

def get_deaths_for_death_type_id(death_type_id: int):
    deaths = Deaths.query.filter_by(death_type_id=death_type_id)
    death_dtos = []
    for death in deaths:
        death_dto = dto_models.DeathDto(id=death['id'], description=death['description'], factors=[], genes=[])

        death_factors = DeathFactors.query.filter_by(id_death = death.id).all()
        death_genes = DeathGenes.query.filter_by(id_death = death.id).all()

        death_dto['factors'] = death_factors
        death_dto['genes'] = death_genes
        death_dtos.append(death_dto)

    return death_dtos


def add_death(death: dict):
    _death = Deaths(description=death['description'], death_type_id=death['death_type_id'])
    db.session.add(_death)
    db.session.commit()



def update_death(death: dict):
    return None


def delete_death(id: int):
    return None

