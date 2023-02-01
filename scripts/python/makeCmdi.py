# -*- coding: utf-8 -*-
from wand.image import Image
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
import os
import re
import sys

def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")

def getHeader():
    return '''<cmd:CMD
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:cmd="http://www.clarin.eu/cmd/1" 
    xmlns:cmdp="http://www.clarin.eu/cmd/1/profiles/clarin.eu:cr1:p_1653377925727"
    CMDVersion="1.2" 
    xsi:schemaLocation="
      http://www.clarin.eu/cmd/1 https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd
      http://www.clarin.eu/cmd/1/profiles/clarin.eu:cr1:p_1653377925727 https://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/1.x/profiles/clarin.eu:cr1:p_1653377925727/xsd">
    <cmd:Header>
        <cmd:MdProfile>clarin.eu:cr1:p_1653377925727</cmd:MdProfile>
    </cmd:Header>
'''

def getResources(base_name, number, filenames=[]):
    resources = '''    <cmd:Resources>
        <cmd:ResourceProxyList>
'''
    resources += f'''            <cmd:ResourceProxy id="s">
                <cmd:ResourceType>Resource</cmd:ResourceType>
                <cmd:ResourceRef>/IN/{base_name}</cmd:ResourceRef>
            </cmd:ResourceProxy>
'''
    path = os.path.dirname(base_name)
    file_name = os.path.basename(base_name)
    #name = re.search(r'(^[^.]*).', file_name).group(1)
    try:
        name = re.search(r'(^[^.]*)\.[^.]+$', file_name).group(1)
    except:
        name = file_name
    if len(filenames)>0:
        num = 0
        for f in filenames:
            filename = os.path.basename(f)
            resources += f'''            <cmd:ResourceProxy id="p{num+1}">
                <cmd:ResourceType>Resource</cmd:ResourceType>
                <cmd:ResourceRef>/OUT/{path}/{filename}</cmd:ResourceRef>
            </cmd:ResourceProxy>
'''
            num += 1
    else:
        for num in range(number):
            resources += f'''            <cmd:ResourceProxy id="p{num+1}">
                <cmd:ResourceType>Resource</cmd:ResourceType>
                <cmd:ResourceRef>/OUT/{path}/{name}-{num}.jpg</cmd:ResourceRef>
            </cmd:ResourceProxy>
'''
    resources += '''        </cmd:ResourceProxyList>
        <cmd:JournalFileProxyList/>
        <cmd:ResourceRelationList/>
    </cmd:Resources>
'''
    return resources

def getComponents(base_name, number):
    path = os.path.dirname(base_name)
    file_name = os.path.basename(base_name)
    try:
        name = re.search(r'(^[^.]*)\.[^.]+$', file_name).group(1)
    except:
        name = file_name
    identifier = re.search(r'(^[^.]*).', file_name).group(1)
    components = f'''    <cmd:Components>
        <cmdp:Vragenlijst>
            <cmdp:identifier>{path}</cmdp:identifier>
            <cmdp:aantalPaginas>0</cmdp:aantalPaginas>
            <cmdp:Scan cmd:ref="s">
                <cmdp:identifier>{name}</cmdp:identifier>
                <cmdp:aantalPaginas>{number}</cmdp:aantalPaginas>
'''
    for num in range(number):
        components += f'''                <cmdp:Pagina cmd:ref="p{num+1}">
                    <cmdp:nr>{num+1}</cmdp:nr>
                    <cmdp:kloekeCode></cmdp:kloekeCode>
                    <cmdp:inzending>0</cmdp:inzending>
                    <cmdp:volgorde></cmdp:volgorde>
                    <cmdp:type>als verwacht</cmdp:type>
                </cmdp:Pagina>
'''

    components += '''            </cmdp:Scan>
        </cmdp:Vragenlijst>
    </cmd:Components>
'''
    return components

def getFooter():
    return '</cmd:CMD>'

def makeCmdi(base_name, number, filenames=[]):
    result = getHeader()
    result += getResources(base_name, number, filenames)
    result += getComponents(base_name, number)
    result += getFooter()
    return result

