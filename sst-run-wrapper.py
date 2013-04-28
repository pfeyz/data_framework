"""Hacky wrapper around sst-run that allows intercepting XML reports for writing
to DB etc.

call it the same as you do sst-run for example, ::

  $ python sst-run-wrapper.py -d google -x -r xml

Replace the logger.warn(suite_name/test_case_name/xml_texy) calls in
report_testcase with code that writes that data to the db. You can do the same
in report_testsuite but I'm not sure if that'd be useful.

I instantiated a separate logger below to test the output (instead of just using
logging.debug) to avoid writing to the same logging stream that sst is already
using. We can't use print statements because sst is capturing stdout.

"""

import logging
from sst.scripts.run import main
from xml.dom.minidom import Document
from sst.junitxmlrunner import _XMLTestResult

# we're going to be overriding these two methods but we still want to be able to
# use them within our new methods.
old_case_reporter = _XMLTestResult._report_testcase
old_suite_reporter = _XMLTestResult._report_testsuite

# I was hoping we could just subclass _XMLTestResult and redfine those methods
# in our subclass, but they're static methods (not sure why) and are hard-coded
# as calls to _XMLTestResult._report_testcase/testsuite in
# _XMLTestResult.generate_reports, but I guess that's why it's got the
# non-public "_" prefix.

def report_testsuite(suite_name, test_result, xml_testsuite, xml_document):
    """ Called when a test suite's xml is being generated. `suite_name` and
    `xml_text` (below) have what you care about."""

    result = old_suite_reporter(suite_name, test_result, xml_testsuite,
                                xml_document)
    xml_text = xml_document.documentElement.toprettyxml(indent='\t')

    return result  # calling code expects this

def report_testcase(suite_name, test_result, xml_testsuite, xml_document):
    """Called when a per-testcase report is being generated. `suite_name`,
    `test_case_name`, and `xml_text` are where the data's at.

    We call the old_case_reporter function twice. The first time we call it with
    a 'fake' test suite element so we can isolate the single testcase being
    reported on. We call it again with the actual xml_testsuite that was passed
    in from the calling code so we don't change its behaviour; the calling code
    will still get all the testcases appended to its xml_testsuite node.

    """
    suite = Document()
    old_case_reporter(suite_name, test_result, suite, xml_document)
    old_case_reporter(suite_name, test_result, xml_testsuite, xml_document)
    test_case_element = suite.documentElement
    test_case_name = test_case_element.getAttribute('name')
    xml_text = test_case_element.toprettyxml(indent='\t')

    logger.warn(suite_name + ':' + test_case_name)
    logger.warn(xml_text)

# monekypatch XMLTestRunner
_XMLTestResult._report_testcase = staticmethod(report_testcase)
_XMLTestResult._report_testsuite = staticmethod(report_testsuite)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.FileHandler('log.txt'))
    main()
