from covid19_outbreak_simulator.plugin import BasePlugin


#
# This plugin changes parameters
#
class setparam(BasePlugin):

    def __init__(self, *args, **kwargs):
        # this will set self.simualtor, self.logger
        super(setparam, self).__init__(*args, **kwargs)

    def get_parser(self):
        parser = super(setparam, self).get_parser()
        parser.description = 'Change parameters of simulation.'
        parser.prog = '--plugin setparam'
        parser.add_argument(
            '--susceptibility',
            nargs='+',
            help='''Weight of susceptibility. The default value is 1, meaning everyone is
                equally susceptible. With options such as
                "--susceptibility nurse=1.2 patients=0.8" you can give weights to different
                groups of people so that they have higher or lower probabilities to be
                infected.''')
        parser.add_argument(
            '--symptomatic-r0',
            nargs='+',
            help='''Production number of symptomatic infectors, should be specified as a single
                fixed number, or a range, and/or multipliers for different groups such as
                A=1.2. For example "--symptomatic-r0 1.4 2.8 nurse=1.2" means a general R0
                ranging from 1.4 to 2.8, while nursed has a range from 1.4*1.2 and 2.8*1.2.'''
        )
        parser.add_argument(
            '--asymptomatic-r0',
            nargs='+',
            help='''Production number of asymptomatic infectors, should be specified as a single
                fixed number, or a range and/or multipliers for different groups'''
        )
        parser.add_argument(
            '--incubation-period',
            nargs='+',
            help='''Incubation period period, should be specified as "lognormal" followed by two
                numbers as mean and sigma, or "normal" followed by mean and sd, and/or
                multipliers for different groups. Default to "lognormal 1.621 0.418"'''
        )
        parser.add_argument(
            '--handle-symptomatic',
            nargs='*',
            help='''How to handle individuals who show symptom, which should be "keep" (stay in
                population), "remove" (remove from population), and "quarantine" (put aside until
                it recovers). all options can be followed by a "proportion", and quarantine can
                be specified as "quarantine_7" etc to specify duration of quarantine. Default to
                "remove", meaning all symptomatic cases will be removed from population.'''
        )
        parser.add_argument(
            '--prop-asym-carriers',
            nargs='*',
            help='''Proportion of asymptomatic cases. You can specify a fix number, or two
            numbers as the lower and higher CI (95%%) of the proportion. Default to 0.10 to 0.40.
            Multipliers can be specified to set proportion of asymptomatic carriers
            for particular groups.''')

        return parser

    def apply(self, time, population, args=None):
        # change parameter
        self.simulator.model.params.set_symptomatic_r0(args.symptomatic_r0)
        self.simulator.model.params.set_asymptomatic_r0(args.asymptomatic_r0)
        self.simulator.model.params.set_incubation_period(
            args.incubation_period)
        self.simulator.model.params.set_susceptibility(args.susceptibility)
        self.simulator.model.params.set_prop_asym_carriers(
            args.prop_asym_carriers)

        if args.handle_symptomatic:
            self.simulator.simu_args.handle_symptomatic = args.handle_symptomatic

        pars = {}
        if args.symptomatic_r0:
            pars['symptomatic_r0'] = args.symptomatic_r0
        if args.asymptomatic_r0:
            pars['asymptomatic_r0'] = args.asymptomatic_r0
        if args.incubation_period:
            pars['incubation_period'] = args.incubation_period
        if args.susceptibility:
            pars['susceptibility'] = args.susceptibility
        if args.prop_asym_carriers:
            pars['prop_asym_carriers'] = args.prop_asym_carriers
        if args.handle_symptomatic:
            pars['handle_symptomatic'] = args.handle_symptomatic
        param = ','.join(f'{x}={y}' for x, y in pars.items())
        self.logger.write(
            f'{self.logger.id}\t{time:.2f}\tDYNAMIC_R\t.\t{param}\n')
        return []
