#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK_Example
# Author: OBATS team
# Description: FSK_Example
# GNU Radio version: 3.9.0.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import osmosdr
import time




class fsk_example(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "FSK_Example", catch_exceptions=True)

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(1e6)
        self.osmosdr_sink_0.set_center_freq(2.4e9, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(80, 0)
        self.osmosdr_sink_0.set_if_gain(80, 0)
        self.osmosdr_sink_0.set_bb_gain(80, 0)
        self.osmosdr_sink_0.set_antenna('TX1', 0)
        self.osmosdr_sink_0.set_bandwidth(5000, 0)
        self.network_udp_source_0 = network.udp_source(gr.sizeof_char, 1, 5005, 0, 81, False, False, False)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                48000,
                200,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.blocks_vco_c_0 = blocks.vco_c(48000, 15708, .500)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 48000,True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.network_udp_source_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))





def main(top_block_cls=fsk_example, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
