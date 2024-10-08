import json

from flask import jsonify

from .db_context import db, Genes, Deaths, DeathGenes, Factors, DeathFactors, DeathTypes


def get_death_types():
    death_types = DeathTypes.query.all()
    return death_types

def get_deaths():
    deaths = Deaths.query.all()
    return deaths

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
    if death_factors == None:
        return factors

    for df in death_factors:
        if df.factor is not None and df.activation is not None:
            f = df.factor
            f.activation = df.activation
            factors.append(f)

    return factors


def add_death_type(death_type: dict):
    _death_type = DeathTypes(Name = death_type['name'], description = death_type['description'])
    db.session.add(_death_type)
    db.session.commit()
    return _death_type


def add_gene(gene: dict):
    _gene = Genes(name=gene['name'])
    db.session.add(_gene)
    db.session.commit()
    return _gene


def add_factor(factor: dict):
    _factor = Factors(name=factor['name'])
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

    if 'genes' in death.keys():
        for g in death['genes']:
            dg = DeathGenes(id_death = _death.id, id_gene=g['id'], activation=g['activation'])
            db.session.add(dg)
    if 'factors' in death.keys():
        for f in death['factors']:
            df = DeathFactors(id_death = _death.id, id_factor=f['id'], activation=f['activation'])
            db.session.add(df)

    db.session.commit()

    return _death

def get_death_by_id(death_id):
    _death = Deaths.query.get(death_id)
    if not _death:
        return []

    genes = get_genes_for_death_id(death_id)
    factors = get_factors_for_death_id(death_id)

    res = {
        "id": _death.id,
        "description": _death.description,
        "death_type": {
            "id": _death.death_type_id
        },
        "genes": [{
            "id": g.id,
            "name": g.name,
            "activation": g.activation
        } for g in genes],
        "factors": [{
            "id": f.id,
            "name": f.name,
            "activation": f.activation
        } for f in factors]
    }

    return res

def update_death(death: dict):
    _death = Deaths.query.get(death['id'])
    _death.description = death['description']
    _death.death_type_id = death['death_type_id']
    db.session.commit()

    genes = get_genes_for_death_id(death['id'])
    factors = get_factors_for_death_id(death['id'])
    gene_ids = []
    factor_ids = []
    for _g in genes:
        gene_ids.append(_g.id)

    for g in death['genes']:
        if len(gene_ids) == 0 or not bool(list(filter(lambda x: x == g['id'], gene_ids))):
            _dg = DeathGenes(id_death=death['id'], id_gene=g['id'], activation=g['activation'])
            db.session.add(_dg)
            db.session.commit()

        dg = DeathGenes.query.filter_by(id_death=death['id'], id_gene=g['id']).first()
        dg.activation = g['activation']
        db.session.commit()

    for _f in factors:
        factor_ids.append(_f.id)

    for f in death['factors']:
        if len(factor_ids) == 0 or not bool(list(filter(lambda x: x == f['id'], factor_ids))):
            _df = DeathFactors(id_death=death['id'], id_factor=f['id'], activation=f['activation'])
            db.session.add(_df)
            db.session.commit()

        df = DeathFactors.query.filter_by(id_death=death['id'], id_factor=f['id']).first()
        df.activation = f['activation']
        db.session.commit()



    death_g_id = []
    for g in death['genes']:
        death_g_id.append(g['id'])

    for g_id in gene_ids:
        if len(death_g_id) == 0 or not bool(list(filter(lambda x: x == g_id, death_g_id))):
            _dg = DeathGenes.query.filter_by(id_gene=g_id, id_death=death['id']).delete()
            db.session.commit()

    death_f_id = []
    for f in death['factors']:
        death_f_id.append(f['id'])

    for f_id in factor_ids:
        if len(death_f_id) == 0 or not bool(list(filter(lambda x: x == f_id, death_f_id))):
            _dg = DeathFactors.query.filter_by(id_factor=f_id, id_death=death['id']).delete()
            db.session.commit()

    genes = get_genes_for_death_id(death['id'])
    factors = get_factors_for_death_id(death['id'])

    res = {"id": death['id'],
           "description": death['description'],
           "death_type": {
               "id": death['death_type_id']
               # "name": death['death_type']['name']
           },
           "genes": [{
               "id": g.id,
               "name": g.name,
               "activation": g.activation

           } for g in genes],

           "factors": [
               {
                   "id": f.id,
                   "name": f.name,
                   "activation": f.activation
               }
               for f in factors]
           }
    return res


def delete_death_type(id: int):
    deaths = Deaths.query.filter_by(death_type_id = id).all()

    for de in deaths:
        delete_death(de.id)

    DeathTypes.query.filter_by(id=id).delete()
    db.session.commit()
    return None


def delete_death(id: int):
    Deaths.query.filter_by(id=id).delete()
    DeathGenes.query.filter_by(id_death=id).delete()
    DeathFactors.query.filter_by(id_death=id).delete()
    db.session.commit()
    return None


def delete_gene(id: int):
    Genes.query.filter_by(id=id).delete()
    DeathGenes.query.filter_by(id_gene=id).delete()
    db.session.commit()
    return None


def delete_factor(id: int):
    Factors.query.filter_by(id=id).delete()
    DeathFactors.query.filter_by(id_factor=id).delete()
    db.session.commit()
    return None

