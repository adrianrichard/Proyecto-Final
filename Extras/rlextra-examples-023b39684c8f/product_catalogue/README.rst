Product Catalogue Example
==========================

This is an example taken from a real world solution to create a catalogue for a business delivering seasonal wild meats.  It demonstrates how to create attractive
listings using our preppy templating system and Report Markup Language.  Most people will be using this kind of workflow, with a templating system to handle
loops/conditionals/variables, embedded in an RML document to control the formatting.

To try it::

 	cd product_catalogue
 	python product_catalog.py

Look at the output files in output/, then the main script, then the .prep file which controls the layout.  Feel free to make some edits


XML product listing converted to a fully customisable PDF in seconds.
==============================================================================


This example is aimed at showing the use of Report Markup Language (RML), which is a component of our commercial tool-kit. All you need to do to download a full evaluation copy is `sign in`_ or `register on our site`_; then, follow the installation instructions to get yourself set up. Once these are completed, you're ready to go.

.. _sign in: https://www.reportlab.com/accounts/login/
.. _register on our site: http://www.reportlab.com/accounts/register/


Run the example
==========================

To see the output, run product_catalog.py and look at the generated file under /output.


How is the PDF generated?
==========================

The main script lives in prodcut_catalog.py, this is just a Python module which starts by pulling in data from an XML file, then uses a Rlextra utility function to first render a RML file from template filled in by the data, then use the rendered RML to produce a PDF. RML is the markup language use to describe the desired PDF document. The template itself uses Preppy, a Python pre-processor used to output valid RML. Preppy is just Python and therefore quite powerful. 

.. code:: python
from rlextra.rml2pdf import rml2pdf

    #generate the RML file from the preppy template
    rml = template.getOutput(dict(products=some_data))
    open(os.path.join(DATA_DIR,'latest.rml'), 'w').write(rml)
    buf = StringIO.StringIO()
	#write the rml into a pdf file using rml2pdf
    rml2pdf.go(rml, outputFileName=buf)
    return buf.getvalue()
