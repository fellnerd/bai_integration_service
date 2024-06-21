import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_pymongo import PyMongo
from schema_handler import apply_schema_defaults, update_schema
from transform_json import transform_json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def create_app(config=None):
    app = Flask(__name__)

    # Flask Configuration
    app.config.from_mapping(
        DEBUG=os.environ.get('DEBUG', 'True').lower() in ['true', '1', 't'],
        MONGO_URI="mongodb://localhost:27017/",
        DATABASE_NAME='BAI_PROD_DB_KIES'
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

            category, data, schema = transform_json(data)
            if category is None:
                return jsonify({"error": data}), 400

            # Select the database and collection dynamically
            db = mongo.cx[app.config['DATABASE_NAME']]
            collection = db[category]
            schema_collection = db["SCHEMAS"]
            metric_collection = db["bai_metric"]

            # Update schema if necessary and get the current schema
            schema_name = f"{category}__SCHEMA"
            current_schema = update_schema(schema_collection, schema_name, schema)

            # Apply schema defaults to each item
            data = [apply_schema_defaults(item, current_schema) for item in data]

            # Insert data into MongoDB
            result = collection.insert_many(data)
            if result.acknowledged:
                metric_collection.insert_one({
                    "timestamp": datetime.now(),
                    "collection": category,
                    "total_items": len(data)
                })
                return jsonify({"message": "Data stored", "id": str(result.inserted_ids)})

        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(port=5002)
