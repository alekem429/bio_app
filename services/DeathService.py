from .db_context import db, Genes, Deaths, DeathGenes, Factors, DeathFactors, DeathTypes


def get_death_types():
    death_types = DeathTypes.query.all()
    return death_types


def get_genes():
    genes = Genes.query.all()
    return genes


def get_factors():
    factors = Factors.query.all()
    return factors


def get_genes_for_death_id(death_id):
    death_genes = DeathGenes.query.filter_by(id_death=death_id).all()
    genes = []
    for dg in death_genes:
        g = dg.genes
        g.activation = dg.activation
        genes.append(g)

    return genes


def get_factors_for_death_id(death_id):
    death_factors = DeathFactors.query.filter_by(id_death=death_id).all()

    factors = []
    for df in death_factors:
        f = df.factor
        f.activation = df.activation
        factors.append(f)

    return factors


def add_death_type(name: str):
    _death_type = DeathTypes(Name=name)
    db.session.add(_death_type)
    db.session.commit()
    return _death_type


def add_gene(name: str):
    _gene = Genes(name=name)
    db.session.add(_gene)
    db.session.commit()
    return _gene


def add_factor(name: str):
    _factor = Factors(name=name)
    db.session.add(_factor)
    db.session.commit()
    return _factor


def get_deaths_for_death_type_id(death_type_id: int):
    deaths_query = Deaths.query.filter_by(death_type_id=death_type_id)
    deaths = deaths_query.all()

    return deaths


def add_death(death: dict):
    _death = Deaths(description=death['description'], death_type_id=death['death_type_id'])
    db.session.add(_death)
    db.session.commit()
    return _death


def update_death(death: dict):
    genes = get_genes_for_death_id(death['id'])
    factors = get_factors_for_death_id(death['id'])

    for g in death['genes']:
        if len(genes[[i for i, e in enumerate(genes) if e.id == g.id][0]]) == 0:
            _dg = DeathGenes(id_death=death['id'], id_gene=g.id, activation=g.activation)
            db.session.add(_dg)
            db.session.commit()

    for f in death['factors']:
        if len(factors[[i for i, e in enumerate(factors) if e.id == f.id][0]]) == 0:
            _df = DeathFactors(id_death=death['id'], id_factor=f.id, activation=f.activation)
            db.session.add(_df)
            db.session.commit()

    return None


def delete_death(id: int):
    return None
