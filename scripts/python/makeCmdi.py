# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import json
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
import os
import pprint as pp
import re
import sys

def getHeader():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<cmd:CMD xmlns:cmd="http://www.clarin.eu/cmd/1" xmlns:cmdp="http://www.clarin.eu/cmd/1/profiles/PROF" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" CMDVersion="1.2" xsi:schemaLocation="       http://www.clarin.eu/cmd/1 https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd       http://www.clarin.eu/cmd/1/profiles/PROF https://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/1.x/profiles/PROF/xsd">
    <cmd:Header>
        <cmd:MdProfile>PROF</cmd:MdProfile>
    </cmd:Header>
'''

def getResources():
    resources = '''    <cmd:Resources>
        <cmd:ResourceProxyList>
            <cmd:ResourceProxy id="lp">
                <cmd:ResourceType>Resource</cmd:ResourceType>
                <cmd:ResourceRef>LANDINGPAGE</cmd:ResourceRef>
            </cmd:ResourceProxy>
        </cmd:ResourceProxyList>
        <cmd:JournalFileProxyList/>
        <cmd:ResourceRelationList/>
    </cmd:Resources>
'''
    return resources

def getComponents(data):
    components = f'''    <cmd:Components>
'''

    components += '''    </cmd:Components>
'''
    return components

def getFooter():
    return '</cmd:CMD>'

def makeItem(key,value):
    return f'<{key}></{key}>'

def makeCmdi(data):
    result = getHeader()
    result += getResources()
    result += getComponents(data)
    result += getFooter()
    return result


def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")

def arguments():
    ap = argparse.ArgumentParser(description='Convert multi page tif files into single page jpeg files"')
    ap.add_argument('-i', '--input',
                    help="input file",
                    default='input/record.json')
    ap.add_argument('-o', '--output',
                    help="output file",
                    default='output/record.cmdi')
    args = vars(ap.parse_args())
    return args

if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputfile = args['input']
    outputfile = args['output']
    stderr(f'convert from {inputfile} to {outputfile}')
    output = open(outputfile,'w',encoding='UTF8')

    data = json.load(open(inputfile))
    pp.pprint(data,indent=4)
    stderr(data.keys())
#    for key,value in data.items():
#        if key=='@context':
#            continue
#        stderr(f'{key} - {value}')
#        output.write(f'{makeItem(key,value)}\n')
    
    output.write(f'{makeCmdi(data)}\n')

    stderr(datetime.today().strftime("end:   %H:%M:%S"))
