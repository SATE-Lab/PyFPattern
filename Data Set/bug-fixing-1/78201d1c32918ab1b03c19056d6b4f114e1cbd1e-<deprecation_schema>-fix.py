

def deprecation_schema():
    deprecation_schema_dict = {
        Required('removed_in'): Any('2.2', '2.3', '2.4', '2.5', '2.6', '2.8', '2.9', '2.10', '2.11', '2.12'),
        Required('why'): Any(*string_types),
        Required('alternative'): Any(*string_types),
        'removed': Any(True),
    }
    return Schema(deprecation_schema_dict, extra=PREVENT_EXTRA)
