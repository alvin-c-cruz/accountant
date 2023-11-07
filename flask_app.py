from application import create_app, db
from pathlib import Path


app = create_app()


if __name__ == "__main__":
    import socket, webbrowser
    
    app.config["FLASKENV"] = "development"
    
    host = socket.gethostbyname(socket.gethostname())
    port = 9000
    
    web_site = f"http://{host}:{port}"
    print(f"Please type on your browser this web address: {web_site}")
    
    # webbrowser.open(web_site)

    instance_path = Path(app.instance_path)
    db_file = instance_path / "data.db"
    if not db_file.is_file():
        with app.app_context():
            db.create_all()
    
    app.run(host="0.0.0.0", port=port)
