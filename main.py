from flask import Flask
from pymongo import MongoClient
from flask import jsonify, request
from bson.json_util import dumps

app = Flask(__name__)


# Application attempts database connection and accordingly returns success or error message
try:
    client = MongoClient(host="3.80.81.163:27020")
    client.server_info()
    db = client.projectdb
    print("Successfully connected to database ", db)
    for collection_name in db.list_collection_names():
        print("Collection available: ",collection_name)

except:
    print("ERROR - could not make connection to database.")


# function add_review() adds a movie review to the database and accordingly returns success or error message
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
        respond = jsonify("ERROR - Could not add movie review.")
        respond.status_code = 400
        return respond


# Function update_review() updates a movie review in database which has the specified review_id and reviewer field values
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
        respond = jsonify("ERROR - could not update movie review.")
        respond.status_code = 400
        return respond


# Function delete_review() deletes a movie review in the database which has the specified review_id and reviewer field values
@app.route('/delete/<review_id>/<reviewer>', methods=['DELETE'])
def delete_review(review_id, reviewer):
    try:
        db.reviews.delete_one({'review_id': review_id,'reviewer':reviewer})
        respond = jsonify("Successfully deleted movie review with id ", review_id)
        respond.status_code = 200
        return respond

    except:
        respond = jsonify("ERROR - could not delete movie review.")
        respond.status_code = 400
        return respond


# Function get_ten_reviews() retrieves the first 10 documents in the database
@app.route('/', methods=['GET'])
def get_ten_reviews():
    try:
        the_reviews = db.reviews.find().limit(10)
        respond = dumps(the_reviews)
        return respond
    except:
        respond = jsonify("ERROR - could not retrieve movie reviews.")
        respond.status_code = 400
        return respond


# Function get_num_reviews() retrieves the number of distinct movies reviewed in the database
@app.route('/count', methods=['GET'])
def get_num_reviews():
    try:
        num_reviews = len(db.reviews.distinct("movie"))
        print("Number of distinct movies reviewed in database: ",num_reviews)
        respond = jsonify("Successfully retrieved number of distinct movies in database: ", num_reviews)
        respond.status_code = 200
        return respond
    except:
        respond = jsonify("ERROR - could not retrieve number of distinct movies in database.")
        respond.status_code = 400
        return respond

# Function get_ten_stars() retrieves the movie titles in the database with 10-star ratings
@app.route('/tenstars', methods=['GET'])
def get_ten_stars():
    try:
        ten_star_titles = db.reviews.find({"rating":"10"},{"movie":1}).distinct("movie")
        respond = dumps(ten_star_titles)
        return respond
    except:
        respond = jsonify("ERROR - could not retrieve 10-star movie titles from database.")
        respond.status_code = 400
        return respond

# Function get_by_reviewer() retrieves reviews created by a specific reviewer
@app.route('/reviewer/<reviewer>', methods=['GET'])
def get_by_reviewer(reviewer):

    try:
        by_reviewer = db.reviews.find({"reviewer":reviewer},{"movie":1,"reviewer":1,"review_detail":1, "_id":0})
        respond = dumps(by_reviewer)
        return respond
    except:
        respond = jsonify("ERROR - could not retrieve reviews by reviewer from database.")
        respond.status_code = 400
        return respond

# Function love_reviews() retrieves all movies in the database which contain the word "love" in the title
@app.route('/love_movies', methods=['GET'])
def love_reviews():
    try:
        love_movies = db.reviews.find({"movie":{'$regex':'.*love.*', '$options':'-i'}}, {"movie":1, "_id":0})
        respond = dumps(love_movies)
        return respond
    except:
        respond = jsonify("ERROR - could not retrieve movies with the word 'love' in the title.")
        respond.status_code = 400
        return respond

# Function spoiler_free() retrieves all spoiler-free reviews for a specified movie title
@app.route('/no_spoiler/<title>', methods=['GET'])
def spoiler_free(title):
    try:
        no_spoilers = db.reviews.find({"movie":title, "spoiler_tag":0},{"_id":0})
        respond = dumps(no_spoilers)
        return respond

    except:
        respond = jsonify("ERROR - could not retrieve spoiler-free reviews for the specified movie title.")
        respond.status_code = 400
        return respond

# Function get_genre() retrieves reviews whose review_summary contains the name of a specific genre (ie. crime)
@app.route('/genre/<genre>', methods=['GET'])
def get_genre(genre):
    try:
        genre_string = '.*'+genre+".*"
        contains_genre = db.reviews.find({"review_summary":{'$regex':genre_string, '$options':'-i'}},{"_id":0})
        respond = dumps(contains_genre)
        return respond

    except:
        respond = jsonify("ERROR - could not retrieve reviews with the requested genre.")
        respond.status_code = 400
        return respond

# Function get_actor() retrieves movie titles whose review_summary mentions the specified actor or actress
@app.route('/actor/<actor>', methods=['GET'])
def get_actor(actor):
    try:
        genre_string = '.*'+actor+".*"
        contains_actor = db.reviews.find({"review_summary":{'$regex':genre_string, '$options':'-i'}},{"_id":0, "movie":1}).distinct("movie")
        respond = dumps(contains_actor)
        return respond

    except:
        respond = jsonify("ERROR - could not retrieve movie titles with the requested actor or actress.")
        respond.status_code = 400
        return respond



if __name__ == "__main__":
    app.run(debug=True)












