def update_schema(schema_collection, schema_name, new_schema):
    current_schema_doc = schema_collection.find_one({"schema_name": schema_name})
    if current_schema_doc is None:
        current_schema_doc = {"schema_name": schema_name, "schema": {}}
    
    current_schema_data = current_schema_doc["schema"]
    updated = False

    for key, value in new_schema.items():
        if key not in current_schema_data:
            current_schema_data[key] = value
            updated = True

    if updated:
        schema_collection.update_one(
            {"schema_name": schema_name}, 
            {"$set": {"schema": current_schema_data}}, 
            upsert=True
        )
    
    return current_schema_data


def apply_schema_defaults(item, schema):
    for key in schema:
        if key not in item:
            item[key] = ""
    return item