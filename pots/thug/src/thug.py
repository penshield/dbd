#!/usr/bin/env python
#
# thug.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA

import sys
import os
import getopt
import logging

from ThugAPI import *
from Plugins.ThugPlugins import *

log = logging.getLogger("Thug")
log.setLevel(logging.WARN)

configuration_path = "/etc/thug"

class Thug(ThugAPI):
    def __init__(self, args):
        ThugAPI.__init__(self, args, configuration_path)

    def usage(self):
        msg = """
Synopsis:
    Thug: Pure Python honeyclient implementation

    Usage:
        python thug.py [ options ] url

    Options:
        -h, --help              \tDisplay this help information
        -V, --version           \tDisplay Thug version
        -u, --useragent=        \tSelect a user agent (see below for values, default: winxpie60)
        -e, --events=           \tEnable comma-separated specified DOM events handling
        -w, --delay=            \tSet a maximum setTimeout/setInterval delay value (in milliseconds)
        -n, --logdir=           \tSet the log output directory
        -o, --output=           \tLog to a specified file
        -r, --referer           \tSpecify a referer
        -p, --proxy=            \tSpecify a proxy (see below for format and supported schemes)
        -l, --local             \tAnalyze a locally saved page
        -x, --local-nofetch     \tAnalyze a locally saved page and prevent remote content fetching
        -v, --verbose           \tEnable verbose mode
        -d, --debug             \tEnable debug mode
        -q, --quiet             \tDisable console logging
        -m, --no-cache          \tDisable local web cache
        -a, --ast-debug         \tEnable AST debug mode (requires debug mode)
        -g, --http-debug        \tEnable HTTP debug mode
        -t, --threshold         \tMaximum pages to fetch
        -E, --extensive         \tExtensive fetch of linked pages
        -T, --timeout=          \tSet the analysis timeout (in seconds)
        -B, --broken-url        \tSet the broken URL mode
        -y, --vtquery           \tQuery VirusTotal for samples analysis
        -s, --vtsubmit          \tSubmit samples to VirusTotal
        -b, --vt-apikey=        \tVirusTotal API key to be used at runtime
        -z, --web-tracking      \tEnable web client tracking inspection
        -N, --no-honeyagent     \tDisable HoneyAgent support

        Plugins:
        -A, --adobepdf=         \tSpecify the Adobe Acrobat Reader version (default: 9.1.0)
        -P, --no-adobepdf       \tDisable Adobe Acrobat Reader plugin
        -S, --shockwave=        \tSpecify the Shockwave Flash version (default: 10.0.64.0)
        -R, --no-shockwave      \tDisable Shockwave Flash plugin
        -J, --javaplugin=       \tSpecify the JavaPlugin version (default: 1.6.0.32)
        -K, --no-javaplugin     \tDisable Java plugin

        Classifiers:
        -Q, --urlclassifier     \tSpecify a list of additional (comma separated) URL classifier rule files
        -W, --jsclassifier      \tSpecify a list of additional (comma separated) JS classifier rule files
        -C, --sampleclassifier  \tSpecify a list of additional (comma separated) sample classifier rule files

        Logging:
        -F, --file-logging      \tEnable file logging mode (default: disabled)
        -Z, --json-logging      \tEnable JSON logging mode (default: disabled)
        -M, --maec11-logging    \tEnable MAEC11 logging mode (default: disabled)
        -G, --elasticsearch-logging\tEnable ElasticSearch logging mode (default: disabled)
        -D, --mongodb-address=  \tSpecify address and port of the MongoDB instance (format: host:port)

    Proxy Format:
        scheme://[username:password@]host:port (supported schemes: http, socks4, socks5)

    Available User-Agents:
"""
        for key, value in sorted(iter(log.ThugOpts.Personality.items()), key = lambda k_v: (k_v[1]['id'], k_v[0])):
            msg += "\t%s\t\t\t%s\n" % (key, value['description'], )

        print(msg)
        sys.exit(0)

    def analyze(self):
        p = getattr(self, 'run_remote', None)

        try:
            self.log_init(self.args)

            if p:
                ThugPlugins(PRE_ANALYSIS_PLUGINS, self)()
                p(self.args['url'])
                ThugPlugins(POST_ANALYSIS_PLUGINS, self)()
        except Exception , s:
            print("There was an exception")
            raise s

        self.log_event()

        return log


def main():
    if not os.getenv('THUG_PROFILE', None):
        Thug(sys.argv[1:])()
    else:
        import cProfile
        import pstats
        cProfile.run('Thug(sys.argv[1:])()', 'countprof')
        p = pstats.Stats('countprof')
        p.print_stats()

if __name__ == "__main__":
    main()
