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

import matplotlib as mpl
import matplotlib.pyplot as plt

from gnuradio import gr, gr_unittest
from gnuradio import analog
from gnuradio import blocks
from gnuradio import uhd

from crimson_qa import single_streamer_lb

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

class qa_single_streamer_loopback( single_streamer_lb ):

    def setUp( self ):
        single_streamer_lb.setUp( self )
        self.vsnk = blocks.vector_sink_c()

    def tearDown( self ):
        single_streamer_lb.tearDown( self )
        self.vsnk.reset()

    def define_flowgraph( self ):
        ##################################################
        # Blocks
        ##################################################

        channels = self.get_channels_rx() # rx_channels == tx_channels for straight loopback configuration
        rx_streamers = self.get_streamers_rx()
        tx_streamers = self.get_streamers_tx()

        #vsrc = analog.sig_source_c( self.get_rate_tx( channels[ 0 ] ), analog.GR_COS_WAVE, 1e6, 0.01 )
        vsrc = blocks.vector_source_c( self.chrp )
        vsrc.set_repeat( False )

        ##################################################
        # Connections
        ##################################################
        for i in range( 0, len( channels ) ):
            self._tb.connect( ( vsrc, i ), ( tx_streamers[ channels[ i ] ], i ) )
            self._tb.connect( ( rx_streamers[ channels[ i ] ], i ), ( self.vsnk, i ) )

    def test_000_num_samps_and_done_with_1s_sob_ch_a( self ):
        ##################################################
        # Variables
        ##################################################

        self.set_debug( True )

        time_now = uhd.time_spec_t( 0.0 )
        #time_now = uhd.time_spec_t( time.time() )
        self.set_time_now( time_now.get_real_secs() )

        samp_rate = 1e6
        channels = [0]
        sob = 5
        chirp_rate = 10
        nseconds = 1.0
        nsamples = int( nseconds * samp_rate )

        chrp = gen_chirp( samp_rate = samp_rate, T = 1.0 / chirp_rate )
        chrp = np.repeat( chrp, int( nseconds * chirp_rate ) )
        self.chrp = chrp

        self.set_channels_tx( channels ) # parent class crimson_qa.straight_loopback sets this for both tx and rx
        self.set_rate_rx( samp_rate )
        self.set_rate_tx( samp_rate )
        self.set_start_time_rx( time_now.get_real_secs() + sob )
        self.set_start_time_tx( time_now.get_real_secs() + sob )
        self.set_nsamps_rx( nsamples )
        self.set_nsamps_tx( nsamples )

        self.common_setup()

        self.run_flowgraph_with_shutdown()

        ##################################################
        # Verify Results
        ##################################################

        expected_data = np.real( np.asarray( tuple( chrp ) ) )
        actual_data = np.real( np.asarray( self.vsnk.data() ) )

        N1 = len( expected_data )
        N2 = len( actual_data )

        print( "N1: {0} N2: {1}".format( N1, N2 ) )

        if N1 == N2:

            expected_data /= np.max( np.abs( expected_data ), axis = 0 )
            actual_data /= np.max( np.abs( actual_data ), axis = 0 )

            N = N1
            t1 = time_now.get_real_secs() + sob
            t2 = t1 + N / samp_rate
            t = np.arange( t1, t2, 1.0/samp_rate )
            f1 = np.real( expected_data )
            f2 = np.real( actual_data )

            mpl.rcParams['agg.path.chunksize'] = 10000

            plt.plot( t, f1, 'b--', t, f2, 'r-' )
            plt.show()

        self.assertEqual( len( expected_data ), len( actual_data ) )
        #self.assertComplexTuplesAlmostEqual2( expected_data, actual_data, 1.0/32768.0, 1.0/32768.0 );

if __name__ == '__main__':
    gr_unittest.run( qa_single_streamer_loopback, "qa_single_streamer_loopback.xml" )
