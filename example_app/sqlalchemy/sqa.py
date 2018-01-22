import sqlalchemy as sqa
import webob.exc

from aalam_common import sqa as zsqa
from example_app.sqlalchemy.models import Owners, Items


def _add_owner_if_not_exists(session, owner_email):
    try:
        owner = session.query(Owners).filter(Owners.email == owner_email).one()
    except sqa.orm.exc.NoResultFound:
        owner = Owners(owner_email)
        session.add(owner)
        session.commit()

    return owner.id


def add_item(session, name, type_, owner_email):
    owner_id = _add_owner_if_not_exists(session, owner_email)

    session.add(Items(name, type_, owner_id))


def get_item(session, name):
    @zsqa.query_process
    def _f():
        return session.query(
            Items.name, Items.type_.label('type'),
            Owners.email.label('owner')).filter(
            Items.name == name, Owners.email == Items.owner)

    ret = _f()
    if len(ret) == 0:
        raise webob.exc.HTTPNotFound(
            explanation="Items '%s' not found" % name)
    return ret[0]


def _validate_owner(session, name, owner):
    ret = session.query(Items.name, Owners.email).filter(
        Items.name == name, Owners.id == Items.owner).all()

    if len(ret) == 0:
        raise webob.exc.HTTPNotFound(
            explanation="Item '%s' not found" % name)

    if ret[0][1] != owner:
        raise webob.exc.HTTPForbidden(
            explanation="You cannot modify this item")


def update_item(session, name, new_type, owner_email):
    try:
        _validate_owner(session, name, owner_email)
        item = session.query(Items).filter(Items.name == name).one()

        item.type = new_type
    except sqa.orm.exc.NoResultFound:
        raise webob.exc.HTTPNotFound(
            'Item not found')


def delete_item(session, name, owner):
    _validate_owner(session, name, owner)
    session.query(Items).filter(Items.name == name).delete()


@zsqa.query_process
def get_items(session, filters):
    query_filters = ()
    query_filter_fields = []

    max_items = filters.pop("max", None)
    match_dict = {
        "type": Items.type_.label('type'),
        "owner": Owners.email,
        "name": Items.name,
    }
    if filters:
        zsqa_eval = zsqa.EvaluateFilters(filters, match_dict)
        try:
            query_filters += zsqa_eval.eval(query_filter_fields)
        except:
            # TODO
            raise webob.exc.HTTPBadRequest(
                explanation="Invalid filter used")

    query_filters += (Owners.id == Items.owner,)
    return session.query(
        Items.name,
        Items.type_.label('type'),
        Owners.email.label('owner')).filter(*query_filters).order_by(Items.name).limit(max_items)
