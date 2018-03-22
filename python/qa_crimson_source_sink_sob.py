#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2017 Per Vices Corporation.
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

import math
import time

import threading

import matplotlib.pyplot as plt

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gnuradio import uhd

#from crimson_sink import crimson_sink
#from crimson_source import crimson_source

import numpy as np
from scipy.signal import chirp, sweep_poly

def gen_chirp( samp_rate = 10000000, A = 0.1, f0 = 200, f1 = 20000, T = 1, phi0 = 0 ):
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

    A = math.fabs( A )

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
    x_i = A * chirp( t, f0, f1, T, method='logarithmic' )
    x_q = 1j * x_i
    x = x_i + x_q

    return x

class qa_crimson_source_sink_sob (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    # utility function for test_002
    def tb_killer_fn( self, delay ):
        #print( "tb_killer_fn(): sleep {0} s".format( delay ) )
        time.sleep( delay )
        #print( "tb_killer_fn(): stopping top block now".format( delay ) )
        self.tb.stop()

    def test_000_num_samps_and_done_with_5s_sob (self):

        ##################################################
        # Variables
        ##################################################
        samp_rate = 1e6
        freq = 15e6
        gain = 0
        channels = [0]
        sob = 5
        chirp_rate = 10
        front_porch = 0
        back_porch = 0
        nseconds = 1.0
        nsamples = int( nseconds * samp_rate )

        chrp = gen_chirp( samp_rate = samp_rate, T = 1.0 / chirp_rate )
        chrp = np.repeat( chrp, int( nseconds * chirp_rate ) )

        ##################################################
        # Blocks
        ##################################################
        stream_args = uhd.stream_args( cpu_format = "fc32", otw_format = "sc16", channels = ( channels ) )
        csrc = uhd.usrp_source( uhd.device_addr_t( "" ), stream_args, False )
        csnk = uhd.usrp_sink( uhd.device_addr_t( "" ), stream_args )

        # issue a stop to flush out the rx channels
        sc = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_STOP_CONTINUOUS )
        csrc.issue_stream_cmd( sc )

        csrc.set_samp_rate( samp_rate )
        csrc.set_center_freq( freq )
        csrc.set_gain( gain )
        
        csnk.set_samp_rate( samp_rate )
        csnk.set_center_freq( freq )
        csnk.set_gain( gain )

        vsrc = blocks.vector_source_c( chrp )
        vsrc.set_repeat( True )
        vsnk = blocks.vector_sink_c()

        ##################################################
        # Connections
        ##################################################
        self.tb.connect( ( vsrc, 0 ), ( csnk, 0 ) )
        self.tb.connect( ( csrc, 0 ), ( vsnk, 0 ) )

        ##################################################
        # Set Start of Burst
        ##################################################

        if True:
            #time_now = uhd.time_spec_t.get_system_time()
            time_now = uhd.time_spec_t( 0.0 )
            csrc.set_time_now( time_now )
        else:
            time_now = csnk.get_time_now()
        print( "Time now is {0}".format( time_now.get_real_secs() ) )
        
        start_time = uhd.time_spec_t( time_now.get_real_secs() + sob )
        print( "Start Time is {0}".format( start_time.get_real_secs() ) )
        
        stop_time = uhd.time_spec_t( start_time.get_real_secs() + nsamples / samp_rate + 10 )
        print( "Stop Time is {0}".format( stop_time.get_real_secs() ) )

        # actually set tx start time
        csnk.set_start_time( start_time )

        # actually set rx start time
        sc = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_NUM_SAMPS_AND_DONE )
        sc.num_samps = nsamples
        sc.stream_now = False
        sc.time_spec = start_time
        csrc.issue_stream_cmd( sc )

        killer = threading.Thread( group = None, target = self.tb_killer_fn, name = "killer", args = ( ( stop_time.get_real_secs() - start_time.get_real_secs() ), ) )
        killer.start()
        
        print( "Sending & Receiving {0} samples...".format( sc.num_samps ) )

        ##################################################
        # Run Flow Graph
        ##################################################
        time_now = csrc.get_time_now()
        print( "Calling run. Time now is {0}".format( time_now.get_real_secs() ) )
        self.tb.run()
        time_now = csrc.get_time_now()
        print( "returned from run. Time now is {0}".format( time_now.get_real_secs() ) )
        
        ##################################################
        # Verify Results
        ##################################################

        expected_data = np.asarray( tuple( chrp ) )
        actual_data = np.asarray( vsnk.data() )

        expected_data /= np.max( np.abs( np.real( expected_data ) ), axis = 0 )
        actual_data /= np.max( np.abs( np.real( actual_data ) ), axis = 0 )

        N1 = len( expected_data )
        N2 = len( actual_data )
        if N1 == N2:
            N = N1
            t1 = start_time.get_real_secs()
            t2 = t1 + N / samp_rate
            t = np.arange( t1, t2, 1.0/samp_rate )
            f1 = np.real( expected_data )
            f2 = np.real( actual_data )
            plt.plot( t, f1, 'b--', t, f2, 'r-' )
            plt.show()

        self.assertComplexTuplesAlmostEqual2( expected_data, actual_data, 1.0/32768.0, 1.0/32768.0 );

if __name__ == '__main__':
    gr_unittest.run(qa_crimson_source_sink_sob, "qa_crimson_source_sink_sob.xml")
