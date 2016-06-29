from django.contrib import admin

from .models.crm import (
    Area, Building, Region, Locality, Street, Project, ProjectContact, FollowerContact, Candidate, FollowerCandidate,
    PollPlace, FamilyStatus, Education, SocialCategory, Sex, FollowerStatus, Follower,
)

from .models.campaign import Campaign
from .models.task import Task
from .models.alphaname import Alphaname
from .models.message import Message

# External CRM views
admin.site.register(Area)
admin.site.register(Building)
admin.site.register(Region)
admin.site.register(Locality)
admin.site.register(Street)
admin.site.register(Project)
admin.site.register(ProjectContact)
admin.site.register(FollowerContact)
admin.site.register(Candidate)
admin.site.register(FollowerCandidate)
admin.site.register(PollPlace)
admin.site.register(FamilyStatus)
admin.site.register(Education)
admin.site.register(SocialCategory)
admin.site.register(Sex)
admin.site.register(FollowerStatus)
admin.site.register(Follower)

# Our app's models
admin.site.register(Campaign)
admin.site.register(Task)
admin.site.register(Alphaname)
admin.site.register(Message)
