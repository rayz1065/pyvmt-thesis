import os
import csv
import matplotlib.pyplot as plt

dirname = os.path.dirname(__file__)
def generate_ltlenc_charts ():
    filename = os.path.join(dirname, 'ltlenc_data.csv')
    with open(filename, 'r', encoding='utf8') as dataf:
        csv_data = csv.reader(dataf)
        header = [x.strip() for x in next(csv_data)]
        lines = [
            { header[i]: x.strip() for i, x in enumerate(line) }
            for line in csv_data
        ]

    ltl2smv_time = [float(x['LTL2SMV_TIME']) for x in lines]
    circuit_time = [float(x['CIRCUIT_TIME']) for x in lines]
    ltl2smv_stvars = [int(x['LTL2SMV_STVARS']) - int(x['START_STVARS']) for x in lines]
    circuit_stvars = [int(x['CIRCUIT_STVARS']) - int(x['START_STVARS']) for x in lines]

    plt.scatter(ltl2smv_time, circuit_time)
    plt.ylabel('Circuit solve time')
    plt.xlabel('LTL2SMV solve time')
    plt.yscale('log')
    plt.xscale('log')
    plt.axis('square')
    plt.axis([0.1, 1000, 0.1, 1000])
    plt.subplot().axline((0, 0), (1, 1), linestyle='--', color='r')
    plt.savefig(os.path.join(dirname, 'ltlenc_time_comparison.png'))
    plt.clf()

    plt.scatter(ltl2smv_stvars, circuit_stvars)
    plt.ylabel('Circuit extra stvars')
    plt.xlabel('LTL2SMV extra stvars')
    plt.yscale('log')
    plt.xscale('log')
    plt.axis('square')
    plt.axis([1, 10000, 1, 10000])
    plt.subplot().axline((0, 0), (1, 1), linestyle='--', color='r')
    plt.savefig(os.path.join(dirname, 'ltlenc_stvar_comparison.png'))
    plt.clf()

def main():
    generate_ltlenc_charts()

if __name__ == '__main__':
    generate_ltlenc_charts()
