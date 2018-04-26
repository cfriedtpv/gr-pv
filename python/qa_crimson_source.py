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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gnuradio import uhd


class qa_crimson_source (gr_unittest.TestCase):

    # Generic SetUp and TearDown

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    # simplest test - essentially just start and stop

#     def test_001_t (self):
#         # set up fg
#         self.tb.run ()
#         # check data

    # utility function for test_002
    def tb_killer_fn( self, delay ):
        #print( "tb_killer_fn(): sleep {0} s".format( delay ) )
        time.sleep( delay )
        #print( "tb_killer_fn(): stopping top block now".format( delay ) )
        self.tb.stop()

    def test_001_num_samps_and_done (self):

        ##################################################
        # Variables
        ##################################################
        samp_rate = 1e6
        freq = 15e6
        gain = 0
        channels = [0]
        sob = 5
        nsamples = 16384

        ##################################################
        # Blocks
        ##################################################
        stream_args = uhd.stream_args( cpu_format = "fc32", otw_format = "sc16", channels = ( channels ) )
        csrc = uhd.usrp_source( uhd.device_addr_t( "" ), stream_args, False )

        # issue a stop to flush out the channels
        sc = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_STOP_CONTINUOUS )
        csrc.issue_stream_cmd( sc )

        csrc.set_samp_rate( samp_rate )
        csrc.set_center_freq( freq )
        csrc.set_gain( gain )

        vsnk = blocks.vector_sink_c()

        ##################################################
        # Connections
        ##################################################
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
        
        stop_time = uhd.time_spec_t( start_time.get_real_secs() + nsamples / samp_rate + 5 )
        print( "Stop Time is {0}".format( stop_time.get_real_secs() ) )

        print( "Setting rx start time to {0}".format( start_time.get_real_secs() ) )
        sc = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_NUM_SAMPS_AND_DONE )
        sc.num_samps = nsamples
        sc.stream_now = False
        sc.time_spec = start_time
        csrc.issue_stream_cmd( sc )

        killer = threading.Thread( group = None, target = self.tb_killer_fn, name = "killer", args = ( ( stop_time.get_real_secs() - start_time.get_real_secs() ), ) )
        killer.start()

        print( "Receiving {0} samples".format( sc.num_samps ) )

        ##################################################
        # Run Flow Graph
        ##################################################
        time_now = csrc.get_time_now()
        print( "Calling run. Time now is {0}".format( time_now.get_real_secs() ) )
        self.tb.run ()
        time_now = csrc.get_time_now()
        print( "returned from run. Time now is {0}".format( time_now.get_real_secs() ) )

        ##################################################
        # Verify Results
        ##################################################

        expected_len = sc.num_samps
        actual_len = len( vsnk.data() )

        self.assertEqual( actual_len, expected_len )

if __name__ == '__main__':
    gr_unittest.run(qa_crimson_source, "qa_crimson_source.xml")
