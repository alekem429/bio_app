from extensions import db
from flask_sqlalchemy import SQLAlchemy
import json
# db = SQLAlchemy()
class DeathTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(1000))
    deaths = db.relationship('Deaths', backref='death_types')

    def __repr__(self):
        return f'<DeathType: {self.Name}'


class Deaths(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50))

    death_type_id = db.Column(db.Integer, db.ForeignKey("death_types.id"))
    # death_type = db.relationship('DeathTypes', backref='deaths')

    gene_deaths = db.relationship('DeathGenes', backref='death')
    death_factors = db.relationship('DeathFactors', backref='death')

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'Description': self.description,
        })


class Genes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    gene_deaths = db.relationship('DeathGenes', backref='genes')

    def __repr__(self):
        return f'<Gene: {self.name}'


class Factors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    death_factors = db.relationship('DeathFactors', backref='factor')

    def __repr__(self):
        return f'<Factor: {self.name}'


class DeathFactors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_death = db.Column(db.Integer, db.ForeignKey("deaths.id"))
    id_factor = db.Column(db.Integer, db.ForeignKey("factors.id"))
    activation = db.Column(db.String(5))
    # factor = db.relationship('Factors', backref='death_factors')
    # death = db.relationship('Deaths', backref='death_factors')


class DeathGenes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_death = db.Column(db.Integer, db.ForeignKey("deaths.id"))
    id_gene = db.Column(db.Integer, db.ForeignKey("genes.id"))
    activation = db.Column(db.String(5))
    # genes = db.relationship('Genes', backref='gene_deaths')
    # death = db.relationship('Deaths', backref='gene_deaths')
