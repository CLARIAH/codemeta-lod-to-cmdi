# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import json
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
import sys
from makeCmdi import makeCmdi


def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")


def arguments():
    ap = argparse.ArgumentParser(description='Convert multi page tif files into single page jpeg files"')
    ap.add_argument('-i', '--input',
                    help="input file",
                    default='input/data.json')
    ap.add_argument('-o', '--output',
                    help="output dir",
                    default='output')
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputfile = args['input']
    outputdir = args['output']
    stderr(f'convert json set {inputfile} to {outputdir}')

    data = json.load(open(inputfile))

    teller = 1
    for item in data['@graph']:
        outfile = f'record_{teller:>02}.cmdi'
        teller += 1
        output = open(f'{outputdir}/{outfile}','w',encoding='UTF8')
        output.write(f"{makeCmdi('Codemeta',item)}\n")

    stderr(datetime.today().strftime("end:   %H:%M:%S"))

