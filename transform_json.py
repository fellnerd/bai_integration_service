import json

def transform_json(data):
    try:
        # JSON-String in ein Python-Dictionary umwandeln
        
        
        # Überprüfen, ob das Dictionary nicht leer ist
        if not data:
            return None
        
        # Den ersten Schlüssel des Dictionaries herausfinden
        first_key = next(iter(data))
        
        # Überprüfen, ob der Wert ein Dictionary ist
        if isinstance(data[first_key], dict):
            # Wenn ja, in eine Liste umwandeln
            data[first_key] = [data[first_key]]
        
        # Das resultierende Dictionary zurück in einen JSON-String umwandeln
        items = data[first_key]
        for item in items:
            for key in item:
                if isinstance(item[key], dict):
                    item[key] = [item[key]]
        return first_key, items
    except json.JSONDecodeError as e:
        return f"Ungültiger JSON-String: {str(e)}"
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"