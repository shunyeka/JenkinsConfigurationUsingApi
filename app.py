from flask import Flask, jsonify, request
from flask_cors import CORS
from jenkins_job_configuration import JenkinsApi

app = Flask(__name__)
CORS(app)


@app.route('/')
def homepage():
    return "Now  you can configure jenkins job using the Python Flask API!!!!!"


@app.route('/jobs', methods=["GET"])
def get_all_job():
    result = JenkinsApi().get_all_jobs()
    return jsonify(result)


@app.route('/jobs', methods=["POST"])
def create_job_using_api():
    data = request.json
    result = JenkinsApi().create_job(data["name"], data["project_type"])
    return jsonify(result)


@app.route('/builds', methods=["POST"])
def build_job_using_api():
    data = request.json
    result = JenkinsApi().build_job(data["name"])
    return jsonify(result)


@app.route('/jobs', methods=["DELETE"])
def delete_job_using_api():
    data = request.json
    result = JenkinsApi().delete_job(data["name"])
    return jsonify(result)


if __name__ == '__main__':
    app.run()
