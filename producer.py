from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import pika

UPLOAD_FOLDER = 'static/data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

def send_data(file):
    cred = pika.PlainCredentials('gunank', 'gunank')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1',
                                                                   port=5673, virtual_host='/',
                                                                   credentials=cred))
    channel = connection.channel()
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    channel.queue_declare(queue='tasks_queue')
    for line in open(path, "r"):
        channel.basic_publish(exchange='', routing_key='tasks_queue', body=line,
                              # properties=pika.BasicProperties(delivery_mode=2,  # make message persistent
                              #                                 )
                              mandatory=1, immediate=0)
    connection.close()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file:
            send_data(file)
            return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
