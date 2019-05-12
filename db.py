import mysql.connector
import user, json

def parse_credentials():
    file = open("credentials.dat", 'r')
    credentials = file.read().split(',')
    return credentials

def connect_db():
    credentials = parse_credentials()
    host = credentials[0]
    db = credentials[1]
    username = credentials[2]
    password = credentials[3]
    mydb = mysql.connector.connect(user=username, password=password,
                                   host=host, database=db,
                                   auth_plugin='mysql_native_password')
    return mydb
def register(username,password):
    SQL = "INSERT INTO user (USERNAME, PASSWORD) VALUES ('" + \
        username + "',SHA('" + password + "'))"
    run_query(SQL)

def check_available(username):
    SQL = "SELECT uid from user where USERNAME='" + username + "'"
    result = run_query(SQL)
    return (len(result) == 0)

def login(username,password, ip):
    sql1 = "SELECT UID FROM user WHERE USERNAME='" + \
        username + "' AND PASSWORD=SHA('" + password + "')"
    response = run_query(sql1)
    if(len(response) > 0):
        sql2 = "UPDATE user SET STATUS=true, IP='" + ip + "' WHERE UID='" + \
            str(response[0][0]) + "'"
        run_query(sql2)
        return response[0][0]
    else:
        return 0
def logout(uid):
    sql = "UPDATE user SET STATUS=false WHERE UID='" + str(uid) + "'"
    run_query(sql)

def get_online_list():
    sql = "SELECT * FROM USER WHERE STATUS=true"
    response = run_query(sql)
    list = []
    for row in response:
        u = user.user(row[0],row[1],None,row[3],row[4])
        list.append(u)
    return list
def get_user_ip(username):
    sql = "SELECT ip FROM user where username='" + username + "'"
    result = run_query(sql)
    return result[0][0]

def set_message(f, t, m):
    sql = "INSERT INTO MESSAGE (fusername, tusername, message) VALUES('" + f + "','" + t + "','" + m + "')"
    run_query(sql)

def get_message(f,t):
    sql1 = "SELECT * from message Where fusername='" + f + "' and tusername='" + t + "'"
    result1 = run_query(sql1)
    sql2 = "SELECT * from message where fusername='" + t + "' and tusername='" + f + "'"
    result2 = run_query(sql2)
    result = result1 + result2
    print(result)
    return result


def run_query(sql):
    response = ""
    try:
        mydb = connect_db()
        cursor = mydb.cursor()
        cursor.execute(sql)
        try:
            response = cursor.fetchall()
        except mysql.connector.Error:
            pass
        mydb.commit()
        return response
    except mysql.connector.Error as e:
        print("Exception:" + str(e))
        return str(e)


get_message("onur", "onur3")
