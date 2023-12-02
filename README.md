# Inefficient but Fast Healthkit to SQLite Converter

I wanted to convert a healthkit export into an sqlite database faster and remove duplicates in v13 (correlation records were added, and healthkit-to-sqlite duplicates DietaryEnergyConsumed as a result).

On my current export this uses ~10 GB of RAM but completes in just under a minute; healthkit-to-sqlite was taking around 7-8 minutes.

The overwhelming majority of the time is writing an SQLite database to disk, progressively. Swapping to in-memory then vacuuming into a file reduced that time to under 30 seconds.

There is a lot of scope to improve this, but it meets my needs so I'm stopping here for now.

## Example Usage
Note: the timestamps per-message are incorrect (delayed printing, not sure why), but the total time is correct.
```
python healthkit_convert.py export.xml healthdb4.db
[18:55:31] DEBUG: Reading XML (this part is inefficient and uses a _lot_ of memory, but relatively quick)
[18:56:08] DEBUG: Inserting Records into database
[18:56:09] DEBUG: Records inserted
[18:56:09] DEBUG: Inserting correlations & correlation records into database
[18:56:09] DEBUG: Correlations inserted
[18:56:09] DEBUG: Correlation Records inserted
[18:56:10] DEBUG: Inserting activity summaries into database
[18:56:10] DEBUG: Activity Summaries inserted
[18:56:10] DEBUG: Inserting workouts into database
[18:56:10] DEBUG: Workouts inserted
[18:56:10] DEBUG: DB built
[18:56:10] DEBUG: Writing DB to file
[18:56:12] DEBUG: DB written
[18:56:12] INFO: Record numbers:
[18:56:12] INFO: BodyMassIndex: 744 entries
[18:56:12] INFO: Height: 2 entries
[18:56:12] INFO: BodyMass: 757 entries
[18:56:12] INFO: HeartRate: 404,554 entries
[18:56:12] INFO: OxygenSaturation: 23,075 entries
[18:56:12] INFO: BloodPressureSystolic: 511 entries
[18:56:12] INFO: BloodPressureDiastolic: 511 entries
[18:56:12] INFO: RespiratoryRate: 35,441 entries
[18:56:12] INFO: BodyFatPercentage: 667 entries
[18:56:12] INFO: LeanBodyMass: 3,784 entries
[18:56:12] INFO: StepCount: 95,305 entries
[18:56:12] INFO: DistanceWalkingRunning: 171,827 entries
[18:56:12] INFO: BasalEnergyBurned: 295,396 entries
[18:56:12] INFO: ActiveEnergyBurned: 884,637 entries
[18:56:12] INFO: FlightsClimbed: 11,864 entries
[18:56:12] INFO: DietaryFatTotal: 787 entries
[18:56:12] INFO: DietaryFatPolyunsaturated: 251 entries
[18:56:12] INFO: DietaryFatMonounsaturated: 251 entries
[18:56:12] INFO: DietaryFatSaturated: 787 entries
[18:56:12] INFO: DietaryCholesterol: 295 entries
[18:56:12] INFO: DietarySodium: 744 entries
[18:56:12] INFO: DietaryCarbohydrates: 814 entries
[18:56:12] INFO: DietaryFiber: 549 entries
[18:56:12] INFO: DietarySugar: 798 entries
[18:56:12] INFO: DietaryEnergyConsumed: 985 entries
[18:56:12] INFO: DietaryProtein: 800 entries
[18:56:12] INFO: DietaryVitaminA: 152 entries
[18:56:12] INFO: DietaryVitaminB6: 195 entries
[18:56:12] INFO: DietaryVitaminB12: 156 entries
[18:56:12] INFO: DietaryVitaminC: 134 entries
[18:56:12] INFO: DietaryVitaminD: 225 entries
[18:56:12] INFO: DietaryVitaminE: 137 entries
[18:56:12] INFO: DietaryVitaminK: 113 entries
[18:56:12] INFO: DietaryCalcium: 278 entries
[18:56:12] INFO: DietaryIron: 202 entries
[18:56:12] INFO: DietaryThiamin: 152 entries
[18:56:12] INFO: DietaryRiboflavin: 177 entries
[18:56:12] INFO: DietaryNiacin: 152 entries
[18:56:12] INFO: DietaryFolate: 147 entries
[18:56:12] INFO: DietaryBiotin: 23 entries
[18:56:12] INFO: DietaryPantothenicAcid: 138 entries
[18:56:12] INFO: DietaryPhosphorus: 108 entries
[18:56:12] INFO: DietaryIodine: 25 entries
[18:56:12] INFO: DietaryMagnesium: 190 entries
[18:56:12] INFO: DietaryZinc: 184 entries
[18:56:12] INFO: DietarySelenium: 182 entries
[18:56:12] INFO: DietaryCopper: 140 entries
[18:56:12] INFO: DietaryManganese: 141 entries
[18:56:12] INFO: DietaryMolybdenum: 3 entries
[18:56:12] INFO: DietaryPotassium: 241 entries
[18:56:12] INFO: AppleExerciseTime: 20,071 entries
[18:56:12] INFO: DietaryCaffeine: 10 entries
[18:56:12] INFO: WaistCircumference: 3 entries
[18:56:12] INFO: RestingHeartRate: 1,892 entries
[18:56:12] INFO: VO2Max: 188 entries
[18:56:12] INFO: WalkingHeartRateAverage: 953 entries
[18:56:12] INFO: EnvironmentalAudioExposure: 45,293 entries
[18:56:12] INFO: HeadphoneAudioExposure: 3,909 entries
[18:56:12] INFO: WalkingDoubleSupportPercentage: 17,392 entries
[18:56:12] INFO: SixMinuteWalkTestDistance: 107 entries
[18:56:12] INFO: AppleStandTime: 46,507 entries
[18:56:12] INFO: WalkingSpeed: 19,414 entries
[18:56:12] INFO: WalkingStepLength: 19,414 entries
[18:56:12] INFO: WalkingAsymmetryPercentage: 5,480 entries
[18:56:12] INFO: StairAscentSpeed: 4,986 entries
[18:56:12] INFO: StairDescentSpeed: 4,018 entries
[18:56:12] INFO: HKDataTypeSleepDurationGoal: 1 entries
[18:56:12] INFO: AppleWalkingSteadiness: 113 entries
[18:56:12] INFO: AppleSleepingWristTemperature: 407 entries
[18:56:12] INFO: HeartRateRecoveryOneMinute: 160 entries
[18:56:12] INFO: EnvironmentalSoundReduction: 2,830 entries
[18:56:12] INFO: TimeInDaylight: 1,193 entries
[18:56:12] INFO: PhysicalEffort: 17,459 entries
[18:56:12] INFO: SleepAnalysis: 20,590 entries
[18:56:12] INFO: AppleStandHour: 23,035 entries
[18:56:12] INFO: HighHeartRateEvent: 8 entries
[18:56:12] INFO: AudioExposureEvent: 8 entries
[18:56:12] INFO: LowCardioFitnessEvent: 6 entries
[18:56:12] INFO: HeartRateVariabilitySDNN: 8,841 entries
[18:56:12] INFO: CorrelationBloodPressureDiastolic: 511 entries
[18:56:12] INFO: CorrelationBloodPressureSystolic: 511 entries
[18:56:12] INFO: CorrelationDietaryCarbohydrates: 814 entries
[18:56:12] INFO: CorrelationDietaryFatSaturated: 787 entries
[18:56:12] INFO: CorrelationDietaryProtein: 800 entries
[18:56:12] INFO: CorrelationDietaryEnergyConsumed: 884 entries
[18:56:12] INFO: CorrelationDietaryCalcium: 278 entries
[18:56:12] INFO: CorrelationDietarySodium: 744 entries
[18:56:12] INFO: CorrelationDietaryIron: 202 entries
[18:56:12] INFO: CorrelationDietarySugar: 798 entries
[18:56:12] INFO: CorrelationDietaryFiber: 549 entries
[18:56:12] INFO: CorrelationDietaryCholesterol: 295 entries
[18:56:12] INFO: CorrelationDietaryVitaminA: 152 entries
[18:56:12] INFO: CorrelationDietaryVitaminC: 134 entries
[18:56:12] INFO: CorrelationDietaryFatTotal: 787 entries
[18:56:12] INFO: CorrelationDietaryVitaminD: 225 entries
[18:56:12] INFO: CorrelationDietaryPotassium: 241 entries
[18:56:12] INFO: CorrelationDietaryCaffeine: 10 entries
[18:56:12] INFO: CorrelationDietaryFatMonounsaturated: 251 entries
[18:56:12] INFO: CorrelationDietaryFatPolyunsaturated: 251 entries
[18:56:12] INFO: CorrelationDietaryMagnesium: 190 entries
[18:56:12] INFO: CorrelationDietaryThiamin: 152 entries
[18:56:12] INFO: CorrelationDietaryPhosphorus: 108 entries
[18:56:12] INFO: CorrelationDietaryFolate: 147 entries
[18:56:12] INFO: CorrelationDietaryVitaminE: 137 entries
[18:56:12] INFO: CorrelationDietaryRiboflavin: 177 entries
[18:56:12] INFO: CorrelationDietaryCopper: 140 entries
[18:56:12] INFO: CorrelationDietaryVitaminK: 113 entries
[18:56:12] INFO: CorrelationDietaryZinc: 184 entries
[18:56:12] INFO: CorrelationDietaryPantothenicAcid: 138 entries
[18:56:12] INFO: CorrelationDietaryNiacin: 152 entries
[18:56:12] INFO: CorrelationDietaryManganese: 141 entries
[18:56:12] INFO: CorrelationDietaryVitaminB12: 156 entries
[18:56:12] INFO: CorrelationDietaryVitaminB6: 195 entries
[18:56:12] INFO: CorrelationDietarySelenium: 182 entries
[18:56:12] INFO: CorrelationDietaryIodine: 25 entries
[18:56:12] INFO: CorrelationDietaryBiotin: 23 entries
[18:56:12] INFO: CorrelationDietaryMolybdenum: 3 entries
[18:56:17] DEBUG: Done
```

## Example Query
I use this to export data to a CSV file using `DB Browser for SQLite`.

Open as a spreadsheet then add in a couple of columns to subtract the predicted weight loss from the previous day, and you can compare what Apple Health predicts your weight should be versus what it actually is; for me, it tracks more-or-less bang on.

The query could be cleaned up, but it works so I've left it as-is.

```
SELECT dateComponents AS day, 
    activeEnergyBurned, 
    activeEnergyBurnedGoal, 
    appleExerciseTime, 
    appleExerciseTimeGoal, 
    z.value AS basalEnergy, 
    z.value + activeEnergyBurned as totalEnergy, 
    zdiet.value as dietaryEnergy, 
    zdiet.value - z.value + activeEnergyBurned AS lossEnergy,
    lossEnergy / 37700 AS predictedLossKG,
    zm.value weight, 
    zf.value fatPercentage, 
    zl.value leanMass, 
    zm.value-zl.value otherMass, 
    zv.value vo2Max, 
    zfl.value flightsClimbed, 
    zhrr.value maxHeartRateRecovery1min, 
    zst.value stepCount, 
    zdist.value distance
FROM ActivitySummary az 
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, SUM(value) value
FROM BasalEnergyBurned
WHERE unit="kJ" AND (sourceName = "Sunwell (Bruce’s Apple Watch)" or sourceName = "Bruce’s Apple Watch")
GROUP BY day) z ON z.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, MAX(value) value
FROM BodyMass
GROUP BY day) zm ON zm.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, MAX(value) value
FROM BodyFatPercentage
GROUP BY day) zf ON zf.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, MAX(value) value
FROM LeanBodyMass
GROUP BY day) zl ON zl.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, MAX(value) value
FROM VO2Max
WHERE sourceName = "Sunwell (Bruce’s Apple Watch)" or sourceName = "Bruce’s Apple Watch"
GROUP BY day) zv ON zv.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, SUM(value) value
FROM FlightsClimbed
WHERE sourceName = "Sunwell (Bruce’s Apple Watch)" or sourceName = "Bruce’s Apple Watch"
GROUP BY day) zfl ON zfl.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, MAX(value) value
FROM HeartRateRecoveryOneMinute
WHERE sourceName = "Sunwell (Bruce’s Apple Watch)" or sourceName = "Bruce’s Apple Watch"
GROUP BY day) zhrr ON zhrr.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, SUM(value) value
FROM StepCount
WHERE sourceName = "Sunwell (Bruce’s Apple Watch)" or sourceName = "Bruce’s Apple Watch"
GROUP BY day) zst ON zst.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, SUM(value) value
FROM DistanceWalkingRunning
WHERE sourceName = "Sunwell (Bruce’s Apple Watch)" or sourceName = "Bruce’s Apple Watch"
GROUP BY day) zdist ON zdist.day=az.dateComponents
LEFT JOIN (SELECT date(substr(startDate, 0,20)) day, SUM(value) value
FROM DietaryEnergyConsumed
GROUP BY day) zdiet ON zdiet.day=az.dateComponents
;
```