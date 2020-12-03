import json
import os

from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename

from modules import Health, FileManager, Resp, Collector, Log, Kafka, PublicApiHelper
from modules.Constants import MAINTENANCE, UPLOAD_DIR, UI_DIR

app = Flask(__name__, template_folder=UI_DIR, static_folder="ui")
app.secret_key = 'SLKJdjD&s%1234!'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
Response(headers={'Content-Type': 'application/json; charset=utf-8'})


@app.route('/ui', methods=['GET'])
def get_ui():
    if MAINTENANCE:
        return render_template('maintenance.html')
    else:
        return render_template('index.html')


@app.route('/ui/public-api', methods=['GET'])
def get_public_api_ui():
    if MAINTENANCE:
        return render_template('maintenance.html')
    else:
        return render_template('public-api/index.html')


@app.route('/ui/public-api/<string:environment>/<string:feed>', methods=['GET'])
def get_public_api_ui_env_feed(environment, feed):
    if environment not in ['dev', 'test', 'preprod', 'prod'] or feed not in ['event-list', 'event']:
        return Resp.throw_error(400)
    if MAINTENANCE:
        return render_template('maintenance.html')
    else:
        return render_template('public-api/' + feed + '.html')


@app.route('/public-api/<string:environment>/<string:feed>', methods=['GET'])
def get_public_api_env_feed(environment, feed):
    if environment not in ['dev', 'test', 'preprod', 'prod'] or feed not in ['event-list', 'event']:
        return Resp.throw_error(400)
    return Resp.get_response(
        PublicApiHelper.get_public_api_data(
            environment=environment,
            feed=feed,
            sport=request.args.get("sport"),
            date=request.args.get("date"),
            id=request.args.get("id")
        )
    )


@app.route('/health-page', methods=['GET'])
def health_page():
    if request.method == 'GET':
        return Resp.get_response(Health.get_health_pages())


@app.route("/config", methods=['GET'])
def get_config():
    return Resp.get_response(FileManager.get_application_config())


@app.route("/urlconfig", methods=['GET'])
def get_url_config():
    return Resp.get_response([FileManager.get_url_mapping_config(), 200])


@app.route('/files', methods=['GET'])
def files():
    if request.method == 'GET':
        return Resp.get_response(FileManager.search_files())


@app.route('/files/upload', methods=['POST'])
def files_uploading():
    if request.method == 'POST':
        if 'file' not in request.files:
            return Resp.throw_error(400)
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


@app.route('/public-api/<string:environment>/<string:feed>/<string:sport>/<string:date>', methods=['GET'])
def get_public_api_data_daily(environment, feed, sport, date):
    if environment in ["dev", "test", "preprod", "prod"] \
            and sport in ["soccer", "basketball", "tennis", "hockey", "cricket"] \
            and feed in ["event-list", "event"] \
            and date:
        return Resp.get_response(PublicApiHelper.get_public_api_data_daily(environment, sport, date))
    else:
        return Resp.throw_error(400)


@app.route('/kafka/produce/<string:environment>/<string:topic>', methods=['POST'])
def kafka_produce(environment, topic):
    if request.args.get("key") and request.json:
        return Resp.get_response(Kafka.produce(environment, topic, request.args.get("key"), request.json))
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
    app.run(host="0.0.0.0", port=80, debug=False)
