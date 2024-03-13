from flask import Flask, render_template, Response, request, redirect, url_for


app = Flask(__name__)
def start_server():
    @app.route('/')
    def render():
        return render_template('hello.html')
    @app.route('/background_process_test')
    def background_process_test():
        print ("Hello")
        return ("nothing")
    
#work please
start_server()
