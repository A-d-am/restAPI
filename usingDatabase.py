import mysql.connector
import settings


class DATA:

    def postDATA(self, user_id, name):  # method for adding information about a new user
        flag = self.checkDATA(user_id)
        # if flag == true - return message, else - add information about a new user
        if flag:
            return f'User with id {user_id} already exists', 400
        else:
            myData = mysql.connector.connect(
                host=settings.host_name,
                user=settings.user_name,
                passwd=settings.user_password,
                database=settings.database
            )
            cur = myData.cursor()
            sql_formula = 'INSERT INTO users (id, full_name) VALUES (%s, %s)'
            users = (user_id, name)
            cur.execute(sql_formula, users)
            cur.close()
            myData.commit()
            myData.close()
            return self.reworkDATA(user_id, name), 201

    def getDATA(self, user_id):  # method for update information about user
        flag = self.checkDATA(user_id)
        # if flag == True - find the required ID in the table and send it to reworkDATA, else - return message
        if flag:
            myData = mysql.connector.connect(
                host=settings.host_name,
                user=settings.user_name,
                passwd=settings.user_password,
                database=settings.database
            )
            cur = myData.cursor()
            sql_formula = 'SELECT * FROM users WHERE id = ' + str(user_id)
            cur.execute(sql_formula)
            for s in cur.fetchall():
                index = s[0]
                full_name = s[1]
                cur.close()
                myData.commit()
                myData.close()
                return self.reworkDATA(index, full_name), 200
        else:
            return 'User not found', 400

    def putDATA(self, user_id, name):  # method for update information about user
        flag = self.checkDATA(user_id)
        myData = mysql.connector.connect(
            host=settings.host_name,
            user=settings.user_name,
            passwd=settings.user_password,
            database=settings.database
        )
        # if flag == True - update information, else - create new record
        if flag:
            cur = myData.cursor()
            sql_formula = 'UPDATE users SET full_name =' + name + 'WHERE id =' + str(user_id)
            cur.execute(sql_formula)
            cur.close()
            myData.commit()
            myData.close()
            return self.reworkDATA(user_id, name), 200
        else:
            cur = myData.cursor()
            sql_formula = 'INSERT INTO users (id, full_name) VALUES (%s, %s)'
            users = (user_id, name)
            cur.execute(sql_formula, users)
            cur.close()
            myData.commit()
            myData.close()
            return self.reworkDATA(user_id, name), 201

    def checkDATA(self, user_id):
        # Checking a table for a record with this id
        myData = mysql.connector.connect(
            host=settings.host_name,
            user=settings.user_name,
            passwd=settings.user_password,
            database=settings.database
        )
        cur = myData.cursor()
        sql_formula = 'SELECT * FROM users WHERE id= ' + str(user_id)
        cur.execute(sql_formula)
        for s in cur.fetchall():
            check = s
            if check is None:
                return False  # return False if there is no such record
            else:
                return True  # return True if there is record with this id

    def deleteDATA(self, user_id):
        # delete information about user with id == user_id
        myData = mysql.connector.connect(
            host=settings.host_name,
            user=settings.user_name,
            passwd=settings.user_password,
            database=settings.database
        )
        cur = myData.cursor()
        sql_formula = 'DELETE FROM users WHERE id = ' + str(user_id)
        cur.execute(sql_formula)
        cur.close()
        myData.commit()
        myData.close()
        return f'User with id {user_id} is deleted.', 201

    def reworkDATA(self, user_id, name):  # create json
        user_json = {
            "id": user_id,
            "full_name": name
        }
        return user_json
