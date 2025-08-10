from flask import Flask,render_template,request

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def template():
    if request.method=='POST':
        #print(request.form)
        name=request.form['inp']
        print(f"input  is {name} ")

    return render_template('index.html')

app.run(debug=True)