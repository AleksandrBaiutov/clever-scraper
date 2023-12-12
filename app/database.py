from models import db
from sqlalchemy import desc


def get_all_filtered(model, age=None, availability=False, sort_type=None):
    data = model.query

    if availability:
        data = data.filter(model.available == True)

    if age:
        data = data.filter(model.min_age <= age)

    if sort_type == 'rating':
        data = data.order_by(desc(model.rating), desc(model.review_number))
    elif sort_type == 'reviews':
        data = data.order_by(desc(model.review_number), desc(model.rating))

    return data

def get_all(model):
    data = model.query.all()
    return data


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()


def commit_changes():
    db.session.commit()
