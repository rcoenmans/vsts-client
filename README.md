# VSTS Client
This project provides a client library, written in Python, for working with VSTS/TFS projects, areas/iterations, sprints, workitems and tasks.

## Installation
```
pip install vsts-client
```

## Connecting to VSTS
In order to connect to VSTS, you need to obtain a [personal access token](https://docs.microsoft.com/en-us/vsts/integrate/get-started/authentication/pats).  
```python
# Import the VstsClient module
from vstsclient.vstsclient import VstsClient

# Initialize the VSTS client using the VSTS instance and personal access token
client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
```
### What about TFS?
To connect to an on-premises TFS environment you supply the server name and port number (default is 8080).
```python
client = VstsClient('tfs.contoso.com:8080', '<personalaccesstoken>')
```
### Connecting from behind a proxy
```python
client.set_proxy('proxy.contoso.com', 8080, '<username>', '<password>')
```

## Team Projects
### Get a list of team projects
Get all team projects in the project collection that the authenticated user has access to.
```python
from vstsclient.vstsclient import VstsClient
from vstsclient.constants import StateFilter

client   = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')

# StateFilter options are WellFormed (default), New, Deleting, CreatePending and All
projects = client.get_projects(StateFilter.WELL_FORMED) 
``` 
### Get a team project
```python
from vstsclient.vstsclient import VstsClient

client  = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
project = client.get_project('Self-flying car')
```
### Create a team project
Create a team project in a Visual Studio Team Services account using the given `SourceControlType` and `ProcessTemplate`.
```python
from vstsclient.vstsclient import VstsClient
from vstsclient.model import (
    ProcessTemplate,
    SourceControlType
)

client  = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
project = client.create_project(
    'Self-flying car',                      # Project name 
    'A project for our self-flying car',    # Project description
    SourceControlType.Git,                  # Source control type: Git or Tfvc
    ProcessTemplate.Agile)                  # Process template: Agile, Scrum or CMMI
```
##