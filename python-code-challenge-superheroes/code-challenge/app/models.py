from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules = ('-heropowers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('HeroPower', back_populates='hero')

    def __repr__(self):
        return f'<Hero {self.name} aka {self.super_name}>'


class Power(db.Model):
    __tablename__ = 'powers'
    serialize_rules = ('-heropowers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('HeroPower', back_populates='power')

    @validates('description')
    def validate_description(self, key, value):
        # Validate description: Ensure it's not empty and length is within bounds
        if not value:
            raise ValueError("Description must not be empty")
        if not (0 < len(value) <= 200):
            raise ValueError(
                "Description must be between 1 and 200 characters")
        # Add additional validation logic as needed
        return value

    def __repr__(self):
        return f'<Power {self.name}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropowers'
    serialize_rules = ('-hero.powers', '-power.heroes',)

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(200), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey(
        'powers.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    @validates('strength')
    def validate_strength(self, key, value):
        # Validate strength: Ensure it's not empty and length is within bounds
        if not value:
            raise ValueError("Strength must not be empty")
        if not (0 < len(value) <= 200):
            raise ValueError("Strength must be between 1 and 200 characters")
        # Add additional validation logic as needed
        return value

    def __repr__(self):
        return f'<HeroPower {self.hero.name} has {self.power.name}>'
