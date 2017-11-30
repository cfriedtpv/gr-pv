#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gnuradio import uhd
from crimson_sink import crimson_sink
from crimson_source import crimson_source
import time

import numpy as np
from scipy.signal import chirp, sweep_poly

def gen_chirp( samp_rate = 10000000, A = 32000, f0 = 200, f1 = 20000, T = 1, phi0 = 0 ):
    """
    
    generate a chirp signal
    
    samp_rate := sample rate of the signal in Samples / s
    A         := Amplitude of chirp (constant)
    f0        := start frequency, Hz
    f1        := stop frequency, Hz
    T         := sweep time, s
    
    See https://en.wikipedia.org/wiki/Chirp
    http://scipy-cookbook.readthedocs.io/items/FrequencySweptDemo.html
    """
    
    if samp_rate <= 0:
        raise ValueError( 'samp_rate must be positive' )

    A = math.abs( A )

    if f0 <= 0:
        raise ValueError( 'f0 must be positive' )

    if f1 <= 0:
        raise ValueError( 'f1 must be positive' )

    if T <= 0:
        raise ValueError( 'T must be positive' )

    N = int( T * samp_rate )
    
    if N <= 0:
        raise ValueError( 'The number of samples must be positive' )

    t = np.linspace(0, T, N )
    x = chirp( t, f0, f1, T, method='linear' )
    
    return x

class qa_crimson_source_sink_sob (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
        self.tb.run ()
        # check data

    def test_0phase_delay_5 (self):
        
        ##################################################
        # Variables
        ##################################################
        sob = 5
        samp_rate = 10e6
        freq = 2.4e9
        gain = 20
        channels = [0]

        ##################################################
        # Blocks
        ##################################################
        csrc = uhd.usrp_source(
                ",".join(("", "crimson:sob-host=1234")),
                uhd.stream_args(
                        cpu_format="sc16",
                        otw_format='sc16',
                        channels=( channels ),
                ),
        )
        csnk = uhd.usrp_sink(
                ",".join(("", "crimson:sob-host=1234")),
                uhd.stream_args(
                        cpu_format="sc16",
                        otw_format='sc16',
                        channels=( channels ),
                ),
        )

        for ch in channels:
            csrc.set_samp_rate( samp_rate, ch )
            csrc.set_center_freq( freq, channel )
            csrc.set_gain( gain, channel )
            csnk.set_samp_rate( samp_rate, ch )
            csnk.set_center_freq( freq, channel )
            csnk.set_gain( gain, channel )
        
        vsrc = blocks.vector_source_c( chirp )
        vsnk = blocks.vector_sink_c()
        
        co = blocks.complex_to_interleaved_short( True )
        dec = blocks.interleaved_short_to_complex( True )

        ##################################################
        # Connections
        ##################################################
        self.tb.connect( ( co, 0 ), ( csnk, 0 ) )
        self.tb.connect( ( dec, 0 ), ( vsnk, 0 ) )
        self.tb.connect( ( dec, 0 ), ( vsnk, 0 ) )
        self.tb.connect( ( vsrc, 0 ), ( co, 0 ) )
        self.tb.connect( ( vsrc, 0 ), ( co, 0 ) )
        self.tb.connect( ( csrc, 0 ), ( dec, 0 ) )    
        
        self.tb.run ()
        
        # check data
        
        expected_data = tuple( map( tuple, chirp ) )
        actual_data = vsnk.data()
        
        self.assertTupleEqual( expected_data, actual_data )
        self.assertEqual( len( expected_data ), len( actual_data ) )

if __name__ == '__main__':
    gr_unittest.run(qa_crimson_source_sink_sob, "qa_crimson_source_sink_sob.xml")
