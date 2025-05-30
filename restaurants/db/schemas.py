from flask_marshmallow import Marshmallow

from restaurants.db.models import Restaurant, Review

ma = Marshmallow()

class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant
        include_relationships = True
        load_instance = True

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_relationships = True
        load_instance = True

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)