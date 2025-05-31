from flask import Flask, Blueprint, jsonify
from flask_restful import Api

from restaurants.api.restaurant_resource import RestaurantResource
from restaurants.api.review_resource import ReviewResource
from restaurants.db import init_db, init_ma
from flasgger import Swagger


app = Flask(__name__)
# api = Api(app)

app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///restaurant.db" )
db = init_db(app)
ma = init_ma(app)

swagger = Swagger(app)

v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v1 = Api(v1_bp)

v2_bp = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api_v2 = Api(v2_bp)

app.register_blueprint(v1_bp)
app.register_blueprint(v2_bp)


api_v1.add_resource(RestaurantResource, "/restaurants", "/restaurants/<int:restaurant_id>")
api_v1.add_resource(ReviewResource, "/restaurants/<int:restaurant_id>/reviews", "/restaurants/<int:restaurant_id>/reviews/<int:review_id>")

@app.route('/')
def hello_world():  # put application's code here
    return {"hello": "Hello World"}

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'error': 'NotFound',
        'message': 'Not found',
    }), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'error': 'InternalServerError',
        'message': 'An Unexpected error occurred',
    })

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        'error': 'InternalServerError',
        'message': 'An Unexpected error occurred',
    }), 500


if __name__ == '__main__':
    app.run(debug=True)
