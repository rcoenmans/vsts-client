# VSTS/TFS Client
This project provides a client library, written in Python, for working with VSTS/TFS projects, areas/iterations, sprints, work items and tasks.

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
from vstsclient.constants import (
    ProcessTemplate,
    SourceControlType
)

client  = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
project = client.create_project(
    'Self-flying car',                      # Project name 
    'A project for our self-flying car',    # Project description
    SourceControlType.GIT,                  # Source control type: Git or Tfvc
    ProcessTemplate.AGILE)                  # Process template: Agile, Scrum or CMMI
```

## Areas and Iterations
All work items have an area and an iteration field. The values that these fields can have are defined in the [classification hierarchies](http://msdn.microsoft.com/en-us/library/ms181692.aspx).
### Get a list of areas and iterations
#### Get the root area tree
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
areas  = client.get_areas('Self-flying car')
```
#### Get the area tree with 2 levels of children
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
areas  = client.get_areas('Self-flying car', 2)

for area in areas.children:
    print(area.name)
```
#### Get the root iteration tree
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
iterations = client.get_iterations('Self-flying car')
```
#### Get the iteration tree with 2 levels of children
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
iterations = client.get_iterations(
    'Self-flying car',                  # Team project name 
    2)                                  # Hierarchy depth

for iteration in iterations.children:
    print(iteration.name)
```
### Get an area and iteration
#### Get an area
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
area = client.get_area('Self-flying car', 'Engine')
```
#### Get an iteration
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
iteration = client.get_iteration('Self-flying car', 'Sprint 1')
```
### Create an area and iteration
#### Create an area
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
area = client.create_area(
    'Self-flying car',          # Team project name
    'Engine')                   # Area name
```
#### Create an iteration
```python
from vstsclient.vstsclient import VstsClient

start_date  = datetime.datetime.utcnow()                # Sprint starts today
finish_date = start_date + datetime.timedelta(days=21)  # Ends in 3 weeks

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
iteration = client.create_iteration(
    'Self-flying car',          # Team project name 
    'Sprint 1',                 # Iteration name
    start_date,                 # Start date
    finish_date)                # End date
```

## Work items
### By IDs
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
workitems = client.get_workitems_by_id('13,21,34')
```
### Get a work item
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
workitem = client.get_workitem(13)
```
### Create a work item
When you create a work item, you can provide values for any of the work item fields.
```python
from vstsclient.vstsclient import VstsClient
from vstsclient.models import JsonPatchDocument
from vstsclient.models import JsonPatchOperation
from vstsclient.constants import SystemFields 
from vstsclient.constants import MicrosoftFields

# Create a JsonPatchDocument and provide the values for the work item fields
doc = JsonPatchDocument()
doc.add(JsonPatchOperation('add', SystemFields.TITLE, 'Left-side wing'))
doc.add(JsonPatchOperation('add', SystemFields.DESCRIPTION, 'Create a left-side wing for our self-flying car.'))
doc.add(JsonPatchOperation('add', SystemFields.CREATED_BY, 'Woody <woody@contoso.com>'))
doc.add(JsonPatchOperation('add', SystemFields.ASSIGNED_TO, 'Buzz <buzz@contoso.com>'))
doc.add(JsonPatchOperation('add', SystemFields.TAGS, 'wing; left'))
doc.add(JsonPatchOperation('add', MicrosoftFields.VALUE_AREA, 'Architectural'))

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
workitem = client.create_workitem(
    'Self-flying car'           # Team project name
    'User Story'                # Work item type (e.g. Epic, Feature, User Story etc.)
    doc)                        # JsonPatchDocument with operations
```
### Update work items
```python
from vstsclient.vstsclient import VstsClient
from vstsclient.models import JsonPatchDocument
from vstsclient.models import JsonPatchOperation
from vstsclient.constants import SystemFields 
from vstsclient.constants import MicrosoftFields

# Create a JsonPatchDocument and provide the values for the fields to update
doc = JsonPatchDocument()
doc.add(JsonPatchOperation('replace', SystemFields.TITLE, 'Right-side wing'))

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')
workitem = client.update_workitem(
    13                          # Work item id
    doc)                        # JsonPatchDocument with operations
``` 

## Work item query language (WIQL)
### Run a query
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('contoso.visualstudio.com', '<personalaccesstoken>')

# Note that the query returns a list of work item ids
query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'User Story A'"
result = client.query(query, 'Self-flying car')

for row in result.rows:
    workitem_id = row['id']
    workitem = client.get_workitem(id)
```