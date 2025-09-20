#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime

db = SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    # Should be set to false in a production environment
    app.debug = True
    app.secret_key = 'somesecretkey'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventdb.sqlite'
    #initialize db with flask app
    db.init_app(app)
    

    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


    Bootstrap5(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.main_bp)
    
    from . import events
    app.register_blueprint(events.destbp)

    from . import auth
    app.register_blueprint(auth.auth_bp)


    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
      return render_template("404.html", error=e)
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    # Custom 401 error page
    @app.errorhandler(401)
    def unauthorized_access(error):
        return render_template('401.html'), 401

    # Custom 500 error page
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500
   
    @app.context_processor
    def get_context():
        time_of_post = datetime.datetime.now() 
        year = time_of_post.year
        time = time_of_post.strftime("%H:%M:%S")
        return dict(year=year, time=time)
   
    
    return app
