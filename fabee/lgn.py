import datajoint as dj
from djaddon import hdf5
from commons import mice

labbook = dj.schema('fabee_labbook', locals())

@labbook
class AtlasStereotacticTargets(dj.Lookup):
    definition = """
    # Unadjusted stereotactic coordinates from the mouse brain atlas

    area                          : varchar(40) # name of the target area
    ---
    caudal                        : double # coordinate caudal from bregma in mm
    lateral                       : double # lateral coordinate in mm
    ventral                       : double # coordinate ventral from cortical surface in mm
    lambda_bregma_basedist=4.21   : double # base distance between lambda and bregma from the stereotactic atlas in mm
    """

    contents =  [('dLGN', 2.3, 2.25, 2.5, 4.21),
                 ('dLGN10302015', 2.4, 2.25, 2.6, 4.21),
                 ('dLGN12032015', 2.5, 2.5, 2.7, 4.21),
                 ('dLGNDeeper', 2.3, 2.4, 2.7, 4.21),
                 ('dLGNmod', 2.3, 2.3, 2.6, 4.21),
                 ('dLGNMoreVentralLateral', 2.3, 2.4, 2.6, 4.21)]



@labbook
class InjectionSubstance(dj.Lookup):
    definition = """
    # Injection agent

    substance          : varchar(100) # injection substance

    ---
    concentration=null      : double      # concentration of the substance in mg/ml
    solvent=null            : enum("PBS", "Saline") # what the substance was diluted with
    """

    contents = [
        dict(substance="Dextran", concentration=1, solvent='PBS'),
        dict(substance="AAV-mRuby2-GCamp6", concentration=1, solvent='PBS'),
        dict(substance="AAV1_Syn_GCamp6s-0.5mul_Alexa_1mM", solvent='Saline')
    ]


@labbook
class PullerProgram(dj.Lookup):
    definition = """
    # Puller program

    number          : int # number of the program
    ---
    """

    contents = [(51,)]

@labbook
class PipetteGlass(dj.Lookup):
    definition = """
    # glass used for pulling pipettes

    item_id         : varchar(40)   # item id from the manufacturer
    ---
    od              : double        # outer diameter
    id              : double        # inner diameter
    manufacturer    : enum('WPI')
    """

    contents = [
        ('1B100F-4', 1 , 0.58, 'WPI')
    ]

@labbook
class Injections(dj.Manual):
    definition = """
    # Injections

    ->mice.Mice
    ->InjectionSubstance
    ->AtlasStereotacticTargets
    ---

    lambda_bregma                 : double # distance between lambda and bregma in mm as measured
    caudal                        : double # coordinate caudal from bregma in mm
    lateral                       : double # lateral coordinate in mm
    ventral                       : double # coordinate ventral from cortical surface in mm
    adjustment                    : double # adjustement factor to convert atlas coordinates to this injection
    volume=null                   : double # injection volume
    speed=null                    : double # injection speed [nl/min]
    ->PipetteGlass
    tip_opening=null              : double # tip opening in um
    toi=CURRENT_TIMESTAMP         : timestamp # time of injection
    """

@labbook
class InjectionNote(dj.Manual):
    definition = """
    # notes concerning injections
    -> Injections
    ts=CURRENT_TIMESTAMP         : timestamp # time of injection
    ---
    text                         : varchar(2000) # note
    """

@labbook
class InjectionImage(dj.Manual):
    definition = """
    # Photo of an injection

    -> Injections
    idx         : int # index of the image
    ---
    image       : longblob # image as array
    """