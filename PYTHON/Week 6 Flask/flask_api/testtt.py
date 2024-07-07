from flask import Flask,render_template , request
app = Flask(__name__)

@app.route('/lekha_cal')
def cal_page():
    return render_template('index.html')

@app.route("/math", methods=['POST'])
def calculator_test():
    ops= request.form['operation']
    first_num= int(request.form['num1'])
    second_number= int(request.form['num2'])

    if(ops=='add'):
        r= first_num + second_number
        return f"addition of {first_num} and {second_num} is {r}"
    if(ops=='subtract'):
        r= first_num - second_number
        return f"subtraction of {first_num} and {second_num} is {r}"
    if(ops=='multiply'):
        r= first_num * second_number
        return f"multiplication of {first_num} and {second_num} is {r}"
    if(ops=='divide'):
        r= first_num / second_number
        return f"division of {first_num} and {second_num} is {r}"
if __name__ =="__main__":
      app.run(host='0.0.0.0',port=5004)
