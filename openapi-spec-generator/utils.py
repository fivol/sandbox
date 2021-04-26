def jsonify_spec(spec_model):
    """Transform Python objects to plain json by recursively call .spec() method"""

    if not hasattr(spec_model, 'spec'):
        return spec_model

    spec_obj = spec_model.spec()

    if isinstance(spec_obj, list):
        return [jsonify_spec(item) for item in spec_obj]
    elif isinstance(spec_obj, dict):
        return {key: jsonify_spec(item) for key, item in spec_obj.items()}
