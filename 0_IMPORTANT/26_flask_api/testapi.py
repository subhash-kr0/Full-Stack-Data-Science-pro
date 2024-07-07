from flask import Flask , request,jsonify , render_template
app = Flask(__name__)

@app.route("/")
def show_form():
    return render_template('index.html')

@app.route("/check_password",methods = ['POST'])
def check_password():
   name =  request.form.get('username')
   password = request.form.get('password')
   print({name} , {password})
   return "usernaem and password received"



if __name__ == "__main__":
   app.run(host="0.0.0.0",port=8000) 