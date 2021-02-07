import mysql.connector
from flask import Flask
from flask_restful import Api, Resource, reqparse
import settings
import usingDatabase

app = Flask(__name__)
api = Api(app)


def choice():
    if settings.repository == 'memory':
        return 'mem'
    elif settings.repository == 'database':
        myData = mysql.connector.connect(
            host=settings.host_name,
            user=settings.user_name,
            passwd=settings.user_password,
            database=settings.database
        )
        cur = myData.cursor()
        try:
            # creating a table "users" if it is not in the selected database
            cur.execute("CREATE TABLE users(id INT, name VARCHAR(255))")
            myData.commit()
            cur.close()
            myData.close()
        except:
            print('The table is already in the database')
        return 'db'


my_data = usingDatabase.DATA()
flag = choice()  # flag to switch between repository implementations
all_users = []  # list to save user's information in computer memory


class Users(Resource):
    def post(self, id):  # method for adding information about a new user
        parser = reqparse.RequestParser()
        parser.add_argument("full_name")
        params = parser.parse_args()
        if flag == 'mem':
            for user in all_users:
                if id == user["id"]:
                    return f'User with id {id} already exists', 400
            user = {
                "id": int(id),
                "full_name": params["full_name"]
            }
            all_users.append(user)
            return user, 201
        else:
            return my_data.postDATA(id, params["full_name"])

    def get(self, id):  # method for reading user information
        if flag == 'mem':
            for user in all_users:
                if user['id'] == id:
                    return user, 200
            return 'User not found', 400
        else:
            return my_data.getDATA(id)

    def put(self, id):  # method for updating user information
        parser = reqparse.RequestParser()
        parser.add_argument("full_name")
        params = parser.parse_args()
        if flag == 'mem':
            for user in all_users:
                if id == user["id"]:
                    user["full_name"] = params["full_name"]
                    return user, 200

            user = {
                "id": int(id),
                "full_name": params["full_name"]
            }
            all_users.append(user)
            return user, 201
        else:
            return my_data.putDATA(id, params["full_name"])

    def delete(self, id):  # method for deleting user record
        if flag == 'mem':
            global all_users
            all_users = [user for user in all_users if user["id"] != id]
            return f'User with id {id} is deleted.', 201
        else:
            return my_data.deleteDATA(id)


# add resource to API, specify path and start Flask.
api.add_resource(Users, "/users", "/users/", "/users/<int:id>")
if __name__ == '__main__':
    if flag != 'db' and flag != 'mem':
        print('Error: the repository is incorrectly specified')
    else:
        app.run(debug=True)
