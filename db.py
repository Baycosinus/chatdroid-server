import mysql.connector
import user

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
    sql2 = "UPDATE user SET STATUS=true, IP='" + ip + "' WHERE UID='" + \
        str(response[0][0]) + "'"
    run_query(sql2)

    if(len(response) > 0):
        return True;
    else:
        return False;
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

#print(register("baycosinus", "b4yc051nu5"))
#login("baycosinus","b4yc051nu5", "192.168.1.1")
#login("test1", "pass1", "192.168.1.3")
#logout(3)
#result = get_online_list()
#for i in result:
#    print(i.username)

result = check_available("werwer")
print(result)