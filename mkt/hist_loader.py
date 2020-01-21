import optparse
import csv
import sys
import os
import sformat
import matplotlib.pyplot as plt
import datetime

def getOption(m):
    opts = {}
    optn = 0
    for i in m:
        opts[optn] = i
        optn += 1

    wrow,wcol = os.popen('stty size','r').read().split()
    spc = 20
    for i in opts:
        print("%2d: %s" %(i,sformat.spacer(spc,opts[i])), end='')
        if not (i+1) % int(int(wcol) / (spc + 5)):
            print()
    print("q: quit")

    while True:
        opt = input('choose product: ')
        if opt == 'q':
            return -1
        else:
            try:
                opt = int(opt)
                if opt in opts:
                    return opts[opt]
            except:
                print("**** Please select from the list")


if __name__ == '__main__':
    ########################################
    # open output file if passed in from argument
    # if it fails to open, or not provided, f_open flag is set to false
    parser = optparse.OptionParser()

    parser.add_option('-i', '--input', dest="input_filename", default="")
    parser.add_option('-v', '--verbose', action="store_true")

    options, remainder = parser.parse_args()

    data = {}

    try:
        with open(options.input_filename, 'r') as f:
            if options.verbose:
                print ("##intput file: " + options.input_filename)
            reader = csv.reader(f)
            for (d, t, *e) in reader:
                # print (d)
                # print (t)
                # print (e)
                if not d in data:
                    data[d] = {}
                data[d][t] = e
    except FileNotFoundError:
        if options.verbose:
            print ("**input file: failed to open data file " + options.input_filename)
        sys.exit(0)
    ########################################

    plt.interactive(True)

    while True:
        opt = getOption(data.keys())

        if opt== -1:
            break
        else:
            plt.clf()
            print(opt)
            x = {}
            y = {}
            for d in data[opt]:
                x0 = sformat.strptime_pre(d, '%Y-%m-%d %H:%M')
                y0 = float(data[opt][d][0])
                s0 = data[opt][d][1]
                print("%s: %s from %s" % (x0, y0, s0))
                x.setdefault(s0,[]).append(x0)
                y.setdefault(s0,[]).append(y0)
            for s in x:
                plt.plot(x[s], y[s],label=s)
            plt.title(opt)
            plt.legend()
            plt.show()
