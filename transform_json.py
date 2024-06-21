import json
from datetime import datetime

def transform_json(data):
    try:
        # Convert JSON string to a Python dictionary
        if isinstance(data, str):
            data = json.loads(data)
        
        # Check if the dictionary is not empty
        if not data:
            return None, None, None
        
        # Get the first key of the dictionary
        first_key = next(iter(data))
        
        # Check if the value is a dictionary
        if isinstance(data[first_key], dict):
            # If so, convert it to a list
            data[first_key] = [data[first_key]]
        
        # Generate the schema based on keys and data types
        schema = {}
        items = data[first_key]
        for item in items:
            item["__ingest_timestamp"] = datetime.now()
            for key in item:
                if isinstance(item[key], dict):
                    item[key] = [item[key]]
                schema[key] = type(item[key]).__name__
        return first_key, items, schema
    except json.JSONDecodeError as e:
        return f"Invalid JSON string: {str(e)}", None, None
    except Exception as e:
        return f"An error occurred: {str(e)}", None, None