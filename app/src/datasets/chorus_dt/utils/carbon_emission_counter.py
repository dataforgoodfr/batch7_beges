def carbon_count():

    """

    Retrieve CO2 emission table,

    RETURN:
     - dict mapping from transport mode to CO2/km/person

    """

    carbon_dict = {}

    carbon_dict["CO2_short_plane"] = 0.0625
    carbon_dict["CO2_long_plane"] = 0.0427
    carbon_dict["CO2_TGV"] = 0.0037
    carbon_dict["CO2_TC"] = 0.07

    return carbon_dict
