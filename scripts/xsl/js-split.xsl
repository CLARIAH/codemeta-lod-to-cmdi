<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:js="http://www.w3.org/2005/xpath-functions" exclude-result-prefixes="js"
    version="1.0">
    
    <xsl:variable name="CTXT" select="/js:map/js:array[@key='@context']"/>
    
    <xsl:template match="text()"/>
    
    <xsl:template match="/">
        <records xmlns="">
            <xsl:apply-templates/>
        </records>
    </xsl:template>
    
    <xsl:template match="js:array[@key='@graph']">
        <xsl:for-each select="*">
            <record id="{position()}" xmlns="">
                <map xmlns="http://www.w3.org/2005/xpath-functions">
                    <xsl:copy-of select="$CTXT" copy-namespaces="no"/>
                    <array key="@graph" xmlns="http://www.w3.org/2005/xpath-functions">
                        <xsl:copy-of select="current()"/>
                    </array>
                </map>
            </record>
        </xsl:for-each>
    </xsl:template>
    
    
</xsl:stylesheet>