#!/usr/bin/env python
import yaml, json
from subprocess import Popen, PIPE

CONFIG_FILE = "config.yaml"

def read_config(filename):
    with open(filename, "r") as f:
        return yaml.load(f)

def run():
    config=read_config(CONFIG_FILE)
    output_report = {}
    
    if config['build']:
        cmd = config['build']['build_system']
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        output_report['build_stdout'] = stdout
        #output_report['build_stderr'] = json.dumps(stderr)
        output_report['build_stderr'] = stderr
        if p.returncode != 0:
            return json.dumps(output_report)

    if config['run_nosetests']:
        cmd = ['nosetests', 
              '--with-xunit',
              '--xunit-file='+config['nose_report_file'] ]

        pid = Popen(cmd,stdout=PIPE,stderr=PIPE)
        stdout, stderr = pid.communicate()
        output_report['test_stdout']=stdout
        output_report['test_stderr']=stderr

    return json.dumps(output_report)

if __name__ == "__main__":
    print run()
