#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 2020

@author: Sergio Llana (@SergioMinuto90)
"""


from pandas import json_normalize
from abc import ABC, abstractmethod
import pandas as pd
import warnings
from statsbombpy import sb
import sbpUtils
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

from processing import PassingNetworkBuilder
from utils import read_json


class StatsBombPassingNetwork(PassingNetworkBuilder, ABC):
    def __init__(self, args):
        self.team_name = args.team_name
        self.match_id = args.match_id

        self.plot_name = None
        self.df_events = None
        self.plot_title = None
        self.names_dict = None
        self.plot_legend = None
        self.num_minutes = None
        self.player_position = None
        self.pair_pass_value = None
        self.pair_pass_count = None
        self.player_pass_value = None
        self.player_pass_count = None

    def read_data(self):
        """
        Read StatsBomb eventing data of the selected 'match_id', generating a pandas DataFrame
        with the events and a dictionary of player names and nicknames.
        Switching to using API over local files has added benefit of parsing player names
        to remove non UTF-8 characters
        """
        # Player name translation dict
        name_dict = sbpUtils.get_lineups(match_id=self.match_id)

        self.names_dict = name_dict

        # Pandas dataframe containing the events of the match
        apiEvents = sb.events(self.match_id,fmt="dict")
        newApiEvents =[]
        for event in apiEvents.keys():
            newApiEvents.append(apiEvents[event])

        event_df = json_normalize(newApiEvents, sep="_").assign(match_id=self.match_id)
        self.df_events = event_df

    def compute_total_minutes(self):
        """
        Compute the maximum number of minutes that are used for the passing network.
        The idea is not to have more/less than 11 players in the team because of substitutions or red cards.
        """
        first_red_card_minute = self.df_events[self.df_events.foul_committed_card_name.isin(["Second Yellow", "Red Card"])].minute.min()
        first_substitution_minute = self.df_events[self.df_events.type_name == "Substitution"].minute.min()
        max_minute = self.df_events.minute.max()

        self.num_minutes = min(first_substitution_minute, first_red_card_minute, max_minute)

    def set_text_info(self):
        """
        Set the plot's name, title and legend information based on the customization chosen with the command line arguments.
        """
        # Name of the .PNG in the plots/ folder
        self.plot_name = "statsbomb_match{0}_{1}".format(self.match_id, self.team_name)

        # Title of the plot
        opponent_team = [x for x in self.df_events.team_name.unique() if x != self.team_name][0]
        self.plot_title ="{0}'s passing network against {1} (StatsBomb eventing data)".format(self.team_name, opponent_team)

        # Information in the legend
        color_meaning =  "number of passes"
        self.plot_legend = "Location: pass origin\nSize: number of passes\nColor: {0}".format(color_meaning)

    @abstractmethod
    def prepare_data(self):
        pass

    @staticmethod
    def _statsbomb_to_point(location, max_width=120, max_height=80):
        '''
        Convert a point's coordinates from a StatsBomb's range to 0-1 range.
        '''
        return location[0] / max_width, 1-(location[1] / max_height)


class StatsBombBasicPassingNetwork(StatsBombPassingNetwork):
    def __init__(self, args):
        super(StatsBombBasicPassingNetwork, self).__init__(args)

    def prepare_data(self):
        """
        Prepares the five pandas DataFrames that 'draw_pass_map' needs.
        """
        # We select all successful passes done by the selected team before the minute
        # of the first substitution or red card.
        df_passes = self.df_events[(self.df_events.type_name == "Pass") &
                                   (self.df_events.pass_outcome_name.isna()) &
                                   (self.df_events.team_name == self.team_name) &
                                   (self.df_events.minute < self.num_minutes)].copy()

        # If available, use player's nickname instead of full name to optimize space in plot
        df_passes["pass_recipient_name"] = df_passes.pass_recipient_name.apply(lambda x: self.names_dict[x] if self.names_dict[x] else x)
        df_passes["player_name"] = df_passes.player_name.apply(lambda x: self.names_dict[x] if self.names_dict[x] else x)

        # In this type of plot, both the size and color (i.e. value) mean the same: number of passes
        self.player_pass_count = df_passes.groupby("player_name").size().to_frame("num_passes")
        self.player_pass_value = df_passes.groupby("player_name").size().to_frame("pass_value")

        # 'pair_key' combines the names of the passer and receiver of each pass (sorted alphabetically)
        df_passes["pair_key"] = df_passes.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
        self.pair_pass_count = df_passes.groupby("pair_key").size().to_frame("num_passes")
        self.pair_pass_value = df_passes.groupby("pair_key").size().to_frame("pass_value")

        # Average pass origin's coordinates for each player
        df_passes["origin_pos_x"] = df_passes.location.apply(lambda x: self._statsbomb_to_point(x)[0])
        df_passes["origin_pos_y"] = df_passes.location.apply(lambda x: self._statsbomb_to_point(x)[1])
        self.player_position = df_passes.groupby("player_name").agg({"origin_pos_x": "median", "origin_pos_y": "median"})

