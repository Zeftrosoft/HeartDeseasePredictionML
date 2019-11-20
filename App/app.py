from flask import Flask, render_template, request, redirect
from predictor import Predictor
from dbhelper import DBHelper

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
helper = DBHelper()
@app.route("/dashboard")
def justdashboard():
    return redirect('/login')

@app.route("/dashboard/<userId>", methods=['GET'])
def dashboard(userId):
    inti_res = {
        'status': False,
        'data' : {
            'age' : 0,
            'sex' : 0,
            'cp' : 0,
            'trestbps' : 0,
            'tbps': 0,
            'chol' : 0,
            'fbs' : 0,
            'restecg' : 0,
            'thalach' : 0,
            'exang' : 0,
            'oldpeak' : 0,
            'slope' : 0,
            'ca' : 0,
            'thal' : 0
        },
        'title': 'Dashboard',
        'userId': userId,
        'prediction' : -1
    }
    res = helper.getUserData(userId)
    print(res)
    if res['status']:
        res['title'] = 'Dashboard'
        res['userId'] = userId
        val = res['data']
        predictor = Predictor()
        prediction = predictor.has_disease(val)
        res['prediction'] = prediction
        return render_template('dashboard.html',data=res)
    else:
        return render_template('dashboard.html',data=inti_res)

@app.route('/login', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
def login():
    res = {
        'init' : True,
        'status': False,
        'data':[],
        'msg':'',
        'title': 'Login'
    }
    if request.method == 'POST':
        user = {
            'email': request.form['email'],
            'password': request.form['pass']
        }
        res = helper.userExists(user, True)
        if res['status']:
            userId = res['data']['userId']
            return redirect('dashboard/'+ str(userId))
        else:
            res['title'] = 'Login'
            res['init'] = False
            return render_template('login.html', data=res)
    else: 
        return render_template('login.html', data=res)

@app.route('/register', methods=['GET','POST'])
def register():
    res = {
        'init' : True,
        'status': False,
        'data':[],
        'msg':'',
        'title': 'Register'
    }
    if request.method == 'POST':
        user = {
            'email': request.form['email'],
            'password': request.form['pass']
        }
        res = helper.registerUser(user)
        res['title'] = 'Register'
        res['init'] = False
        if res['status'] :
            return redirect('login')
        else:
            return render_template('register.html', data=res)
    else:
        return render_template('register.html', data=res)

@app.route('/userdata', methods=['POST'])
def userdata():
    if request.method == 'POST':
        userData = {
           'age' : request.form['age'],
           'sex' : request.form['sex'],
           'cp' : request.form['cp'],
           'trestbps' : request.form['trestbps'],
           'chol' : request.form['chol'],
           'fbs' : request.form['fbs'],
           'restecg' : request.form['restecg'],
           'thalach' : request.form['thalach'],
           'exang' : request.form['exang'],
           'oldpeak' : request.form['oldpeak'],
           'slope' : request.form['slope'],
           'ca' : request.form['ca'],
           'thal' : request.form['thal'],
           'userId' : request.form['userId']
        }
        res = helper.upsertUserData(userData)
        return redirect('/dashboard/'+userData['userId'])
    else:
        return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)


