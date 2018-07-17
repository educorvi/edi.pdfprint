from zope.interface import Interface
from five import grok

grok.templatedir('view_templates')

class Importer(grok.View):
    grok.context(Interface)


    def render(self):
        return 'Hallo Welt'

