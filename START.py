import app.server as serv
import waitress

waitress.serve(serv.app, port=8080, host="127.0.0.1")