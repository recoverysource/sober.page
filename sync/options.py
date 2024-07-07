#!/usr/bin/env python3
'''
Runtime options
'''
import argparse


def parser():
    '''
    Load and parse command line arguments
    '''
    # Template
    parser = argparse.ArgumentParser(
            usage='python3 -m sync [-h] [actions] <options>',
            description='Synchronize sober.page data with various destinations',
            epilog='At least one [action] must be provided.',
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=30))

    # Actions
    actions = parser.add_argument_group('actions')
    actions.add_argument(
        '-n',
        dest='genmap',
        action='store_true',
        help='Generate an nginx map file')
    actions.add_argument(
        '-r',
        dest='records',
        action='store_true',
        help='Synchronize DNS records')

    # Options
    parser.add_argument(
        '-m',
        dest='mapfile',
        action='store',
        metavar='<path>',
        default='/etc/nginx/canonical_redirects.map',
        help='Location of generated Nginx map file')
    parser.add_argument(
        '-d',
        dest='data',
        action='store',
        metavar='<path>',
        default='./data/domains.yaml',
        help='YAML file containing DNS data')
    parser.add_argument(
        '-l',
        dest='loglevel',
        action='store',
        metavar='<level>',
        default='INFO',
        help='Log level (DEBUG, INFO*, WARNING, ERROR)')

    return parser
