from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi

from Acquisition import aq_inner
from zope.component import getMultiAdapter

from bghw.stammblatt.interfaces import IStammblatt
from Products.ATContentTypes.interfaces.document import IATDocument
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.interfaces import ILaTeXView
from ftw.pdfgenerator.view import MakoLaTeXView
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
from zope.schema import getFieldsInOrder
from plone.app.textfield import RichText
from zope.schema import *

class EdiDocumentView(api.View):
    api.context(Interface)

    def render(self):
        return self.context.getText()


class EdiPrintView(api.Page):
    api.context(Interface)

    def formatList(self, field_value):
        html = '<ul>'
        for i in field_value:
            html += '<li>%s</li>' % i
        html += '</ul>'
        return html
        

    def render(self):
        html = ''
        schema = getUtility(IDexterityFTI, name=self.context.portal_type).lookupSchema()
        for name, field in getFieldsInOrder(schema):
            if name not in ['title', 'description']:
                html += '<h1>%s</h1>' % field.title
                field_value = getattr(self.context, name)
                if field_value: #fragt das Feld im aktuellen Context ab
                    if isinstance(field, RichText):
                        if field_value.output:
                            html += field_value.output
                    if isinstance(field, TextLine):
                        html += '<p>%s</p>' % field_value
                    if isinstance(field, List):
                        if isinstance(field.value_type, TextLine):
                            html += self.formatList(field_value)
        return html

class StammblattLaTeXView(MakoLaTeXView):
    adapts(IATDocument, Interface, ILaTeXLayout)
    implements(ILaTeXView)

    template_directories = ['stammblatt_templates']
    template_name = 'view.tex'


    def getView(self, name):
        context = aq_inner(self.context)
        view = context.restrictedTraverse('@@'+name)
        return view.render()

    def get_render_arguments(self):
        return {'title': self.convert(self.context.Title()),
                'description': self.convert(self.context.description),
                'details': self.convert(self.getView(name='edidocumentview'))}
