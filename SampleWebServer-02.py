from flask import render_template
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('APISwagger.yml')

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    print("Console Output: Hello, World!")
    # return render_template('home.html')
    return "Web Output: Hello, World!"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)