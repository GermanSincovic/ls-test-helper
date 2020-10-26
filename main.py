import os

# TEST

from flask import Flask, request, Response, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

from modules import Health, FileManager, Resp, Collector, Log, Kafka
from modules.Constants import MAINTENANCE, UPLOAD_DIR, UI_DIR

app = Flask(__name__, template_folder=UI_DIR, static_folder="ui")
cors = CORS(app)
app.secret_key = 'SLKJdjD&s%1234!'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
Response(headers={'Content-Type': 'application/json; charset=utf-8'})


@app.route('/ui', methods=['GET'])
def get_ui():
    if MAINTENANCE:
        return render_template('maintenance.html')
    else:
        return render_template('index.html')


@app.route('/health-page', methods=['GET'])
def health_page():
    if request.method == 'GET':
        return Resp.get_response(Health.get_health_pages())


@app.route("/config", methods=['GET'])
def get_config():
    return Resp.get_response(FileManager.get_application_config())


@app.route('/files', methods=['GET'])
def files():
    if request.method == 'GET':
        return Resp.get_response(FileManager.search_files())


@app.route('/files/upload', methods=['POST'])
def files_uploading():
    if request.method == 'POST':
        if 'file' not in request.files:
            return Resp.throw_error(418)
        file = request.files['file']
        if file.filename == '':
            return Resp.throw_error(400)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return Resp.get_response(["OK", 200])
    else:
        return Resp.throw_error(405)


@app.route('/files/<string:folder>/<string:filename>', methods=['GET', 'DELETE'])
def file_handling(folder, filename):
    if request.method == 'DELETE':
        return Resp.get_response(FileManager.delete_file(folder, filename))
    if request.method == 'GET' and request.args.get("separate"):
        return Resp.get_response(FileManager.separate_file(folder, filename))
    if request.method == 'GET' and request.args.get("moveto"):
        return Resp.get_response(FileManager.move_file(folder, request.args.get("moveto"), filename))
    if request.method == 'GET':
        return Resp.get_response(FileManager.get_file(folder, filename))
    else:
        return Resp.throw_error(400)


@app.route('/collector/run', methods=['POST'])
def collect():
    if request.json:
        return Resp.get_response(Collector.collect(request.json))
    else:
        return Resp.throw_error(400)


@app.route('/kafka/produce/<string:topic>', methods=['POST'])
def kafka_produce(topic):
    if request.args.get("key") and request.json:
        return Resp.get_response(Kafka.produce(topic, request.args.get("key"), request.json))
    else:
        return Resp.throw_error(400)


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def page_not_found(exception):
    return Resp.throw_error(exception.code)


FileManager.check_dirs_existing()
FileManager.run_cleaner()

if __name__ == '__main__':
    Log.info("Application starting...")
    app.run(host="0.0.0.0", port=8090, debug=False)
