from sqlalchemy.orm import class_mapper


def serialize(model,exclude=[]):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    columns = [c.key for c in class_mapper(model.__class__).columns if c.key not in exclude ]
    return dict((c, getattr(model, c)) for c in columns)

def get_integer_param(param, default):
        try:
            return int(param)
        except (TypeError, ValueError):
            return default