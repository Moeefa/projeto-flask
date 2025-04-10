from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Edie Correia Santana!"

@app.route('/page')
def page():
    return render_template('page.html')

if __name__ == '__main__':
    app.run(debug=True)