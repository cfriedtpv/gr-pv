import numbers
import threading
import time

from abc import abstractmethod

from gnuradio import gr, gr_unittest, uhd

class base( gr_unittest.TestCase ):
    """Abstract base class for most of Crimson's signal QA
    """
    #__metaclass__ = ABCMeta

    def setUp(self):
        self._tb = gr.top_block()
        self.reset()

    def tearDown(self):
        self._tb = None
        self._rx_streamers = {}
        self._tx_streamers = {}

    def reset( self ):

        self._debug = False

        # this variable can be altered when we have more channels to work with
        # it's kind of arbitrary, to be honest
        N = 4

        self._time_now = None # use Crimson's clock

        self._channels_rx = range( 0, N )
        self._channels_tx = range( 0, N )

        # TODO: @CF: 20180322: create getters and setters for _addr_rx and _addr_tx
        self._addr_rx = {}
        self._addr_tx = {}

        self._cpu_format_rx = {}
        self._cpu_format_tx = {}
        self._rate_rx = {}
        self._rate_tx = {}
        self._freq_rx = {}
        self._freq_tx = {}
        self._gain_rx = {}
        self._gain_tx = {}
        self._start_time_rx = {}
        self._start_time_tx = {}
        self._nsamps_rx = {}
        self._nsamps_tx = {}

        self._rx_streamers = {}
        self._tx_streamers = {}

        self._streamer_channels_rx = {}
        self._streamer_channels_tx = {}

        self._flowgraph_defined = False

        #
        # Sane Default values
        #

        for c in range( 0, N ):
            self._cpu_format_rx[ c ] = "fc32"
            self._cpu_format_tx[ c ] = "fc32"
            self._rate_rx[ c ] = 1e6
            self._rate_tx[ c ] = 1e6
            self._freq_rx[ c ] = 15e6
            self._freq_tx[ c ] = 15e6
            self._gain_rx[ c ] = 0.0
            self._gain_tx[ c ] = 0.0
            self._start_time_rx[ c ] = 0.0
            self._start_time_tx[ c ] = 0.0
            self._nsamps_rx[ c ] = None
            self._nsamps_tx[ c ] = None

    def D( self, x ):
        if self._debug:
            if not self._rx_streamers and not self._tx_streamers :
                t = time.time()
            else:
                if self._rx_streamers:
                    streamers = self._rx_streamers
                else:
                    streamers = self._tx_streamers
                first = streamers[ 0 ]
                t = first.get_time_now().get_real_secs()
            #t = time.time()
            print( "{0}: {1}".format( t, x ) )

    def set_debug( self, en ):
        self._debug = en

    def get_channels_rx( self ):
        return self._rx_channels

    def set_channels_rx( self, channels ):
        for c in channels:
            if not isinstance( c, numbers.Integral ) or c < 0 or uhd.ALL_CHANS == c:
               raise ValueError( "not a valid channel {0}".format( c ) )
        keys = {}
        for e in channels:
            keys[ e ] = 1
        self._rx_channels = keys.keys()

    def get_channels_tx( self ):
        return self._tx_channels

    def set_channels_tx( self, channels ):
        for c in channels:
            if not isinstance( c, numbers.Integral ) or c < 0 or uhd.ALL_CHANS == c:
               raise ValueError( "not a valid channel {0}".format( c ) )
        keys = {}
        for e in channels:
            keys[ e ] = 1
        self._tx_channels = keys.keys()

    def get_cpu_format_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._cpu_format_rx[ chan ]

    def set_cpu_format_rx( self, fmt, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_rx():
                base.set_cpu_format_rx( self, fmt, c )
            return
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( fmt, basestring ):
            raise ValueError( "invalid sample format {0}".format( fmt ) )
        self._cpu_format_rx[ chan ] = fmt

    def get_cpu_format_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._cpu_format_tx[ chan ]

    def set_cpu_format_tx( self, fmt, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_tx():
                base.set_cpu_format_tx( self, fmt, c )
            return
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( fmt, basestring ):
            raise ValueError( "invalid sample format {0}".format( fmt ) )
        self._cpu_format_tx[ chan ] = fmt

    def get_rate_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._rate_rx[ chan ]

    def set_rate_rx( self, rate, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_rx():
                base.set_rate_rx( self, rate, c )
            return
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( rate, numbers.Real ) or rate <= 0.0:
            raise ValueError( "invalid sample rate {0}".format( rate ) )
        self._rate_rx[ chan ] = rate

    def get_rate_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._rate_tx[ chan ]

    def set_rate_tx( self, rate, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_tx():
                base.set_rate_tx( self, rate, c )
            return
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( rate, numbers.Real ) or rate <= 0.0:
            raise ValueError( "invalid sample rate {0}".format( rate ) )
        self._rate_tx[ chan ] = rate

    def get_freq_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._freq_rx[ chan ]

    def set_freq_rx( self, freq, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_rx():
                base.set_freq_rx( self, freq, c )
            return
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( freq, numbers.Real ) or freq <= 0.0:
            raise ValueError( "invalid frequency {0}".format( freq ) )
        self._freq_rx[ chan ] = freq

    def get_freq_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._freq_tx[ chan ]

    def set_freq_tx( self, freq, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_tx():
                base.set_freq_tx( self, freq, c )
            return
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( freq, numbers.Real ) or freq <= 0.0:
            raise ValueError( "invalid frequency {0}".format( freq ) )
        self._freq_tx[ chan ] = freq

    def get_gain_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._gain_rx[ chan ]

    def set_gain_rx( self, gain, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_rx():
                base.set_gain_rx( self, gain, c )
            return
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( gain, numbers.Real ) or gain <= 0.0:
            raise ValueError( "invalid gain {0}".format( gain ) )
        self._gain_rx[ chan ] = gain

    def get_gain_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._gain_tx[ chan ]

    def set_gain_tx( self, gain, chan):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_tx():
                base.set_gain_tx( self, gain, c )
            return
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( gain, numbers.Real ) or gain <= 0.0:
            raise ValueError( "invalid gain {0}".format( gain ) )
        self._gain_tx[ chan ] = gain

    def get_start_time_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._start_time_rx[ chan ]

    def set_start_time_rx( self, start_time, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_rx():
                base.set_start_time_rx( self, start_time, c )
            return
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( start_time, numbers.Real ) or start_time < 0.0:
            raise ValueError( "invalid start_time {0}".format( start_time ) )
        self._start_time_rx[ chan ] = start_time

    def get_start_time_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._start_time_tx[ chan ]

    def set_start_time_tx( self, start_time, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_tx():
                base.set_start_time_tx( self, start_time, c )
            return
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( start_time, numbers.Real ) or start_time < 0.0:
            raise ValueError( "invalid start_time {0}".format( start_time ) )
        self._start_time_tx[ chan ] = start_time

    def get_nsamps_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._nsamps_rx[ chan ]

    def set_nsamps_rx( self, nsamps, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_rx():
                base.set_nsamps_rx( self, nsamps, c )
            return
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( nsamps, numbers.Integral ) or nsamps < 0:
            raise ValueError( "invalid nsamps {0}".format( nsamps ) )
        if 0 == nsamps:
            nsamps = None
        self._nsamps_rx[ chan ] = nsamps

    def set_nsamps_tx( self, nsamps, chan = uhd.ALL_CHANS ):
        if uhd.ALL_CHANS == chan:
            for c in self.get_channels_tx():
                base.set_nsamps_tx( self, nsamps, c )
            return
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( nsamps, numbers.Integral ) or nsamps < 0:
            raise ValueError( "invalid nsamps {0}".format( nsamps ) )
        if 0 == nsamps:
            nsamps = None
        self._nsamps_tx[ chan ] = nsamps

    def set_time_now( self, time_now ):
        self._time_now = time_now

    @abstractmethod
    def define_flowgraph( self ):
        pass

    @abstractmethod
    def get_data_tx( self, chan ):
        pass

    @abstractmethod
    def get_data_rx( self, chan ):
        pass

    @abstractmethod
    def get_streamers_rx( self ):
        pass

    @abstractmethod
    def get_streamers_tx( self ):
        pass

    def get_streamer_channels_rx( self, streamer ):
        self.get_streamers_rx()
        return self._streamer_channels_rx[ streamer ]

    def get_streamer_channels_tx( self, streamer ):
        self.get_streamers_tx()
        return self._streamer_channels_tx[ streamer ]

    def shutdown_delay( self ):

        d = []

        rx_streamers = self.get_streamers_rx()
        tx_streamers = self.get_streamers_tx()

        # max ofself._tb.
        #   _start_time_rx[ i ] + _nsamps_rx[ i ] / _rate_rx[ i ] + 0.1 for all channels, i
        #   _start_time_tx[ i ] + _nsamps_tx[ i ] / _rate_tx[ i ] + 0.1 for all channels, i

        already = {}
        for k,rx in rx_streamers.iteritems():
            if rx in already:
                continue
            already[ rx ] = 1

            channels = self.get_streamer_channels_rx( rx )
            # second, set streamer properties that can still be set on a per-channel basis
            for c in channels:
                if self._nsamps_rx[ c ] is not None:
                    d.append( self._start_time_rx[ c ] - self._time_now + self._nsamps_rx[ c ] / self._rate_rx[ c ] )

        already = {}
        for k,tx in tx_streamers.iteritems():
            if tx in already:
                continue
            already[ tx ] = 1

            channels = self.get_streamer_channels_tx( tx )
            # second, set streamer properties that can still be set on a per-channel basis
            for c in channels:
                if self._nsamps_tx[ c ] is not None:
                    d.append( self._start_time_tx[ c ] - self._time_now + self._nsamps_tx[ c ] / self._rate_tx[ c ] )

        d = sorted( d )

        delay = d[ -1 ] + 3.0

        self.D( "shutdown delay is {0}".format( delay ) )

        return delay

    def shutdown( self, tb, delay ):
        time.sleep( delay )
        self.D( "stopping flowgraph.." )
        tb.stop()

    def run_flowgraph_with_shutdown( self ):
        self.D( "creating shutdown thread.." )
        shutdown_thread = threading.Thread( group = None, target = self.shutdown, name = "shutdown", args = ( self._tb, self.shutdown_delay(), ) )
        shutdown_thread.start()
        self.D( "running flowgraph.." )
        self._tb.run()

    def common_setup( self ):
        already = {}

        setup_start = time.time()

        rx_channels = self.get_channels_rx()
        tx_channels = self.get_channels_tx()
        rx_streamers = self.get_streamers_rx()
        tx_streamers = self.get_streamers_tx()

        #
        # RX Setup
        #

        already = {}
        for k,rx in rx_streamers.iteritems():
            if rx in already:
                self.D( "skipping rx {0}".format( rx ) )
                continue
            already[ rx ] = 1

            channels = self.get_streamer_channels_rx( rx )

            # first, set common properties used by all channels for a specific streamer
            if self.get_rate_rx( channels[ 0 ] ) != rx.get_samp_rate():
                self.D( "setting sample rate for rx streamer {0} to {1}".format( k, self.get_rate_rx( channels[ 0 ] ) ) )
                rx.set_samp_rate( self.get_rate_rx( channels[ 0 ] ) )
                sr = rx.get_samp_rate()
                if sr != self.get_rate_rx( channels[ 0 ] ):
                    self.D( "storing corrected sample rate for rx streamer {0} of {1}".format( k, sr ) )
                    for c in channels:
                        self.set_rate_rx( sr, c )

            # second, set streamer properties that can still be set on a per-channel basis
            for i in range( 0, len( channels ) ):
                if self.get_freq_rx( channels[ i ] ) != rx.get_center_freq( channels[ i ] ):
                    #self.D( "center freq on channel {0} is currently {1}".format( chr( ord( 'A' ) + channels[ i ] ), rx.get_center_freq( channels[ i ] ) ) )
                    self.D( "setting center freq for rx channel {0} to {1}".format( chr( ord( 'A' ) + channels[ i ] ), self.get_freq_rx( channels[ i ] ) ) )
                    rx.set_center_freq( self.get_freq_rx( channels[ i ] ), i )
                    fc = rx.get_center_freq( channels[ i ] )
                    if self.get_freq_rx( channels[ i ] ) != fc:
                        self.D( "storing corrected center freq for rx channel {0} of {1}".format(  chr( ord( 'A' ) + channels[ i ] ), fc ) )
                        self.set_freq_rx( fc, channels[ i ] )
                if self.get_gain_rx( channels[ i ] ) != rx.get_gain( channels[ i ] ):
                    self.D( "setting gain for rx channel {0} to {1}".format( chr( ord( 'A' ) + channels[ i ] ), self.get_gain_rx( channels[ i ] ) ) )
                    rx.set_gain( self.get_gain_rx( channels[ i ] ), i )

        #
        # TX Setup
        #

        print( "len( tx_streamers ): {0}".format( len( tx_streamers ) ) )

        already = {}
        for k,tx in tx_streamers.iteritems():
            if tx in already:
                self.D( "skipping tx {0}".format( tx ) )
                continue
            already[ tx ] = 1

            channels = self.get_streamer_channels_tx( tx )

            # first, set common properties used by all channels for a specific streamer
            #if self.get_rate_tx( channels[ 0 ] ) != tx.get_samp_rate():
            if True:
                self.D( "setting sample rate for tx streamer {0} to {1}".format( k, self.get_rate_tx( channels[ 0 ] ) ) )
                tx.set_samp_rate( self.get_rate_tx( channels[ 0 ] ) )
                sr = tx.get_samp_rate()
                if sr != self.get_rate_tx( channels[ 0 ] ):
                    self.D( "storing corrected sample rate for tx streamer {0} of {1}".format( k, sr ) )
                    for c in channels:
                        self.set_rate_tx( sr, c )

            # second, set streamer properties that can still be set on a per-channel basis
            for i in range( 0, len( channels ) ):
                #if self.get_freq_tx( channels[ i ] ) != tx.get_center_freq( channels[ i ] ):
                if True:
                    #self.D( "center freq on channel {0} is currently {1}".format( chr( ord( 'A' ) + channels[ i ] ), tx.get_center_freq( channels[ i ] ) ) )
                    self.D( "setting center freq for tx channel {0} to {1}".format( chr( ord( 'A' ) + channels[ i ] ), self.get_freq_tx( channels[ i ] ) ) )
                    tx.set_center_freq( self.get_freq_tx( channels[ i ] ), i )
                    fc = tx.get_center_freq( channels[ i ] )
                    if self.get_freq_tx( channels[ i ] ) != fc:
                        self.D( "storing corrected center freq for tx channel {0} of {1}".format(  chr( ord( 'A' ) + channels[ i ] ), fc ) )
                        self.set_freq_tx( fc, channels[ i ] )
                #if self.get_gain_tx( channels[ i ] ) != tx.get_gain( channels[ i ] ):
                if True:
                    self.D( "setting gain for tx channel {0} to {1}".format( chr( ord( 'A' ) + channels[ i ] ), self.get_gain_tx( channels[ i ] ) ) )
                    tx.set_gain( self.get_gain_tx( channels[ i ] ), i )


        if not self._flowgraph_defined:
            self.define_flowgraph()

        #
        # More RX Setup
        #

        already = {}
        for k,rx in rx_streamers.iteritems():
            if rx in already:
                continue
            already[ rx ] = 1

            channels = self.get_streamer_channels_rx( rx )

            if self._time_now is not None:
                self.D( "setting rx streamer {0} time spec to {1}".format( k, self._time_now ) )
                rx.set_time_now( uhd.time_spec_t( self._time_now ) )

            if self.get_nsamps_rx( channels[ 0 ] ) is None:
                self.D( "setting rx streamer {0} mode to START_CONTINUOUS".format( k ) )
                scmd = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_START_CONTINUOUS )
                scmd.num_samps = 0
            else:
                scmd = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_NUM_SAMPS_AND_DONE )
                scmd.num_samps = self.get_nsamps_rx( channels[ 0 ] )
                self.D( "setting rx streamer {0} mode to NUM_SAMPS_AND_DONE with {1} samples".format( k, scmd.num_samps ) )

            scmd.stream_now = False
            scmd.time_spec = uhd.time_spec_t( self.get_start_time_rx( channels[ 0 ] ) )
            self.D( "setting rx streamer {0} start time to {1}".format( k, scmd.time_spec.get_real_secs() ) )
            rx.issue_stream_cmd( scmd )

        #
        # More TX Setup
        #

        already = {}
        for k,tx in tx_streamers.iteritems():
            if tx in already:
                continue
            already[ tx ] = 1

            channels = self.get_streamer_channels_tx( tx )

            # FIXME: @CF: 20180327: We currently do not differentiate between crimson devices by address
            # as a work-around for multiply setting "time now" on one crimson, this is commented out
            # *** NON-LOOPBACK TESTS WILL FAIL UNTIL THIS IS FIXED ***

#             if self._time_now is not None:
#                 self.D( "setting tx streamer {0} time spec to {1}".format( k, self._time_now ) )
#                 tx.set_time_now( uhd.time_spec_t( self._time_now ) )

            self.D( "setting tx streamer {0} start time to {1}".format( k, self.get_start_time_tx( channels[ 0 ] ) ) )
            tx.set_start_time( uhd.time_spec_t( self.get_start_time_tx( channels[ 0 ] ) ) )


        setup_stop = time.time()

        self.D( "common_setup() completed in {0} s".format( setup_stop - setup_start ) )

class straight_loopback( base ):
    """An abstract class for Crimson's signal QA where TX A is wired to RX A, etc.
    A given RX-TX channel pair will share the same frequency. Derived classes may
    impose further restraints.
    """

    def set_channels_rx( self, channels ):
        base.set_channels_rx( self, channels )
        base.set_channels_tx( self, channels )

    def set_channels_tx( self, channels ):
        self.set_channels_rx( channels )

    def set_freq_rx( self, freq, chan = uhd.ALL_CHANS ):
        base.set_freq_rx( self, freq, chan )
        base.set_freq_tx( self, freq, chan )

    def set_freq_tx( self, freq, chan = uhd.ALL_CHANS ):
        self.set_freq_rx( self, freq, chan )

    def set_freq( self, freq, chan = uhd.ALL_CHANS ):
        self.set_freq_tx( freq, chan )

    # TODO: @CF: 20180323: create a bunch of straight loopback tests here so that they
    # do not need to be replecated in derived classes


class multi_streamer_lb( straight_loopback ):
    """An abstract class for Crimson's signal QA where TX A is wired to RX A, etc.
    A given RX-TX channel pair will share the same frequency. RX channels, bzw
    TX channels may have different sample rates. The number and choices of RX channels
    is equal to the number and choices of TX channels. Several underlying streamers
    are used; one for each channel requested.
    """

    def get_streamers_rx( self ):
        if not self._rx_streamers:
            for c in self.get_channels_rx():
                channels = ( c, )
                stream_args = uhd.stream_args( cpu_format = self.get_cpu_format_rx( 0 ), otw_format = "sc16", channels = channels )
                streamer = uhd.usrp_source( uhd.device_addr_t( "" ), stream_args, False )
                self._rx_streamers[ c ] = streamer
                self._streamer_channels_rx[ streamer ] = channels
        return self._rx_streamers

    def get_streamers_tx( self ):
        if not self._tx_streamers:
            for c in self.get_channels_tx():
                channels = ( c, )
                stream_args = uhd.stream_args( cpu_format = self.get_cpu_format_tx( 0 ), otw_format = "sc16", channels = channels )
                streamer = uhd.usrp_sink( uhd.device_addr_t( "" ), stream_args )
                self.set_tx_streamer( c, streamer )
                self._streamer_channels_tx[ streamer ] = channels
        return self._tx_streamers


class single_streamer_lb( straight_loopback ):
    """An abstract class for Crimson's signal QA where TX A is wired to RX A, etc.
    A given RX-TX channel pair will share the same frequency. All RX channels, bzw
    TX channels will share a common sample rate. The number and choices of RX
    channels is equal to the number and choices of TX channels. One underlying RX
    and one underlying TX streamer is used for multiple channels.
    """

    def set_cpu_format_rx( self, fmt, chan = uhd.ALL_CHANS ):
        straight_loopback.set_cpu_format_rx( self, fmt )

    def set_cpu_format_tx( self, fmt, chan = uhd.ALL_CHANS ):
        straight_loopback.set_cpu_format_tx( self, fmt )

    def set_rate_rx( self, rate, chan = uhd.ALL_CHANS ):
        straight_loopback.set_rate_rx( self, rate )

    def set_rate_tx( self, rate, chan = uhd.ALL_CHANS ):
        straight_loopback.set_rate_tx( self, rate )

    def set_start_time_rx( self, start_time, chan = uhd.ALL_CHANS ):
        straight_loopback.set_start_time_rx( self, start_time )

    def set_start_time_tx( self, start_time, chan = uhd.ALL_CHANS ):
        straight_loopback.set_start_time_tx( self, start_time )

    def set_nsamps_rx( self, nsamps, chan = uhd.ALL_CHANS ):
        straight_loopback.set_nsamps_rx( self, nsamps )

    def set_nsamps_tx( self, nsamps, chan = uhd.ALL_CHANS ):
        straight_loopback.set_nsamps_tx( self, nsamps )

    def get_streamers_rx( self ):
        if not self._rx_streamers:
            channels = self.get_channels_rx()
            stream_args = uhd.stream_args( cpu_format = self.get_cpu_format_rx( channels[ 0 ] ), otw_format = "sc16", channels = channels )
            streamer = uhd.usrp_source( uhd.device_addr_t( "" ), stream_args, False )
            self._streamer_channels_rx[ streamer ] = channels
            for c in channels:
                self._rx_streamers[ c ] = streamer
        return self._rx_streamers

    def get_streamers_tx( self ):
        if not self._tx_streamers:
            channels = self.get_channels_tx()
            stream_args = uhd.stream_args( cpu_format = self.get_cpu_format_tx( channels[ 0 ] ), otw_format = "sc16", channels = channels )
            streamer = uhd.usrp_sink( uhd.device_addr_t( "" ), stream_args )
            self._streamer_channels_tx[ streamer ] = channels
            for c in channels:
                self._tx_streamers[ c ] = streamer
        return self._tx_streamers
