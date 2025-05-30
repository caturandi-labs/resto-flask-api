from flask_restful import Resource, reqparse

from restaurants.api.data_store import restaurants
from restaurants.db import db
from restaurants.db.models import Review, Restaurant
from restaurants.db.schemas import review_schema, reviews_schema, ReviewSchema


class ReviewResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rating', type=float, required=True, help='Rating is required (1-5)')
    parser.add_argument('comment', type=str, required=False)

    def get(self, restaurant_id, review_id=None):
        if review_id:
            review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
            return review_schema.dump(review), 200

        all_restaurant_reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()
        return reviews_schema.dump(all_restaurant_reviews), 200

    def post(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        args = ReviewSchema.parser.parse_args()
        new_review  = Review(**args)
        db.session.add(new_review)
        db.session.commit()

        return review_schema.dump(new_review), 201

    def put(self, restaurant_id, review_id):
        review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
        args = ReviewSchema.parser.parse_args()
        review.rating = args['rating']
        review.comment = args['comment']
        db.session.commit()
        return review_schema.dump(review), 200


    def delete(self, restaurant_id, review_id):
       review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
       db.session.delete(review)
       db.session.commit()

       return "", 204

