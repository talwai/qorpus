import os
import docx
from constants import ALLOWED_EXTENSIONS, PYTHON_DOCX_EXTENSIONS

class Qorpus(object):
    def __init__(self, name=None, raw_text=None, filepath=None):
        self.name = name
        if filepath:
            _, extension = os.path.splitext(filepath)
            if extension not in ALLOWED_EXTENSIONS:
                raise ValueError('Extension %s is not supported by Qorpus. Allowed extensions are %s'
                        % (extension, ALLOWED_EXTENSIONS) )

            if extension in PYTHON_DOCX_EXTENSIONS:
                try:
                    self.document = docx.Document(filepath)
                except Exception as e:
                    print ("Python-docx failed to open document : %s" % e)

        self.raw_text = raw_text if raw_text else ''

    @classmethod
    def concat_all(cls, qs, name=None):
        acc = ''
        for q in qs:
            acc.join(q.raw_text)
        return Qorpus(name=name, raw_text=acc)

    def add_raw_text(self, txt):
        self.raw_text = self.raw_text.join(txt)
