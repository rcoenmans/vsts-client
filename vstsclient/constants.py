# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2018 Robbie Coenmans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

class ProcessTemplate(object):
    AGILE = 'adcc42ab-9882-485e-a3ed-7678f01f66bc'
    SCRUM = '6b724908-ef14-45cf-84f8-768b5384da45'
    CMMI  = '27450541-8e31-4150-9947-dc59f998fc01'

class SourceControlType(object):
    GIT  = 'Git'
    TFVC = 'Tfvc'

class StateFilter(object):
    WELL_FORMED    = 'WellFormed'
    CREATE_PENDING = 'CreatePending'
    DELETING       = 'Deleting'
    NEW            = 'New'
    ALL            = 'All'

class SystemFields(object):
    TITLE          = '/fields/System.Title'
    DESCRIPTION    = '/fields/System.Description'

    AREA_PATH      = '/fields/System.AreaPath'
    TEAM_PROJECT   = '/fields/System.TeamProject'
    ITERATION_PATH = '/fields/System.IterationPath' 

    WORKITEM_TYPE  = '/fields/System.WorkItemType' 
    STATE          = '/fields/System.State' 
    REASON         = '/fields/System.Reason'

    ASSIGNED_TO    = '/fields/System.AssignedTo'      
    CREATED_DATE   = '/fields/System.CreatedDate' 
    CREATED_BY     = '/fields/System.CreatedBy' 
    CHANGED_DATE   = '/fields/System.ChangedDate' 
    CHANGED_BY     = '/fields/System.ChangedBy'

    TAGS           = '/fields/System.Tags' 
    HISTORY        = '/fields/System.History'

class MicrosoftFields(object):
    VALUE_AREA   = '/fields/Microsoft.VSTS.Common.ValueArea'
    PRIORITY     = '/fields/Microsoft.VSTS.Common.Priority'

    REPRO_STEPS  = '/fields/Microsoft.VSTS.TCM.ReproSteps'

    STORY_POINTS = '/fields/Microsoft.VSTS.Scheduling.StoryPoints'

class State(object):
    ACTIVE   = 'Active'
    CLOSED   = 'Closed'
    NEW      = 'New'
    REMOVED  = 'Removed'
    RESOLVED = 'Resolved'

class LinkTypes(object):
    CHILD   = 'System.LinkTypes.Hierarchy-Forward' 
    PARENT  = 'System.LinkTypes.Hierarchy-Reverse'
    RELATED = 'System.LinkTypes.Related'

    ATTACHED_FILE = 'AttachedFile'
    HYPERLINK     = 'Hyperlink'