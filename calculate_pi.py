from multiprocessing import Process, Pipe
import random
import json


class PICalculator(object):
    def __init__(self, shots, resource_count, reporting_rate):
        self.shots = int(shots)
        self.resource_count = int(resource_count)
        self.reporting_rate = int(reporting_rate)
        self.shots_per_resource = int(self.shots / self.resource_count)

    def calculte(self, shots, reporting_rate, conn):
        print(shots, reporting_rate)
        reports = []
        incircle = 0

        for i in range(1, shots+1):
            random1 = random.uniform(-1.0, 1.0)
            random2 = random.uniform(-1.0, 1.0)
            if((random1*random1 + random2*random2) < 1):
                incircle += 1

            if (i % reporting_rate == 0):
                reports.append([i, incircle])

        print('rl', len(reports))
        conn.send([reports])
        conn.close()

    def get_reports(self):
        reports = []
        processes = [] # create a list to keep all processes
        parent_connections = [] # create a list to keep connections

        for r in range(self.resource_count):
            parent_conn, child_conn = Pipe()
            parent_connections.append(parent_conn)
            process = Process(target=self.calculte, args=(self.shots_per_resource, self.reporting_rate, child_conn))
            processes.append(process)

        # start all processes
        for process in processes:
            process.start()

        # make sure that all processes have finished
        for process in processes:
            process.join()

        for parent_connection in parent_connections:
            reports.append(parent_connection.recv()[0])

        return reports


def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(body);

    calculator = PICalculator(body['shots'], body['resource_count'], body['reporting_rate']);
    reports = calculator.get_reports();

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({
            'reports': reports
        }),
    }
