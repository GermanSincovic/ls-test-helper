import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename

from modules import Health, FileManager, Resp, Collector, Log, Kafka, PublicApiHelper, BotController
from modules.Constants import MAINTENANCE, UPLOAD_DIR, UI_DIR, MODULES_DIR
from modules.PushNotificationTesting.Dispatcher import PushRegressionDispatcher

app = Flask(__name__, template_folder=UI_DIR, static_folder="ui")
app.secret_key = 'SLKJdjD&s%1234!'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
Response(headers={'Content-Type': 'application/json; charset=utf-8'})

PRD = PushRegressionDispatcher()


@app.route('/ui', methods=['GET'])
def get_ui():
    if MAINTENANCE:
        return render_template('maintenance.html')
    else:
        return render_template('index.html')


@app.route("/ui/push-regression", methods=['GET'])
def get_push_regression_ui():
    return render_template('push-regression-ui/panel.html')


@app.route("/push-regression-data", methods=['GET'])
def get_push_regression_data():
    return Resp.get_response([FileManager.get_file(os.path.join(MODULES_DIR, "PushNotificationTesting"), "TestDataSet.json")[0], 200])


@app.route('/prd', methods=['GET'])
def run_prd():
    PRD.clear_test_data_list()
    PRD.clear_response_data_list()
    return Resp.get_response(PRD.run_regression(request.args.get("env"), request.args.get("spid"), request.args.get("eid")))


@app.route('/push', methods=['GET'])
def retrieve_push_data():
    PRD.retrieve_push(request.args.get("system_time"), request.args.get("not_app_name"), request.args.get("not_title"),
                      request.args.get("notification"))
    return Resp.get_response(["OK", 200])


@app.route("/prd/report", methods=['GET'])
def get_prd_results():
    return Resp.get_response(PRD.get_results())


@app.route('/ui/public-api', methods=['GET'])
def get_public_api_ui():
    if MAINTENANCE:
        return render_template('maintenance.html')
    else:
        return render_template('public-api/index.html')


@app.route('/ui/collector/<string:folder>/<string:file>', methods=['GET'])
def get_file_to_compare(folder, file):
    if not folder or not file:
        return Resp.throw_error(400)
    else:
        return render_template('collector/result.html', data=FileManager.get_file(folder, file), folder=folder,
                               filename=file)


@app.route('/ui/public-api/<string:environment>/<string:feed>', methods=['GET'])
def get_public_api_ui_env_feed(environment, feed):
    if environment not in ['dev', 'test', 'preprod', 'prod'] or feed not in ['event-list', 'event']:
        return Resp.throw_error(400)
    if MAINTENANCE:
        return render_template('maintenance.html')
    else:
        if feed == 'event-list':
            if not request.args.get("update"):
                return render_template('public-api/event-list.html')
            else:
                return render_template('public-api/daily-rows.html',
                                       data=PublicApiHelper.get_public_api_data(
                                           environment=environment,
                                           feed=feed,
                                           sport=request.args.get("sport"),
                                           date=request.args.get("date"),
                                           pid=request.args.get("pid"),
                                           id=request.args.get("id")
                                       )[0], url_config=FileManager.get_url_mapping_config()[environment],
                                       environment=environment,
                                       sport=request.args.get("sport"))
        if feed == 'event':
            if not request.args.get("update"):
                return render_template('public-api/event.html')
            else:
                return render_template('public-api/event-data-' + request.args.get("sport") + '.html',
                                       data=PublicApiHelper.get_public_api_data(
                                           environment=environment,
                                           feed=feed,
                                           sport=request.args.get("sport"),
                                           date=request.args.get("date"),
                                           pid=request.args.get("pid"),
                                           id=request.args.get("id")
                                       )[0], url_config=FileManager.get_url_mapping_config()[environment],
                                       environment=environment,
                                       sport=request.args.get("sport"),
                                       sport_id=PublicApiHelper.get_sport_id_by_name(request.args.get("sport")))


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
            pid=request.args.get("pid"),
            id=request.args.get("id")
        )
    )


@app.route('/public-api/<string:environment>/live/count', methods=['GET'])
def get_public_api_env_live_count(environment):
    if environment not in ['dev', 'test', 'preprod', 'prod']:
        return Resp.throw_error(400)
    return Resp.get_response(PublicApiHelper.get_public_api_live_count(environment))


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


scheduler = BackgroundScheduler()

FileManager.check_dirs_existing()
scheduler.add_job(func=FileManager.remove_old_result_files, trigger="interval", hours=3)
Log.info("Cleaner running in background")

BotController.check_subscriptions_cache_file_existence()
scheduler.add_job(func=BotController.update_subscriptions_list, trigger="interval", seconds=15)
Log.info("Telegram Bot update reader is running")

scheduler.start()

if __name__ == '__main__':
    Log.info("Application starting...")
    app.run(host="0.0.0.0", port=80, debug=False)
