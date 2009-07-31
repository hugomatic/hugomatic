#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# You will find the latest version of this code at the following address:
# http://hugomatic.ca/source/cncOnline
#
# You can contact me at the following email address:
# hugo@hugomatic.ca
#


"""
the toolkit module's purpose is to load the web or the local toolkit.
It detects if its working in a cgi environment by looking in the environment
for CGI specific variables. 
"""

import os
import sys

def isWebApplication():
    if os.environ.has_key('REQUEST_METHOD'):
        return True
    return False # TkInter app


if isWebApplication():
    from hugomatic.web.toolkitW import *
else:    
    # either a cmd line invocation or a tkinter gui
    from hugomatic.toolkitX import *

        
