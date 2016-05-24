# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import sys, os

# ---------------------

def build(platform_dir, products_dir, debug = False):
    
    # Add platform scritps path to python module search paths
    sys.path.append(platform_dir + "/scripts")
    
    print("Using :" + platform_dir + "/scripts")
    # Get gerenator
    from platformGenerator import Generator
    
    gen = Generator(products_dir, platform_dir, debug)
    gen.generate_code()
    gen.compile()

if __name__ == '__main__':
    import argparse
    cur_path = os.getcwd()
    # First parse command line arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument("products_dir",
                        help="The directory where stride products where generated",
                        nargs='?',
                        default= cur_path + '/Gamma/tests/modulation.stride_Products'
#                        default='/home/andres/Documents/src/Stride/StreamStack/platforms/Arduino/examples/test.stride_Products'
                        )
    parser.add_argument("platform_dir",
                        help="The directory of the platform to be used",
                        nargs='?',
                        default= cur_path + '/Gamma/1.0'
#                        default=this_path + '/../../../Arduino/1.0'
                        )
    args = parser.parse_args()
    
    platform_dir = args.platform_dir
    products_dir = args.products_dir
    
    build(platform_dir, products_dir, True)
    
