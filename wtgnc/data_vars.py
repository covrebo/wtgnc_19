from wtgnc.models import Driver, Pick, Event

# Create the entry list
# entry_list_detailed = Driver.query.all()
#
# entry_list_brief = [('#' + str(driver.car_number) + ' ' + driver.driver, '#' + str(driver.car_number) + ' ' + driver.driver) for driver in entry_list_detailed]

#entry_list_brief = [(1, '#1 Kurt Busch'), (2, '#2 Brad Keselowski')]

# # schedule_detailed = [
#     {
#         'week': 1,
#         'track': 'Daytona',
#         'race': 'Daytona 500',
#         'date': '2019-02-17'
#     },
#     {
#         'week': 2,
#         'track': 'Atlanta',
#         'race': 'Folds of Honor QuikTrip 500',
#         'date': '2019-02-24'
#     },
#     {
#         'week': 3,
#         'track': 'Las Vegas',
#         'race': 'Pennzoil 400',
#         'date': '2019-03-03'
#     },
#     {
#         'week': 4,
#         'track': 'Phoenix',
#         'race': 'TicketGuardian 500',
#         'date': '2019-03-10'
#     },
#     {
#         'week': 5,
#         'track': 'California',
#         'race': 'Auto Club 400',
#         'date': '2019-03-17'
#     }
# ]

schedule_detailed = Event.query.all()

schedule_week_name = [('Week ' + str(d.week_id) + ' ' + d.track, 'Week ' + str(d.week_id) + ' ' + d.track) for d in schedule_detailed]

schedule_week_num = [(str(d.week_id), 'Week ' + str(d.week_id) + ' ' + d.track) for d in schedule_detailed]

results = [
    {
        'week': 1,
        'car_number': 1,
        'driver': 'Kurt Busch',
        'points': 10
    },
    {
        'week': 1,
        'car_number': 2,
        'driver': 'Brad Keselowski',
        'points': 15
    },
    {
        'week': 1,
        'car_number': 3,
        'driver': 'Austin Dillon',
        'points': 20
    },
    {
        'week': 1,
        'car_number': 4,
        'driver': 'Kevin Harvick',
        'points': 25
    },
    {
        'week': 1,
        'car_number': 6,
        'driver': 'Ryan Newman',
        'points': 30
    },
    {
        'week': 2,
        'car_number': 1,
        'driver': 'Kurt Busch',
        'points': 30
    },
    {
        'week': 2,
        'car_number': 2,
        'driver': 'Brad Keselowski',
        'points': 35
    },
    {
        'week': 2,
        'car_number': 3,
        'driver': 'Austin Dillon',
        'points': 40
    },
    {
        'week': 2,
        'car_number': 4,
        'driver': 'Kevin Harvick',
        'points': 45
    },
    {
        'week': 2,
        'car_number': 6,
        'driver': 'Ryan Newman',
        'points': 50
    }
]

# pick_list = Pick.query.all()



picks = [
    {
        'week': 1,
        'display_name': 'Chris',
        'driver_1': 1,
        'driver_2': 2,
        'driver_3': 4,
        'make': 'Chevrolet'
    },
    {
        'week': 1,
        'display_name': 'Jodi',
        'driver_1': 2,
        'driver_2': 3,
        'driver_3': 4,
        'make': 'Ford'
    },
    {
        'week': 2,
        'display_name': 'Chris',
        'driver_1': 1,
        'driver_2': 2,
        'driver_3': 3,
        'make': 'Ford'
    },
    {
        'week': 2,
        'display_name': 'Jodi',
        'driver_1': 3,
        'driver_2': 4,
        'driver_3': 6,
        'make': 'Ford'
    },
]

make_list = [
    ('Chevrolet', 'Chevrolet'),
    ('Ford', 'Ford'),
    ('Toyota', 'Toyota')
]
