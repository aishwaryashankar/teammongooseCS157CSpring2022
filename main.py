from flask import Flask
from pymongo import MongoClient
from flask import jsonify, request
from bson.json_util import dumps

app = Flask(__name__)

try:
    client = MongoClient(host="54.173.47.150:27020")
    client.server_info()
    db = client.projectdb
    print("Successfully connected to database ", db)
    for collection_name in db.list_collection_names():
        print("Collection available: ",collection_name)

except:
    print("ERROR - could not make connection to database")

@app.route('/create', methods=['POST'])
def add_review():
    try:
        req = request.json
        review_id = req['review_id']
        reviewer = req['reviewer']
        movie = req['movie']
        rating = req['rating']
        review_summary = req['review_summary']
        review_date = req['review_date']
        spoiler_tag = req['spoiler_tag']
        review_detail = req['review_detail']
        helpful = req['helpful']

        insert_id = db.reviews.insert_one({'review_id':review_id, 'reviewer':reviewer, 'movie':movie, 'rating':rating, 'review_summary':review_summary, 'review_date':review_date,'spoiler_tag':spoiler_tag,'review_detail':review_detail, "helpful":helpful})
        print(id)
        respond = jsonify("Successfully added movie review.")
        respond.status_code = 200
        return respond
    except:
        respond = jsonify("Error - Could not add movie review.")
        respond.status_code = 400
        return respond


@app.route('/update/<review_id>/<reviewer>', methods=['PUT'])
def update_review(review_id, reviewer):
    try:
        rev_id = review_id
        rev_person = reviewer
        req = request.json
        review_id = req['review_id']
        reviewer = req['reviewer']
        movie = req['movie']
        rating = req['rating']
        review_summary = req['review_summary']
        review_date = req['review_date']
        spoiler_tag = req['spoiler_tag']
        review_detail = req['review_detail']
        helpful = req['helpful']

        condition = {'review_id':rev_id,'reviewer':rev_person}
        updates = {"$set":{'review_id':review_id, 'reviewer':reviewer, 'movie':movie, 'rating':rating,'review_summary':review_summary, 'review_date':review_date,'spoiler_tag':spoiler_tag,'review_detail':review_detail,"helpful":helpful}}
        db.reviews.update_one(condition, updates)

        respond = jsonify("Successfully updated movie review with id ", review_id)
        respond.status_code = 200
        return respond
    except:
        respond = jsonify("Error - could not update movie review.")
        respond.status_code = 400
        return respond


@app.route('/delete/<review_id>/<reviewer>', methods=['DELETE'])
def delete_review(review_id, reviewer):
    try:
        db.reviews.delete_one({'review_id': review_id,'reviewer':reviewer})
        respond = jsonify("Successfully deleted movie review with id ", review_id)
        respond.status_code = 200
        return respond

    except:
        respond = jsonify("Error - could not delete movie review.")
        respond.status_code = 400
        return respond

@app.route('/', methods=['GET'])
def get_reviews():
    try:
        the_reviews = db.reviews.find().limit(10)
        respond = dumps(the_reviews)
        return respond
    except:
        respond = jsonify("Error - could not retrieve movie reviews")
        respond.status_code = 400
        return respond

if __name__ == "__main__":
    app.run(debug=True)












