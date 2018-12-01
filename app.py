import piweb

if __name__ == "__main__":
    app = piweb.create_app()

    app.run(debug=True)