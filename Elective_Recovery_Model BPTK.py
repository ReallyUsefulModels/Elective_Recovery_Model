
# Really Useful Models - Elective Recovery Model

# Built using BPTK
    
import numpy as np
from scipy.interpolate import interp1d
from scipy.special import gammaln
from scipy.stats import norm
import math, statistics, random, logging
from datetime import datetime
import re
import itertools
from copy import copy, deepcopy



def cartesian_product(listoflists):
    """
    Helper for Cartesian product
    :param listoflists:
    :return:
    """
    if len(listoflists) == 1:
        return listoflists[0]
    res = list(itertools.product(*listoflists))

    if len(res) == 1:
        return res[0]

    return res

def LERP(x,points):
    """
    Linear interpolation between a set of points
    :param x: x to obtain y for
    :param points: List of tuples containing the graphical function's points [(x,y),(x,y) ... ]
    :return: y value for x obtained using linear interpolation
    """
    x_vals = np.array([ x[0] for x in points])
    y_vals = np.array([x[1] for x in points])

    if x<= x_vals[0]:
        return y_vals[0]

    if x >= x_vals[len(x_vals)-1]:
        return y_vals[len(x_vals)-1]

    f = interp1d(x_vals, y_vals)
    return float(f(x))

class simulation_model():
    def __init__(self):
        # Simulation Settings
        self.dt = 0.25
        self.starttime = 0.0
        self.stoptime = 520.0
        self.units = 'Weeks'
        self.method = 'Euler'
        self.equations = {

        # Stocks
        
    
        '13wkWaitForUrgentTreatment'          : lambda t: ( (( self.memoize('positiveTestResultsUrgent', t) + self.memoize('lessThan6mthToUrgent', t) + self.memoize('between6To12mthWaitToUrgent', t) + self.memoize('between12To24mthWaitToUrgent', t) ) * 13.0) if ( t  <=  self.starttime ) else (self.memoize('13wkWaitForUrgentTreatment',t-self.dt) + self.dt * ( self.memoize('positiveTestResultsUrgent',t-self.dt) + self.memoize('lessThan6mthToUrgent',t-self.dt) + self.memoize('between6To12mthWaitToUrgent',t-self.dt) + self.memoize('between12To24mthWaitToUrgent',t-self.dt) - ( self.memoize('urgentTreatment',t-self.dt) ) )) ),
        'depletingStockOfUnmetNeed'          : lambda t: ( (0.0) if ( t  <=  self.starttime ) else (self.memoize('depletingStockOfUnmetNeed',t-self.dt) + self.dt * ( self.memoize('holdingStockReleasedAtEndOfCovid',t-self.dt) - ( self.memoize('delayedNeedNotPresenting',t-self.dt) + self.memoize('covidDelayedNeedPresenting',t-self.dt) ) )) ),
        'holdingStockOfPotentialUnmetNeed'          : lambda t: ( (max([0 , 0.0])) if ( t  <=  self.starttime ) else (self.memoize('holdingStockOfPotentialUnmetNeed',t-self.dt) + self.dt * ( self.memoize('decisionNotToPresent',t-self.dt) - ( self.memoize('holdingStockReleasedAtEndOfCovid',t-self.dt) ) )) ),
        'outcomeOfConsultation'          : lambda t: ( (max([0 , 0.0])) if ( t  <=  self.starttime ) else (self.memoize('outcomeOfConsultation',t-self.dt) + self.dt * ( self.memoize('needPresentingAsUsual',t-self.dt) - ( self.memoize('proceedingToTestsWithoutCovidDelay',t-self.dt) + self.memoize('nfaFollowingInitialConsultation',t-self.dt) ) )) ),
        'outcomeOfConsultationForDelayedDemand'          : lambda t: ( (max([0 , 0.0])) if ( t  <=  self.starttime ) else (self.memoize('outcomeOfConsultationForDelayedDemand',t-self.dt) + self.dt * ( self.memoize('covidDelayedNeedPresenting',t-self.dt) - ( self.memoize('delayedDemandToWaitForDiagnostics',t-self.dt) + self.memoize('nfaFollowingInitialConsultationForCovidDelayedNeed',t-self.dt) ) )) ),
        'recognisedNeedForGpConsultation'          : lambda t: ( (max([0 , 0.0])) if ( t  <=  self.starttime ) else (self.memoize('recognisedNeedForGpConsultation',t-self.dt) + self.dt * ( self.memoize('incidenceOfCondition',t-self.dt) - ( self.memoize('decisionNotToPresent',t-self.dt) + self.memoize('needPresentingAsUsual',t-self.dt) ) )) ),
        'testResults'          : lambda t: ( (max([0 , 0.0])) if ( t  <=  self.starttime ) else (self.memoize('testResults',t-self.dt) + self.dt * ( self.memoize('undergoingDiagnosticTests',t-self.dt) - ( self.memoize('positiveTestResultsUrgent',t-self.dt) + self.memoize('negativeTestResults',t-self.dt) + self.memoize('positiveTestResultsRoutine',t-self.dt) ) )) ),
        'waiting12To24mthsForTreatment'          : lambda t: ( (max([0 , 100.0])) if ( t  <=  self.starttime ) else (self.memoize('waiting12To24mthsForTreatment',t-self.dt) + self.dt * ( self.memoize('waitingMoreThan12mths',t-self.dt) - ( self.memoize('waitingMoreThan2yrs',t-self.dt) + self.memoize('between12To24mthWaitToUrgent',t-self.dt) + self.memoize('routineTreatmentFrom12To24mthWait',t-self.dt) ) )) ),
        'waiting6To12mthsForTreatment'          : lambda t: ( (max([0 , 500.0])) if ( t  <=  self.starttime ) else (self.memoize('waiting6To12mthsForTreatment',t-self.dt) + self.dt * ( self.memoize('waitingMoreThan6mths',t-self.dt) - ( self.memoize('waitingMoreThan12mths',t-self.dt) + self.memoize('between6To12mthWaitToUrgent',t-self.dt) + self.memoize('routineTreatmentFrom6To12thWaits',t-self.dt) ) )) ),
        'waiting6mthsForTreatment'          : lambda t: ( (max([0 , 500.0])) if ( t  <=  self.starttime ) else (self.memoize('waiting6mthsForTreatment',t-self.dt) + self.dt * ( self.memoize('positiveTestResultsRoutine',t-self.dt) - ( self.memoize('waitingMoreThan6mths',t-self.dt) + self.memoize('lessThan6mthToUrgent',t-self.dt) ) )) ),
        'waitingForDiagnostics'          : lambda t: ( (max([0 , self.memoize('proceedingToTestsWithoutCovidDelay', t) * self.memoize('averagePreCovidWaitForDiagnostics', t)])) if ( t  <=  self.starttime ) else (self.memoize('waitingForDiagnostics',t-self.dt) + self.dt * ( self.memoize('proceedingToTestsWithoutCovidDelay',t-self.dt) + self.memoize('delayedDemandToWaitForDiagnostics',t-self.dt) - ( self.memoize('undergoingDiagnosticTests',t-self.dt) ) )) ),
        'waitingOver24mthsForTreatment'          : lambda t: ( (max([0 , 0.0])) if ( t  <=  self.starttime ) else (self.memoize('waitingOver24mthsForTreatment',t-self.dt) + self.dt * ( self.memoize('waitingMoreThan2yrs',t-self.dt) - ( self.memoize('routineTreatment',t-self.dt) ) )) ),
        
    
        # Flows
        'between12To24mthWaitToUrgent'             : lambda t: max([0 , ( self.memoize('waiting12To24mthsForTreatment', t) * ( self.memoize('percentBecomingUrgentByWaitingTimePa[between12To24mths]', t) / 100.0 ) ) / 52.0]),
        'between6To12mthWaitToUrgent'             : lambda t: max([0 , ( self.memoize('waiting6To12mthsForTreatment', t) * ( self.memoize('percentBecomingUrgentByWaitingTimePa[between6To12mths]', t) / 100.0 ) ) / 52.0]),
        'covidDelayedNeedPresenting'             : lambda t: max([0 , self.memoize('percentOfUnmetNeedReturning', t) / 100.0]),
        'decisionNotToPresent'             : lambda t: max([0 , ( self.memoize('incidenceOfCondition', t) * ( self.memoize('percentPeopleNotPresentingDuringCovid', t) / 100.0 ) * ( self.memoize('covidPeriod', t) / 100.0 ) ) * self.memoize('covidSwitch', t)]),
        'delayedDemandToWaitForDiagnostics'             : lambda t: max([0 , self.memoize('covidDelayedNeedPresenting', t) * ( ( self.memoize('percentOfNeedReferredForDiagnostics', t) + self.memoize('increasedPercentOfNeedForDiagnosticsForCovidDelayedDemand', t) ) / 100.0 )]),
        'delayedNeedNotPresenting'             : lambda t: max([0 , 0.0]),
        'holdingStockReleasedAtEndOfCovid'             : lambda t: max([0 , self.memoize('holdingStockOfPotentialUnmetNeed', t) * ( 1.0 - ( self.memoize('covidPeriod', t) / 100.0 ) )]),
        'incidenceOfCondition'             : lambda t: max([0 , self.memoize('expectedPopulationRateOfIncidencePw', t) + ( ( self.memoize('underlyingTrendInHealthNeeds', t) - 1.0 ) * self.memoize('underlyingTrendInHealthNeeds', t) * self.memoize('switchForDemographicIncrease', t) )]),
        'lessThan6mthToUrgent'             : lambda t: max([0 , ( self.memoize('waiting6mthsForTreatment', t) * ( self.memoize('percentBecomingUrgentByWaitingTimePa[lessThan6mths]', t) / 100.0 ) ) / 52.0]),
        'needPresentingAsUsual'             : lambda t: max([0 , self.memoize('incidenceOfCondition', t) - self.memoize('decisionNotToPresent', t)]),
        'negativeTestResults'             : lambda t: max([0 , self.memoize('undergoingDiagnosticTests', t) * ( self.memoize('percentNegativeTestResults', t) / 100.0 )]),
        'nfaFollowingInitialConsultation'             : lambda t: max([0 , self.memoize('needPresentingAsUsual', t) * ( self.memoize('percentOfNeedReferredForDiagnostics', t) / 100.0 )]),
        'nfaFollowingInitialConsultationForCovidDelayedNeed'             : lambda t: max([0 , self.memoize('covidDelayedNeedPresenting', t) - self.memoize('delayedDemandToWaitForDiagnostics', t)]),
        'positiveTestResultsRoutine'             : lambda t: max([0 , self.memoize('undergoingDiagnosticTests', t) - self.memoize('negativeTestResults', t) - self.memoize('positiveTestResultsUrgent', t)]),
        'positiveTestResultsUrgent'             : lambda t: max([0 , ( self.memoize('undergoingDiagnosticTests', t) - self.memoize('negativeTestResults', t) ) * ( self.memoize('covidModifiedPercentUrgent', t) / 100.0 )]),
        'proceedingToTestsWithoutCovidDelay'             : lambda t: max([0 , self.memoize('needPresentingAsUsual', t) - self.memoize('nfaFollowingInitialConsultation', t)]),
        'routineTreatment'             : lambda t: max([0 , self.memoize('totalTreatmentCapacity', t) - self.memoize('urgentTreatment', t)]),
        'routineTreatmentFrom12To24mthWait'             : lambda t: max([0 , ( (self.memoize('totalTreatmentCapacity', t) - self.memoize('urgentTreatment', t)) if (self.memoize('waitingOver24mthsForTreatment', t) == 0.0) else (0.0) )]),
        'routineTreatmentFrom6To12thWaits'             : lambda t: max([0 , ( (self.memoize('totalTreatmentCapacity', t) - self.memoize('urgentTreatment', t)) if (self.memoize('waiting12To24mthsForTreatment', t) == 0.0) else (0.0) )]),
        'undergoingDiagnosticTests'             : lambda t: max([0 , ( self.memoize('preCovidCapacityForDiagnostics', t) * ( 1.0 - ( self.memoize('covidPeriod', t) / 100.0 ) * ( self.memoize('reducedDiagnosticCapacityDuringCovid', t) / 100.0 ) * self.memoize('covidSwitch', t) ) ) + ( ( ( ( self.memoize('percentIncreaseInDiagnosticCapacityPostCovid', t) / 100.0 ) * self.memoize('covidSwitch', t) ) * self.memoize('preCovidCapacityForDiagnostics', t) ) * ( self.memoize('timingOfNewDiagnosticCapacity', t) / 100.0 ) )]),
        'urgentTreatment'             : lambda t: max([0 , 0.0]),
        'waitingMoreThan12mths'             : lambda t: max([0 , self.delay( self.memoize('waitingMoreThan6mths', ( t - (26.0) )),26.0,self.memoize('waitingMoreThan6mths', (self.starttime)),t) - self.memoize('between6To12mthWaitToUrgent', t) - self.memoize('routineTreatmentFrom6To12thWaits', t)]),
        'waitingMoreThan2yrs'             : lambda t: max([0 , self.delay( self.memoize('waitingMoreThan12mths', ( t - (52.0) )),52.0,self.memoize('waitingMoreThan12mths', (self.starttime)),t) - self.memoize('between12To24mthWaitToUrgent', t) - self.memoize('waitingMoreThan12mths', t) - self.memoize('routineTreatmentFrom12To24mthWait', t)]),
        'waitingMoreThan6mths'             : lambda t: max([0 , self.delay( self.memoize('positiveTestResultsRoutine', ( t - (26.0) )),26.0,self.memoize('positiveTestResultsRoutine', (self.starttime)),t) - self.memoize('lessThan6mthToUrgent', t)]),
        
    
        # converters
        'averagePreCovidWaitForDiagnostics'      : lambda t: 13.0,
        'averageWaitForDiagnosticTest'      : lambda t: self.memoize('waitingForDiagnostics', t) / self.memoize('undergoingDiagnosticTests', t),
        'baselineTreatmentCapacity'      : lambda t: self.memoize('preCovidTreatmentCapacity', t) - ( self.memoize('covidSwitch', t) * ( self.memoize('covidPeriod', t) / 100.0 ) * ( ( 1.0 - ( self.memoize('percentReductionInTreatmentCapacityDuringCovid', t) / 100.0 ) ) * self.memoize('preCovidTreatmentCapacity', t) ) ),
        'covidDelayedPercentOfPositiveTestsUrgent'      : lambda t: 50.0,
        'covidModifiedPercentUrgent'      : lambda t: ( self.memoize('preCovidPercentOfPositiveTestsUrgent', t) * ( self.memoize('proceedingToTestsWithoutCovidDelay', t) / ( self.memoize('delayedDemandToWaitForDiagnostics', t) + self.memoize('proceedingToTestsWithoutCovidDelay', t) ) ) ) + ( self.memoize('covidDelayedPercentOfPositiveTestsUrgent', t) * ( self.memoize('delayedDemandToWaitForDiagnostics', t) / ( self.memoize('delayedDemandToWaitForDiagnostics', t) + self.memoize('proceedingToTestsWithoutCovidDelay', t) ) ) ),
        'covidSwitch'      : lambda t: 0.0,
        'expectedPopulationRateOfIncidencePw'      : lambda t: 100.0,
        'increasedPercentOfNeedForDiagnosticsForCovidDelayedDemand'      : lambda t: 10.0,
        'newCapacityWeekAvailable'      : lambda t: 208.0,
        'percentBecomingUrgentByWaitingTimePa'      : lambda t: self.memoize('percentBecomingUrgentByWaitingTimePa[lessThan6mths]', t) + self.memoize('percentBecomingUrgentByWaitingTimePa[between6To12mths]', t) + self.memoize('percentBecomingUrgentByWaitingTimePa[between12To24mths]', t) + self.memoize('percentBecomingUrgentByWaitingTimePa[over24mths]', t),
        'percentBecomingUrgentByWaitingTimePa[lessThan6mths]'      : lambda t: 5.0,
        'percentBecomingUrgentByWaitingTimePa[between6To12mths]'      : lambda t: 10.0,
        'percentBecomingUrgentByWaitingTimePa[between12To24mths]'      : lambda t: 15.0,
        'percentBecomingUrgentByWaitingTimePa[over24mths]'      : lambda t: 20.0,
        'percentIncreaseInDiagnosticCapacityPostCovid'      : lambda t: 30.0,
        'percentNegativeTestResults'      : lambda t: 40.0,
        'percentOfNeedReferredForDiagnostics'      : lambda t: 80.0,
        'percentOfUnmetNeedReturning'      : lambda t: 50.0,
        'percentPeopleNotPresentingDuringCovid'      : lambda t: 50.0,
        'percentReductionInTreatmentCapacityDuringCovid'      : lambda t: 20.0,
        'periodOfReturnInWks'      : lambda t: 156.0,
        'postCovidIncreaseInTreatmentCapacity'      : lambda t: 3.0,
        'preCovidCapacityForDiagnostics'      : lambda t: 20.0,
        'preCovidPercentOfPositiveTestsUrgent'      : lambda t: 20.0,
        'preCovidTreatmentCapacity'      : lambda t: 11.0,
        'reducedDiagnosticCapacityDuringCovid'      : lambda t: 70.0,
        'switchForDemographicIncrease'      : lambda t: 0.0,
        'totalTreatmentCapacity'      : lambda t: ( (( self.memoize('baselineTreatmentCapacity', t) + self.memoize('postCovidIncreaseInTreatmentCapacity', t) )) if ( t  > self.memoize('newCapacityWeekAvailable', t) and self.memoize('covidSwitch', t) == 1.0) else (self.memoize('baselineTreatmentCapacity', t)) ),
        'totalWaitingForDiagnosticsOrTreatment'      : lambda t: self.memoize('waiting6mthsForTreatment', t) + self.memoize('waiting6To12mthsForTreatment', t) + self.memoize('waiting12To24mthsForTreatment', t) + self.memoize('waitingOver24mthsForTreatment', t) + self.memoize('waitingForDiagnostics', t),
        
    
        # gf
        'covidPeriod' : lambda t: LERP(  t , self.points['covidPeriod']),
        'netCovidInducedChangesInUnderlyingHealthNeeds?' : lambda t: LERP(  t , self.points['netCovidInducedChangesInUnderlyingHealthNeeds?']),
        'timingOfNewDiagnosticCapacity' : lambda t: LERP(  t , self.points['timingOfNewDiagnosticCapacity']),
        'underlyingTrendInHealthNeeds' : lambda t: LERP(  t , self.points['underlyingTrendInHealthNeeds']),
        
    
        #constants
        
    
    
        }
    
        self.points = {
            'covidPeriod' :  [(0.0, 0.0), (4.333333333333351, 0.0), (8.666666666666702, 0.0), (13.000000000000052, 0.0), (17.333333333333403, 0.0), (21.66666666666675, 0.0), (26.000000000000103, 0.0), (30.333333333333453, 0.0), (34.666666666666806, 0.0), (39.00000000000015, 0.0), (43.3333333333335, 0.0), (47.666666666666856, 0.0), (52.000000000000206, 100.0), (56.333333333333556, 100.0), (60.666666666666906, 100.0), (65.00000000000026, 100.0), (69.33333333333361, 100.0), (73.66666666666696, 100.0), (78.0000000000003, 100.0), (82.33333333333366, 100.0), (86.666666666667, 100.0), (91.00000000000037, 100.0), (95.33333333333371, 100.0), (99.66666666666706, 100.0), (104.00000000000041, 100.0), (108.33333333333375, 100.0), (112.66666666666711, 100.0), (117.00000000000045, 100.0), (121.33333333333381, 100.0), (125.66666666666717, 100.0), (130.0000000000005, 100.0), (134.33333333333385, 100.0), (138.66666666666723, 100.0), (143.00000000000057, 100.0), (147.3333333333339, 100.0), (151.66666666666728, 100.0), (156.0000000000006, 0.0), (160.33333333333397, 0.0), (164.6666666666673, 0.0), (169.00000000000065, 0.0), (173.333333333334, 0.0), (177.66666666666737, 0.0), (182.00000000000074, 0.0), (186.33333333333405, 0.0), (190.66666666666742, 0.0), (195.00000000000077, 0.0), (199.3333333333341, 0.0), (203.66666666666745, 0.0), (208.00000000000082, 0.0), (212.3333333333342, 0.0), (216.6666666666675, 0.0), (221.00000000000088, 0.0), (225.33333333333422, 0.0), (229.66666666666757, 0.0), (234.0000000000009, 0.0), (238.33333333333428, 0.0), (242.66666666666762, 0.0), (247.00000000000097, 0.0), (251.33333333333434, 0.0), (255.66666666666768, 0.0), (260.000000000001, 0.0), (264.33333333333434, 0.0), (268.6666666666677, 0.0), (273.0000000000011, 0.0), (277.33333333333445, 0.0), (281.66666666666777, 0.0), (286.00000000000114, 0.0), (290.3333333333345, 0.0), (294.6666666666678, 0.0), (299.00000000000114, 0.0), (303.33333333333456, 0.0), (307.6666666666679, 0.0), (312.0000000000012, 0.0), (316.3333333333346, 0.0), (320.66666666666794, 0.0), (325.00000000000125, 0.0), (329.3333333333346, 0.0), (333.666666666668, 0.0), (338.0000000000013, 0.0), (342.3333333333347, 0.0), (346.666666666668, 0.0), (351.0000000000014, 0.0), (355.33333333333474, 0.0), (359.66666666666805, 0.0), (364.0000000000015, 0.0), (368.3333333333348, 0.0), (372.6666666666681, 0.0), (377.0000000000015, 0.0), (381.33333333333485, 0.0), (385.66666666666816, 0.0), (390.00000000000153, 0.0), (394.3333333333349, 0.0), (398.6666666666682, 0.0), (403.0000000000016, 0.0), (407.3333333333349, 0.0), (411.6666666666683, 0.0), (416.00000000000165, 0.0), (420.33333333333496, 0.0), (424.6666666666684, 0.0), (429.0000000000017, 0.0), (433.333333333335, 0.0), (437.6666666666684, 0.0), (442.00000000000176, 0.0), (446.3333333333351, 0.0), (450.66666666666845, 0.0), (455.0000000000018, 0.0), (459.33333333333513, 0.0), (463.6666666666685, 0.0), (468.0000000000018, 0.0), (472.3333333333352, 0.0), (476.66666666666856, 0.0), (481.0000000000019, 0.0), (485.33333333333525, 0.0), (489.6666666666686, 0.0), (494.00000000000193, 0.0), (498.33333333333525, 0.0), (502.6666666666687, 0.0), (507.000000000002, 0.0), (511.33333333333536, 0.0), (515.6666666666687, 0.0), (520.000000000002, 0.0)]  , 'netCovidInducedChangesInUnderlyingHealthNeeds?' :  [(0.0, 0.0), (4.333333333333351, 1.0), (8.666666666666702, 1.0), (13.000000000000052, 1.0), (17.333333333333403, 1.0), (21.66666666666675, 1.0011), (26.000000000000103, 1.0021), (30.333333333333453, 1.0032), (34.666666666666806, 1.0043), (39.00000000000015, 1.0043), (43.3333333333335, 1.0053), (47.666666666666856, 1.0064), (52.000000000000206, 1.0074), (56.333333333333556, 1.0074), (60.666666666666906, 1.0085), (65.00000000000026, 1.0096), (69.33333333333361, 1.0096), (73.66666666666696, 1.0106), (78.0000000000003, 1.01115), (82.33333333333366, 1.0128), (86.666666666667, 1.0128), (91.00000000000037, 1.0138), (95.33333333333371, 1.0138), (99.66666666666706, 1.0149), (104.00000000000041, 1.0149), (108.33333333333375, 1.016), (112.66666666666711, 1.017), (117.00000000000045, 1.017), (121.33333333333381, 1.0181), (125.66666666666717, 1.0181), (130.0000000000005, 1.0181), (134.33333333333385, 1.0191), (138.66666666666723, 1.0202), (143.00000000000057, 1.0202), (147.3333333333339, 1.0213), (151.66666666666728, 1.0213), (156.0000000000006, 1.0223), (160.33333333333397, 1.0234), (164.6666666666673, 1.0234), (169.00000000000065, 1.0245), (173.333333333334, 1.0245), (177.66666666666737, 1.0245), (182.00000000000074, 1.0255), (186.33333333333405, 1.0255), (190.66666666666742, 1.0266), (195.00000000000077, 1.0277), (199.3333333333341, 1.0287), (203.66666666666745, 1.0287), (208.00000000000082, 1.0298), (212.3333333333342, 1.0298), (216.6666666666675, 1.0309), (221.00000000000088, 1.0314), (225.33333333333422, 1.0319), (229.66666666666757, 1.033), (234.0000000000009, 1.033), (238.33333333333428, 1.034), (242.66666666666762, 1.034), (247.00000000000097, 1.0351), (251.33333333333434, 1.0362), (255.66666666666768, 1.0362), (260.000000000001, 1.0362), (264.33333333333434, 1.0372), (268.6666666666677, 1.0383), (273.0000000000011, 1.0383), (277.33333333333445, 1.0383), (281.66666666666777, 1.0394), (286.00000000000114, 1.0404), (290.3333333333345, 1.04095), (294.6666666666678, 1.0415), (299.00000000000114, 1.04205), (303.33333333333456, 1.0426), (307.6666666666679, 1.0431), (312.0000000000012, 1.0436), (316.3333333333346, 1.04415), (320.66666666666794, 1.0447), (325.00000000000125, 1.0457), (329.3333333333346, 1.0468), (333.666666666668, 1.0479), (338.0000000000013, 1.0484), (342.3333333333347, 1.0489), (346.666666666668, 1.0489), (351.0000000000014, 1.05), (355.33333333333474, 1.05055), (359.66666666666805, 1.0511), (364.0000000000015, 1.0521), (368.3333333333348, 1.0532), (372.6666666666681, 1.0543), (377.0000000000015, 1.0553), (381.33333333333485, 1.0553), (385.66666666666816, 1.05585), (390.00000000000153, 1.0564), (394.3333333333349, 1.0574), (398.6666666666682, 1.0585), (403.0000000000016, 1.0596), (407.3333333333349, 1.0596), (411.6666666666683, 1.0617), (416.00000000000165, 1.0617), (420.33333333333496, 1.0628), (424.6666666666684, 1.0628), (429.0000000000017, 1.0638), (433.333333333335, 1.0649), (437.6666666666684, 1.0649), (442.00000000000176, 1.066), (446.3333333333351, 1.066), (450.66666666666845, 1.067), (455.0000000000018, 1.067), (459.33333333333513, 1.0681), (463.6666666666685, 1.0681), (468.0000000000018, 1.0681), (472.3333333333352, 1.0691), (476.66666666666856, 1.0691), (481.0000000000019, 1.0691), (485.33333333333525, 1.0702), (489.6666666666686, 1.0702), (494.00000000000193, 1.0702), (498.33333333333525, 1.0713), (502.6666666666687, 1.0718), (507.000000000002, 1.0723), (511.33333333333536, 1.0723), (515.6666666666687, 1.0734), (520.000000000002, 1.0755)]  , 'timingOfNewDiagnosticCapacity' :  [(0.0, 0.0), (4.333333333333351, 0.0), (8.666666666666702, 0.0), (13.000000000000052, 0.0), (17.333333333333403, 0.0), (21.66666666666675, 0.0), (26.000000000000103, 0.0), (30.333333333333453, 0.0), (34.666666666666806, 0.0), (39.00000000000015, 0.0), (43.3333333333335, 0.0), (47.666666666666856, 0.0), (52.000000000000206, 0.0), (56.333333333333556, 0.0), (60.666666666666906, 0.0), (65.00000000000026, 0.0), (69.33333333333361, 0.0), (73.66666666666696, 0.0), (78.0000000000003, 0.0), (82.33333333333366, 0.0), (86.666666666667, 0.0), (91.00000000000037, 0.0), (95.33333333333371, 0.0), (99.66666666666706, 0.0), (104.00000000000041, 0.0), (108.33333333333375, 0.0), (112.66666666666711, 0.0), (117.00000000000045, 0.0), (121.33333333333381, 0.0), (125.66666666666717, 0.0), (130.0000000000005, 0.0), (134.33333333333385, 0.0), (138.66666666666723, 0.0), (143.00000000000057, 0.0), (147.3333333333339, 0.0), (151.66666666666728, 0.0), (156.0000000000006, 5.0), (160.33333333333397, 12.0), (164.6666666666673, 18.6), (169.00000000000065, 39.9), (173.333333333334, 58.0), (177.66666666666737, 66.5), (182.00000000000074, 70.2), (186.33333333333405, 78.7), (190.66666666666742, 84.0), (195.00000000000077, 92.0), (199.3333333333341, 95.7), (203.66666666666745, 96.8), (208.00000000000082, 97.9), (212.3333333333342, 98.4), (216.6666666666675, 100.0), (221.00000000000088, 100.0), (225.33333333333422, 100.0), (229.66666666666757, 100.0), (234.0000000000009, 100.0), (238.33333333333428, 100.0), (242.66666666666762, 100.0), (247.00000000000097, 100.0), (251.33333333333434, 100.0), (255.66666666666768, 100.0), (260.000000000001, 100.0), (264.33333333333434, 100.0), (268.6666666666677, 100.0), (273.0000000000011, 100.0), (277.33333333333445, 100.0), (281.66666666666777, 100.0), (286.00000000000114, 100.0), (290.3333333333345, 100.0), (294.6666666666678, 100.0), (299.00000000000114, 100.0), (303.33333333333456, 100.0), (307.6666666666679, 100.0), (312.0000000000012, 100.0), (316.3333333333346, 100.0), (320.66666666666794, 100.0), (325.00000000000125, 100.0), (329.3333333333346, 100.0), (333.666666666668, 100.0), (338.0000000000013, 100.0), (342.3333333333347, 100.0), (346.666666666668, 100.0), (351.0000000000014, 100.0), (355.33333333333474, 100.0), (359.66666666666805, 100.0), (364.0000000000015, 100.0), (368.3333333333348, 100.0), (372.6666666666681, 100.0), (377.0000000000015, 100.0), (381.33333333333485, 100.0), (385.66666666666816, 100.0), (390.00000000000153, 100.0), (394.3333333333349, 100.0), (398.6666666666682, 100.0), (403.0000000000016, 100.0), (407.3333333333349, 100.0), (411.6666666666683, 100.0), (416.00000000000165, 100.0), (420.33333333333496, 100.0), (424.6666666666684, 100.0), (429.0000000000017, 100.0), (433.333333333335, 100.0), (437.6666666666684, 100.0), (442.00000000000176, 100.0), (446.3333333333351, 100.0), (450.66666666666845, 100.0), (455.0000000000018, 100.0), (459.33333333333513, 100.0), (463.6666666666685, 100.0), (468.0000000000018, 100.0), (472.3333333333352, 100.0), (476.66666666666856, 100.0), (481.0000000000019, 100.0), (485.33333333333525, 100.0), (489.6666666666686, 100.0), (494.00000000000193, 100.0), (498.33333333333525, 100.0), (502.6666666666687, 100.0), (507.000000000002, 100.0), (511.33333333333536, 100.0), (515.6666666666687, 100.0), (520.000000000002, 100.0)]  , 'underlyingTrendInHealthNeeds' :  [(0.0, 1.0), (4.333333333333351, 1.0), (8.666666666666702, 1.0), (13.000000000000052, 1.0021), (17.333333333333403, 1.0043), (21.66666666666675, 1.0064), (26.000000000000103, 1.0085), (30.333333333333453, 1.0096), (34.666666666666806, 1.0117), (39.00000000000015, 1.0128), (43.3333333333335, 1.0149), (47.666666666666856, 1.016), (52.000000000000206, 1.0191), (56.333333333333556, 1.0202), (60.666666666666906, 1.0223), (65.00000000000026, 1.0255), (69.33333333333361, 1.02605), (73.66666666666696, 1.0287), (78.0000000000003, 1.0298), (82.33333333333366, 1.033), (86.666666666667, 1.0335), (91.00000000000037, 1.0351), (95.33333333333371, 1.0362), (99.66666666666706, 1.0394), (104.00000000000041, 1.0404), (108.33333333333375, 1.0415), (112.66666666666711, 1.0447), (117.00000000000045, 1.0457), (121.33333333333381, 1.0479), (125.66666666666717, 1.0489), (130.0000000000005, 1.05), (134.33333333333385, 1.0511), (138.66666666666723, 1.0543), (143.00000000000057, 1.0553), (147.3333333333339, 1.0574), (151.66666666666728, 1.0585), (156.0000000000006, 1.0596), (160.33333333333397, 1.0617), (164.6666666666673, 1.0628), (169.00000000000065, 1.0638), (173.333333333334, 1.0649), (177.66666666666737, 1.067), (182.00000000000074, 1.06755), (186.33333333333405, 1.0691), (190.66666666666742, 1.0702), (195.00000000000077, 1.0713), (199.3333333333341, 1.0723), (203.66666666666745, 1.0745), (208.00000000000082, 1.0766), (212.3333333333342, 1.07765), (216.6666666666675, 1.0787), (221.00000000000088, 1.0809), (225.33333333333422, 1.083), (229.66666666666757, 1.0835), (234.0000000000009, 1.0862), (238.33333333333428, 1.0872), (242.66666666666762, 1.0894), (247.00000000000097, 1.0915), (251.33333333333434, 1.09255), (255.66666666666768, 1.0936), (260.000000000001, 1.0947), (264.33333333333434, 1.0968), (268.6666666666677, 1.0989), (273.0000000000011, 1.1011), (277.33333333333445, 1.1021), (281.66666666666777, 1.1032), (286.00000000000114, 1.1053), (290.3333333333345, 1.1064), (294.6666666666678, 1.1085), (299.00000000000114, 1.1096), (303.33333333333456, 1.1117), (307.6666666666679, 1.11225), (312.0000000000012, 1.1138), (316.3333333333346, 1.1149), (320.66666666666794, 1.1181), (325.00000000000125, 1.1191), (329.3333333333346, 1.1202), (333.666666666668, 1.1223), (338.0000000000013, 1.12285), (342.3333333333347, 1.1255), (346.666666666668, 1.1277), (351.0000000000014, 1.1287), (355.33333333333474, 1.1298), (359.66666666666805, 1.1309), (364.0000000000015, 1.133), (368.3333333333348, 1.1351), (372.6666666666681, 1.1372), (377.0000000000015, 1.1388), (381.33333333333485, 1.1404), (385.66666666666816, 1.1426), (390.00000000000153, 1.1447), (394.3333333333349, 1.14575), (398.6666666666682, 1.1468), (403.0000000000016, 1.1489), (407.3333333333349, 1.1511), (411.6666666666683, 1.1543), (416.00000000000165, 1.15535), (420.33333333333496, 1.1574), (424.6666666666684, 1.1585), (429.0000000000017, 1.1596), (433.333333333335, 1.1617), (437.6666666666684, 1.1628), (442.00000000000176, 1.1649), (446.3333333333351, 1.166), (450.66666666666845, 1.1681), (455.0000000000018, 1.1691), (459.33333333333513, 1.1734), (463.6666666666685, 1.17395), (468.0000000000018, 1.1766), (472.3333333333352, 1.17715), (476.66666666666856, 1.1787), (481.0000000000019, 1.1809), (485.33333333333525, 1.1819), (489.6666666666686, 1.183), (494.00000000000193, 1.1851), (498.33333333333525, 1.1862), (502.6666666666687, 1.1872), (507.000000000002, 1.1883), (511.33333333333536, 1.1894), (515.6666666666687, 1.1915), (520.000000000002, 1.1957)]  , 
        }
    
    
        self.dimensions = {
        	'waitingTime': {
                'labels': [ 'lessThan6mths',  'between6To12mths',  'between12To24mths',  'over24mths'  ],
                'variables': [ 'percentBecomingUrgentByWaitingTimePa'  ],
            },
        	'': {
                'labels': [  ],
                'variables': [  ],
            },
        }
                
        self.dimensions_order = {'percentBecomingUrgentByWaitingTimePa': ['waitingTime']}     
    
        self.stocks = ['13wkWaitForUrgentTreatment',   'depletingStockOfUnmetNeed',   'holdingStockOfPotentialUnmetNeed',   'outcomeOfConsultation',   'outcomeOfConsultationForDelayedDemand',   'recognisedNeedForGpConsultation',   'testResults',   'waiting12To24mthsForTreatment',   'waiting6To12mthsForTreatment',   'waiting6mthsForTreatment',   'waitingForDiagnostics',   'waitingOver24mthsForTreatment'  ]
        self.flows = ['between12To24mthWaitToUrgent',   'between6To12mthWaitToUrgent',   'covidDelayedNeedPresenting',   'decisionNotToPresent',   'delayedDemandToWaitForDiagnostics',   'delayedNeedNotPresenting',   'holdingStockReleasedAtEndOfCovid',   'incidenceOfCondition',   'lessThan6mthToUrgent',   'needPresentingAsUsual',   'negativeTestResults',   'nfaFollowingInitialConsultation',   'nfaFollowingInitialConsultationForCovidDelayedNeed',   'positiveTestResultsRoutine',   'positiveTestResultsUrgent',   'proceedingToTestsWithoutCovidDelay',   'routineTreatment',   'routineTreatmentFrom12To24mthWait',   'routineTreatmentFrom6To12thWaits',   'undergoingDiagnosticTests',   'urgentTreatment',   'waitingMoreThan12mths',   'waitingMoreThan2yrs',   'waitingMoreThan6mths'  ]
        self.converters = ['averagePreCovidWaitForDiagnostics',   'averageWaitForDiagnosticTest',   'baselineTreatmentCapacity',   'covidDelayedPercentOfPositiveTestsUrgent',   'covidModifiedPercentUrgent',   'covidSwitch',   'expectedPopulationRateOfIncidencePw',   'increasedPercentOfNeedForDiagnosticsForCovidDelayedDemand',   'newCapacityWeekAvailable',   'percentBecomingUrgentByWaitingTimePa',   'percentBecomingUrgentByWaitingTimePa[lessThan6mths]',   'percentBecomingUrgentByWaitingTimePa[between6To12mths]',   'percentBecomingUrgentByWaitingTimePa[between12To24mths]',   'percentBecomingUrgentByWaitingTimePa[over24mths]',   'percentIncreaseInDiagnosticCapacityPostCovid',   'percentNegativeTestResults',   'percentOfNeedReferredForDiagnostics',   'percentOfUnmetNeedReturning',   'percentPeopleNotPresentingDuringCovid',   'percentReductionInTreatmentCapacityDuringCovid',   'periodOfReturnInWks',   'postCovidIncreaseInTreatmentCapacity',   'preCovidCapacityForDiagnostics',   'preCovidPercentOfPositiveTestsUrgent',   'preCovidTreatmentCapacity',   'reducedDiagnosticCapacityDuringCovid',   'switchForDemographicIncrease',   'totalTreatmentCapacity',   'totalWaitingForDiagnosticsOrTreatment'  ]
        self.gf = ['covidPeriod',   'netCovidInducedChangesInUnderlyingHealthNeeds?',   'timingOfNewDiagnosticCapacity',   'underlyingTrendInHealthNeeds'  ]
        self.constants= []
        self.events = [
            ]
    
        self.memo = {}
        for key in list(self.equations.keys()):
          self.memo[key] = {}  # DICT OF DICTS!
          
    
    """
    Builtin helpers
    """
    def ramp(self,slope,start,t):
        if not start:
            start = self.starttime
        if t <= start: return 0
        return (t-start)*slope
        
    def rootn(self,expression,order):
        order = round(order,0)
        if expression < 0 and order % 2 == 0: # Stella does not allow even roots for negative numbers as no complex numbers are supported
            return np.nan
        return -abs(expression)**(1/round(order,0)) if expression < 0 else abs(expression)**(1/round(order,0)) # Stella Logic! No Complex numbers for negative numbers. Hence take the nth root of the absolute value and then add the negativity (if any)
    
    """
    Statistical builtins with Seed
    """
    def pareto_with_seed(self, shape, scale, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.pareto(shape) * scale  
    
    def weibull_with_seed(self, shape, scale, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.weibull(shape) * scale      
    
    def poisson_with_seed(self, mu, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.poisson(mu)   
    
    def negbinomial_with_seed(self, successes, p, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.negative_binomial(successes, p)  
    
    def lognormal_with_seed(self, mean, stdev, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.lognormal(mean, stdev)   
    
    def logistic_with_seed(self, mean, scale, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.logistic(mean, scale)
    
    def random_with_seed(self, seed, t ):
        if t == self.starttime:
            random.seed(int(seed))
        return random.random()

    def beta_with_seed(self, a,b,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.beta(a,b)
        
    def binomial_with_seed(self, n,p,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.binomial(n,p)
        
    def gamma_with_seed(self, shape,scale,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.gamma(shape,scale)
        
    def exprnd_with_seed(self, plambda,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.exponential(plambda)
        
    def geometric_with_seed(self, p, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.geometric(p)
    
    def triangular_with_seed(self, left, mode, right, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.triangular(left, mode, right)
    
    def rank(self, lis, rank):
        rank = int(rank)
        sorted_list = np.sort(lis)
        try:
            rankth_elem = sorted_list[rank-1]
        except IndexError as e:
            logging.error("RANK: Rank {} too high for array of size {}".format(rank,len(lis)))
        return (lis==rankth_elem).nonzero()[0][0]+1
        

    def interpolate(self, variable, t, *args):
        """
        Helper for builtin "interpolate". Uses the arrayed variable and args to compute the interpolation
        :param variable:
        :param t:
        :param args: Interpolation weight for each dimension, between one or zero
        :return:
        """
        def compute_x(values): #
            """
            Compute x values for interpolation. Always from 0 to 1. E.g. values = [1,2,3], then x = [0, 0.5, 1.0]
            :param values:
            :return:
            """
            #
            x = [0]
            for i in range(1, len(values)): x += [x[i - 1] + 1 / (len(values) - 1)]
            return x

        def interpolate_values(index, y_val):  # Internal interpolate of a dimension's results
            x_val = compute_x(y_val)
            points = [(x_val[i], y_val[i]) for i in range(0, len(x_val))]
            return LERP(index, points)

        # Fix each weight to a value between 0 and 1
        args = [max(0,min(x,1)) for x in args]

        # Get dimensions of variable (2,3,4 ...)
        dimensions = self.dimensions_order[variable]

        # Get Labels
        labels = {key: dim["labels"] for key, dim in
                  dict(filter(lambda elem: elem[0] in dimensions, self.dimensions.items())).items()}

        # Compute
        results = {}
        if len(labels.keys()) == 1:
            return interpolate_values(args[0], self.equation(variable + "[*]", t))
        for index, dimension in enumerate(dimensions):
            results[dimension] = []
            for label in labels[dimension]:
                indices = ["*" if i != index else label for i in
                           range(0, len(dimensions))]  # Build indices, such as "*,element1" or "1,*"

                results[dimension] += [
                    interpolate_values(args[index], self.equation(variable + "[{}]".format(",".join(indices)), t))]

        return [interpolate_values(args[i], v) for i, v in enumerate(results.values())][0]

    def lookupinv(self,gf, value):
        """
        Helper for lookupinv builtin. Looks for the corresponding x of a given y
        :param gf: Name of graphical function
        :param value: Value we are looking for (y)
        :return:
        """
        def lerpfun(x, points):  # Special lerp function for the reversed points
            from scipy.interpolate import interp1d
            x_vals = np.array([x[0] for x in points])
            y_vals = np.array([x[1] for x in points])
            f = interp1d(x_vals, y_vals)
            return f(x)

        results = []
        for t in np.arange(self.starttime, self.stoptime + self.dt,
                           self.dt):  # Compute all y values for graphical functions using standard interpolate (LERP)
            results += [(LERP(t, self.points[gf]), t)] # y,x

        return np.round(lerpfun(value, results),
                     3)  # Use LERP function for the reversed set of points (y,x) and find the correct value. Cannot use standard LERP here because that would require continuous X (1,2,3..)

    def delay(self, tdelayed, offset, initial, t):
        '''
        Delay builtin
        :param tdelayed: Delayed T
        :param offset: Offset
        :param initial: Initial value
        :param t:
        :return:
        '''
        if (t - self.starttime) < offset: return initial
        else: return tdelayed

    def counter(self,start, interval, t):
        '''
        Counter bultin
        :param start:
        :param interval:
        :param t:
        :return:
        '''
        num_elems = (interval / start / self.dt)
        value = interval / num_elems
        t_copy = copy(t)

        while t >= interval: t = t - interval
        if (t_copy > interval): return (start + (t / self.dt) * value)

        return (t / self.dt * value)

    def npv(self, initial, p, t):
        """
        NPV (Net Present Value) builtin
        :param initial:
        :param p:
        :param t:
        :return:
        """
        rate = 1.0 / (1.0 + p) ** (t - self.dt - self.starttime + self.dt)
        return initial if (t <= self.starttime) else ( self.npv(initial, p, t - self.dt) + (self.dt * rate * initial) )# Recurse

    def irr(self, stock_name, missing, t,myname):
        """
        Approximate IRR (Internal Rate of Return)
        :param stock_name: Identifier of Stock to approximate for
        :param missing: Replace missing values with this value
        :param t:
        :return:
        """

        def compute_npv(stock_name, t, i, missing):
            I = missing if missing else self.equation(stock_name, self.starttime)
            return I + sum( [self.memoize(stock_name, t) / (1 + i) ** t for t in np.arange(self.starttime+self.dt , t, self.dt)])

        i = 0
        try:
            i = 0 if t <= self.starttime + self.dt else self.memo[myname][t-self.dt]
        except:
            pass

        if t == self.starttime: return None

        best_kw = {i : compute_npv(stock_name, t, i, missing)}
        for _ in range(0, 300):
            # Here we approximate the IRR
            kw = compute_npv(stock_name, t, i, missing)

            change = 0.001

            best_kw[i] = kw

            if abs(kw) < self.memoize(stock_name, t)*0.1: change = 0.0001

            if abs(kw) < self.memoize(stock_name, t)*0.05: change = 0.00001

            if abs(kw) < self.memoize(stock_name, t)*0.02: change = 0.000001

            if kw < 0: i -= change
            elif kw > 0:  i += change

            if kw == 0: return i
        best_kw = {k: v for k, v in sorted(best_kw.items(), key=lambda item: item[1])}
        x = {v: k for k, v in sorted(best_kw.items(), key=lambda item: item[1])} # Sort by best npv
        return x[min(x.keys())]

    def normalcdf(self,left, right, mean, sigma):
        import scipy.stats
        right = scipy.stats.norm(float(mean), float(sigma)).cdf(float(right))
        left = scipy.stats.norm(float(mean), float(sigma)).cdf(float(left))
        return round(right - left, 3)

    def cgrowth(self, p):
        from sympy.core.numbers import Float
        import sympy as sy
        z = sy.symbols('z', real=True) # We want to find z
        dt = self.dt

        x = (1 + dt * (1 * z))

        for i in range(1, int(1 / dt)): x = (x + dt * (x * z))

        # Definition of the equation to be solved
        eq = sy.Eq(1 + p, x)

        # Solve the equation
        results = [x for x in (sy.solve(eq)) if type(x) is Float and x > 0] # Quadratic problem, hence usually a positive, negative and 2 complex solutions. We only require the positive one
        return float(results[0])

    def montecarlo(self,probability,seed, t):
        """
        Montecarlo builtin
        :param probability:
        :param seed:
        :param t:
        :return:
        """
        if seed and t==self.starttime:
            random.seed(seed)
        rndnumber = random.uniform(0,100)
        return 1 if rndnumber < (probability*self.dt) else 0


    def derivn(self, equation, order, t):
        """
        nth derivative of an equation
        :param equation: Name of the equation
        :param order: n
        :param t: current t
        :return:
        """
        memo = {}
        dt = 0.25

        def mem(eq, t):
            """
            Memo for internal equations
            :param eq:
            :param t:
            :return:
            """
            if not eq in memo.keys(): memo[eq] = {}
            mymemo = memo[eq]
            if t in mymemo.keys(): return mymemo[t]
            else:
                mymemo[t] = s[eq](t)
                return mymemo[t]

        s = {}
        s[1] = lambda t: 0 if t <= self.starttime else (self.memoize(equation, t) - self.memoize(equation, t - dt)) / dt

        def addEquation(n):
            s[n] = lambda t: 0 if t <= self.starttime else (mem(n - 1, t) - mem(n - 1, t - dt)) / dt

        for n in list(range(2, order + 1)): addEquation(n)

        return s[order](t) if ( t >= self.starttime + (dt * order) ) else 0

    def smthn(self, inputstream, averaging_time, initial, n, t):
        """
        Pretty complex operator. Actually we are building a whole model here and have it run
        Find info in https://www.iseesystems.com/resources/help/v1-9/default.htm#08-Reference/07-Builtins/Delay_builtins.htm#kanchor364
        :param inputstream:
        :param averaging_time:
        :param initial:
        :param n:
        :param t:
        :return:
        """
        memo = {}
        dt = self.dt
        from copy import deepcopy

        def mem(eq, t):
            """
            Internal memo for equations
            :param eq:
            :param t:
            :return:
            """
            if not eq in memo.keys(): memo[eq] = {}
            mymemo = memo[eq]
            if t in mymemo.keys():return mymemo[t]
            else:
                mymemo[t] = s[eq](t)
                return mymemo[t]

        s = {}

        def addEquation(n, upper):
            y = deepcopy(n)
            if y == 1:
                s["stock1"] = lambda t: (
                    (max([0, (self.memoize(inputstream, t) if (initial is None) else initial)])) if (
                                t <= self.starttime) else (
                                mem('stock1', t - dt) + dt * (mem('changeInStock1', t - dt))))
                s['changeInStock1'] = lambda t: (self.memoize(inputstream, t) - mem('stock1', t)) / (
                            averaging_time / upper)
            if y > 1:
                s["stock{}".format(y)] = lambda t: (
                    (max([0, (self.memoize(inputstream, t) if (initial is None) else initial)])) if (t <= self.starttime) else (
                                mem("stock{}".format(y), t - dt) + dt * (mem('changeInStock{}'.format(y), t - dt))))
                s['changeInStock{}'.format(y)] = lambda t: (mem("stock{}".format(y - 1), t) - mem("stock{}".format(y),
                                                                                                  t)) / (averaging_time / upper)
        n = int(n)

        for i in list(range(0, n + 1)): addEquation(i, n)

        return s['stock{}'.format(n)](t)

    def forcst(self,inputstream, averaging_time, horizon, initial, t):
        memo = {"change_in_input": {}, "average_input": {}, "trend_in_input": {}, "forecast_input": {}}

        def mem(eq, t):
            """
            Internal memo for equations
            :param eq:
            :param t:
            :return:
            """
            mymemo = memo[eq]
            if t in mymemo.keys(): return mymemo[t]
            else:
                mymemo[t] = s[eq](t)
                return mymemo[t]

        s = {
            "change_in_input": lambda t: max([0, (self.memoize(inputstream,t) - mem('average_input', t)) / averaging_time]),
            "average_input": lambda t: ((self.memoize(inputstream,t)) if (t <= self.starttime) else (
                        mem("average_input", t - self.dt) + self.dt * (mem("change_in_input", t - self.dt)))),
            "trend_in_input": lambda t: (((self.memoize(inputstream,t) - self.memoize('averageInput', t)) / (
                        self.memoize('averageInput', t) * self.memoize('averagingTime', t))) if (
                        self.memoize('averageInput', t) > 0.0) else (np.nan)),
            "forecast_input": lambda t: self.memoize(inputstream,t) * (1.0 + mem("trend_in_input", t) * horizon)
        }

        return s["forecast_input"](t)

    #Helpers for Dimensions (Arrays)

    def find_dimensions(self, stock):
        stockdimensions = {}
        for dimension, values in self.dimensions.items():
            if stock in values["variables"]:
                stockdimensions[dimension] = values["labels"]

        if len(stockdimensions.keys()) == 1:
            return [stock + "[{}]".format(x) for x in stockdimensions[list(stockdimensions.keys())[0]]]

    def get_dimensions(self, equation, t):
        re_find_indices = r'\[([^)]+)\]'
        group = re.search(re_find_indices, equation).group(0).replace("[", "").replace("]", "")
        equation_basic = equation.replace(group, "").replace("[]", "")
        labels = []
        for index, elem in enumerate(group.split(",")):
            if len(elem.split(":")) > 1: # List operator
                try:
                    bounds = [int(x) for x in elem.split(":")]
                except ValueError as e:
                    logging.error(e)
                    continue
                bounds = sorted(bounds)
                if len(bounds) > 2:
                    logging.error("Too many arguments for list operator. Expecting 2, got {}".format(len(bounds)))

                labels += [list(range(bounds[0], bounds[1]+1))]

            elif elem == "*": # Star operator
                dim = self.dimensions_order[equation_basic][index]
                labels += [self.dimensions[dim]["labels"]]
            else:
                if not type(elem) is list:
                    labels += [[elem]]
                else:
                    labels += [elem]

        products = cartesian_product(labels)

        return_list = []

        for product in products:
            prod = str(product).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
            return_list += [self.memoize(equation_basic + "[{}]".format(prod), t)]
            
        return np.array(return_list)


    #Access equations API

    def equation(self, equation, arg):
        return self.memoize(equation,arg)


    #Memoizer for equations. Also does most of API work

    def memoize(self, equation, arg):
        if type(equation) is float or type(equation) is int: # Fallback for values
            return equation
        if "*" in equation or ":" in equation:
            return self.get_dimensions(equation,arg)
            
        if not equation in self.equations.keys():

            # match array pattern and find non-arrayed var
            import re
            match = re.findall(r'\[[a-zA-Z1-9,_]*\]', equation)

            if match:

                equation_replaced = equation.replace(match[0], "")

                if equation_replaced in self.equations:
                    return self.memoize(equation=equation_replaced,arg=arg)
            else:
                logging.error("Equation '{}' not found!".format(equation))

        mymemo = self.memo[equation]

        if arg in mymemo.keys():
            return mymemo[arg]
        else:
            result = self.equations[equation](arg)
            mymemo[arg] = result

        return result


    def setDT(self, v):
        self.dt = v

    def setStarttime(self, v):
        self.starttime = v

    def setStoptime(self, v):
        self.stoptime = v
    
    def specs(self):
        return self.starttime, self.stoptime, self.dt, 'Weeks', 'Euler'
    