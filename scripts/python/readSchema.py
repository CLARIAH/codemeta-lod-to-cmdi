# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
#import json
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
import sys
import xml.etree.ElementTree as ET

ns = {'s' : 'http://di.huc.knaw.nl/sd/hi/schema'} 

def make_ns_attr(attr):
    ns_attr = '{' + f'{ns["s"]}' + '}' + attr
    return ns_attr

def traverse(element,indent=1):
    indent_str = '    ' * indent
    for child in element:
        attrs = ''
        minimum = 0
        try:
            minimum = int(child.attrib[make_ns_attr('min')])
            attrs += f' CardinalityMin="{minimum}"'
        except:
            pass
        try:
            if minimum>1:
                maximum = 'unbounded'
            else:
                maximum = child.attrib[make_ns_attr('max')]
            attrs += f' CardinalityMax="{maximum}"'
        except:
            pass
        if child:
            stderr(f'{indent_str}Component name="{child.tag}"{attrs}')
            traverse(child,indent=indent+1)
        else:
            if child.tag!=make_ns_attr('instance'):
                stderr(f'{indent_str}Element name="{child.tag}"{attrs}')



def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")


def arguments():
    ap = argparse.ArgumentParser(description='Convert multi page tif files into single page jpeg files"')
    ap.add_argument('-i', '--input',
                    help="input file",
                    default='schema.xml')
    ap.add_argument('-o', '--output',
                    help="output gile",
                    default='result.xml')
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputfile = args['input']
    outputfile = args['output']
    stderr(f'convert schema.xml to {outputfile}')


    tree = ET.parse(inputfile)
    root = tree.getroot()
#    stderr(f'root: {root.tag}')
#    stderr(f'attrib: {root.attrib}')
#    stderr(f'children: {root.children}')
    stderr(f'Component name="Codemeta" CardinalityMin="1" CardinalityMax="1"')
    codemeta = root.find('Codemeta')
    traverse(codemeta)

    stderr(datetime.today().strftime("end:   %H:%M:%S"))

