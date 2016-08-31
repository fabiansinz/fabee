from pprint import pprint

import datajoint as dj
from commons import inj
from djaddon import hdf5
from commons import mice, virus, inj
from scipy.misc import imread
schema = dj.schema('fabee_labbook', locals())

@schema
class InjectionAssessment(dj.Manual):
    definition = """
    # evaluation of injections

    -> inj.VirusInjection
    ---
    success     : tinyint       # whether injection was succeful or not
    notes       : varchar(1024) # evaluation
    image=null  : longblob      # image of the injection site
    """

    def populate(self):
        todo = inj.VirusInjection() * mice.Death() * virus.Virus() - self
        for k in todo.fetch.as_dict:
            pprint(k)
            k['notes'] = input('Please input notes: ')
            path = input('Please input path to image (leave empty for no image)')
            if path.strip():
                k['image'] = scipy.imread(path).astype(float)
            self.insert1(k, ignore_extra_fields=True)