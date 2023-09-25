#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    heroes = Hero.query.all()
    hero_data = [{
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name
    } for hero in heroes]
    return jsonify(hero_data)


# Define route to get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name
    } for hero in heroes]
    return jsonify(hero_data)

# Define route to get a specific hero by ID


@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        powers = [{
            'id': hero_power.power.id,
            'name': hero_power.power.name,
            'description': hero_power.power.description
        } for hero_power in hero.powers]
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': powers
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

# Define route to get all powers


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{
        'id': power.id,
        'name': power.name,
        'description': power.description
    } for power in powers]
    return jsonify(power_data)

# Define route to get a specific power by ID


@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

# Define route to update an existing power by ID


@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        try:
            data = request.get_json()
            power.description = data.get('description')
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': ['Validation errors']}), 400
    else:
        return jsonify({'error': 'Power not found'}), 404

# Define route to create a new HeroPower


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if hero and power:
            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)
            db.session.commit()

            # Fetch the related hero data to send in the response
            powers = [{
                'id': hero_power.power.id,
                'name': hero_power.power.name,
                'description': hero_power.power.description
            } for hero_power in hero.powers]

            hero_data = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                'powers': powers
            }

            return jsonify(hero_data)
        else:
            return jsonify({'errors': ['Validation errors']}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['Validation errors']}), 400


if __name__ == '__main__':
    app.run(port=5000)
