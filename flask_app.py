from application import create_app


app = create_app()


if __name__ == "__main__":
    import socket, webbrowser, waitress
    
    app.config["FLASKENV"] = "development"
    
    host = socket.gethostbyname(socket.gethostname())
    port = 9000
    print(f"Starting host @ {host}")
    
    web_site = f"http://{host}:{port}"
    
    webbrowser.open(web_site)
    
    waitress.serve(app=app, host=host, port=port)