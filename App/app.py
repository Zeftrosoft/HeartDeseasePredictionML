from flask import Flask, render_template, request
from predictor import Predictor
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

@app.route("/dashboard")
def dashboard():
    # data : {
    #     status : asdasdasd
    #     userdata : {
    #         gender :
    #     },
    #     prediction : 
    # }
    # Fetch data
    # if yes -> process() op + data + status true -> pass to ui
    # no -> status -> false
    val = (70,1,0,145,174,0,1,125,1,2.6,0,0,3)
    predictor = Predictor()
    prediction = predictor.has_disease(val)
    return render_template('dashboard.html',data={'title':prediction})

@app.route('/')
def login():
    # post -> body -> fetch data from db -> compare with pass -> yes -> dashboard
    # no -> login
    return render_template('login.html')

@app.route('/register')
def register():
    #  post req -> body -> save in sql -> yes -> login
    #     no -> register 
    return render_template('register.html')

# @app.route('/userdata')
# def userdata():
#     # post req -> body -> save in sql -> yes -> dashboard
#     # no -> dashboard 
#     return 

if __name__ == "__main__":
    app.run(debug=True)