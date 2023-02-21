/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package nl.knaw.huc.di.ingformstools;

import net.sf.saxon.s9api.QName;
import net.sf.saxon.s9api.SaxonApiException;
import net.sf.saxon.s9api.XdmDestination;
import net.sf.saxon.s9api.XdmNode;
import net.sf.saxon.s9api.XsltTransformer;
import org.apache.commons.io.FileUtils;
import org.apache.commons.cli.*;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.util.Collection;

import net.sf.saxon.s9api.XsltExecutable;
import nl.mpi.tla.util.Saxon;
import javax.xml.transform.stream.StreamSource;
import me.tongfei.progressbar.ProgressBar;
import net.sf.saxon.s9api.XdmAtomicValue;

import static nl.mpi.tla.util.Saxon.buildDocument;
import static nl.mpi.tla.util.Saxon.xpath2boolean;

public class SchemaTool {

  public static CommandLine setArgs(String[] args) {
    Options options = new Options();

    Option dir = new Option("d", "dir", true, "input directory path (mandatory)");
    dir.setRequired(true);
    options.addOption(dir);
    Option vocabs = Option.builder("v").longOpt("vocabdir").hasArg().numberOfArgs(Option.UNLIMITED_VALUES).desc("ingforms vocabulary directory path (optional, multiple)").build();
    options.addOption(vocabs);
    Option ext = new Option("x", "ext", true, "input file extension (optional, default: xml)");
    options.addOption(ext);
    Option out = new Option("s", "schema", true, "output schema path (optional, default: stdout)");
    options.addOption(out);
    Option filter = new Option("f", "filter", true, "filter (xpath) to sort out unwanted records (optional, default: '')");
    options.addOption(filter);

    CommandLineParser parser = new DefaultParser();
    HelpFormatter formatter = new HelpFormatter();
    CommandLine cmd = null;

    try {
      cmd = parser.parse(options, args);
    } catch (ParseException e) {
      System.out.println(e.getMessage());
      formatter.printHelp("java -jar schemaTool.jar", options);

      System.exit(1);
    }
    return cmd;
  }

  public static void main(String[] args) throws SaxonApiException, IOException {
    CommandLine cmd = setArgs(args);
    String dir = cmd.getOptionValue("d");
    // String ing = cmd.getOptionValue("i");
    String out = cmd.getOptionValue("s");
    String filter = cmd.getOptionValue("f");
    boolean result = filter=="";
    String ext = cmd.getOptionValue("x","xml");
    Collection<File> inputs = FileUtils.listFiles(new File(dir), new String[]{ext}, true);

    XdmNode schemaNode = buildDocument(new StreamSource(SchemaTool.class.getResource("/schema-template.xml").toString()));
    XsltExecutable schExec = Saxon.buildTransformer(SchemaTool.class.getResource("/schema.xsl"));
    for (File input : ProgressBar.wrap(inputs, "INGForms to schema")) {
        try {
            XsltTransformer xsltTransformer = schExec.load();
            xsltTransformer.setParameter(new QName("schema"), schemaNode);
            XdmNode document = buildDocument(new StreamSource(input));
            result = xpath2boolean(document, filter);
            if (result) {
                xsltTransformer.setSource(document.asSource());
                XdmDestination destination = new XdmDestination();
                xsltTransformer.setDestination(destination);
                xsltTransformer.transform();
                schemaNode = destination.getXdmNode();
//                PrintStream o = new PrintStream("test-"+input.getName()+".xml");
//                o.println(schemaNode.toString());
            }
        } catch (Exception e) {
            System.err.println("!ERR["+input.getCanonicalPath()+"]:"+e.getMessage());
            e.printStackTrace();
        }
    }

    XsltExecutable dtExec = Saxon.buildTransformer(SchemaTool.class.getResource("/datatypes.xsl"));
    XsltTransformer xsltTransformer = dtExec.load();
    xsltTransformer.setParameter(new QName("vocabdirs"), new XdmAtomicValue((cmd.hasOption("v")?String.join(",", cmd.getOptionValues("v")):"")));
    xsltTransformer.setSource(schemaNode.asSource());
    XdmDestination destination = new XdmDestination();
    xsltTransformer.setDestination(destination);
    xsltTransformer.transform();
    schemaNode = destination.getXdmNode();

    XsltExecutable clExec = Saxon.buildTransformer(SchemaTool.class.getResource("/cleanup.xsl"));
    xsltTransformer = clExec.load();
    xsltTransformer.setSource(schemaNode.asSource());
    destination = new XdmDestination();
    xsltTransformer.setDestination(destination);
    xsltTransformer.transform();
    schemaNode = destination.getXdmNode();

    PrintStream o = System.out;
    if (out != null)
      o = new PrintStream(out);
    o.println(schemaNode.toString());

  }

}
