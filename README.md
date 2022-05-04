# Some example code for NiFi

## Publish metrics

A custom NiFi ExecuteScript code in Python, to publish metrics to a time-series database like Graphite.  
Will work with the official [Grahpite Docker image](https://registry.hub.docker.com/r/graphiteapp/graphite-statsd/) from the Docker registry.

---

Credits:  

How to read a property in NiFi: 
- https://stackoverflow.com/questions/55572625/read-external-properties-in-executescript-processor/55575949  

ExecuteScript samples:
- https://github.com/SherifEldeeb/nifi-executescript-samples/tree/master/src/test/resources/python
- https://github.com/sucitw/python-script-in-NiFi

NiFi Expression language docs:
- https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html

