import numbers

from abc import abstractmethod

class base( object ):
    """Abstract base class for most of Crimson's signal QA
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__( self ):
        
        self._channels_rx = [ 0, 1, 2, 3 ]
        self._channels_tx = [ 0, 1, 2, 3 ]
  
        # TODO: @CF: 20180322: create getters and setters for _addr_rx and _addr_tx
        self._addr_rx = {}
        self._addr_tx = {}
  
        self._rate_rx = {}
        self._rate_tx = {}
        self._freq_rx = {}
        self._freq_tx = {}
        self._gain_rx = {}
        self._gain_tx = {}
        self._start_time_rx = {}
        self._start_time_tx = {}
        self._nsamps_rx = {}
        
        for c in self._channels:
            self._rate_rx.append( 1e6 )
            self._rate_tx.append( 1e6 )
            self._freq_rx.append( 15e6 )
            self._freq_tx.append( 15e6 )
            self._gain_rx.append( 0.0 )
            self._gain_tx.append( 0.0 )
            self._start_time_rx.append( 0.0 )
            self._start_time_tx.append( 0.0 )
            self._nsamps_rx.append( None )

    def get_channels_rx( self ):
        return self._rx_channels

    def set_channels_rx( self, channels ):
        for c in channels:
            if not isinstance( c, numbers.Integral ) or c < 0:
               raise ValueError( "not a valid channel {0}".format( c ) )
        self._rx_channels = []
        for c in channels: 
            _rx_channels.append( c )

    def get_channels_tx( self ):
        return self._tx_channels1

    def set_channels_tx( self, channels ):
        for c in channels:
            if not isinstance( c, numbers.Integral ) or c < 0:
               raise ValueError( "not a valid channel {0}".format( c ) )
        self._tx_channels = []
        for c in channels: 
            _tx_channels.append( c )

    def get_samp_rate_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._samp_rate_rx[ chan ]

    def set_samp_rate_rx( self, chan, rate ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( rate, numbers.Real ) or rate <= 0.0:
            raise ValueError( "invalid sample rate {0}".format( rate ) )
        self._samp_rate_rx[ chan ] = rate


    def get_samp_rate_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._samp_rate_tx[ chan ]

    def set_samp_rate_tx( self, chan, rate ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( rate, numbers.Real ) or rate <= 0.0:
            raise ValueError( "invalid sample rate {0}".format( rate ) )
        self._samp_rate_tx[ chan ] = rate

    def get_freq_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._freq_rx[ chan ]

    def set_freq_rx( self, chan, freq ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( freq, numbers.Real ) or freq <= 0.0:
            raise ValueError( "invalid frequency {0}".format( freq ) )
        self._freq_rx[ chan ] = freq

    def get_freq_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._freq_tx[ chan ]

    def set_freq_tx( self, chan, freq ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( freq, numbers.Real ) or freq <= 0.0:
            raise ValueError( "invalid frequency {0}".format( freq ) )
        self._freq_tx[ chan ] = freq

    def get_gain_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._gain_rx[ chan ]

    def set_gain_rx( self, chan, gain ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( gain, numbers.Real ) or gain <= 0.0:
            raise ValueError( "invalid gain {0}".format( gain ) )
        self._gain_rx[ chan ] = gain

    def get_gain_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._gain_tx[ chan ]

    def set_gain_tx( self, chan, gain ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( gain, numbers.Real ) or gain <= 0.0:
            raise ValueError( "invalid gain {0}".format( gain ) )
        self._gain_tx[ chan ] = gain

    def get_start_time_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._start_time_rx[ chan ]

    def set_start_time_rx( self, chan, start_time ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( start_time, numbers.Real ) or start_time <= 0.0:
            raise ValueError( "invalid start_time {0}".format( start_time ) )
        self._start_time_rx[ chan ] = start_time

    def get_start_time_tx( self, chan ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        return self._start_time_tx[ chan ]

    def set_start_time_tx( self, chan, start_time ):
        if chan not in self.get_channels_tx():
            raise ValueError( "invalid tx channel {0}".format( chan ) )
        if not isinstance( start_time, numbers.Real ) or start_time <= 0.0:
            raise ValueError( "invalid start_time {0}".format( start_time ) )
        self._start_time_tx[ chan ] = start_time

    def get_nsamps_rx( self, chan ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        return self._nsamps_rx[ chan ]

    def set_nsamps_rx( self, chan, nsamps ):
        if chan not in self.get_channels_rx():
            raise ValueError( "invalid rx channel {0}".format( chan ) )
        if not isinstance( nsamps, numbers.Integral ) or nsamps < 0:
            raise ValueError( "invalid nsamps {0}".format( nsamps ) )
        if 0 == nsamps:
            nsamps = None
        self._nsamps_rx[ chan ] = nsamps

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
    def get_streamers_rx( self, uhd ):
        pass

    @abstractmethod
    def get_streamers_tx( self, uhd ):
        pass


class straight_loopback( base ):
    """An abstract class for Crimson's signal QA where TX A is wired to RX A, etc.
    A given RX-TX channel pair will share the same frequency. Derived classes may
    impose further restraints.
    """
    
    @abstractmethod
    def __init__( self ):
        pass
    
    def set_channels_rx( self, channels ):
        base.set_channels_rx( self, channels )
        base.set_channels_tx( self, channels )

    def set_channels_tx( self, channels ):
        self.set_channels_rx( channels )

    def set_freq_rx( self, chan, freq ):
        for c in self.get_channels_rx():
            base.set_freq_rx( self, chan, freq )

    def set_freq_tx( self, chan, freq ):
        for c in self.get_channels_rx():
            base.set_freq_rx( self, chan, freq )


class multi_streamer_lb( straight_loopback ):
    """An abstract class for Crimson's signal QA where TX A is wired to RX A, etc.
    A given RX-TX channel pair will share the same frequency. RX channels, bzw
    TX channels may have different sample rates. The number and choices of RX channels
    is equal to the number and choices of TX channels.
    """

    @abstractmethod
    def __init__( self ):
        base.__init__( self )
        
    def get_streamers_rx( self, uhd ):
        # TODO: @CF: 20180322: create streamers using addrs
        streamers = {}
        return streamers

    def get_streamers_tx( self, uhd ):
        # TODO: @CF: 20180322: create streamers using addrs
        streamers = {}
        return streamers

class single_streamer_lb( straight_loopback ):
    """An abstract class for Crimson's signal QA where TX A is wired to RX A, etc.
    A given RX-TX channel pair will share the same frequency. All RX channels, bzw
    TX channels will share a common sample rate. The number and choices of RX
    channels is equal to the number and choices of TX channels.
    """

    @abstractmethod
    def __init__( self ):
        base.__init__( self )
        
    def set_samp_rate_rx( self, chan, rate ):
        for c in self.channels_rx():
            straight_loopback.set_rate_rx( self, c, rate )

    def set_samp_rate_tx( self, chan, rate ):
        for c in self.channels_tx():
            straight_loopback.set_rate_tx( self, c, rate )

    def set_start_time_rx( self, chan, start_time ):
        for c in self.channels_rx():
            straight_loopback.set_start_time_rx( self, c, start_time )

    def set_start_time_tx( self, chan, start_time ):
        for c in self.channels_tx():
            straight_loopback.set_start_time_tx( self, c, start_time )
    
    def set_nsamps_rx( self, chan, nsamps ):
        for c in self.get_channels_rx():
            straight_loopback.set_nsamps_rx( self, c, nsamps )

    def get_streamers_rx( self, uhd ):
        # TODO: @CF: 20180322: create streamers using addrs
        streamers = {}
        return streamers

    def get_streamers_tx( self, uhd ):
        # TODO: @CF: 20180322: create streamers using addrs
        streamers = {}
        return streamers

