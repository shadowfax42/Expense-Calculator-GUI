
def normalize_field_name(field_name):
    """Normalize the field name to match the entry keys"""

    return field_name.lower().replace(" ", "_").replace("($)", "").replace("(%)", "")
