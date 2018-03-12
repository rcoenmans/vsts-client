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

class MicrosoftFields(object):
    VALUE_AREA = '/fields/Microsoft.VSTS.Common.ValueArea'

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