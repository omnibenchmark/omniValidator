import unittest
import omniValidator as ov 
from IPython.core.display import HTML
from IPython.core.display import display, HTML

class testGetSchema(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_is_url(self):
        # just tests if we can get correctly an url from schemas
        self.assertTrue(ov.is_url(ov.get_schema('a','a','a')))
    
    def test_display_requirements(self):
        # tests if we can correctly get an html table from the example config
        from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
        omni_obj = get_omni_object_from_yaml('tests/data/config.yaml')
        result = ov.display_requirements(omni_obj = omni_obj, raw_html = True)         
        self.assertIsInstance(HTML(result), HTML)

    def test_attr_from_omni_obj(self): 
        # test to check if keyword and benchmark can be loaded into omniobject
        # then runs a schema_exist (omni batch data)
        from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
        omni_obj = get_omni_object_from_yaml('tests/data/config.yaml')
        keyword = omni_obj.keyword[0]
        benchmark = omni_obj.benchmark_name
        out = ov.schema_exist(benchmark, keyword)
        self.assertTrue(out)


    ## Section to test validate requirements main fun ------------------
    #===================================================================

    def test_validate_requirements(self): 
        # tests the validate requirements based on correct config file
        from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
        omni_obj = get_omni_object_from_yaml('tests/data/config.yaml')
        out = ov.validate_requirements(omni_obj = omni_obj)
        self.assertTrue(out)

    def test_validate_requirements_wrongKey(self): 
        # tests the validate requirements based on wrong config file
        from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
        omni_obj = get_omni_object_from_yaml('tests/data/wrong/config_Wkeyword.yaml')
        try: 
            out_test = False
            out = ov.validate_requirements(omni_obj = omni_obj)
        except Exception: 
            out_test = True
        self.assertTrue(out_test)
    
    def test_validate_requirements_wrongBenchmark(self): 
        # tests the validate requirements based on wrong config file
        from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
        omni_obj = get_omni_object_from_yaml('tests/data/wrong/config_Wbenchmark.yaml')
        try: 
            out_test = False
            out = ov.validate_requirements(omni_obj = omni_obj)
        except Exception: 
            out_test = True
        self.assertTrue(out_test)

    def test_validate_requirements_wrongOutputs(self): 
        # tests the validate requirements based on wrong config file
        from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
        omni_obj = get_omni_object_from_yaml('tests/data/wrong/config_Woutputs.yaml')
        try: 
            out_test = False
            out = ov.validate_requirements(omni_obj = omni_obj)
        except Exception: 
            out_test = True
        self.assertTrue(out_test)


# TODO: ask chatgpt how to tell to look into test/ 
unittest.main()