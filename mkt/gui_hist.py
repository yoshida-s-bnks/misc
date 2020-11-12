import optparse
import csv
import sys
import os
import sformat
import matplotlib.pyplot as plt
import datetime
import tkinter

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
                if not d in data:
                    data[d] = {}
                data[d][t] = e
    except FileNotFoundError:
        if options.verbose:
            print ("**input file: failed to open data file " + options.input_filename)
        sys.exit(0)
    ########################################

    w1 = tkinter.Tk()
    w1.mainloop()

    # plt.interactive(True)

    # while True:
    #     opt = getOption(data.keys())
    #
    #     if opt== -1:
    #         break
    #     else:
    #         plt.clf()
    #         print(opt)
    #         x = {}
    #         y = {}
    #         for d in data[opt]:
    #             x0 = sformat.strptime_pre(d, '%Y-%m-%d %H:%M')
    #             y0 = float(data[opt][d][0])
    #             s0 = data[opt][d][1]
    #             print("%s: %s from %s" % (x0, y0, s0))
    #             x.setdefault(s0,[]).append(x0)
    #             y.setdefault(s0,[]).append(y0)
    #         for s in x:
    #             plt.plot(x[s], y[s],label=s)
    #         plt.title(opt)
    #         plt.legend()
    #         plt.show()
