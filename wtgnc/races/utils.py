from wtgnc.models import Make


# TODO: Dynamically update by moving to routes file https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
def generate_make_list():
    # TODO: Return an error if a week has not been selected
    detailed_make_list = Make.query.all()
    make_list = [(make.make, make.make) for make in detailed_make_list]
    return make_list