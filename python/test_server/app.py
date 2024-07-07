from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route and a function to handle requests to that route


@app.route('/')
def hello():
    return "Hello, World!"


# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8001)
