from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from PICalculator import PICalculator
import requests
import boto3


app = Flask(__name__)
ec2 = boto3.client('ec2',
    region_name='us-east-1',
    aws_access_key_id='x',
    aws_secret_access_key='y'
)

@app.route('/', methods = ['POST'])
@cross_origin()
def index():
    body = request.json
    print(body)

    calculator = PICalculator(body['shots'], body['reporting_rate'])
    report = calculator.calculate()

    return jsonify({'report': report})


@app.route('/kill',  methods = ['POST'])
@cross_origin()
def kill():
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    instance_id = response.text

    response = ec2.terminate_instances(
        InstanceIds=[instance_id],
        DryRun=False
    )
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
