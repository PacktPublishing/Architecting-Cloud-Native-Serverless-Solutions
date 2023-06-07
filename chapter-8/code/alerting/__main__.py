from datetime import datetime
import sys
import json

def alert(msg):
    # Add your alerting implementation here
    # This code only logs to stdout
    print(msg)

def main(params):
    if params['temp'] >= params['threshold']:
        msg = "Device " + params['device'] + " temperature breached at " + str(datetime.fromtimestamp(int(params['timestamp'])))
        alert(msg)
        return({"message":msg})
    else:
        print(params)
        return({"message": "Device " + params['device'] + " temperature under threshold"})

if __name__ == '__main__':
    params=json.load(open(sys.argv[1]))
    main(params)
