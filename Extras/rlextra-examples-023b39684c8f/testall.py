"""Invokes all relevant tests for the rlextra_examples package

ReportLab will check these work against our nightly packages.
You can also run it by simply executing 'test.py'
"""
import os, sys, glob, shutil
from reportlab.lib.utils import annotateException
import unittest
import doctest

from rlextra.rml2pdf import rml2pdf

class TrivialTestCase(unittest.TestCase):
    "We need one to be sure the test machinery is working"
    def test_laws_of_mathematics(self):
        self.assertEqual(2+2, 4, "the world is OK")

class ParameterizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parameterized should
        inherit from this class.  Useful when we want to turn,
        e.g., a directory of 50 RML files into 50 separate TestCase
        instance; or work through a list of input/output pairs.

        Borrowed from Eli Bendersky, spelling fixed by ReportLab ;-)
          http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
    """
    def __init__(self, methodName='runTest',**kwds):
        super(ParameterizedTestCase, self).__init__(methodName)
        self.__dict__.update(kwds)

    @staticmethod
    def parameterize(testcase_klass, **kwds):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, **kwds))
        return suite

class RmlTestCase(ParameterizedTestCase):
    #assume rml full path name stored in self.param
    def setUp(self):
        self.dirName, self.fileName = os.path.split(self.param)
        self.startDir = os.getcwd()
        if self.dirName:
            os.chdir(self.dirName)
    def tearDown(self):
        os.chdir(self.startDir)
    def shortDescription(self):
        return 'rml2pdf: %s' % self.fileName

    def testRml(self):
        source = open(self.fileName, 'rb').read()
        expectError = getattr(self,'expectError',False)
        try:
            rml2pdf.go(source)
            if expectError:
                raise ValueError('Expected error in %s did not occur' % self.fileName)
        except Exception as e:
            if not expectError:
                annotateException('while rendering %s' % self.fileName)

def haveDejaVu():
    from reportlab.pdfbase.ttfonts import TTFont
    for x in ('DejaVuSans','DejaVuSans-Bold','DejaVuSans-Oblique','DejaVuSans-BoldOblique'):
        try:
            TTFont(x,x+'.ttf')
        except:
            return False
    return True

def makeRmlTests():
    suite = unittest.TestSuite()
    targets = sorted(glob.glob(os.path.join('rml_tests', '*.rml')))
    from reportlab.lib.pdfencrypt import pyaes
    skips = []
    if pyaes is None:
        targets.remove(os.path.join('rml_tests','test_000_simple_e256.rml'))
        skips.append('test_000_simple_e256')
    if not haveDejaVu():
        targets.remove(os.path.join('rml_tests','test_053_known_entities.rml'))
        skips.append('test_053_known_entities')

    #one quirk:  we need test_000_simple.rml to execute before test_000_complex.rml,
    #so put it first.  At some point we should arrange in alpha order.

    do_first = os.path.join('rml_tests','test_000_simple.rml')
    try:
        targets.remove(do_first)
        targets.insert(0, do_first)
    except ValueError:
        pass #don't include these in examples, it's too complex for users, might not be there

    for target in targets:
        suite.addTest(ParameterizedTestCase.parameterize(RmlTestCase, param=target, expectError=target.endswith('_error.rml')))
    if skips:
        t = ['class SkipTestCase(unittest.TestCase):'].append
        for _ in skips:
            t(f''' @unittest.skip("s")
 def {_}(*args,**kwds):
  pass
''')
        t = '\n'.join(t.__self__)
        #print(t)
        NS = {}
        exec(t,dict(unittest=unittest),NS)
        loader = unittest.defaultTestLoader
        suite.addTests(loader.loadTestsFromTestCase(NS['SkipTestCase']))
    return suite

class ManualsAndDemos(unittest.TestCase):
    """Initialise this with the current directory.

    It will CD to wherever and generate each needed manual"""
    baseDir = os.getcwd()  #provide a default, but the actual one is set at run time

    def setUp(self):
        self.startDir = os.getcwd()
#        self.docsDir = os.path.normpath(os.path.join(self.startDir, '../docs'))
        os.chdir(self.baseDir)

    def tearDown(self):
        os.chdir(self.startDir)

    def testProductCatalogue(self):
        os.chdir('product_catalogue')
        sys.path.insert(0, os.getcwd())
        import product_catalog
        product_catalog.main(verbose=False)
        sys.path = sys.path[1:]

    # def testRmlUserGuide(self):
    #     os.chdir('../docs/rml2pdf')
    #     sys.path.insert(0, os.getcwd())
    #     #need some fakery to run it 'as if from command line'
    #     class FakeOptions(object):
    #         pass

    #     fakeOptions = FakeOptions()
    #     fakeOptions.DULL = False
    #     import gen_rmluserguide
    #     gen_rmluserguide.run(fakeOptions)
    #     sys.path = sys.path[1:]
    #     shutil.copyfile('rml2pdf-userguide.pdf', self.docsDir + '/rml2pdf-userguide.pdf')

    # def testRmlForBeginners(self):
    #     os.chdir('../docs/rml2pdf/rml-for-beginners')
    #     sys.path.insert(0, os.getcwd())

    #     class FakeOptions(object):
    #         pass

    #     fakeOptions = FakeOptions()
    #     fakeOptions.DULL = False
    #     import gen_rml_for_beginners
    #     gen_rml_for_beginners.run(fakeOptions)
    #     sys.path = sys.path[1:]
    #     shutil.copyfile('rml-for-beginners.pdf', self.docsDir + '/rml-for-beginners.pdf')

    # def testPageCatcherUserGuide(self):
    #     os.chdir('../docs/pagecatcher')
    #     rml = open('pagecatcher-userguide.rml','rb').read()
    #     rml2pdf.go(rml, outDir='..')  #create in docs

    # def testDiagraUserGuide(self):
    #     os.chdir('../docs/diagra')
    #     rml = open('diagradoc.rml','rb').read()
    #     rml2pdf.go(rml, outDir='..')  #create in docs

    #     #diagra guide not yet done, depends heavily on graphics examples directory

def makeSuite():
    from reportlab.lib.testutils import eqCheck, equalStrings
    from reportlab.lib.utils import rl_add_builtins
    rl_add_builtins(eqCheck=eqCheck,equalStrings=equalStrings)

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TrivialTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ManualsAndDemos))
    
    #load all RML samples in test directory
    suite.addTests(makeRmlTests())

    #find all the RML samples
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(makeSuite())
