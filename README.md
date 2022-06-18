<h1>Hosts File Minifier in Python</h1>
Downloads a text webpage and converts it to a file located in the same directory as the script. Removes Comments, unnecessary whitespaces, empty lines, duplicates and checks for a regex pattern.<br>
Can be executed with an argument to change the hosts source - for example:<br>
"python hostsMinifier.py www.hostsfile.com/hosts.txt"<br>
Default is "https://someonewhocares.org/hosts/zero/hosts".<br>

<h2>Code:</h2>

```
from urllib.request import urlopen
import re
import os
import sys


def main():

    if len(sys.argv) > 1:
        hostsSource = urlopen(sys.argv[1]).read().decode('utf-8')
    else:
        hostsSource = urlopen("https://someonewhocares.org/hosts/zero/hosts").read().decode('utf-8')

    hostsSource = hostsSource.split("\n")

    hostsContent = "127.0.0.1 localhost\n127.0.0.1 localhost.localdomain\n127.0.0.1 local\n255.255.255.255 broadcasthost\n::1 localhost\n::1 ip6-localhost\n::1 ip6-loopback\nfe80::1%lo0 localhost\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts\n0.0.0.0 0.0.0.0\n"
    pattern = re.compile("([0-9]{1,3}\.){3}[0-9]{1,3}\s\S+(\.\S+)+")

    for line in hostsSource:

        line = removeComments(line)
        line = removeWhitespaces(line)

        if not pattern.match(line):  # skip entry if it doesn't match the regex pattern
            continue

        if line not in hostsContent:  # check for duplicate entries
            hostsContent += ("\n" + line)

    hostsFile = open(os.path.join(os.path.dirname(__file__), 'hosts'), 'w')
    hostsFile.write(hostsContent)
    hostsFile.close()


def removeComments(line):
    index = line.find('#')

    if index != -1:
        line = line.split('#')[0]

    return line


def removeWhitespaces(line):
    line = re.sub(' +', ' ', line)
    return line.strip()


if __name__ == "__main__":
    main()
```
