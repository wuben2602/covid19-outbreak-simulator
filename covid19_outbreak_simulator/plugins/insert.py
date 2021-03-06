import random

from covid19_outbreak_simulator.event import Event, EventType
from covid19_outbreak_simulator.plugin import BasePlugin
from covid19_outbreak_simulator.population import Individual


class insert(BasePlugin):

    # events that will trigger this plugin
    apply_at = 'after_core_events'

    def __init__(self, *args, **kwargs):
        # this will set self.simualtor, self.logger
        super(insert, self).__init__(*args, **kwargs)

    def get_parser(self):
        parser = super(insert, self).get_parser()
        parser.prog = '--plugin insert'
        parser.description = 'insert new individuals to the population'
        parser.add_argument(
            'popsize',
            nargs='+',
            help='''Population size, which should only
                add to existing populations''')
        parser.add_argument(
            '--prop-of-infected',
            type=float,
            default=1.0,
            help='''Proportion of infected. Default to 1, meaning all are infected.'''
        )
        parser.add_argument(
            '--leadtime',
            help='''With "leadtime" infections are assumed to happen before the simulation.
            This option can be a fixed positive number `t` when the infection happens
            `t` days before current time. If can also be set to 'any' for which the
            carrier can be any time during its course of infection, or `asymptomatic`
            for which the leadtime is adjust so that the carrier does not show any
            symptom at the time point (in incubation period for symptomatic case).
            All events triggered before current time are ignored.''')
        return parser

    def apply(self, time, population, args=None):
        events = []
        for ps in args.popsize:
            name = ps.split('=', 1)[0] if '=' in ps else ''
            sz = int(ps.split('=', 1)[1]) if '=' in ps else int(ps)

            if name not in population.subpops:
                raise ValueError(f'can only add to existing subpopulations')

            population.add([
                Individual(
                    f'{name}{idx}',
                    group=name,
                    susceptibility=getattr(self.simulator.model.params,
                                           f'susceptibility_multiplier_{name}',
                                           1),
                    model=self.simulator.model,
                    logger=self.logger) for idx in range(
                        population.subpops[name], population.subpops[name] + sz)
            ])

            n_infected = int(sz * args.prop_of_infected)
            for idx in range(population.subpops[name],
                             population.subpops[name] + n_infected):
                events.append(
                    Event(
                        time,
                        EventType.INFECTION,
                        target=f'{name}{idx}',
                        logger=self.logger,
                        by=None,
                        handle_symptomatic=self.simulator.simu_args
                        .handle_symptomatic,
                        leadtime=args.leadtime))
            population.subpops[name] += sz

        return events
