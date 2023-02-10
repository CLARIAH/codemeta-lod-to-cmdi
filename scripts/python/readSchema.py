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

def traverse(element,uitvoer,indent=1):
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
        try:
            datatype = child.attrib[make_ns_attr('datatype')]
            attrs += f' DataType="{datatype}"'
        except:
            pass
        if child:
            uitvoer.write(f'{indent_str}<Component name="{child.tag}"{attrs}>\n')
            traverse(child,uitvoer,indent=indent+1)
            uitvoer.write(f'{indent_str}</Component>\n')
        else:
#            if child.tag!=make_ns_attr('instance'):
                tag = child.tag.replace(ns['s'],'s').replace("{s}","s:")
                uitvoer.write(f'{indent_str}<Element name="{tag}"{attrs}/>\n')



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
    uitvoer = open(outputfile,'w')
    uitvoer.write('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ComponentSpec isProfile="true" CMDVersion="1.2" CMDOriginalVersion="1.2" xsi:noNamespaceSchemaLocation="https://infra.clarin.eu/CMDI/1.x/xsd/cmd-component.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <Header>
        <ID>clarin.eu:cr1:p_1653377925727</ID>
        <Name>Vragenlijst</Name>
        <Description>Voor de curatie van de vragenlijsten</Description>
        <Status>development</Status>
    </Header>
''')


    tree = ET.parse(inputfile)
    root = tree.getroot()
#    stderr(f'root: {root.tag}')
#    stderr(f'attrib: {root.attrib}')
#    stderr(f'children: {root.children}')
    uitvoer.write(f'<Component name="Codemeta" CardinalityMin="1" CardinalityMax="1">\n')
    codemeta = root.find('Codemeta')
    traverse(codemeta,uitvoer)
    uitvoer.write(f'</Component>\n')

    stderr(datetime.today().strftime("end:   %H:%M:%S"))

