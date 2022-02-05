import random


class PICalculator(object):
    def __init__(self, shots, reporting_rate):
        self.shots = int(shots)
        self.reporting_rate = int(reporting_rate)

    def calculate(self):
        report = []
        incircle = 0

        for i in range(1, self.shots+1):
            random1 = random.uniform(-1.0, 1.0)
            random2 = random.uniform(-1.0, 1.0)
            if((random1*random1 + random2*random2) < 1):
                incircle += 1

            if (i % self.reporting_rate == 0):
                report.append([i, incircle])

        print('rl', len(report))
        return report
