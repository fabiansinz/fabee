import os
from glob import glob

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
    """

    def populate(self):
        path = input('Please enter image path (format PATH/{animal_id}/*.jpg): ')
        path = os.path.expanduser(path)
        if path[-1] != '/':
            path += '/'
        path += '{animal_id}/*.jpg'
        todo = inj.VirusInjection() * mice.Death() * virus.Virus() - self
        with self.connection.transaction:
            for k in todo.fetch.as_dict:
                pprint(k)
                k['notes'] = input('Please input notes: ')
                k['success'] = int(input('Target region successfully infected? [1,0]: '))
                self.insert1(k, ignore_extra_fields=True)

                images = glob(path.format(**k))
                if len(images) > 0:
                    imp = input('Found images in ~/Dropbox/experiments/{animal_id}/. Import? [Y/n]'.format(**k))
                    if imp.strip().lower() in ('', 'y'):
                        for i, image in enumerate(images):
                            print('Loading ', image)
                            k['image'] = imread(image).astype(float)
                            k['image_id'] = i
                            self.Image().insert1(k, ignore_extra_fields=True)
                if input('Exit? [y/N]').strip().lower() == 'y':
                    break


    class Image(dj.Part):
        definition = """
        # image of the injection

        -> InjectionAssessment
        image_id    : smallint
        ---
        image       : longblob
        """