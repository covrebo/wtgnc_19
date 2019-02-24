from wtgnc import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Feature requests
# TODO: Add pick history page
# TODO: Add active class to navigation links via http://jinja.pocoo.org/docs/tricks/