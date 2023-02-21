<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:s="http://di.huc.knaw.nl/sd/hi/schema"
    xmlns:cmd="http://www.clarin.eu/cmd/1" xmlns:cmdp="http://www.clarin.eu/cmd/1/profiles/PROF" 
    exclude-result-prefixes="xs" version="3.0">

    <xsl:param name="schema"
        select="document('schema-template.xml')"/>
    
    <xsl:param name="recs" select="0"/>
    <xsl:param name="SKIP" select="()"/>

    <xsl:template match="text()"/>

    <xsl:template name="createSchema">
        <xsl:param name="name"/>
        <xsl:param name="s"/>
        <xsl:param name="nodes"/>
        <xsl:variable name="snode" select="$s/*[local-name() = $name]"/>
        <xsl:element name="{$name}">
            <xsl:attribute name="s:min"
                select="min((count($nodes[exists(text()[normalize-space(.) != '']) or exists(node())]), $snode/@s:min))"/>
            <xsl:attribute name="s:max" select="
                max((for $p in $nodes/..
                return
                count($p/*[local-name() = $name]), $snode/@s:max))"/>
            <xsl:if test="exists(@org)">
                <xsl:attribute name="s:uri" select="@org"/>
            </xsl:if>
            <xsl:for-each-group select="$nodes[exists(text()[normalize-space(.) != ''])]"
                group-by="normalize-space(.)">
                <s:instance
                    freq="{count(current-group()) + number(($snode/s:instance[.=current-grouping-key()]/@freq,'0')[.!=''][1])}">
                    <xsl:value-of select="current-grouping-key()"/>
                </s:instance>
            </xsl:for-each-group>
            <xsl:for-each select="
                    for $i in $snode/s:instance
                    return
                        if (empty($nodes[. = $i])) then
                            ($i)
                        else
                            ()">
                <xsl:copy-of select="."/>
            </xsl:for-each>
            <xsl:for-each-group select="$nodes/*" group-by="local-name()">
                <xsl:call-template name="createSchema">
                    <xsl:with-param name="name" select="current-grouping-key()"/>
                    <xsl:with-param name="nodes" select="current-group()"/>
                    <xsl:with-param name="s" select="$snode"/>
                </xsl:call-template>
            </xsl:for-each-group>
            <xsl:for-each select="
                for $sn in ($snode/(* except s:instance))
                    return
                        if (empty($nodes/*[local-name() = local-name($sn)])) then
                            ($sn)
                        else
                            ()">
                <xsl:element name="{local-name()}">
                    <xsl:attribute name="s:min" select="0"/>
                    <xsl:copy-of select="@* except @s:min"/>
                    <xsl:copy-of select="*"/>
                </xsl:element>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>

    <xsl:template match="/">
        <s:S recs="{$recs}">
            <xsl:for-each-group select="/cmd:CMD/cmd:Components/*[not(name()=$SKIP)]" group-by="local-name()">
                <xsl:call-template name="createSchema">
                    <xsl:with-param name="name" select="current-grouping-key()"/>
                    <xsl:with-param name="nodes" select="current-group()"/>
                    <xsl:with-param name="s" select="$schema/s:S"/>
                </xsl:call-template>
            </xsl:for-each-group>
<!--            <xsl:variable name="rec" select="."/>
            <xsl:copy-of select="for $r in $schema/s:S/* return if (empty($rec/*[name()=name($r)])) then ($r) else ()"/>
-->        </s:S>
    </xsl:template>

</xsl:stylesheet>
