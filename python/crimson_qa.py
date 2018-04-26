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
        self.tb = gr.top_block()
        self.reset()

    def tearDown(self):
        self.tb = None

    def reset( self ):
        
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
        if not isinstance( start_time, numbers.Real ) or start_time <= 0.0:
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
        if not isinstance( start_time, numbers.Real ) or start_time <= 0.0:
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

    def shutdown( self, tb, delay ):
        time.sleep( delay )
        tb.stop()
        
    def shutdown_delay( self ):
        
        d = []
        
        rx_streamers = self.get_streamers_rx()
        tx_streamers = self.get_streamers_tx()
        
        # max of
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
                    d.append( self._start_time_rx[ c ] - self._time_now + self._nsamps_rx[ c ] / self._rate_rx[ c ] + 0.1 )
                
        already = {}
        for k,tx in tx_streamers.iteritems():
            if tx in already:
                continue
            already[ tx ] = 1

            channels = self.get_streamer_channels_tx( tx )
            # second, set streamer properties that can still be set on a per-channel basis            
            for c in channels:
                if self._nsamps_tx[ c ] is not None:
                    d.append( self._start_time_tx[ c ] - self._time_now + self._nsamps_tx[ c ] / self._rate_tx[ c ] + 0.1 )
        
        d = sorted( d )
        
        return d[ -1 ]

    def run_flowgraph_with_shutdown( self ):
        shutdown_thread = threading.Thread( group = None, target = self.shutdown, name = "shutdown", args = ( self.tb, self.shutdown_delay(), ) )
        shutdown_thread.start()
        self.tb.run()

    def common_setup( self ):
        already = {}

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
                continue
            already[ rx ] = 1

            channels = self.get_streamer_channels_rx( rx )

            # first, set common properties used by all channels for a specific streamer
            rx.set_samp_rate( self.get_rate_rx( channels[ 0 ] ) )

            # second, set streamer properties that can still be set on a per-channel basis            
            for i in range( 0, len( channels ) ):
                rx.set_center_freq( self.get_freq_rx( channels[ i ] ), i )
                rx.set_gain( self.get_gain_rx( channels[ i ] ), i )

        #
        # TX Setup
        #

        already = {}
        for k,tx in tx_streamers.iteritems():
            if tx in already:
                continue
            already[ tx ] = 1
            
            channels = self.get_streamer_channels_tx( tx )
            
            # first, set common properties used by all channels for a specific streamer
            tx.set_samp_rate( self.get_rate_tx( channels[ 0 ] ) )
            
            # second, set streamer properties that can still be set on a per-channel basis
            for i in range( 0, len( channels ) ):
                tx.set_center_freq( self.get_freq_tx( channels[ i ] ), i )
                tx.set_gain( self.get_gain_tx( channels[ i ] ), i )


        self.define_flowgraph()
        
        #
        # More RX Setup
        #

        already = {}
        for k,rx in rx_streamers.iteritems():
            if rx in already:
                continue
            already[ rx ] = 1

            if self._time_now is not None:
                rx.set_time_now( uhd.time_spec_t( self._time_now ) )
            if self.get_nsamps_rx( channels[ 0 ] ) is None:
                scmd = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_START_CONTIUOUS )
                scmd.num_samps = 0
            else:
                scmd = uhd.stream_cmd_t( uhd.stream_cmd_t.STREAM_MODE_NUM_SAMPS_AND_DONE )
                scmd.num_samps = self.get_nsamps_rx( channels[ 0 ] )
            scmd.stream_now = False
            scmd.time_spec = uhd.time_spec_t( self.get_start_time_rx( channels[ 0 ] ) )
            rx.issue_stream_cmd( scmd )

        #
        # More TX Setup
        #
        
        already = {}
        for k,tx in tx_streamers.iteritems():
            if tx in already:
                continue
            already[ tx ] = 1

            if self._time_now is not None:
                tx.set_time_now( uhd.time_spec_t( self._time_now ) )
            tx.set_start_time( uhd.time_spec_t( self.get_start_time_tx( channels[ 0 ] ) ) )            


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
