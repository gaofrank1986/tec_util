import tecplot as tp
import tecplot.constant as tpc
import test
import unittest
from tec_util.__main__ import main

def load_and_replace(dataset_name):
    return tp.data.load_tecplot(dataset_name, read_data_option=tpc.ReadDataOption.Replace)

class TestMain(unittest.TestCase):
    ''' Tests for the main program '''

    def test_extract(self):
        ''' Make sure extract command works '''
        with test.temp_workspace():
            main([
                'extract',
                '--variables=x,y',
                '--zones="*:[1-4]"',
                test.data_item_path('sphere.dat')
            ])
            ds = load_and_replace("extract.plt")
            self.assertEqual(ds.num_variables,2)
            self.assertEqual(ds.num_zones,4)

    def test_interp(self):
        ''' Make sure interp command works '''
        with test.temp_workspace():
            main([
                'interp',
                test.data_item_path('interp_src.dat'),
                test.data_item_path('interp_tgt.dat'),
            ])
            ds = load_and_replace("interp.plt")
            vrange = ds.variable("r").values(0).minmax()
            self.assertAlmostEqual(max(vrange), 6.39408e-01, delta=1e-6)
            self.assertAlmostEqual(min(vrange), 5.10930e-01, delta=1e-6)

    def test_revolve(self):
        ''' Make sure revolve command works '''
        with test.temp_workspace():
            main([
                'revolve',
                test.data_item_path('axi_sphere_surf.plt'),
                '-o', 'axi_sphere_rev.dat',
                '-n', '25',
                '-a', '90.0',
                '-r', 'v1',
                '-v', 'v2:v2y,v2z',
                '-v', 'q2',
            ]),
            ds = load_and_replace('axi_sphere_rev.dat')
            vs = [v.name for v in ds.variables()]
            self.assertEqual(vs,[
                'x', 'y', 'q1',
                'q2', 'q2_cos', 'q2_sin',
                'v1', 'z',
                'v2', 'v2y', 'v2z',
            ])
            self.assertEqual(ds.zone(0).dimensions, (11,25,1))

    def test_revolve_quotes(self):
        ''' Make sure we can read arguments in quoted strings '''
        with test.temp_workspace():

            # Support various kinds of quoting
            main([
                'revolve',
                test.data_item_path('axi_sphere_surf.plt'),
                '-o', 'axi_sphere_rev.dat',
                '-n', '25',
                '-a', '90.0',
                '-r', 'v1',
                '-v', '"v2":\'v2y\',v2z',
                '-v', 'q2',
            ]),
            ds = load_and_replace('axi_sphere_rev.dat')
            vs = [v.name for v in ds.variables()]
            self.assertEqual(vs,[
                'x', 'y', 'q1',
                'q2', 'q2_cos', 'q2_sin',
                'v1', 'z',
                'v2', 'v2y', 'v2z',
            ])

            # Support quoting the full argument
            main([
                'revolve',
                test.data_item_path('axi_sphere_surf.plt'),
                '-o', 'axi_sphere_rev.dat',
                '-n', '25',
                '-a', '90.0',
                '-r', 'v1',
                '-v', '"v2:v2y,v2z"',
                '-v', 'q2',
            ]),
            ds = load_and_replace('axi_sphere_rev.dat')
            vs = [v.name for v in ds.variables()]
            self.assertEqual(vs,[
                'x', 'y', 'q1',
                'q2', 'q2_cos', 'q2_sin',
                'v1', 'z',
                'v2', 'v2y', 'v2z',
            ])
