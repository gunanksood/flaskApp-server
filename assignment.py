from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
import sys
import pika


UPLOAD_FOLDER = 'static/data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(path)
            f = open(path, "r")
            itr = f.read()
            channel.queue_declare(queue='task_queue')
            channel.basic_publish(exchange='', routing_key='task_queue', body=itr,
                                  # properties=pika.BasicProperties(delivery_mode=2,  # make message persistent
                                  #                                 )
            )
            print(itr)

            connection.close()
            return redirect(url_for('upload_file',
                                    filename=filename))

            # url = '127.0.0.1:5000/post'
            # files = request.files
            # r = request.post(url, files)
            # return filename
    return render_template('index.html')


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

if __name__ == '__main__':
    app.run('127.0.0.1', '5001', debug=True)

