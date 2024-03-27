import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_pymongo import PyMongo
from transform_json import transform_json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def create_app(config=None):
    app = Flask(__name__)

    # Flask Configuration
    app.config.from_mapping(
        DEBUG=os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't'],
        MONGO_URI=os.environ.get('MONGO_URI', "mongodb://localhost:27017"),
        DATABASE_NAME=os.environ.get('DATABASE_NAME', 'BAI_PROD_DB')
        # ... any other configuration
    )
    if config:
        app.config.update(config)

    # Setup CORS
    CORS(app)

    # Setup MongoDB
    mongo = PyMongo(app)

    # Route Definitions
    @app.route("/")
    def hello_world():
        return "Service is up and running. Version: latest-test"

    @app.route("/api/ingest", methods=["POST"])
    def ingest_data():
        try:
            # Get JSON data from request
            data = request.get_json()
            if data is None:
                return jsonify({"error": "Invalid data"}), 400

            category, data = transform_json(data)

            # Select the database and collection dynamically
            db = mongo.cx[app.config['DATABASE_NAME']]
            collection = db[category]
            
            
            metric_collection = db["bai_metric"]

            # Insert data into MongoDB
            result = collection.insert_many(data)
            try:
                if result.acknowledged:
                    metric_collection.insert_one({
                        "timestamp": datetime.now(),
                        "collection": category,
                        "total_items": len(data)
                    })
            except:
                return Response(status=500)
            return jsonify({"message": "Data stored", "id": str(result.inserted_ids)})

        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
