from flask import Flask,request,abort,jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import time
auth =HTTPBasicAuth()
app =Flask(__name__)

app.config.update({
   "DEBUG": True
})

users =[
   {
       'username': 'aslam',
       'password': 'py',
       'age': 18,
       'city': 'delhi_sarita vahar',
       'bio': "hello this Aslam and learning programming"
    },
   {
       'username': 'nitin',
       'password': 'rahul',
       'age': 25,
       'city': 'delhi sarita vihar',
       'bio': "hello this is Nitin and i learning programming in navgurukul"
   },
    {
        'username': 'rahul',
        'password': 'python',
        'age': 25,
        'city': 'delhi sarita vihar',
        'bio': "hello this is Rahul and i learning programming in navgurukul"
    }

]

places =[
   {
       'username': 'aslam',
       'place': 'delhi',
       'addedOn': time.strftime("%d/%m/%Y"),
       'details': 'good place',
       'likes': 500,
       'id': 1
    },
   {
       'username': 'nitin',
       'place': 'sarita vihar',
       'addedtime': time.strftime("%d/%m/%Y"),
       'details': 'owsm place',
       'likes': 500,
       'id': 2
   },
   {
       'username': 'rahul',
       'place': 'us',
       'addedOn': time.strftime("%d/%m/%Y"),
       'details': 'this is place for incient kings',
       'likes': 300,
       'id': 3
   }

]

comments =[
   {
       'id': 1,
       'username': 'aslam',
       'text': "wow this course is owsm",
       'addedOn': time.strftime("%d/%m/%Y")
   },
   {
       'id': 3,
       'username': 'rahul',
       'text': "wow this course is owsm",
       'addedOn': time.strftime("%d/%m/%Y")
   },
   {
       'id': 2,
       'username': 'nitin',
       'text': "wow this course is owsm",
       'addedOn': time.strftime("%d/%m/%Y")
   }

]


@auth.get_password
def get_password(username):
   user =[user for user in users if username ==user['username']]
   if len(user) == 0:
       abort(400)
   return user[0]['password']



@auth.error_handler
def unauthorzed():
   return make_response(jsonify({'error': 'unauthorized access'}), 401)



@app.route('/hello/user', methods=['GET'])
@auth.login_required
def get_user_place():
   place =[place for place in places if auth.username() == place['username']]
   return jsonify({'user_place': place}), 201




@app.route('/visitor/place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_visitor_place(place_id):
   place =[place for place in places if auth.username() == place['username']]
   second_place =[second_place for second_place in place if place_id ==second_place['id']]
   return jsonify({'user_place': second_place}), 201




@app.route('/visitor/datails', methods=['GET'])
@auth.login_required
def get_visitor_details():
   user =[user for user in users if auth.username() == user['username']]
   return jsonify({'user_place': user}), 201




@app.route('/visitor/signup', methods=['POST'])
@auth.login_required
def creat_user():
   if not request.json and     not 'user' in request.json:
       abort(400)
   user={
       'username': request.json['username'],
       'password': request.json['password'],
       'age': request.json['age'],
       'city': request.json['city'],
       'bio': request.json['bio']
   }
   users.append(user)
   return jsonify({'user':users}), 201



@app.route('/visitor/addedplace', methods=['POST'])
@auth.login_required
def new_place():
   if not request.json and not 'placeName' in request.json:
       abort(400)
   place ={
       'place': request.json['place'],
       'addedOn': time.strftime("%d/%m/%Y"),
       'details': request.json['details'],
       'likes': request.json['likes'],
       'id': places[-1]['id'] +1,
       'username': auth.username()
   }
   places.append(place)
   return jsonify({'places': places}), 201



@app.route('/change_details/change/<int:details_id>', methods=['PUT'])
@auth.login_required
def update_details(details_id):
    detail = [detail for detail in places if detail['id'] == details_id]
    if len(detail) == 0:
         abort(404)
    if not request.json:
         abort(400)
    if 'details' in request.json and type(request.json['details']) is not unicode:
         abort(400)
    detail[0]['details'] = request.json.get('details', detail[0]['details'])
    return jsonify({'detail': detail[0]})



@app.route('/user/add_comment/<int:comment_id>', methods=['POST'])
@auth.login_required
def add_comment(comment_id):
   if not request.json and not 'text' in request.json:
       abort(400)
   comment =[comment for comment in comments if comment_id ==comment['id']]
   user_comment1 =[user_comment1 for user_comment1 in comment if auth.username() ==user_comment1['username']]
   user_comment ={
       'text': request.json['text'],
       'username': auth.username(),
       'addedOn': time.strftime("%d/%m/%Y")
   }
   comments.append(user_comment)
   return jsonify({'comment': comment})


if __name__ =="__main__":
   app.run()