#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK_Example
# Author: OBATS team
# Description: FSK_Example
# GNU Radio version: v3.8.2.0-57-gd71cd177

from gnuradio import blocks
import numpy
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time


class fsk_example(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "FSK_Example")

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
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(5000, 0)
        self.blocks_vco_c_0 = blocks.vco_c(48000, 15708, .500)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 48000,True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, 1056)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(.068)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(.850)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1024))), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.osmosdr_sink_0, 0))






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
