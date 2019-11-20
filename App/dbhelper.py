import sqlite3
class DBHelper:

  def connect(self):
    self.conn = sqlite3.connect('./data/mydb.sqlite')
    self.cursor = self.conn.cursor()
    return self.conn
    print("Opened database successfully")
  
  def getcursor(self):
    return self.cursor

  def close(self):
    self.conn.close()
    print('Connection closed')

  def registerUser(self, user):
    res = self.userExists(user, False)
    if not res['status']:
      querry = "INSERT INTO user (email, pass) VALUES ('"+user['email']+"','"+user['password']+"')"
      self.connect()
      self.cursor.execute(querry)
      self.conn.commit()
      self.conn.close()
      return {
        'status': True,
        'msg': 'User Registerd',
        'data': []
      }
    else:
      return {
        'status': False,
        'msg': 'User Exists',
        'data': []
      }

  
  def userExists(self, user, isLogin):
    user_exists = True
    if isLogin:
      querry = "SELECT userId FROM user where email='"+user['email']+"' AND pass='"+user['password']+"'"
    else:
      querry = "SELECT userId FROM user where email='"+user['email']+"'"
    self.connect()
    users = self.cursor.execute(querry)
    user_list = list(users)
    if len(user_list) <= 0 :
      user_exists = {
        'status':False,
        'data':[],
        'msg': 'User Doesnot Exists'
      }
    else:
      user_exists = {
        'status':True,
        'data':{'userId':user_list[0][0]},
        'msg': 'User Exists'
      }
    self.conn.commit()
    self.conn.close()
    return user_exists

  def getUserData(self, userId):
    querry = "SELECT age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal FROM user_data where userId='"+userId+"'"
    self.connect()
    users = self.cursor.execute(querry)
    user_list = list(users)
    if len(user_list) <= 0 :
      user_data = {
        'status':False,
        'data':[],
        'msg': 'User Data Doesnot Exists'
      }
    else:
      user_data = {
        'status':True,
        'data':user_list[0],
        'msg': 'User Data Exists'
      }
    self.conn.commit()
    self.conn.close()
    return user_data

  def upsertUserData(self, user):
    userId = user['userId']
    res = self.getUserData(userId)
    if res['status']:
      querry = "UPDATE user_data SET age={0},sex={1},cp={2},trestbps={3},chol={4},fbs={5},restecg={6},thalach={7},exang={8},oldpeak={9},slope={10},ca={11},thal={12} WHERE userId={13}" \
      .format(user['age'],user['sex'],user['cp'],user['trestbps'],user['chol'],user['fbs'],user['restecg'],user['thalach'],user['exang'],user['oldpeak'],user['slope'],user['ca'],user['thal'],userId)
    else:
      querry = "INSERT into user_data('userId','age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal') \
        VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13})" \
        .format(userId, user['age'],user['sex'],user['cp'],user['trestbps'],user['chol'],user['fbs'],user['restecg'],user['thalach'],user['exang'],user['oldpeak'],user['slope'],user['ca'],user['thal'])
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()
    return {
      'status': True,
      'msg': 'User Data Added',
      'data': []
    }