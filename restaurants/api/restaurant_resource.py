from flasgger import swag_from
from flask_restful import Resource, reqparse, abort
from flask import request, jsonify

from restaurants.db import db
from restaurants.db.models import Restaurant
from restaurants.db.schemas import restaurant_schema


class RestaurantResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="name is required")
    parser.add_argument('address', type=str, required=False, help="Address of the restaurant")

    get_restaurant_specs_dict = {
        "tags": ["Restaurants"],
        "parameters": [
            {
                "name": "restaurant_id",
                "in": "path",
                "schema": {
                    "type": "integer",
                },
                "required": False,
            },
            {
                "name": "page",
                "in": "query",
                "schema": {
                    "type": "integer",
                },
                "required": False,
            },
            {
                "name": "per_page",
                "in": "query",
                "schema": {
                    "type": "integer",
                },
                "required": False,
            }
        ],
        "responses": {
            "200": {
                "description": "A single restaurant or a list of restaurants",
            },
            "404": {
                "description": "Restaurant Not found",
            }
        }
    }

    @swag_from(get_restaurant_specs_dict)
    def get(self, restaurant_id=None):
        if restaurant_id:
            restaurant = Restaurant.query.get_or_404(restaurant_id)
            return restaurant_schema.dump(restaurant)

        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=5, type=int)
        pagination = Restaurant.query.paginate(page=page, per_page=per_page, error_out=False)

        restaurants = pagination.items

        return jsonify({
            "data": [restaurant_schema.dump(restaurant) for restaurant in restaurants],
            "meta": {
                "page": page,
                "pages": pagination.pages,
                "per_page": per_page,
                "total": pagination.total,
                "prev": pagination.prev_num if pagination.has_prev else None,
                "next": pagination.next_num if pagination.has_next else None,
            }
        })

    def post(self):
        """Create a new restaurant. """
        args = RestaurantResource.parser.parse_args()
        new_restaurant = Restaurant(name=args['name'], address=args['address'])
        db.session.add(new_restaurant)
        db.session.commit()
        return restaurant_schema.dump(new_restaurant), 200



    def put(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)

        """Update a restaurant. """
        args = RestaurantResource.parser.parse_args()
        for key, value in args.items():
            setattr(restaurant, key, value)
        db.session.commit()
        return restaurant_schema.dump(restaurant), 200

    def delete(self, restaurant_id):
        """Delete a restaurant. """
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204
