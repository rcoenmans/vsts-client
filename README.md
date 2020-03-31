# Azure DevOps (VSTS) & TFS Client
A client library for working with Azure DevOps (formerly VSTS) and TFS projects, areas/iterations, sprints, work items and tasks written in Python.

Please feel free to send me a pull request if you've fixed a bug or added a feature.
## Installation
```
pip install vsts-client
```
## Connecting to Azure DevOps
In order to connect to Azure DevOps, you need to obtain a [personal access token](https://docs.microsoft.com/en-us/vsts/integrate/get-started/authentication/pats).  
```python
# Import the VstsClient module
from vstsclient.vstsclient import VstsClient

# Initialize the VSTS client using the Azure DevOps url and personal access token
client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
```
Or you can still use visualstudio.com. 
```python
client = VstsClient('<account>.visualstudio.com', '<personalaccesstoken>')
```
### What about TFS?
To connect to an on-premises TFS environment you supply the server name and port number (default is 8080).
```python
client = VstsClient('tfs.contoso.com:8080', '<personalaccesstoken>')
```
The VSTS client will pick the `DefaultCollection` by default. You can specify a different collection using the optional `collection` parameter.
```python
client = VstsClient('tfs.contoso.com:8080', '<personalaccesstoken>', '<your collection>')
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

client   = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')

# StateFilter options are WellFormed (default), New, Deleting, CreatePending and All
projects = client.get_projects(StateFilter.WELL_FORMED) 
``` 
### Get a team project
```python
from vstsclient.vstsclient import VstsClient

client  = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
project = client.get_project('Contoso')
```
### Create a team project
Create a team project in a Azure DevOps account using the given `SourceControlType` and `ProcessTemplate`.
```python
from vstsclient.vstsclient import VstsClient
from vstsclient.constants import (
    ProcessTemplate,
    SourceControlType
)

client  = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
project = client.create_project(
    'Contoso',                  # Project name 
    'A project description',    # Project description
    SourceControlType.GIT,      # Source control type: Git or Tfvc
    ProcessTemplate.AGILE)      # Process template: Agile, Scrum or CMMI
```
## Areas and Iterations
All work items have an area and an iteration field. The values that these fields can have are defined in the [classification hierarchies](http://msdn.microsoft.com/en-us/library/ms181692.aspx).
### Get a list of areas and iterations
#### Get the root area tree
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
areas  = client.get_areas('Contoso')
```
#### Get the area tree with 2 levels of children
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
areas  = client.get_areas('Contoso', 2)

for area in areas.children:
    print(area.name)
```
#### Get the root iteration tree
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
iterations = client.get_iterations('Contoso')
```
#### Get the iteration tree with 2 levels of children
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
iterations = client.get_iterations(
    'Contoso',  # Team project name 
    2)          # Hierarchy depth

for iteration in iterations.children:
    print(iteration.name)
```
### Get an area and iteration
#### Get an area
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
area = client.get_area('Contoso', 'Area 1')
```
#### Get an iteration
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
iteration = client.get_iteration('Contoso', 'Sprint 1')
```
### Create an area and iteration
#### Create an area
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
area = client.create_area(
    'Contoso',  # Team project name
    'Area 1')   # Area name
```
#### Create an iteration
```python
from vstsclient.vstsclient import VstsClient

start_date  = datetime.datetime.utcnow()                # Sprint starts today
finish_date = start_date + datetime.timedelta(days=21)  # Ends in 3 weeks

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
iteration = client.create_iteration(
    'Contoso',          # Team project name 
    'Sprint 1',         # Iteration name
    start_date,         # Start date
    finish_date)        # End date
```
## Work items
### By IDs
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
workitems = client.get_workitems_by_id('1,2,3,5,8,13,21,34')
```
### Get a work item
```python
from vstsclient.vstsclient import VstsClient

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
workitem = client.get_workitem(13)
```
### Create a work item
When you create a work item, you can provide values for any of the work item fields.
```python
from vstsclient.vstsclient import VstsClient
from vstsclient.models import JsonPatchDocument, JsonPatchOperation
from vstsclient.constants import SystemFields, MicrosoftFields

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')

# Create a JsonPatchDocument and provide the values for the work item fields
doc = JsonPatchDocument()
doc.add(JsonPatchOperation('add', SystemFields.TITLE, 'Work item 1'))
doc.add(JsonPatchOperation('add', SystemFields.DESCRIPTION, 'Work item description.'))
doc.add(JsonPatchOperation('add', SystemFields.TAGS, 'tag1; tag2'))

# Create a new work item by specifying the project and work item type
workitem = client.create_workitem(
    'Contoso',          # Team project name
    'User Story',       # Work item type (e.g. Epic, Feature, User Story etc.)
    doc)                # JsonPatchDocument with operations
```
### Update work items
```python
from vstsclient.vstsclient import VstsClient
from vstsclient.models import JsonPatchDocument, JsonPatchOperation
from vstsclient.constants import SystemFields

client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')

# Create a JsonPatchDocument and provide the values for the fields to update
doc = JsonPatchDocument()
doc.add(JsonPatchOperation('replace', SystemFields.TITLE, 'Work item 2'))

# Update work item id 13
workitem = client.update_workitem(13, doc)
``` 
#### Change work item type
> Only supported on Azure DevOps (not on TFS).
```python
client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
client.change_workitem_type(13, 'Task')
```
#### Move a work item
> Only supported on Azure DevOps (not on TFS).
```python
client = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')

# To move a work item, provide the Team Project, Area path and Iteration path to move to
client.move_workitem(13, 'Contoso', 'Contoso', 'Sprint 1')
``` 
#### Add a tag
```python
tags = ['Tag1', 'Tag2']
client.add_tags(13, tags)
```
#### Add a link
```python
from vstsclient.constants import LinkTypes

feature = client.get_workitem(1)        # Get a feature
userstory = client.get_workitem(2)      # Get a user story

# Create a parent/child link between the feature and the userstory
client.add_link(userstory.id, feature.id, LinkTypes.PARENT, 'Adding this user story to feature x')

# Note that you can create the same link the other way around
client.add_link(feature.id, userstory.id, LinkTypes.CHILD, 'Adding user story x to this feature')
```
#### Add an attachment
To attach a file to a work item, upload the attachment to the attachment store using `upload_attachment`, then attach it to the work item.
```python
workitem   = client.get_workitem(1) 
attachment = None

# Upload the attachment to the attachment store
with open('./example.png', 'rb') as f:
    attachment = client.upload_attachment('example.png', f)
            
# Link the attachment to the work item
client.add_attachment(workitem.id, attachment.url, 'Linking example.png to a work item')
```
#### Update work items bypassing rules
Bypassing the rules engine allows you to modify work item fields without any restrictions, for example you can assign a work item to a user no longer in the organization.

> To modify the `System.CreatedBy`, `System.CreatedDate`, `System.ChangedBy`, or `System.ChangedDate` fields, you must be a member of the Project Collection Service Acccounts group.
```python
doc = JsonPatchDocument()
doc.add(JsonPatchOperation('add', SystemFields.CHANGED_BY, 'Woody <woody@contoso.com>'))
doc.add(JsonPatchOperation('add', SystemFields.CHANGED_DATE, '01-01-2018'))

# Set the bypass_rules parameter to True
client.update_workitem(13, doc, bypass_rules=True)
``` 
> `System.CreatedBy` and `System.CreatedDate` can only be modified using bypass rules on work item creation, i.e. the first revision of a work item. 
```python
# Set the Created By and Created Date fields
doc = JsonPatchDocument()
doc.add(JsonPatchOperation('add', SystemFields.TITLE, 'Work item 1'))
doc.add(JsonPatchOperation('add', SystemFields.DESCRIPTION, 'Work item description.'))
doc.add(JsonPatchOperation('add', SystemFields.CREATED_BY, 'Woody <woody@contoso.com>'))
doc.add(JsonPatchOperation('add', SystemFields.CREATED_DATE, '01-01-2018'))

# Set the bypass_rules parameter to True
client.create_workitem('Contoso', 'User Story', doc, bypass_rules=True)
``` 
### Delete a work item
```python
client.delete_workitem(1)
```
## Access team and team members in a project
### Get all teams in a project in a project
```python
from vstsclient.vstsclient import VstsClient

client   = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
for team in client.get_teams('project name')['value']:
    print(str(team))
```
### Get members of all teams in a project
```python
from vstsclient.vstsclient import VstsClient

client   = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
project_name = 'project name'
for team in client.get_teams(project_name)['value']:
	for dev in client.get_team_members(project_name, team['id'])['value']:
		print(dev['identity']['displayName']] + ': ' + dev['identity']['uniqueName'])
```
## Fields
### Create a field
Create a new field.
```python
from vstsclient.vstsclient import VstsClient

client   = VstsClient('dev.azure.com/<account>', '<personalaccesstoken>')
name     = 'New work item field'
ref_name = 'new.work.item.field'

field = client.create_field(
    name,                   # Name 
    ref_name,               # Reference name
    'Contoso',              # Project name
    'Field description',    # Field description
    'string',               # Field type: boolean, string, dateTime, integer, double, guid, html, identity, plainText, etc.
    'workItem',             # Field usage: none, tree, workItem, workItemLink or workItemTypeExtension
    [{                      # Supported operations
        'referenceName': 'SupportedOperations.Equals',
        'name': '='
    }])
```
### Get a field
```python
ref_name = 'new.workitem.field' # Name or reference name
prj_name = 'Contoso'            # Project name

field = client.get_field(ref_name, prj_name)
```
### Delete a field
```python
ref_name = 'new.workitem.field' # Name or reference name
prj_name = 'Contoso'            # Project name

client.delete_field(ref_name, prj_name)
```
## Work item query language (WIQL)
### Run a query
```python
# Specifying the team project is optional
query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'User Story A'"
result = client.query(query, 'Contoso')

for row in result.rows:
    workitem_id = row['id']
    workitem = client.get_workitem(id)
```
> Note that the query returns a list of work item ids