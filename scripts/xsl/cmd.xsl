<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:cmd="http://www.clarin.eu/cmd/1" xmlns:js="http://www.w3.org/2005/xpath-functions" exclude-result-prefixes="xs" version="3.0">

    <xsl:param name="PROF" select="'clarin.eu:cr1:p_1659015263833'"/>
    <xsl:param name="CL_TOOLS" select="'https://tools.clariah.nl/'"/>

    <xsl:variable name="prof" select="document(concat('https://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/1.x/profiles/', $PROF, '/xml'))"/>
    <xsl:variable name="cmdp-ns-uri" select="concat('http://www.clarin.eu/cmd/1/profiles/', $PROF)"/>

<!--    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>-->
    
    <xsl:template match="text()"/>

    <xsl:template match="js:map/js:array[@key = '@graph']/js:map">
        <cmd:CMD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" CMDVersion="1.2" xsi:schemaLocation="http://www.clarin.eu/cmd/1 https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd http://www.clarin.eu/cmd/1/profiles/{$PROF} https://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/1.x/profiles/{$PROF}/xsd">
            <cmd:Header>
                <cmd:MdProfile>
                    <xsl:value-of select="$PROF"/>
                </cmd:MdProfile>
            </cmd:Header>
            <cmd:Resources>
                <cmd:ResourceProxyList>
                    <cmd:ResourceProxy id="lp">
                        <cmd:ResourceType>Resource</cmd:ResourceType>
                        <cmd:ResourceRef>
                            <xsl:value-of select="concat($CL_TOOLS,js:string[@key='identifier'])"/>
                        </cmd:ResourceRef>
                    </cmd:ResourceProxy>
                </cmd:ResourceProxyList>
                <cmd:JournalFileProxyList/>
                <cmd:ResourceRelationList/>
            </cmd:Resources>
            <cmd:Components>
                <xsl:call-template name="component">
                    <xsl:with-param name="component" select="$prof/ComponentSpec/Component"/>
                </xsl:call-template>
            </cmd:Components>
        </cmd:CMD>
    </xsl:template>


    <xsl:template name="component">
        <xsl:param name="component"/>
        <xsl:variable name="current" select="."/>
        <xsl:message>DBG: welcome to component[<xsl:value-of select="$component/@name"/>]</xsl:message>
        <xsl:variable name="instance">
            <xsl:for-each select="$component/Element">
                <xsl:variable name="element" select="."/>
                <xsl:variable name="instances" select="$current/*[matches(@key,concat('^(',$element/@name,'|@',$element/@name,'|.*/',$element/@name,'|.*#',$element/@name,'|.*:',$element/@name,')$'))]"/>
                <!--<xsl:variable name="instances" select="$current/*[@key=$element/@name]"/>-->
                <xsl:message>DBG: welcome to element[<xsl:value-of select="$element/@name"/>][<xsl:value-of select="concat('^(',$element/@name,'|@',$element/@name,'|.*/',$element/@name,'|.*#',$element/@name,'|.*:',$element/@name,')$')"/>][<xsl:value-of select="count($instances)"/>]</xsl:message>
                <xsl:for-each select="$instances">
                    <xsl:choose>
                        <xsl:when test="self::js:array">
                            <xsl:for-each select="*">
                                <xsl:element name="{$element/@name}" namespace="{$cmdp-ns-uri}">
                                    <xsl:value-of select="."/>
                                </xsl:element>                            
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:element name="{$element/@name}" namespace="{$cmdp-ns-uri}">
                                <xsl:value-of select="."/>
                            </xsl:element>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="$component/Component">
                <xsl:variable name="c" select="."/>
                <xsl:for-each select="$current/(js:array[matches(@key,concat('^(',$c/@name,'|@',$c/@name,'|.*/',$c/@name,'|.*#',$c/@name,'|.*:',$c/@name,')$'))]/js:map,js:map[matches(@key,concat('^(',$c/@name,'|@',$c/@name,'|.*/',$c/@name,'|.*#',$c/@name,'|.*:',$c/@name,')$'))])">
                    <xsl:call-template name="component">
                        <xsl:with-param name="component" select="$c"/>
                    </xsl:call-template>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:variable>
        
        <!--<xsl:if test="not(empty($instance/*))">-->
            <xsl:element name="{$component/@name}" namespace="{$cmdp-ns-uri}">
                <xsl:copy-of select="$instance"/>
            </xsl:element>
        <!--</xsl:if>-->

    </xsl:template>



</xsl:stylesheet>
