from flask import Flask
from routes import allByUser_bp
from routes import netMerchant_bp

app = Flask(__name__)

# Create the application context for testing purposes
app_context = app.app_context()
app_context.push()

# Register the blueprints
app.register_blueprint(allByUser_bp)
app.register_blueprint(netMerchant_bp)

app_context.pop()

if __name__ == '__main__':

    # this func initializes the database (creates and fills it). Since the pythonsqlite.db file is static and my csv
    # won't change throughout the project there is no point in running this anymore. However, I'll keep it in
    # here to show how I ran it originally.
    # dbManager.dbInit()

    app.run()
