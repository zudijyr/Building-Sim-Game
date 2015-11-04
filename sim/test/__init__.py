import unittest

def unit_suite():
	return unittest.TestLoader().discover('test', pattern='*.py', top_level_dir='sim')

def directory_test(directory):
	return unittest.TestLoader().discover(directory, pattern='*.py', top_level_dir='sim')

def integration_suite():
	loader = unittest.TestLoader()
	loader.testMethodPrefix = 'integration_test'
	return loader.discover('test', pattern='*.py', top_level_dir='sim')

def full_suite():
	suite = unit_suite()
	suite.addTest(integration_suite())
	return suite

def name_test(name):
	loader = unittest.TestLoader()
	return loader.loadTestsFromName(name)

def single_test(test):
	loader = unittest.TestLoader()
	loader.testMethodPrefix = test
	return loader.discover('test', pattern='*.py', top_level_dir='sim')
