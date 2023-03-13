# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import json
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
import re
import sys


url_regexp = re.compile(
    r"(\w+://)?"                # protocol                      (optional)
    r"(\w+\.)?"                 # host                          (optional)
    r"((\w+)\.(\w+))"           # domain
    r"(\.\w+)*"                 # top-level domain              (optional, can have > 1)
    r"([\w\-\._\~/]*)*(?<!\.)"  # path, params, anchors, etc.   (optional)
)


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


def getComponents(tag,data,indent=2,debug=False):
    if debug:
        stderr(f'tag: {tag}')
        stderr(f'data: {data}')
        stderr(f'instance: {type(data)}')
    indent_str = '    ' * indent
    if tag=='@context':
        return '',''
    new_tag = tag
    result = ''
    attrs = ''
    new_attrs = ''
    md = url_regexp.search(tag)
    if md!=None:
        attrs = f' org="{tag}"'
        new_tag = tag.split('/')[-1]
        new_tag = new_tag.split('#')[-1]
    else:
        parts = tag.split(':')
        if len(parts)>1:
            new_attrs = f' org="{tag}"'
            new_tag = parts[-1]
    if debug:
        stderr(f'new_tag: {new_tag}')
        stderr(f'new_attrs: {new_attrs}')
    if new_tag[0]=='@':
        new_tag = ''

    if isinstance(data,list):
        for v in data:
            res,att = getComponents(f'{tag}',v,indent)
            result += f'{res}'
            if debug:
                stderr(f'tag in list: {tag}')
                stderr(f'res in list: {result}')
                stderr(f'att in list: {att}')
    elif isinstance(data,dict):
        if debug:
            stderr(f'dict: {data}')
        indent += 1
        for k,v in data.items():
            res,att = getComponents(f'{k}',v,indent,debug)
            if debug:
                stderr(f'res: {res}')
            result += res
            if att!='':
                attrs += f' {att}'
        if debug:
            stderr(f'result: {result}')
        if result!='':
            result = f'{indent_str}<cmdp:{new_tag}{new_attrs}>\n{result}{indent_str}</cmdp:{new_tag}>\n'
        attrs = ''
    elif isinstance(data,str) or isinstance(data,int):
        if tag[0]=='@':
            if debug:
                stderr(f'dont use tag')
            attrs = f'{tag[1:]}="{data}"'
            tag = ''
        else:
            result += f'{indent_str}<cmdp:{new_tag}{attrs}{new_attrs}>{escape_chars(data)}</cmdp:{new_tag}>\n'
            attrs = ''
    else:
        stderr(f'{data} is type: {type(data)}')
    if debug:
        stderr(f'result: {result}')
        stderr(f'attrs: {attrs}')
    return result,attrs

def escape_chars(text):
    if isinstance(text,int):
        return text
    text = text.replace('&','&amp;')
    text = text.replace('<','&lt;')
    return text

def getFooter():
    return '</cmd:CMD>'


def makeCmdi(tag,data):
    result = getHeader()
    result += getResources()
    res,att = getComponents(tag,data)
    result += f'    <cmd:Components>\n{res}    </cmd:Components>\n'
    result += getFooter()
    return result


def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")


def arguments():
    ap = argparse.ArgumentParser(description='Convert json file to cmdi file"')
    ap.add_argument('-i', '--input',
                    help="input file (default input/record.json)",
                    default='input/record.json')
    ap.add_argument('-o', '--output',
                    help="output file (default output/record.cmdi)",
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
    
    output.write(f"{makeCmdi('Codemeta',data)}\n")

    stderr(datetime.today().strftime("end:   %H:%M:%S"))

