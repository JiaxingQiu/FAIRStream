""" MediTFDS processor object.

Module description details...

    Usage example:

"""
import dictionaries
from prep_id_pool import prep_id_pool
from prep_id_subset import prep_id_subset
import gnrt_tfds_cohort


class MediTFDSGenerator:
    def __init__(self):
        self.source_dict = dictionaries.source_dict
        self.variable_dict = dictionaries.variable_dict
        self.id_pool = prep_id_pool(self.source_dict)

    def __str__(self):
        return '\n'.join([
            f'Sources: {[self.source_dict[key]["info"] for key in self.source_dict.keys()]}',
            f'Variables: {[key for key in self.variable_dict.keys()]}',
            f'Number of total subjects: {len(self.id_pool)}'
        ])

    def defineEvent(self, binwidth, bins_before, bins_after, bins_gap=None):
        self.binwidth = binwidth
        self.bins_before = bins_before
        self.bins_after = bins_after
        if bins_gap is not None:
            self.bins_gap = bins_gap
        else:
            self.bins_gap = self.bins_before + self.bins_after

    def generateTFDS(self, nsbj):
        self.id_list = prep_id_subset(nsbj)
        self.dataset = gnrt_tfds_cohort(self.id_list, self.source_dict, self.variable_dict,
                                        self.binwidth, self.bins_before, self.bins_after, self.bins_gap)
