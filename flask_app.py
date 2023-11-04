from application import create_app


app = create_app()


if __name__ == "__main__":
    import socket, webbrowser
    
    app.config["FLASKENV"] = "development"
    
    host = socket.gethostbyname(socket.gethostname())
    port = 9000
    
    web_site = f"http://{host}:{port}"
    print(f"Please type on your browser this web address: {web_site}")
    
    # webbrowser.open(web_site)
    
    app.run(host="0.0.0.0", port=port)
