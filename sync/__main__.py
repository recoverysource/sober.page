#!/usr/bin/env python3
'''
Utility script to perform synchronization operations for sober.page URLs.

See "options.py" or "python3 -m sync --help" for usage.
'''
import logging

# Local imports
import sync.cloudflare
import sync.hugo
import sync.nginx
import sync.options


def main():
    '''
    Primary script logic
    '''
    # Read command line arguments
    options = sync.options.parser().parse_args()

    # Set log level (from options)
    logging.getLogger().setLevel(options.loglevel.upper())

    # Load source data from hugo
    logging.debug(f'Reading input data from {options.data}')
    hugo_data = sync.hugo.load_yaml(options.data)
    source_data = sync.hugo.normalize(hugo_data)

    # [-n] Generate an nginx map file
    if options.genmap:
        logging.info(f'Generating nginx map file at {options.mapfile}')
        sync.nginx.make_map(source_data, options.mapfile)

    # [-r] Sync DNS records with current provider
    if options.records:
        logging.info('Synchronizing DNS with cloudflare')
        sync.cloudflare.push_dns(source_data)


if __name__ == '__main__':
    main()
