
# Can't get lxml or base python lib to parse doctype tags...
doctype_healthkit_version = 13
doctype_healthkit = {
    'HealthData': {
        'attributes': {
            'locale': 'text'
        },
        'children': ['ExportDate', 'Me', 'Record', 'Correlation', 'Workout', 'ActivitySummary', 'ClinicalRecord', 'Audiogram', 'VisionPrescription']
    },
    'ExportDate': {
        'attributes': {
            'value': 'datetime'
        },
        'children': []
    },
    'Me': {
        'attributes': {
            'HKCharacteristicTypeIdentifierDateOfBirth': 'date',
            'HKCharacteristicTypeIdentifierBiologicalSex': 'text',
            'HKCharacteristicTypeIdentifierBloodType': 'text',
            'HKCharacteristicTypeIdentifierFitzpatrickSkinType': 'text',
            'HKCharacteristicTypeIdentifierCardioFitnessMedicationsUse': 'text',
        },
        'children': []
    },
    'Record': {
        'attributes': {
            'type': 'text',
            'unit': 'text',
            'value': 'float',
            'sourceName': 'text',
            'sourceVersion': 'text',
            'device': 'text',
            'creationDate': 'datetime',
            'startDate': 'datetime',
            'endDate': 'datetime',
        },
        'children': ['MetadataEntry', 'HeartRateVariabilityMetadataList']
    },
    'Correlation': {
        'attributes': {
            'type': 'text',
            'sourceName': 'text',
            'sourceVersion': 'text',
            'device': 'text',
            'creationDate': 'datetime',
            'startDate': 'datetime',
            'endDate': 'datetime',
        },
        'children': ['MetadataEntry', 'Record']
    },
    'Workout': {
        'attributes': {
            'workoutActivityType': 'text',
            'duration': 'text',
            'sourceName': 'text',
            'device': 'text',
            'creationDate': 'datetime',
            'startDate': 'datetime',
            'endDate': 'datetime',
            'duration': 'float',
            'durationUnit': 'text',
        },
        'children': ['MetadataEntry', 'WorkoutEvent', 'WorkoutRoute', 'WorkoutStatistics']
    },
    'WorkoutActivity': {
        'attributes': {
            'uuid': 'text',
            'startDate': 'datetime',
            'endDate': 'datetime',
            'duration': 'float',
            'durationUnit': 'text',
        },
        'children': ['MetadataEntry']
    },
    'WorkoutEvent': {
        'attributes': {
            'type': 'text',
            'date': 'datetime',
            'duration': 'float',
            'durationUnit': 'text',
        },
        'children': ['MetadataEntry']
    },
    'WorkoutStatistics': {
        'attributes': {
            'type': 'text',
            'startDate': 'datetime',
            'endDate': 'datetime',
            'average': 'float',
            'minimum': 'float',
            'maximum': 'float',
            'sum': 'float',
            'unit': 'text',
        },
        'children': []
    },
    'WorkoutRoute': {
        'attributes': {
            'sourceName': 'text',
            'sourceVersion': 'text',
            'device': 'text',
            'creationDate': 'datetime',
            'startDate': 'datetime',
            'endDate': 'datetime',
        },
        'children': ['MetadataEntry', 'FileReference']
    },
    'FileReference': {
        'attributes': {
            'path': 'text',
        },
        'children': []
    },
    'ActivitySummary': {
        'attributes': {
            'dateComponents': 'date',
            'activeEnergyBurned': 'float',
            'activeEnergyBurnedGoal': 'int',
            'activeEnergyBurnedUnit': 'text',
            'appleMoveTime': 'int',
            'appleMoveTimeGoal': 'int',
            'appleExerciseTime': 'int',
            'appleExerciseTimeGoal': 'int',
            'appleStandHours': 'int',
            'appleStandHoursGoal': 'int',
        },
        'children': []
    },
    'MetadataEntry': {
        'attributes': {
            'key': 'text',
            'value': 'text',
        },
        'children': []
    },
    'HeartRateVariabilityMetadataList': {
        'attributes': {

        },
        'children': ['InstantaneousBeatsPerMinute']
    },
    'InstantaneousBeatsPerMinute': {
        'attributes': {
            'bpm': 'int',
            'time': 'time',
        },
        'children': []
    },
    'ClinicalRecord': {
        'attributes': {
            'type': 'text',
            'identifier': 'text',
            'sourceName': 'text',
            'sourceURL': 'text',
            'fhirVersion': 'text',
            'receivedDate': 'date',
            'resourceFilePath': 'text',
        },
        'children': []
    },
    'Audiogram': {
        'attributes': {
            'type': 'text',
            'sourceName': 'text',
            'sourceVersion': 'text',
            'device': 'text',
            'creationDate': 'datetime',
            'startDate': 'datetime',
            'endDate': 'datetime',
        },
        'children': ['MetadataEntry', 'SensitivityPoint']
    },
    'SensitivityPoint': {
        'attributes': {
            'frequencyValue': 'float',
            'frequencyUnit': 'text',
            'leftEarValue': 'float',
            'leftEarUnit': 'float',
            'rightEarValue': 'float',
            'rightEarUnit': 'float',
        },
        'children': []
    },
    'VisionPrescription': {
        'attributes': {
            'type': 'text',
            'dateIssued': 'date',
            'expirationDate': 'date',
            'brand': 'text',
        },
        'children': ['RightEye', 'LeftEye', 'Attachment', 'MetadataEntry']
    },
    'RightEye': {
        'attributes': {
            'sphere': 'float',
            'sphereUnit': 'text',
            'cylinder': 'float',
            'cylinderUnit': 'text',
            'axis': 'float',
            'axisUnit': 'text',
            'add': 'float',
            'addUnit': 'text',
            'vertex': 'float',
            'vertexUnit': 'text',
            'prismAmount': 'float',
            'prismAmountUnit': 'text',
            'prismAngle': 'float',
            'prismAngleUnit': 'text',
            'farPD': 'float',
            'farPDUnit': 'text',
            'nearPD': 'float',
            'nearPDUnit': 'text',
            'baseCurve': 'float',
            'baseCurveUnit': 'text',
            'diameter': 'float',
            'diameterUnit': 'text',
        },
        'children': []
    },
    'LeftEye': {
        'attributes': {
            'sphere': 'float',
            'sphereUnit': 'text',
            'cylinder': 'float',
            'cylinderUnit': 'text',
            'axis': 'float',
            'axisUnit': 'text',
            'add': 'float',
            'addUnit': 'text',
            'vertex': 'float',
            'vertexUnit': 'text',
            'prismAmount': 'float',
            'prismAmountUnit': 'text',
            'prismAngle': 'float',
            'prismAngleUnit': 'text',
            'farPD': 'float',
            'farPDUnit': 'text',
            'nearPD': 'float',
            'nearPDUnit': 'text',
            'baseCurve': 'float',
            'baseCurveUnit': 'text',
            'diameter': 'float',
            'diameterUnit': 'text',
        },
        'children': []
    },
    'Attachment': {
        'attributes': {
            'identifier': 'text',
        },
        'children': []
    },
}
