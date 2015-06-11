# context-broker-periodical-action

The context-broker-periodical-action is a python software that allows to define periodical task related to Orion contextBroker as updatecontext, queryContext and discoverContextAvailability.

It links a ContextBroker with another service and  lets to provide real  time data from sources which have no problems with traffic at regular intervals.
The software includes the [DataManager](https://github.com/gzarrub/context-broker-periodical-action/blob/master/tools/DataManager.py), a library that makes easier to work with ContextBroker responses, so it's relatively accessible to adapt any type of data source.

# Installing the software

Run setup.py in order to install all python required packages
```
   python setup.py install
```

