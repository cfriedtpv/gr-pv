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
from gnuradio import analog, blocks
from gnuradio import uhd

from crimson_qa import single_streamer_lb

#from crimson_sink import crimson_sink
#from crimson_source import crimson_source

import numpy as np

class qa_loopback_rx_phase( single_streamer_lb ):

    def setUp(self):
        single_streamer_lb.setUp( self )
        self.vsnk = {}

    def tearDown(self):
        single_streamer_lb.tearDown( self )
        for k,snk in self.vsnk.iteritems():
            snk.reset()

    def define_flowgraph( self ):

        self._flowgraph_defined = True

        ##################################################
        # Blocks
        ##################################################

        channels = self.get_channels_rx() # rx_channels == tx_channels for straight loopback configuration

        self.D( "getting rx streamers.." )
        rx_streamers = self.get_streamers_rx()
        self.D( "getting tx streamers.." )
        tx_streamers = self.get_streamers_tx()

        self.D( "creating cosine signal source.." )
        src = analog.sig_source_c( self.get_rate_tx( channels[ 0 ] ), analog.GR_COS_WAVE, 10e3, 0.01 )
        for c in channels:
            self.D( "creating vector sink for channel {0}".format( chr( ord( 'A' ) + c ) ) )
            self.vsnk[ c ] = blocks.vector_sink_c()

        ##################################################
        # Connections
        ##################################################
        already = {}
        for i,rx in rx_streamers.iteritems():
            if rx in already:
                continue
            already[ rx ] = 1

            channels = self.get_streamer_channels_rx( rx )
            for j in np.arange( 0, len( channels ) ):
                self.D( "connecting vector sink for RX streamer {0}, position {1} for channel {2} ".format( i, j, chr( ord( 'A' ) + channels[ j ] ) ) )
                self._tb.connect( ( rx, j ), ( self.vsnk[ channels[ j ] ], 0 ) )

        already = {}
        for i,tx in tx_streamers.iteritems():
            if tx in already:
                continue
            already[ tx ] = 1

            channels = self.get_streamer_channels_tx( tx )
            for j in np.arange( 0, len( channels ) ):
                self.D( "connecting cosine signal source for TX streamer {0}, channel {1} ".format( i, chr( ord( 'A' ) + channels[ j ] ) ) )
                self._tb.connect( ( src, 0 ), ( tx, j ) )

        self.D( "flowgraph defined!" )

    def test_000_rx_phase( self ):
        ##################################################
        # Variables
        ##################################################

        self.set_debug( True )

        time_now = uhd.time_spec_t( 0.0 )
        self.set_time_now( time_now.get_real_secs() )

        samp_rate = 1e6
        channels = [0,1,2,3]
        sob = 8
        nseconds = 1.0
        nsamples = int( nseconds * samp_rate )

        self.set_channels_tx( channels ) # parent class crimson_qa.straight_loopback sets this for both tx and rx
        self.set_rate_rx( samp_rate )
        self.set_rate_tx( samp_rate )
        self.set_start_time_rx( time_now.get_real_secs() + sob )
        self.set_start_time_tx( time_now.get_real_secs() + sob )
        # rx receives samples until the flow graph is killed
        #self.set_nsamps_rx( nsamples )
        self.set_nsamps_rx( nsamples )

        ntrials = 3
        phi = np.zeros( ( ntrials, len( channels ) - 1 ) )

        for trial in np.arange( 0, ntrials ):

            trial_start = time.time()

            self.D( 80 * '#' )
            self.D( "{0}BEGINNING TRIAL {1}".format( 30 * ' ', trial ) )
            self.D( 80 * '#' )

            self.common_setup()
            self.run_flowgraph_with_shutdown()


            #expected_data = np.asarray( tuple( chrp ) )
            f = {}
            for c in channels:
                f[ c ] = np.real( np.asarray( self.vsnk[ c ].data() ) )
                if 0 == len( f[ c ] ):
                    print( "SKIPPING ANALYSIS BECAUSE NO SAMPLES WERE RECEIVED!!!!!!" )
                else:
                    f[ c ] /= np.max( np.abs( f[ c ] ) )
                    self.vsnk[ c ].reset()

            for i in range( 0, len( channels ) - 1 ):
                if 0 != len( f[ i + 1 ] ) and 0 != len( f[ 0 ] ) :
                    phi[ trial, i ] = np.mean( np.arctan2( f[ i + 1 ], f[ 0 ] ) * 180 / np.pi )

            trial_stop = time.time()
            self.D( "trial {0} took {1} s".format( trial, trial_stop - trial_start ) )

        ##################################################
        # Verify Results
        ##################################################


#         plt.figure( 1 )
#         plt.plot( t, f[ 0 ], 'r', t, f[ 1 ], 'y', t, f[ 2 ], 'g', t, f[ 3 ], 'b'  )
#         plt.show()
#
#         plt.figure( 2 )
#         plt.plot( t, phi[ 1 ], 'y', t, phi[ 2 ], 'g', t, phi[ 3 ], 'b' )
#         plt.show()

        self.D( "done!" )
        #self.assertEqual( len( expected_data ), len( actual_data[ 0 ] ) )
        #self.assertComplexTuplesAlmostEqual2( expected_data, actual_data, 1.0/32768.0, 1.0/32768.0 );

if __name__ == '__main__':
    gr_unittest.run( qa_single_streamer_loopback, "qa_single_streamer_loopback.xml" )
