<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://di.huc.knaw.nl/sd/hi/schema" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="3.0">
    
    <!-- file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/generic/,file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/sport/lists/ -->
<!--    <xsl:param name="vocabdirs" select="'file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/generic/,file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/sport/lists/'"/>
    -->
 
    
    <xsl:template match="node() | @*" mode="#all">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="node()[exists(s:instance)]">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="s:instance">
                <xsl:sort select="lower-case(.)"/>
            </xsl:apply-templates>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
