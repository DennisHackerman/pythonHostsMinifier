#!/usr/bin/env python3

from urllib.request import urlopen
import re


hosts_url = 'https://someonewhocares.org/hosts/zero/hosts' # Dan Pollock's hosts file
#hosts_url = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts' # StevenBlack's hosts file

hosts_header = ( # header of final hosts file (useful local redirects)
    '127.0.0.1 localhost',
    '127.0.0.1 localhost.localdomain',
    '127.0.0.1 local',
    '255.255.255.255 broadcasthost',
    '::1 localhost',
    '::1 ip6-localhost',
    '::1 ip6-loopback',
    'fe80::1%lo0 localhost',
    'ff00::0 ip6-localnet',
    'ff00::0 ip6-mcastprefix',
    'ff02::1 ip6-allnodes',
    'ff02::2 ip6-allrouters',
    'ff02::3 ip6-allhosts',

    '127.0.0.1 kubernetes.docker.internal',
    '0.0.0.0 0.0.0.0'
    )

# pattern and redirection address for ipv4
entry_pattern = re.compile("([0-9]{1,3}\.){3}[0-9]{1,3}\s+(\S+\.)+\S+") # also accepts '999.999.999.999', but the adress will be removed anyway so it's fine
redirect_address = '0.0.0.0'


def main():
    print('Downloading the hosts source...')

    with urlopen(hosts_url) as hosts_source:
        print('Parsing the hosts source...')

        hosts_content = hosts_source.read().decode('utf_8').split('\n') # create list of all lines in hosts source

        hosts_content = {normalizeEntry(entry) for entry in hosts_content} # normalize entries, and remove duplicates by creating a set
        hosts_content -= {entry.split()[-1] for entry in hosts_header} # remove duplicates of header entries
        hosts_content -= {'\n','', None} # remove empty lines

        with open('hosts', mode='w', encoding='utf_8') as hosts_file: # write file
            print('Writing the output to \'hosts\'...')

            for entry in hosts_header: # write header first
                hosts_file.write(f'{entry}\n')

            hosts_file.write('\n')

            for domain in sorted(hosts_content): # write domain entries, sorted alphabetically
                hosts_file.write(f'{redirect_address} {domain}\n')

            print('Done!')


def normalizeEntry(entry: str) -> str:
    entry = entry.split('#')[0] # remove comments
    entry = entry.strip() # remove trailing whitespaces

    if isValidEntry(entry):
        return entry.split()[-1] # return only domain
    else:
        return None

def isValidEntry(entry: str) -> bool:

    return entry_pattern.fullmatch(entry) is not None # Match object is none if it doesn't match



main()
