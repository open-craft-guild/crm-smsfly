# Add recognized model option to django
# :seealso: https://djangosnippets.org/snippets/2687/
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('db_route',)

# from .crm import *
# from .campaign import Campaign
# from .task import Task
# from .alphaname import Alphaname
# from .message import Message
