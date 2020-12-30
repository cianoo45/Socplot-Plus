#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 2020

@author: Sergio Llana (@SergioMinuto90)
"""

from processing.eventing import StatsBombBasicPassingNetwork

from utils import parse_args


def buildPassNetwork(match_id,team):
    '''
    Instantiates a Passing Network Builder depending on the type of plot selected with the arguments
    in the command line.
    '''
    args = ['-m',str(match_id),'-t',team]
    parsed_args = parse_args(args)
    if parsed_args:
        plot_builder = StatsBombBasicPassingNetwork(parsed_args)
        plot_builder.build_and_save()

