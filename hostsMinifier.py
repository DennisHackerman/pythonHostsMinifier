from urllib.request import urlopen
import re
import os
import sys

def removeComments(line):
    index = line.find('#')

    if(index != -1):
        line = line.split('#')[0]

    return line

def removeWhitespaces(line):
    line = re.sub(' +', ' ', line)
    return line.strip()

pattern = re.compile("([0-9]{1,3}\.){3}[0-9]{1,3}\s\S+(\.\S+)+")

def isRegexOK(line):
    return pattern.match(line)

def main():
    if(len(sys.argv) > 1):
        hostsSource = urlopen(sys.argv[1]).read().decode('utf-8')
    else:
        hostsSource = urlopen("https://someonewhocares.org/hosts/zero/hosts").read().decode('utf-8')

    hostsSource = hostsSource.split("\n")

    hostsContent = "127.0.0.1 localhost\n127.0.0.1 localhost.localdomain\n127.0.0.1 local\n255.255.255.255 broadcasthost\n::1 localhost\n::1 ip6-localhost\n::1 ip6-loopback\nfe80::1%lo0 localhost\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts\n0.0.0.0 0.0.0.0\n"

    for line in hostsSource:
        line = removeComments(line)
        line = removeWhitespaces(line)
        if(not isRegexOK(line)):
            continue
        
        if not line in hostsContent:
            hostsContent += ("\n" + line)

    hostsFile = open(os.path.join(os.path.dirname(__file__), 'hosts'), 'w')
    hostsFile.write(hostsContent)
    hostsFile.close()

if __name__ == "__main__":
    main()
