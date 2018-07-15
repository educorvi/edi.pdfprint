from bghw.stammblatt.interfaces import IStammblatt
from Products.ATContentTypes.interfaces.document import IATDocument
from ftw.pdfgenerator.layout.makolayout import MakoLayoutBase
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.interfaces import ICustomizableLayout
from ftw.pdfgenerator.layout.customizable import CustomizableLayout
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements

class StammblattLayout(MakoLayoutBase):
    adapts(IATDocument, Interface, IBuilder)
    implements(ICustomizableLayout)

    template_directories = ['stammblatt_templates']
    template_name = 'layout.tex'

    def before_render_hook(self):
        self.use_babel()
        self.use_package('inputenc', options='utf8')
        self.use_package('fontenc', options='T1')
        self.use_package('lmodern')
        self.use_package('url')
        self.use_package('amssymb')
        self.use_package('graphicx')
        self.use_package('scrpage2')
        self.use_package('textpos', options='absolute')
        self.use_babel()

    def get_render_arguments(self):
        args = {}
        args['headline'] = self.context.title
        args['stand'] = '01.01.1900'
        try:
            args['stand'] = self.context.effective().strftime('%d.%m.%Y')
        except:
            args['stand'] = '01.01.1900'
        args['bestellnummer'] = u'4711'
        return args
