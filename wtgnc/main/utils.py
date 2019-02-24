from wtgnc.models import Event


def generate_week_num_list():
    schedule_detailed = Event.query.all()
    schedule_week_num = [(str(d.week_id), 'Week ' + str(d.week_id) + ' ' + d.track) for d in schedule_detailed]
    return schedule_week_num
