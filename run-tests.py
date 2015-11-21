# Requirements:
#  * python 2.6 backport of test discovery ( https://pypi.python.org/pypi/discover )
#  * xmlrunner: https://pypi.python.org/pypi/xmlrunner/1.7.3
#  * coverage.py
import os
from unittest import TestSuite
import sys

if __name__ == '__main__':
    from discover import DiscoveringTestLoader
    import xmlrunner
    import coverage

    loader = DiscoveringTestLoader()

    sys.path.append(os.path.join(os.path.dirname(__file__), "test"))

    cov = coverage.coverage(source=["src"])
    cov.start()

    tests = loader.discover(start_dir="test", pattern='test*.py', top_level_dir="test")

    runner = xmlrunner.XMLTestRunner(output='test-reports')
    runner.run(tests)
    cov.stop()
    cov.html_report(ignore_errors=True, directory='python-coverage-html')
