from functools import wraps
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS, cross_origin
from .errors_handling import not_found
from .auth import requires_auth, check_permissions

from database.models import  Drink
from . import routes

PERMISSON = {
    "GET_DRINKS_DETAIL": "get:drinks-detail",
    "POST_DRINKS": "post:drinks",
    "PATCH_DRINKS": "patch:drinks",
    "DELETE_DRINKS": "delete:drinks",
}

def mappingDrinks(drinks):
    result = []
    for drink in drinks:
        res = {
            "id": drink.id,
            "title": drink.title,
            "recipe": json.loads(drink.recipe),
        }
        result.append(res)
    return result

    
# GET /drinks
@routes.route("/drinks")
@cross_origin()
def get_drinks():
    try:
        result = []
        drinks = Drink.query.order_by(Drink.id.desc()).all()
        for drink in drinks:
            val = drink.short()
            result.append(val)

        return jsonify({
            'drinks': result,
            'status': 200,
            'success': True
        })
    except Exception as e:
        abort(404)

# get detail drinks - 'get:drinks-detail' permission
@routes.route("/drinks-detail")
@cross_origin()
@requires_auth(PERMISSON['GET_DRINKS_DETAIL'])
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.order_by(Drink.id.desc()).all()
        result = mappingDrinks(drinks)
        return jsonify({
            'drinks': result,
            'status': 200,
            'success': True
        })
    except Exception as e:
        abort(404)

# create new drink - 'post:drinks' permission
@routes.route("/drinks", methods=['POST'])
@cross_origin()
@requires_auth(PERMISSON["POST_DRINKS"])
def add_drink(payload):
    try:
        body = request.get_json()
        new_title = body.get("title")
        new_recipe = body.get("recipe")
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))

        drink.insert()
        result = mappingDrinks([drink])
        return jsonify({
                "success": True,
                "drinks": result
            }
        )

    except Exception as e:
        abort(422)

# update drink - 'patch:drinks' permission
@routes.route("/drinks/<int:drink_id>", methods=['PATCH'])
@cross_origin()
@requires_auth(PERMISSON["PATCH_DRINKS"])
def update_drink(payload, drink_id):
    try:
        body = request.get_json()
        new_title = body.get("title")
        new_recipe = body.get("recipe")
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drink.title = new_title
        drink.recipe = json.dumps(new_recipe)

        drink.update()
        result = mappingDrinks([drink])
        return jsonify({
                "success": True,
                "drinks": result
            }
        )

    except Exception as e:
        abort(422)

# delete drink - 'delete:drinks' permission
@routes.route("/drinks/<int:drink_id>", methods=['DELETE'])
@cross_origin()
@requires_auth(PERMISSON["DELETE_DRINKS"])
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            return not_found(404)

        drink.delete()

        return jsonify(
            {
                "success": True,
                "delete": drink_id
            }
        )
   
        
    except Exception as e:
        abort(422)


