from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class FixedValuesCA746:
    INSERTION_ORDER = [6, 13, 23, 10, 16, 14, 26, 8, 11, 4, 21, 18, 7, 1, 15, 20, 12, 5, 25, 17, 22, 2, 24, 9, 3, 19]
    KWH_FOR_EACH_EV = [24, 20, 17, 4.4, 12, 20, 8, 12, 16, 17, 24, 24, 17, 24, 16, 41.8, 41.8, 20, 24, 4.4, 85, 20, 8,
                       23, 22, 85]
    PV_SHAPES = ['pv_shape_rainy', 'pv_shape_cloudy', 'pv_shape_varied', 'pv_shape_varied', 'pv_shape_rainy',
                 'pv_shape_cloudy', 'pv_shape_cloudy']
    PHASES = [(1, 2), (2, 3), (1, 2), (2, 3), (2, 3), (2, 3), (1, 3), (1, 2), (1, 2), (1, 3), (1, 3), (1, 3), (1, 2),
              (1, 3), (1, 3), (2, 3), (1, 2), (1, 3), (2, 3), (1, 2), (1, 3), (1, 2), (2, 3), (2, 3), (2, 3), (2, 3)]
    EV_CHARGERS_POWERS = [3.6, 3.6, 7.2, 7.2, 7.2, 3.6, 7.2, 7.2, 7.2, 7.2, 7.2, 7.2, 3.6, 7.2, 7.2, 7.2, 3.6, 7.2, 7.2,
                          7.2, 7.2, 7.2, 7.2, 7.2, 7.2, 7.2]
    MAX_PV_POWER = [5, 9, 10, 8, 6, 7, 6, 5, 5, 9, 8, 10, 5, 10, 8, 5, 8, 6, 8, 6, 9, 10, 8, 7, 7, 7]

    EV_SHAPES_BY_DAY = {
        1: [1638, 1397, 2232, 1965, 2215, 621, 480, 1837, 1833, 416, 4908, 1512, 1741, 3631, 2832, 4573, 2541, 1546,
            4857,
            368, 1960, 3490, 4437, 822, 897, 2692],
        2: [4968, 4954, 1630, 2753, 161, 4837, 3961, 1955, 664, 3343, 1654, 825, 1964, 2462, 2354, 4393, 607, 4410,
            3775,
            4815, 1448, 457, 117, 2529, 1024, 4539],
        3: [3881, 2286, 2420, 1533, 1288, 4341, 518, 3060, 4254, 4717, 4114, 1440, 3006, 4853, 2927, 3475, 4412, 3425,
            2043, 3754, 2132, 3712, 3328, 2379, 2356, 1472],
        4: [888, 4769, 4563, 2040, 2264, 2487, 2257, 1995, 211, 2359, 2572, 3548, 33, 458, 1218, 4777, 4898, 1258, 3700,
            2968, 1466, 3702, 2856, 3817, 2678, 2731],
        5: [107, 4130, 2830, 4783, 1472, 4868, 2421, 750, 3079, 1940, 2470, 1482, 563, 1333, 2136, 1088, 1765, 1029,
            4878,
            4234, 2873, 1651, 2309, 3684, 4724, 4805],
        6: [319, 4377, 134, 4596, 1896, 3392, 2316, 4756, 29, 2215, 73, 4552, 1563, 2938, 1171, 1814, 1600, 1946, 2703,
            630, 2308, 2494, 953, 4011, 1595, 2896],
        7: [2077, 415, 201, 2804, 2044, 4781, 444, 1616, 643, 1981, 4615, 11, 4156, 3493, 1145, 4184, 673, 3809, 4178,
            1278, 2422, 2112, 3728, 325, 4206, 2808]
    }

class EvKwh(Enum):
    TOYOTA_RAV4_SUV = 41.8
    TESLA_MODEL_S = 85
    TOYOTA_PRIUS_PLUG_IN = 4.4
    RENAULT_FLUENCE_RENAULT_ZOE = 22
    OPEL_AMPERA_MITSUBISHI_I_MIEV_CITROEN_C_ZERO_PEUGEOT_ION = 16
    NISSAN_LEAF_FIAT_500E = 24
    FORD_FUSION_ENERGY = 8
    MIA_MIA = 12
    FORD_FOCUS_ELECTRIC = 23
    FORD_C_MAX_ENERGY = 8
    BYD_E6 = 61
    CHEVROLET_SPARK_HONDA_FIT_EV = 20
    CHEVROLET_VOLT = 17


class PVShapesPossibilities(Enum):
    PV_SHAPE_SUNNY = 'pv_shape_sunny'
    PV_SHAPE_RAINY = 'pv_shape_rainy'
    PV_SHAPE_CLOUDY = 'pv_shape_cloudy'
    PV_SHAPE_VARIED = 'pv_shape_varied'


class EvChargerPowerKw(Enum):
    MAX_KW = 7.2
    MIN_KW = 3.6


class MaxPowerPVKW(Enum):
    MAX_KW = 10
    MIN_KW = 5

EV_CHARGER_POWER_POSSIBILITIES = [5.225, 14.167, 2.933, 2.444, 10.72, 6.286, 2.286, 3.429, 3.2, 16.4, 19.0, 6.0, 3.2,
                                  4.989, 6.667, 6.892]


TARGET_LOADS_CA746 = """New Load.residence1   phases=3 bus1=CA746RES1   kV=0.220  kW=2.500     pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence2   phases=3 bus1=CA746RES2   kV=0.220  kW=3.024   pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence3   phases=3 bus1=CA746RES3   kV=0.220  kW=2.604   pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence4   phases=3 bus1=CA746RES4   kV=0.220  kW=2.749  pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence5   phases=3 bus1=CA746RES5   kV=0.220  kW=2.635   pf=0.92 model=1 conn=wye status=variable daily=RES-Type5-WE
    New Load.residence6   phases=3 bus1=CA746RES6   kV=0.220  kW=2.377   pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence7   phases=3 bus1=CA746RES7   kV=0.220  kW=2.170   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence8   phases=3 bus1=CA746RES8   kV=0.220  kW=2.995   pf=0.92 model=1 conn=wye status=variable daily=RES-Type7-WE
    New Load.residence9   phases=3 bus1=CA746RES9   kV=0.220  kW=3.135   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence10  phases=3 bus1=CA746RES10  kV=0.220  kW=3.126   pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence11  phases=3 bus1=CA746RES11  kV=0.220  kW=2.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence12  phases=3 bus1=CA746RES12  kV=0.220  kW=2.700   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence13  phases=3 bus1=CA746RES13  kV=0.220  kW=2.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence14  phases=3 bus1=CA746RES14  kV=0.220  kW=2.726   pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence15  phases=3 bus1=CA746RES15  kV=0.220  kW=2.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type5-WE
    New Load.residence16  phases=3 bus1=CA746RES16  kV=0.220  kW=2.300   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence17  phases=3 bus1=CA746RES17  kV=0.220  kW=2.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence18  phases=3 bus1=CA746RES18  kV=0.220  kW=2.726   pf=0.92 model=1 conn=wye status=variable daily=RES-Type8-WE
    New Load.residence19  phases=3 bus1=CA746RES19  kV=0.220  kW=2.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type9-WE
    New Load.residence20  phases=3 bus1=CA746RES20  kV=0.220  kW=2.817   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence21  phases=3 bus1=CA746RES21  kV=0.220  kW=3.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence22  phases=3 bus1=CA746RES22  kV=0.220  kW=3.726   pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence23  phases=3 bus1=CA746RES23  kV=0.220  kW=3.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence24  phases=3 bus1=CA746RES24  kV=0.220  kW=2.800   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence25  phases=3 bus1=CA746RES25  kV=0.220  kW=2.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type7-WE
    New Load.residence26  phases=3 bus1=CA746RES26  kV=0.220  kW=2.300   pf=0.92 model=1 conn=wye status=variable daily=RES-Type7-WE"""


PL_PERCENTAGES = (25, 50, 75, 100)

class ColumnsMapVoltages(Enum):
    V1 = 1
    V2 = 3
    V3 = 5


ordered_labels = [" ",
                  "0 | 20", "0 | 40", "0 | 60", "0 | 80", "0 | 100",
                  "20 | 0", "20 | 20", "20 | 40", "20 | 60", "20 | 80", "20 | 100",
                  "40 | 0", "40 | 20", "40 | 40", "40 | 60", "40 | 80", "40 | 100",
                  "60 | 0", "60 | 20", "60 | 40", "60 | 60", "60 | 80", "60 | 100",
                  "80 | 0", "80 | 20", "80 | 40", "80 | 60", "80 | 80", "80 | 100",
                  "100 | 0", "100 | 20", "100 | 40", "100 | 60", "100 | 80", "100 | 100"
                  ]

control_modes = ['no_control', 'voltvar', 'voltwatt']