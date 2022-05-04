###############################################################################
# Custom ExecuteScript code to publish real-time metrics in Graphite.
# Will read the 'metric' and 'value' dynamic properties of an ExecuteScript.
# The value of the properties can be derived using the NiFi Expression language.
# For example, ${fileSize():toNumber()}
# 
#
# Variables provided in scope by script engine:
#
#    session - ProcessSession
#    context - ProcessContext
#    log - ComponentLog
#    REL_SUCCESS - Relationship
#    REL_FAILURE - Relationship
###############################################################################
import socket
import sys
import time

def publish_grafana(content):
    s = socket.socket()
    try:
        # Carbon aggregator port
        s.connect(('your.graphite.docker.ip', 2023))
    except:
        log.error('Error connecting to Carbon listener. {}'.format(sys.exc_info()[0]))
        return False
    try:
        s.sendall(str.encode(str(content)))
    except:

        log.error('Error sending Graphite metric.')
        return False
    s.close()
    return True

flowFile = session.get()
if flowFile != None:
    error = False
    publish = False
    metric_str = str(metric.evaluateAttributeExpressions(flowFile).getValue())
    value_str = str(value.evaluateAttributeExpressions(flowFile).getValue())
    # Check metric name validity (prefix etc.), rollback session if error->true
    if not metric_str.startswith('metric.'):
        log.error('Metric name must start with "metric."')
        session.rollback()
        error = True 
    # Validate value, rollback session if error->true
    try:
        tmp = int(value_str)
    except:
        log.error('Value must be integer.')
        session.rollback()
        error = True
    # Try to publish if no errors so far
    if not error:
        now = int(time.time())
        publish = publish_grafana("%s %d %d\n" %(metric_str, int(value_str), now))
        if not publish:
            session.rollback()
    # Transfer to success if no error and publishing was successful.
    if (not error) and (publish):
        session.transfer(flowFile, REL_SUCCESS)
