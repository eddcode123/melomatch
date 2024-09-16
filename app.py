from flask import Flask, render_template

app = Flask(__name__)

# landing page to route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("aboutus.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/features')
def features():
    return render_template("features.html")

if __name__ == "__main__":
    app.run(debug=True)