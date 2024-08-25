from typing import List

from flask import Blueprint, request
from services import DeathService as ds

main = Blueprint("controller", __name__)


@main.route("/")
def hello_word():
    return "hello_word"


@main.route("/get_list_of_death_types", methods=['GET'])
def get_death_types():
    res: List[ds.DeathTypes] = ds.get_death_types()
    return [
        {
            "id": r.id,
            "name": r.Name,
            "description": r.description
        }
        for r in res
    ]

@main.route("/get_death_for_death_type_id", methods=['GET'])
def get_deaths():
    id_death_type = int(request.args.get('id_death_type'))
    dt = ds.get_death_types()
    deaths: List[ds.Deaths] = ds.get_deaths_for_death_type_id(id_death_type)

    res = []

    for d in deaths:
        genes = ds.get_genes_for_death_id(d.id)
        factors = ds.get_factors_for_death_id(d.id)

        buf = {"id": d.id,
               "description": d.description,
               "death_type": {
                   "id": d.death_type_id,
                   "name": dt[[i for i, e in enumerate(dt) if e.id == d.death_type_id][0]].Name
               },
               "genes": [{
                   "id": g.id,
                   "name": g.name,
                   "activation": g.activation

               }for g in genes],

               "factors": [
                   {
                       "id": f.id,
                       "name": f.name,
                       "activation": f.activation
                   }
                   for f in factors]
               }
        res.append(buf)

    return res


@main.route("/get_list_of_genes", methods=['GET'])
def get_genes():
    genes: List[ds.Genes] = ds.get_genes()
    return [
        {
            "id": g.id,
            "name": g.name,
        }
        for g in genes
    ]

@main.route("/get_list_of_factors", methods=['GET'])
def get_factors():
    factors: List[ds.Factors] = ds.get_factors()
    return [
        {
            "id": f.id,
            "name": f.name,
        }
        for f in factors
    ]

@main.route("/add_death_type", methods=['Post'])
def add_death_type():
    data = request.json
    dt = ds.add_death_type(data)
    return {
            "id": dt.id,
            "name": dt.Name,
            "description": dt.description
        }


@main.route("/add_death", methods=['Post'])
def add_death():
    data = request.json
    dt = ds.add_death(data)
    return {
            "id": dt.id,
            "death_type_id": dt.death_type_id,
            "description": dt.description
        }

@main.route("/add_gene", methods=['Post'])
def add_gene():
    data = request.json
    dt = ds.add_gene(data)
    return {
            "id": dt.id,
            "name": dt.name
        }

@main.route("/add_factor", methods=['Post'])
def add_factor():
    data = request.json
    dt = ds.add_factor(data)
    return {
            "id": dt.id,
            "name": dt.name
        }


@main.route("/update_death", methods=['Post'])
def update_death():
    data = request.json
    dt = ds.update_death(data)
    return dt


@main.route("/remove_death_type", methods=['GET'])
def remove_death_type():
    print(request.args)
    death_type_id = int(request.args.get('id_death_type'))
    ds.delete_death_type(death_type_id)
    return "hello_word"


@main.route("/remove_death", methods=['GET'])
def remove_death():
    death_id = request.args.get('id_death')
    ds.delete_death(int(death_id))
    return "hello_word"


@main.route("/remove_gene", methods=['GET'])
def remove_gene():
    gene_id = int(request.args.get('id_gene'))
    ds.delete_gene(gene_id)
    return "hello_word"

@main.route("/remove_factors", methods=['GET'])
def remove_attribute():
    factor_id = int(request.args.get('id_factor'))
    ds.delete_factor(factor_id)
    return "hello_word"



@main.route("/remove_multiple_deaths", methods=['GET'])
def remove_multiple_deaths():
    query = request.args.getlist('id_death')
    for q in query:
        ds.delete_death(int(q))

    return "hello_word"


@main.route("/remove_multiple_genes", methods=['GET'])
def remove_multiple_genes():
    query = request.args.getlist('id_gene')
    for q in query:
        ds.delete_gene(int(q))

    return "hello_word"


@main.route("/remove_multiple_factors", methods=['GET'])
def remove_multiple_factors():
    query = request.args.getlist('id_factor')
    for q in query:
        ds.delete_factor(int(q))

    return "hello_word"

@main.route("/remove_multiple_death_types", methods=['GET'])
def remove_multiple_death_types():
    query = request.args.getlist('id_death_type')

    for q in query:
        ds.delete_death_type(int(q))

    return "hello_word"