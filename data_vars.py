
entry_list_detailed = [
    {
        'car_number': 1,
        'driver': 'Kurt Busch',
        'sponsor': 'Monster Energy',
        'make': 'Chevrolet',
        'team': 'Chip Ganassi Racing'
    },
    {
        'car_number': 2,
        'driver': 'Brad Keselowski',
        'sponsor': 'Miller Lite',
        'make': 'Ford',
        'team': 'Team Penske'
    },
    {
        'car_number': 3,
        'driver': 'Austin Dillon',
        'sponsor': 'Bass Pro Shops/Tracker Boats',
        'make': 'Chevrolet',
        'team': 'Richard Childress Racing'
    },
    {
        'car_number': 4,
        'driver': 'Kevin Harvick',
        'sponsor': 'Busch Beer Can2Can',
        'make': 'Ford',
        'team': 'Stewart-Haas Racing'
    },
    {
        'car_number': 6,
        'driver': 'Ryan Newman',
        'sponsor': 'Wyndham Rewards',
        'make': 'Ford',
        'team': 'Rousch Fenway Racing'
    }
]

entry_list_brief = [(d['driver'], '#' + str(d['car_number']) + ' ' + d['driver']) for d in entry_list_detailed]


schedule_detailed = [
    {
        'week': 1,
        'track': 'Daytona',
        'race': 'Daytona 500',
        'date': '2019-02-17'
    },
    {
        'week': 2,
        'track': 'Atlanta',
        'race': 'Folds of Honor QuikTrip 500',
        'date': '2019-02-24'
    },
    {
        'week': 3,
        'track': 'Las Vegas',
        'race': 'Pennzoil 400',
        'date': '2019-03-03'
    },
    {
        'week': 4,
        'track': 'Phoenix',
        'race': 'TicketGuardian 500',
        'date': '2019-03-10'
    },
    {
        'week': 5,
        'track': 'California',
        'race': 'Auto Club 400',
        'date': '2019-03-17'
    }
]

schedule_brief = [('Week ' + str(d['week']) + ' ' + d['track'], 'Week ' + str(d['week']) + ' ' + d['track']) for d in schedule_detailed]

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
