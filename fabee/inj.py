import datajoint as dj
from djaddon import hdf5
from commons import mice, virus

schema = dj.schema('fabee_injections', locals())


@schema
class AtlasStereotacticTargets(dj.Lookup):
    definition = """
    # Unadjusted stereotactic coordinates from the mouse brain atlas

    area                          : char(30) # name of the target area
    ---
    caudal                        : double # coordinate caudal from bregma in mm
    lateral                       : double # lateral coordinate in mm
    ventral                       : double # coordinate ventral from cortical surface in mm
    lambda_bregma_basedist=4.21   : double # base distance between lambda and bregma from the stereotactic atlas in mm
    """
    contents =  [('dLGN_01', 2.3, 2.25, 2.5, 4.21),       # dLGN
                 ('dLGN_Tang2016', 2.6, 2.15, 2.7, 4.21), # Tang2016_dLGN
                 ('dLGN_05', 2.4, 2.25, 2.6, 4.21),       # dLGN10302015
                 ('dLGN_06', 2.5, 2.5, 2.7, 4.21),        # dLGN12032015
                 ('dLGN_02', 2.3, 2.4, 2.7, 4.21),        # dLGNDeeper
                 ('dLGN_03', 2.3, 2.3, 2.6, 4.21),        # dLGNmod
                 ('dLGN_04', 2.3, 2.4, 2.6, 4.21),        # dLGNMoreVentralLateral
                 ('V1_perp', 3.8, 2.5, .35, 4.21)]        # dLGNMoreVentralLateral



@schema
class Dye(dj.Lookup):
    definition = """
    # lookup for dyes

    dye_name       : char(30)
    """

    contents = [('Dextran',)]

@schema
class Substance(dj.Lookup):
    definition = """
    # Injection substance

    substance_id            : smallint    # injection substance

    ---
    substance_type          : enum("virus","dye")
    """

    def _prepare(self):
        with self.connection.transaction:
            contents = [
                dict(substance_id=0, substance_type='dye'),
                dict(substance_id=1, substance_type='virus'),
                dict(substance_id=2, substance_type='virus'),
                dict(substance_id=3, substance_type='virus'),
                dict(substance_id=4, substance_type='virus'),
            ]
            
            self.insert(contents, skip_duplicates=True)

            viruses = [
                dict(substance_id=1, virus_id=31), 
                dict(substance_id=2, virus_id=32), 
                dict(substance_id=3, virus_id=33), 
                dict(substance_id=4, virus_id=34),
            ]
            self.Virus().insert(viruses, skip_duplicates=True)

            dyes = [
                dict(substance_id=0, dye_name='Dextran', solvent='PBS')
            ]
            self.Dye().insert(dyes, skip_duplicates=True)


    class Virus(dj.Part):
        definition = """
        # viral injection substances

        ->Substance
        ---
        ->virus.Virus
        concentration=null      : double                # concentration of the virus in mg/ml
        solvent=null            : enum("PBS", "Saline") # what the substance was diluted with
        """

    class Dye(dj.Part):
        definition = """
        # dye injection substances

        ->Substance
        ---
        ->Dye
        concentration=null      : double                # concentration of the substance in mg/ml
        solvent=null            : enum("PBS", "Saline") # what the substance was diluted with
        """


@schema
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
        ('1B100F-4', 1, 0.58, 'WPI')
    ]


@schema
class PullerProgram(dj.Lookup):
    definition = """
    # Puller program

    number          : int # number of the program
    ---
    """

    # contents = [(51,)]


@schema
class Injection(dj.Manual):
    definition = """
    # Injections

    ->mice.Mice
    ->Substance
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


@schema
class InjectionNote(dj.Manual):
    definition = """
    # notes concerning injections
    -> Injection
    ts=CURRENT_TIMESTAMP         : timestamp # time of injection
    ---a
    text                         : varchar(2000) # note
    """

