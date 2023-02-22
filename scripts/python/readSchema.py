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


    # first Elements, than Components!!!
def traverse(element,uitvoer,indent=1):
    indent_str = '    ' * indent
    for child in element:
        attrs = ''
        try:
            minimum = int(child.attrib[make_ns_attr('min')])
        except:
            minimum = 0 
        try:
            maximum = int(child.attrib[make_ns_attr('max')])
            if maximum > 1:
                maximum = 'unbounded'
        except:
            maximum = 0 
        if minimum>1: 
            minimum = 1
            maximum = 'unbounded'
        attrs += f' CardinalityMin="{minimum}"'
        attrs += f' CardinalityMax="{maximum}"'
        try:
            uri = child.attrib[make_ns_attr('uri')]
            if not uri=='':
                attrs += f' ConceptLink="{uri}"'
        except:
            pass
        try:
            datatype = child.attrib[make_ns_attr('datatype')]
            if datatype == 'text':
                datatype = 'string'
            elif datatype == 'uri':
                datatype = 'anyURI'
            attrs += f' ValueScheme="{datatype}"'
            uitvoer.write(f'{indent_str}<Element name="{child.tag}"{attrs}/>\n')
            continue
        except:
            pass
        if child:
            uitvoer.write(f'{indent_str}<Component name="{child.tag}"{attrs}>\n')
            traverse(child,uitvoer,indent=indent+1)
            uitvoer.write(f'{indent_str}</Component>\n')
        else:
            if child.tag!=make_ns_attr('instance'):
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
    stderr(f'convert {inputfile} to {outputfile}')
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
    uitvoer.write(f'<Component name="Codemeta" CardinalityMin="1" CardinalityMax="1">\n')
    codemeta = root.find('Codemeta')
    # first Elements, than Components!!!
    traverse(codemeta,uitvoer)
    uitvoer.write(f'</Component>\n</ComponentSpec>\n')

    stderr(datetime.today().strftime("end:   %H:%M:%S"))

