from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DeathTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), unique=True)

    deaths = db.relationship('Deaths', backref='death_types')

    def __repr__(self):
        return f'<DeathType: {self.Name}'


class Deaths(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50))

    death_type_id = db.Column(db.Integer, db.ForeignKey("death_types.id"))

    gene_chats = db.relationship('GeneDeaths', backref='deaths')
    factor_chats = db.relationship('FactorDeaths', backref='deaths')

    def __repr__(self):
        return f'<Death: {self.description}'


class Genes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    user_chats = db.relationship('GeneDeaths', backref='genes')

    def __repr__(self):
        return f'<Gene: {self.name}'


class Factors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    death_factors = db.relationship('DeathFactors', backref='factors')

    def __repr__(self):
        return f'<Factor: {self.name}'


class DeathFactors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_death = db.Column(db.Integer, db.ForeignKey("deaths.id"))
    id_factor = db.Column(db.Integer, db.ForeignKey("factors.id"))
    activation = db.Column(db.String(5))


class DeathGenes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_death = db.Column(db.Integer, db.ForeignKey("deaths.id"))
    id_gene = db.Column(db.Integer, db.ForeignKey("genes.id"))
    activation = db.Column(db.String(5))
