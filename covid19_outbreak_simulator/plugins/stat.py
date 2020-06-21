import argparse
import random

from covid19_outbreak_simulator.plugin import BasePlugin
from covid19_outbreak_simulator.simulator import EventType


#
# This plugin take random samples from the population during evolution.
#
class stat(BasePlugin):

    # events that will trigger this plugin
    events = set()

    def __init__(self, *args, **kwargs):
        # this will set self.population, self.simualtor, self.logger
        super(stat, self).__init__(*args, **kwargs)

    def get_parser(self):
        parser = super(stat, self).get_parser()
        parser.prog = '--plugin stat'
        parser.description = 'Print STAT information'
        return parser

    def apply(self, time, args=None):
        if not super(stat, self).can_apply(time, args):
            return []

        res = {}
        res[f'n_recovered'] = len([
            x for x, ind in self.population.items()
            if ind.recovered not in (None, False)
        ])
        res[f'n_infected'] = len([
            x for x, ind in self.population.items()
            if ind.infected not in (False, None)
        ])
        res[f'n_popsize'] = len([x for x, ind in self.population.items()])
        res[f'incidence_rate'] = '0' if res[
            f'n_popsize'] == 0 else '{:.4f}'.format(res[f'n_infected'] /
                                                    res[f'n_popsize'])
        res[f'seroprevalence'] = '0' if res[
            f'n_popsize'] == 0 else '{:.4f}'.format(
                (res[f'n_recovered'] + res[f'n_infected']) / res[f'n_popsize'])

        groups = set([x.group for x in self.population.values()])
        for group in groups:
            if group == '':
                continue
            res[f'n_{group}_recovered'] = len([
                x for x, ind in self.population.items()
                if ind.recovered is True and ind.group == group
            ])
            res[f'n_{group}_infected'] = len([
                x for x, ind in self.population.items()
                if ind.infected not in (False, None) and ind.group == group
            ])
            res[f'n_{group}_popsize'] = len(
                [x for x, ind in self.population.items() if ind.group == group])
            res[f'{group}_incidence_rate'] = 0 if res[
                f'n_{group}_popsize'] == '0' else '{:.3f}'.format(
                    res[f'n_{group}_infected'] / res[f'n_{group}_popsize'])
            res[f'{group}_seroprevalence'] = 0 if res[
                f'n_{group}_popsize'] == '0' else '{:.3f}'.format(
                    (res[f'n_{group}_recovered'] + res[f'n_{group}_infected']) /
                    res[f'n_{group}_popsize'])
        param = ','.join(f'{k}={v}' for k, v in res.items())
        self.logger.write(
            f'{self.logger.id}\t{time:.2f}\t{EventType.STAT.name}\t.\t{param}\n'
        )

        return []