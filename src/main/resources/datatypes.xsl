<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://di.huc.knaw.nl/sd/hi/schema" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="3.0">
    
    <!-- file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/generic/,file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/sport/lists/ -->
    <xsl:param name="vocabdirs" select="'file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/generic/,file:/Users/menzowi/Documents/Projects/OpenHuygens/Resources/ingformslists/ingforms/data/sport/lists/'"/>
    
    <xsl:variable name="VOCABS" as="document-node()*">
        <xsl:choose>
            <xsl:when test="normalize-space($vocabdirs)=''">
                <xsl:sequence select="()"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:for-each select="tokenize($vocabdirs,',')">
                    <xsl:variable name="dir" select="."/>
                    <xsl:if test="doc-available($dir)">
                        <xsl:for-each select="collection(concat($dir,'?select=*.xml'))">
                            <xsl:variable name="vocab" select="."/>
                            <xsl:sequence select="$vocab"></xsl:sequence>           
                        </xsl:for-each>
                    </xsl:if>
                </xsl:for-each>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    
    <xsl:function name="s:findVocabulary">
        <xsl:param name="vals" as="element(s:instance)*"/>
        <xsl:iterate select="$VOCABS">
            <xsl:variable name="vocab" select="."/>
            <xsl:choose>
                <xsl:when test="empty(for $v in $vals return if (empty($vocab//item[item_key=$v][use='use'])) then ($v) else ())">
                    <xsl:sequence select="$vocab"/>
                    <xsl:break/>
                </xsl:when>
            </xsl:choose>
        </xsl:iterate>
    </xsl:function>
    
    <xsl:template match="/s:S">
        <!--<xsl:message>START [types]</xsl:message>-->
        <xsl:variable name="types">
            <xsl:apply-templates mode="types"/>
        </xsl:variable>
        <!--<xsl:message>START [dates]</xsl:message>-->
        <xsl:variable name="dates">
            <xsl:apply-templates select="$types" mode="dates"/>
        </xsl:variable>
        <!--<xsl:message>START [skip]</xsl:message>-->
        <xsl:variable name="skip">
            <xsl:apply-templates select="$dates" mode="skip"/>
        </xsl:variable>
        <!--<xsl:message>START [uniq]</xsl:message>-->
        <xsl:variable name="uniq">
            <xsl:apply-templates select="$skip" mode="uniq"/>
        </xsl:variable>
        <!--<xsl:message>STOP</xsl:message>-->
        <xsl:copy>
            <xsl:copy-of select="$uniq"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="node() | @*" mode="#all">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- uniq -->
    
    <xsl:template match="node() | @*" mode="uniq" priority="10">
        <xsl:copy>
            <xsl:apply-templates select="@* except @s:uniq" mode="#current"/>
            <xsl:attribute name="s:uniq" select="generate-id()"/>
            <xsl:apply-templates select="node()" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- types -->
    
    <!-- leaf with no values, i.e. its never instantiated -->
    <xsl:template match="node()[empty(*)] except s:instance" mode="types">
        <xsl:copy>
            <xsl:apply-templates select="@* except (@s:datatype)"/>
            <xsl:attribute name="s:datatype" select="'text'"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- leafs with values -->
    <xsl:template match="node()[exists(s:instance)]" mode="types">
        <xsl:copy>
            <xsl:apply-templates select="@* except (@s:datatype,@s:vocabulary)"/>
             <xsl:variable name="vocab" select="s:findVocabulary(s:instance)"/>
            <xsl:choose>
                <xsl:when test="exists($vocab)">
                    <xsl:attribute name="s:datatype" select="'enum'"/>
                    <xsl:attribute name="s:vocabulary" select="base-uri($vocab)"/>
                </xsl:when>
               <xsl:when test="empty(s:instance[not(matches(normalize-space(.),'^[0-9]+$'))])">
                   <xsl:attribute name="s:datatype" select="'integer'"/>
                   <xsl:variable name="vals" select="for $n in s:instance return number($n)"/>
                   <xsl:variable name="min" select="min($vals)"/>
                   <xsl:variable name="max" select="max($vals)"/>                   
                   <xsl:choose>
                       <xsl:when test="$min gt 0 and $min le 12 and $max gt 0 and $max le 12">
                           <xsl:attribute name="s:semtype" select="'month'"/>                          
                       </xsl:when>
                       <xsl:when test="$min gt 0 and $min le 31 and $max gt 0 and $max le 31">
                           <xsl:attribute name="s:semtype" select="'day'"/>
                       </xsl:when>
                       <xsl:when test="$min gt 0 and $min le 9999 and $max gt 0 and $max le 9999">
                           <xsl:attribute name="s:semtype" select="'year'"/>                           
                       </xsl:when>
                   </xsl:choose>
               </xsl:when>
                <xsl:when test="empty(s:instance[not(matches(normalize-space(.),'^https?://.+$'))])">
                <!-- uri http(s) -->
                    <xsl:attribute name="s:datatype" select="'uri'"/>
                 </xsl:when>
                <!--
                    dateTime
                -->
                <xsl:when test="empty(s:instance[not(matches(normalize-space(.),'^[0-9]+\.[0-9]+$'))])">
                    <xsl:attribute name="s:datatype" select="'float'"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="s:datatype" select="'text'"/>
                    <xsl:if test="empty(s:instance[not(matches(normalize-space(.),'&lt;[^&lt;]+&gt;'))])">
                        <xsl:attribute name="s:semtype" select="'html'"/>
                    </xsl:if>
                </xsl:otherwise>
            </xsl:choose>
            
            <xsl:apply-templates select="node()" mode="#current">
                <xsl:with-param name="vocab" select="$vocab" tunnel="yes"></xsl:with-param>
            </xsl:apply-templates>
            
            <!-- add s:instance for non-appearing values -->
            <xsl:variable name="n" select="."/>
            <xsl:for-each select="$vocab//item[use='use']">
                <xsl:variable name="v" select="."/>
                <xsl:if test="empty($n/s:instance[.=$v/item_key])">
                    <s:instance freq="0" label="{$v/item_value}">
                        <xsl:value-of select="$v/item_key"/>
                    </s:instance>
                </xsl:if>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="s:instance" mode="types">
        <xsl:param name="vocab" tunnel="yes"/>
        <xsl:variable name="val" select="."/>
        <xsl:copy>
            <xsl:apply-templates select="@* except label" mode="#current"/>
            <xsl:if test="exists($vocab//item[item_key=$val])">
                <xsl:attribute name="label" select="$vocab//item[item_key=$val][use='use']/item_value"/>
            </xsl:if>
            <xsl:apply-templates select="node()" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- dates -->
    
    <xsl:template match="*[exists(*[@s:semtype='year']) and exists(*[@s:semtype='month'])  and exists(*[@s:semtype='month']) and empty(*[not(@s:semtype=('year','month','day'))])]" mode="dates">
        <xsl:copy>
            <xsl:apply-templates select="@* except (@s:datatype,@s:min,@s:max)" mode="#current"/>
            <xsl:attribute name="s:datatype" select="'date'"/>
            <xsl:variable name="y" select="local-name(*[@s:semtype='year'][1])"/>
            <xsl:variable name="m" select="local-name(*[@s:semtype='month'][1])"/>
            <xsl:variable name="d" select="local-name(*[@s:semtype='day'][1])"/>
            <xsl:attribute name="s:min" select="min((@s:min,*[@s:semtype='year'][1]/@s:min,*[@s:semtype='month'][1]/@s:min,*[@s:semtype='day'][1]/@s:min))"></xsl:attribute>
            <xsl:attribute name="s:max" select="max((@s:max,*[@s:semtype='year'][1]/@s:max,*[@s:semtype='month'][1]/@s:max,*[@s:semtype='day'][1]/@s:max))"></xsl:attribute>
            <xsl:attribute name="s:pattern" expand-text="yes">if (normalize-space({$y})!='' and normalize-space({$m})!='' and normalize-space({$d})!='') then (concat({$y},'-',{$m},'-',{$d})) else ('')</xsl:attribute>
            <xsl:apply-templates select="node()" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- skip -->
    
    <xsl:template match="*[@s:semtype='year'][parent::*/@s:datatype='date']" mode="skip">
        <xsl:copy>
            <xsl:apply-templates select="@* except @s:datatype except @s:skip" mode="#current"/>
            <xsl:attribute name="s:skip" select="'yes'"/>
            <xsl:apply-templates select="node()" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="*[@s:semtype='month'][parent::*/@s:datatype='date']" mode="skip">
        <xsl:copy>
            <xsl:apply-templates select="@* except @s:datatype except @s:skip" mode="#current"/>
            <xsl:attribute name="s:skip" select="'yes'"/>
            <xsl:apply-templates select="node()" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="*[@s:semtype='day'][parent::*/@s:datatype='date']" mode="skip">
        <xsl:copy>
            <xsl:apply-templates select="@* except @s:datatype except @s:skip" mode="#current"/>
            <xsl:attribute name="s:skip" select="'yes'"/>
            <xsl:apply-templates select="node()" mode="#current"/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
