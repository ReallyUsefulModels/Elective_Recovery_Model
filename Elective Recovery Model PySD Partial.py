"""
Python model 'Elective Recovery Model Tinkered.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.2.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


_subscript_dict = {
    "Waiting_time": [
        "Less_than_6mths",
        "Between_6_to_12mths",
        "Between_12_to_24mths",
        "Over_24mths",
    ]
}

component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 520,
    "time_step": lambda: 1 / 4,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="INITIAL TIME", units="Weeks", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="FINAL TIME", units="Weeks", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="TIME STEP", units="Weeks", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="Weeks",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The save time step for the simulation.
    """
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Incidence of condition",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "expected_population_rate_of_incidence_pw": 1,
        "underlying_trend_in_health_needs": 2,
        "switch_for_demographic_increase": 1,
    },
)
def incidence_of_condition():
    return (
        expected_population_rate_of_incidence_pw()
        + (underlying_trend_in_health_needs() - 1)
        * underlying_trend_in_health_needs()
        * switch_for_demographic_increase()
    )


@component.add(
    name="Expected population rate of incidence pw",
    comp_type="Constant",
    comp_subtype="Normal",
)
def expected_population_rate_of_incidence_pw():
    return 100


@component.add(
    name="COVID period",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def covid_period():
    return np.interp(
        time(),
        [
            0.0,
            4.33333333,
            8.66666667,
            13.0,
            17.33333333,
            21.66666667,
            26.0,
            30.33333333,
            34.66666667,
            39.0,
            43.33333333,
            47.66666667,
            52.0,
            56.33333333,
            60.66666667,
            65.0,
            69.33333333,
            73.66666667,
            78.0,
            82.33333333,
            86.66666667,
            91.0,
            95.33333333,
            99.66666667,
            104.0,
            108.33333333,
            112.66666667,
            117.0,
            121.33333333,
            125.66666667,
            130.0,
            134.33333333,
            138.66666667,
            143.0,
            147.33333333,
            151.66666667,
            156.0,
            160.33333333,
            164.66666667,
            169.0,
            173.33333333,
            177.66666667,
            182.0,
            186.33333333,
            190.66666667,
            195.0,
            199.33333333,
            203.66666667,
            208.0,
            212.33333333,
            216.66666667,
            221.0,
            225.33333333,
            229.66666667,
            234.0,
            238.33333333,
            242.66666667,
            247.0,
            251.33333333,
            255.66666667,
            260.0,
            264.33333333,
            268.66666667,
            273.0,
            277.33333333,
            281.66666667,
            286.0,
            290.33333333,
            294.66666667,
            299.0,
            303.33333333,
            307.66666667,
            312.0,
            316.33333333,
            320.66666667,
            325.0,
            329.33333333,
            333.66666667,
            338.0,
            342.33333333,
            346.66666667,
            351.0,
            355.33333333,
            359.66666667,
            364.0,
            368.33333333,
            372.66666667,
            377.0,
            381.33333333,
            385.66666667,
            390.0,
            394.33333333,
            398.66666667,
            403.0,
            407.33333333,
            411.66666667,
            416.0,
            420.33333333,
            424.66666667,
            429.0,
            433.33333333,
            437.66666667,
            442.0,
            446.33333333,
            450.66666667,
            455.0,
            459.33333333,
            463.66666667,
            468.0,
            472.33333333,
            476.66666667,
            481.0,
            485.33333333,
            489.66666667,
            494.0,
            498.33333333,
            502.66666667,
            507.0,
            511.33333333,
            515.66666667,
            520.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
    )


@component.add(
    name="Decision not to present",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "incidence_of_condition": 1,
        "percent_people_not_presenting_during_covid": 1,
        "covid_period": 1,
        "covid_switch": 1,
    },
)
def decision_not_to_present():
    return (
        incidence_of_condition()
        * (percent_people_not_presenting_during_covid() / 100)
        * (covid_period() / 100)
    ) * covid_switch()


@component.add(
    name="Holding stock released at end of COVID",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"holding_stock_of_potential_unmet_need": 1, "covid_period": 1},
)
def holding_stock_released_at_end_of_covid():
    return holding_stock_of_potential_unmet_need() * (1 - covid_period() / 100)


@component.add(
    name="Need presenting as usual",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"incidence_of_condition": 1, "decision_not_to_present": 1},
)
def need_presenting_as_usual():
    return incidence_of_condition() - decision_not_to_present()


@component.add(
    name="Percent people not presenting during COVID",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percent_people_not_presenting_during_covid():
    return 50


@component.add(
    name="Underlying trend in health needs",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def underlying_trend_in_health_needs():
    return np.interp(
        time(),
        [
            0.0,
            4.33333333,
            8.66666667,
            13.0,
            17.33333333,
            21.66666667,
            26.0,
            30.33333333,
            34.66666667,
            39.0,
            43.33333333,
            47.66666667,
            52.0,
            56.33333333,
            60.66666667,
            65.0,
            69.33333333,
            73.66666667,
            78.0,
            82.33333333,
            86.66666667,
            91.0,
            95.33333333,
            99.66666667,
            104.0,
            108.33333333,
            112.66666667,
            117.0,
            121.33333333,
            125.66666667,
            130.0,
            134.33333333,
            138.66666667,
            143.0,
            147.33333333,
            151.66666667,
            156.0,
            160.33333333,
            164.66666667,
            169.0,
            173.33333333,
            177.66666667,
            182.0,
            186.33333333,
            190.66666667,
            195.0,
            199.33333333,
            203.66666667,
            208.0,
            212.33333333,
            216.66666667,
            221.0,
            225.33333333,
            229.66666667,
            234.0,
            238.33333333,
            242.66666667,
            247.0,
            251.33333333,
            255.66666667,
            260.0,
            264.33333333,
            268.66666667,
            273.0,
            277.33333333,
            281.66666667,
            286.0,
            290.33333333,
            294.66666667,
            299.0,
            303.33333333,
            307.66666667,
            312.0,
            316.33333333,
            320.66666667,
            325.0,
            329.33333333,
            333.66666667,
            338.0,
            342.33333333,
            346.66666667,
            351.0,
            355.33333333,
            359.66666667,
            364.0,
            368.33333333,
            372.66666667,
            377.0,
            381.33333333,
            385.66666667,
            390.0,
            394.33333333,
            398.66666667,
            403.0,
            407.33333333,
            411.66666667,
            416.0,
            420.33333333,
            424.66666667,
            429.0,
            433.33333333,
            437.66666667,
            442.0,
            446.33333333,
            450.66666667,
            455.0,
            459.33333333,
            463.66666667,
            468.0,
            472.33333333,
            476.66666667,
            481.0,
            485.33333333,
            489.66666667,
            494.0,
            498.33333333,
            502.66666667,
            507.0,
            511.33333333,
            515.66666667,
            520.0,
        ],
        [
            1.0,
            1.0,
            1.0,
            1.0021,
            1.0043,
            1.0064,
            1.0085,
            1.0096,
            1.0117,
            1.0128,
            1.0149,
            1.016,
            1.0191,
            1.0202,
            1.0223,
            1.0255,
            1.02605,
            1.0287,
            1.0298,
            1.033,
            1.0335,
            1.0351,
            1.0362,
            1.0394,
            1.0404,
            1.0415,
            1.0447,
            1.0457,
            1.0479,
            1.0489,
            1.05,
            1.0511,
            1.0543,
            1.0553,
            1.0574,
            1.0585,
            1.0596,
            1.0617,
            1.0628,
            1.0638,
            1.0649,
            1.067,
            1.06755,
            1.0691,
            1.0702,
            1.0713,
            1.0723,
            1.0745,
            1.0766,
            1.07765,
            1.0787,
            1.0809,
            1.083,
            1.0835,
            1.0862,
            1.0872,
            1.0894,
            1.0915,
            1.09255,
            1.0936,
            1.0947,
            1.0968,
            1.0989,
            1.1011,
            1.1021,
            1.1032,
            1.1053,
            1.1064,
            1.1085,
            1.1096,
            1.1117,
            1.11225,
            1.1138,
            1.1149,
            1.1181,
            1.1191,
            1.1202,
            1.1223,
            1.12285,
            1.1255,
            1.1277,
            1.1287,
            1.1298,
            1.1309,
            1.133,
            1.1351,
            1.1372,
            1.1388,
            1.1404,
            1.1426,
            1.1447,
            1.14575,
            1.1468,
            1.1489,
            1.1511,
            1.1543,
            1.15535,
            1.1574,
            1.1585,
            1.1596,
            1.1617,
            1.1628,
            1.1649,
            1.166,
            1.1681,
            1.1691,
            1.1734,
            1.17395,
            1.1766,
            1.17715,
            1.1787,
            1.1809,
            1.1819,
            1.183,
            1.1851,
            1.1862,
            1.1872,
            1.1883,
            1.1894,
            1.1915,
            1.1957,
        ],
    )


@component.add(
    name="Period of return in wks", comp_type="Constant", comp_subtype="Normal"
)
def period_of_return_in_wks():
    return 156


@component.add(
    name="Proceeding to tests without COVID delay",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"need_presenting_as_usual": 1, "nfa_following_initial_consultation": 1},
)
def proceeding_to_tests_without_covid_delay():
    return need_presenting_as_usual() - nfa_following_initial_consultation()


@component.add(
    name="Percent of need referred for diagnostics",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percent_of_need_referred_for_diagnostics():
    return 80


@component.add(
    name="Net COVID induced changes in underlying health needs?",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def net_covid_induced_changes_in_underlying_health_needs():
    return np.interp(
        time(),
        [
            0.0,
            4.33333333,
            8.66666667,
            13.0,
            17.33333333,
            21.66666667,
            26.0,
            30.33333333,
            34.66666667,
            39.0,
            43.33333333,
            47.66666667,
            52.0,
            56.33333333,
            60.66666667,
            65.0,
            69.33333333,
            73.66666667,
            78.0,
            82.33333333,
            86.66666667,
            91.0,
            95.33333333,
            99.66666667,
            104.0,
            108.33333333,
            112.66666667,
            117.0,
            121.33333333,
            125.66666667,
            130.0,
            134.33333333,
            138.66666667,
            143.0,
            147.33333333,
            151.66666667,
            156.0,
            160.33333333,
            164.66666667,
            169.0,
            173.33333333,
            177.66666667,
            182.0,
            186.33333333,
            190.66666667,
            195.0,
            199.33333333,
            203.66666667,
            208.0,
            212.33333333,
            216.66666667,
            221.0,
            225.33333333,
            229.66666667,
            234.0,
            238.33333333,
            242.66666667,
            247.0,
            251.33333333,
            255.66666667,
            260.0,
            264.33333333,
            268.66666667,
            273.0,
            277.33333333,
            281.66666667,
            286.0,
            290.33333333,
            294.66666667,
            299.0,
            303.33333333,
            307.66666667,
            312.0,
            316.33333333,
            320.66666667,
            325.0,
            329.33333333,
            333.66666667,
            338.0,
            342.33333333,
            346.66666667,
            351.0,
            355.33333333,
            359.66666667,
            364.0,
            368.33333333,
            372.66666667,
            377.0,
            381.33333333,
            385.66666667,
            390.0,
            394.33333333,
            398.66666667,
            403.0,
            407.33333333,
            411.66666667,
            416.0,
            420.33333333,
            424.66666667,
            429.0,
            433.33333333,
            437.66666667,
            442.0,
            446.33333333,
            450.66666667,
            455.0,
            459.33333333,
            463.66666667,
            468.0,
            472.33333333,
            476.66666667,
            481.0,
            485.33333333,
            489.66666667,
            494.0,
            498.33333333,
            502.66666667,
            507.0,
            511.33333333,
            515.66666667,
            520.0,
        ],
        [
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0011,
            1.0021,
            1.0032,
            1.0043,
            1.0043,
            1.0053,
            1.0064,
            1.0074,
            1.0074,
            1.0085,
            1.0096,
            1.0096,
            1.0106,
            1.01115,
            1.0128,
            1.0128,
            1.0138,
            1.0138,
            1.0149,
            1.0149,
            1.016,
            1.017,
            1.017,
            1.0181,
            1.0181,
            1.0181,
            1.0191,
            1.0202,
            1.0202,
            1.0213,
            1.0213,
            1.0223,
            1.0234,
            1.0234,
            1.0245,
            1.0245,
            1.0245,
            1.0255,
            1.0255,
            1.0266,
            1.0277,
            1.0287,
            1.0287,
            1.0298,
            1.0298,
            1.0309,
            1.0314,
            1.0319,
            1.033,
            1.033,
            1.034,
            1.034,
            1.0351,
            1.0362,
            1.0362,
            1.0362,
            1.0372,
            1.0383,
            1.0383,
            1.0383,
            1.0394,
            1.0404,
            1.04095,
            1.0415,
            1.04205,
            1.0426,
            1.0431,
            1.0436,
            1.04415,
            1.0447,
            1.0457,
            1.0468,
            1.0479,
            1.0484,
            1.0489,
            1.0489,
            1.05,
            1.05055,
            1.0511,
            1.0521,
            1.0532,
            1.0543,
            1.0553,
            1.0553,
            1.05585,
            1.0564,
            1.0574,
            1.0585,
            1.0596,
            1.0596,
            1.0617,
            1.0617,
            1.0628,
            1.0628,
            1.0638,
            1.0649,
            1.0649,
            1.066,
            1.066,
            1.067,
            1.067,
            1.0681,
            1.0681,
            1.0681,
            1.0691,
            1.0691,
            1.0691,
            1.0702,
            1.0702,
            1.0702,
            1.0713,
            1.0718,
            1.0723,
            1.0723,
            1.0734,
            1.0755,
        ],
    )


@component.add(
    name="NFA following initial consultation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "need_presenting_as_usual": 1,
        "percent_of_need_referred_for_diagnostics": 1,
    },
)
def nfa_following_initial_consultation():
    return need_presenting_as_usual() * (
        percent_of_need_referred_for_diagnostics() / 100
    )


@component.add(
    name="Undergoing diagnostic tests",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pre_covid_capacity_for_diagnostics": 2,
        "covid_period": 1,
        "reduced_diagnostic_capacity_during_covid": 1,
        "covid_switch": 2,
        "timing_of_new_diagnostic_capacity": 1,
        "percent_increase_in_diagnostic_capacity_post_covid": 1,
    },
)
def undergoing_diagnostic_tests():
    return pre_covid_capacity_for_diagnostics() * (
        1
        - (covid_period() / 100)
        * (reduced_diagnostic_capacity_during_covid() / 100)
        * covid_switch()
    ) + (
        ((percent_increase_in_diagnostic_capacity_post_covid() / 100) * covid_switch())
        * pre_covid_capacity_for_diagnostics()
    ) * (
        timing_of_new_diagnostic_capacity() / 100
    )


@component.add(
    name="Pre COVID capacity for diagnostics",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pre_covid_capacity_for_diagnostics():
    return 20


@component.add(
    name="Percent of unmet need returning", comp_type="Constant", comp_subtype="Normal"
)
def percent_of_unmet_need_returning():
    return 50


@component.add(
    name="Delayed need not presenting", comp_type="Constant", comp_subtype="Normal"
)
def delayed_need_not_presenting():
    return 0


@component.add(
    name="COVID delayed need presenting",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percent_of_unmet_need_returning": 1},
)
def covid_delayed_need_presenting():
    return percent_of_unmet_need_returning() / 100


@component.add(
    name="Increased percent of need for diagnostics for COVID delayed demand",
    comp_type="Constant",
    comp_subtype="Normal",
)
def increased_percent_of_need_for_diagnostics_for_covid_delayed_demand():
    return 10


@component.add(
    name="Delayed demand to wait for diagnostics",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "covid_delayed_need_presenting": 1,
        "percent_of_need_referred_for_diagnostics": 1,
        "increased_percent_of_need_for_diagnostics_for_covid_delayed_demand": 1,
    },
)
def delayed_demand_to_wait_for_diagnostics():
    return covid_delayed_need_presenting() * (
        (
            percent_of_need_referred_for_diagnostics()
            + increased_percent_of_need_for_diagnostics_for_covid_delayed_demand()
        )
        / 100
    )


@component.add(
    name="NFA following initial consultation for COVID delayed need",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "covid_delayed_need_presenting": 1,
        "delayed_demand_to_wait_for_diagnostics": 1,
    },
)
def nfa_following_initial_consultation_for_covid_delayed_need():
    return covid_delayed_need_presenting() - delayed_demand_to_wait_for_diagnostics()


@component.add(
    name="Average pre COVID wait for diagnostics",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_pre_covid_wait_for_diagnostics():
    return 13


@component.add(
    name="Reduced diagnostic capacity during COVID",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reduced_diagnostic_capacity_during_covid():
    return 70


@component.add(
    name="Percent increase in diagnostic capacity post COVID",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percent_increase_in_diagnostic_capacity_post_covid():
    return 30


@component.add(
    name="Timing of new diagnostic capacity",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def timing_of_new_diagnostic_capacity():
    return np.interp(
        time(),
        [
            0.0,
            4.33333333,
            8.66666667,
            13.0,
            17.33333333,
            21.66666667,
            26.0,
            30.33333333,
            34.66666667,
            39.0,
            43.33333333,
            47.66666667,
            52.0,
            56.33333333,
            60.66666667,
            65.0,
            69.33333333,
            73.66666667,
            78.0,
            82.33333333,
            86.66666667,
            91.0,
            95.33333333,
            99.66666667,
            104.0,
            108.33333333,
            112.66666667,
            117.0,
            121.33333333,
            125.66666667,
            130.0,
            134.33333333,
            138.66666667,
            143.0,
            147.33333333,
            151.66666667,
            156.0,
            160.33333333,
            164.66666667,
            169.0,
            173.33333333,
            177.66666667,
            182.0,
            186.33333333,
            190.66666667,
            195.0,
            199.33333333,
            203.66666667,
            208.0,
            212.33333333,
            216.66666667,
            221.0,
            225.33333333,
            229.66666667,
            234.0,
            238.33333333,
            242.66666667,
            247.0,
            251.33333333,
            255.66666667,
            260.0,
            264.33333333,
            268.66666667,
            273.0,
            277.33333333,
            281.66666667,
            286.0,
            290.33333333,
            294.66666667,
            299.0,
            303.33333333,
            307.66666667,
            312.0,
            316.33333333,
            320.66666667,
            325.0,
            329.33333333,
            333.66666667,
            338.0,
            342.33333333,
            346.66666667,
            351.0,
            355.33333333,
            359.66666667,
            364.0,
            368.33333333,
            372.66666667,
            377.0,
            381.33333333,
            385.66666667,
            390.0,
            394.33333333,
            398.66666667,
            403.0,
            407.33333333,
            411.66666667,
            416.0,
            420.33333333,
            424.66666667,
            429.0,
            433.33333333,
            437.66666667,
            442.0,
            446.33333333,
            450.66666667,
            455.0,
            459.33333333,
            463.66666667,
            468.0,
            472.33333333,
            476.66666667,
            481.0,
            485.33333333,
            489.66666667,
            494.0,
            498.33333333,
            502.66666667,
            507.0,
            511.33333333,
            515.66666667,
            520.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            5.0,
            12.0,
            18.6,
            39.9,
            58.0,
            66.5,
            70.2,
            78.7,
            84.0,
            92.0,
            95.7,
            96.8,
            97.9,
            98.4,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
            100.0,
        ],
    )


@component.add(
    name="Negative test results",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"undergoing_diagnostic_tests": 1, "percent_negative_test_results": 1},
)
def negative_test_results():
    return undergoing_diagnostic_tests() * (percent_negative_test_results() / 100)


@component.add(
    name="Percent negative test results", comp_type="Constant", comp_subtype="Normal"
)
def percent_negative_test_results():
    return 40


@component.add(name="COVID switch", comp_type="Constant", comp_subtype="Normal")
def covid_switch():
    return 0


@component.add(
    name="Switch for demographic increase", comp_type="Constant", comp_subtype="Normal"
)
def switch_for_demographic_increase():
    return 0


@component.add(
    name="Recognised need for GP consultation",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_recognised_need_for_gp_consultation": 1},
    other_deps={
        "_integ_recognised_need_for_gp_consultation": {
            "initial": {},
            "step": {
                "incidence_of_condition": 1,
                "decision_not_to_present": 1,
                "need_presenting_as_usual": 1,
            },
        }
    },
)
def recognised_need_for_gp_consultation():
    return _integ_recognised_need_for_gp_consultation()


_integ_recognised_need_for_gp_consultation = Integ(
    lambda: incidence_of_condition()
    - decision_not_to_present()
    - need_presenting_as_usual(),
    lambda: 0,
    "_integ_recognised_need_for_gp_consultation",
)


@component.add(
    name="Holding stock of potential unmet need",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_holding_stock_of_potential_unmet_need": 1},
    other_deps={
        "_integ_holding_stock_of_potential_unmet_need": {
            "initial": {},
            "step": {
                "decision_not_to_present": 1,
                "holding_stock_released_at_end_of_covid": 1,
            },
        }
    },
)
def holding_stock_of_potential_unmet_need():
    return _integ_holding_stock_of_potential_unmet_need()


_integ_holding_stock_of_potential_unmet_need = Integ(
    lambda: decision_not_to_present() - holding_stock_released_at_end_of_covid(),
    lambda: 0,
    "_integ_holding_stock_of_potential_unmet_need",
)


@component.add(
    name="Outcome of consultation",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_outcome_of_consultation": 1},
    other_deps={
        "_integ_outcome_of_consultation": {
            "initial": {},
            "step": {
                "need_presenting_as_usual": 1,
                "proceeding_to_tests_without_covid_delay": 1,
                "nfa_following_initial_consultation": 1,
            },
        }
    },
)
def outcome_of_consultation():
    return _integ_outcome_of_consultation()


_integ_outcome_of_consultation = Integ(
    lambda: need_presenting_as_usual()
    - proceeding_to_tests_without_covid_delay()
    - nfa_following_initial_consultation(),
    lambda: 0,
    "_integ_outcome_of_consultation",
)


@component.add(
    name="Waiting for diagnostics",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_waiting_for_diagnostics": 1},
    other_deps={
        "_integ_waiting_for_diagnostics": {
            "initial": {
                "proceeding_to_tests_without_covid_delay": 1,
                "average_pre_covid_wait_for_diagnostics": 1,
            },
            "step": {
                "proceeding_to_tests_without_covid_delay": 1,
                "delayed_demand_to_wait_for_diagnostics": 1,
                "undergoing_diagnostic_tests": 1,
            },
        }
    },
)
def waiting_for_diagnostics():
    return _integ_waiting_for_diagnostics()


_integ_waiting_for_diagnostics = Integ(
    lambda: proceeding_to_tests_without_covid_delay()
    + delayed_demand_to_wait_for_diagnostics()
    - undergoing_diagnostic_tests(),
    lambda: proceeding_to_tests_without_covid_delay()
    * average_pre_covid_wait_for_diagnostics(),
    "_integ_waiting_for_diagnostics",
)


@component.add(
    name="Depleting stock of unmet need",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_depleting_stock_of_unmet_need": 1},
    other_deps={
        "_integ_depleting_stock_of_unmet_need": {
            "initial": {},
            "step": {
                "holding_stock_released_at_end_of_covid": 1,
                "delayed_need_not_presenting": 1,
                "covid_delayed_need_presenting": 1,
            },
        }
    },
)
def depleting_stock_of_unmet_need():
    return _integ_depleting_stock_of_unmet_need()


_integ_depleting_stock_of_unmet_need = Integ(
    lambda: holding_stock_released_at_end_of_covid()
    - delayed_need_not_presenting()
    - covid_delayed_need_presenting(),
    lambda: 0,
    "_integ_depleting_stock_of_unmet_need",
)


@component.add(
    name="Outcome of consultation for delayed demand",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_outcome_of_consultation_for_delayed_demand": 1},
    other_deps={
        "_integ_outcome_of_consultation_for_delayed_demand": {
            "initial": {},
            "step": {
                "covid_delayed_need_presenting": 1,
                "delayed_demand_to_wait_for_diagnostics": 1,
                "nfa_following_initial_consultation_for_covid_delayed_need": 1,
            },
        }
    },
)
def outcome_of_consultation_for_delayed_demand():
    return _integ_outcome_of_consultation_for_delayed_demand()


_integ_outcome_of_consultation_for_delayed_demand = Integ(
    lambda: covid_delayed_need_presenting()
    - delayed_demand_to_wait_for_diagnostics()
    - nfa_following_initial_consultation_for_covid_delayed_need(),
    lambda: 0,
    "_integ_outcome_of_consultation_for_delayed_demand",
)


@component.add(
    name="Test results",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_test_results": 1},
    other_deps={
        "_integ_test_results": {
            "initial": {},
            "step": {"undergoing_diagnostic_tests": 1, "negative_test_results": 1},
        }
    },
)
def test_results():
    return _integ_test_results()


_integ_test_results = Integ(
    lambda: undergoing_diagnostic_tests() - negative_test_results(),
    lambda: 0,
    "_integ_test_results",
)
