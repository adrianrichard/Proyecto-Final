import os
import base64
import preppy
from io import BytesIO
from reportlab.lib.utils import asUnicodeEx, asBytes

from xml.sax.saxutils import escape, unescape
from rlextra.radxml.xml2tt import xml2TT
from rlextra.radxml.xmlutils import TagWrapper
from rlextra.radxml.html_cleaner import cleanInline
from rlextra.rml2pdf import rml2pdf

DATA_DIR = 'data'

class Product(object):
    "Empty class to hold parsed product attributes"
    pass

def fix(tag):
    "Apply fixes to their descriptive markup"
    src = asUnicodeEx(tag)
    step1 = src.replace(u'\x82',u'&eacute;')
    step2 = unescape(step1)
    step3 = step2.encode('utf-8')
    return step3

def parse_catalog(filename):

    """Validate and parse XML.  This will complain if invalid

    We fully parse the XML and turn into Python variables, so that any encoding
    issues are confronted here rather than in the template
    """
    xml = open(filename,'rb').read()
    tree = xml2TT(xml)
    tagTree = TagWrapper(tree)
    request_a_quote = [109,110,4121,4122,4123]
    # we now need to de-duplicate; the query returns multiple rows with different images
    # in them.  if id is same, assume it's the same product.
    ids_seen = set()
    products = []
    for prodTag in tagTree:
        id = int(str(prodTag.ProductId1))   #extract tag content
        if id in ids_seen:
            continue
        else:
            ids_seen.add(id)
        prod = Product()
        prod.id = id
        prod.modelNumber = int(str(prodTag.ModelNumber))
        prod.archived = (str(prodTag.Archived) == 'true')
        prod.name = fix(prodTag.ModelName)
        prod.summary= fix(prodTag.Summary)
        prod.description= fix(prodTag.Description)

        #originally the images came from a remote site.  We have stashed them in
        #the img/ subdirectory, so just chop off the final part of the path.
        prod.image = os.path.split(str(prodTag.ImageUrl))[-1].replace(' ','')
        
        if prod.modelNumber in request_a_quote:
            prod.price = "Call us on 01635 246830 for a quote"
        else:
            prod.price =  '&pound;' + str(prodTag.UnitCost)[0:len(str(prodTag.UnitCost))-2]
        if prod.archived:
            pass
        else:
            products.append(prod)
    products.sort(key=lambda x: x.modelNumber)
    return products

def create_pdf(catalog, template):
    """Creates PDF as a binary stream in memory, and returns it

    This can then be used to write to disk from management commands or crons,
    or returned to caller via Django views.
    """
    RML_DIR = 'rml'
    templateName = os.path.join(RML_DIR, template)
    template = preppy.getModule(templateName)
    namespace = {
        'products':catalog,
        'RML_DIR': RML_DIR,
        'IMG_DIR': 'img'

        }
    rml = template.getOutput(namespace,quoteFunc=preppy.stdQuote)
    open(os.path.join(DATA_DIR,'latest.rml'), 'wb').write(asBytes(rml))
    buf = BytesIO()
    rml2pdf.go(asBytes(rml), outputFileName=buf)
    return buf.getvalue()

def main(verbose=True):
    filename = os.path.join(DATA_DIR, 'products.xml')
    if verbose:
        print('\n'+'#'*20 + '\nabout to parse file: %s' % filename)
    products = parse_catalog(filename)
    if verbose:
        print('file parsed OK \n')

    
    pdf = create_pdf(products, 'flyer_template.prep')
    filename ='output/harwood_flyer.pdf'
    open(filename,'wb').write(pdf)
    if verbose:
        print('Created %s' % filename)


if __name__ == '__main__':
    main()
