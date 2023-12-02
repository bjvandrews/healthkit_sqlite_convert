import argparse
import logging
import sqlite_utils

from lxml import etree


DB_BUILD_RATE = 10000
MAX_RECORDS_IN_MEMORY = 1000

logging.basicConfig(
     level=logging.INFO, 
     format= '[%(asctime)s] %(levelname)s: %(message)s',
     datefmt='%H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def parse_xml_and_generate_tables(xml_path, db_path):
    # Building this database in memory, rather than on disk, is _significantly_ faster (~30sec, down from ~7-8 minutes)
    db = sqlite_utils.Database(memory=True)
    table_stats = dict()

    def _write_to_db(table_name, rows):
        db[table_name].insert_all(rows, alter=True, column_order=['startDate', 'endDate', 'value', 'unit'], batch_size=DB_BUILD_RATE)

    def _parse_record(records_dict, node, correlation_id, prefix=""):
        record = dict(node.attrib)
        record['correlation_id'] = correlation_id
        record_type = prefix + record['type'].replace("HKQuantityTypeIdentifier", "").replace("HKCategoryTypeIdentifier", "")
        record['type'] = record_type
        
        for m in node.iterchildren('MetadataEntry'):
            record[f"MetadataEntry_{m.attrib['key']}"] = m.attrib['value']
        
        if record_type not in records_dict:
            records_dict[record_type] = []    
            table_stats[record_type] = 0
        records_dict[record_type].append(record)
        table_stats[record_type] += 1
        if len(records_dict[record_type]) > MAX_RECORDS_IN_MEMORY:
            _write_to_db(record_type, records_dict[record_type])
            records_dict[record_type] = []
    
    logger.debug("Reading XML (this part is inefficient and uses a _lot_ of memory, but relatively quick)")

    tree = etree.parse(xml_path)
    health_data = tree.getroot()
    metadata = {
        'locale': health_data.attrib['locale']
    }
    
    # TODO: Swap this to single select
    for c in health_data.iterchildren('ExportDate'):
        metadata['ExportDate'] = c.attrib['value']
    for c in health_data.iterchildren('Me'):
        for key, value in c.attrib.items():
            metadata[key] = value

    records = dict()
        
    for c in health_data.iterchildren('Record'):
        _parse_record(records, c, None)

    logger.debug("Inserting Records into database")
    for key, data in records.items():
        _write_to_db(key, data)
    logger.debug("Records inserted")
    del records  # free RAM

    # Kinda looks like correlations just duplicate records... can't see anything linking them
    correlations = dict()
    correlation_records = dict()
    correlation_id = 0
    for c in health_data.iterchildren('Correlation'):
        entry = dict(c.attrib)
        entry['correlation_id'] = correlation_id
        
        entry['type'] = entry['type'].replace("HKQuantityTypeIdentifier", "").replace("HKCategoryTypeIdentifier", "").replace("HKCorrelationTypeIdentifier", "")
        
        for m in c.iterchildren('MetadataEntry'):
            key = m.attrib['key'].replace("HKMetadataKey", "").replace("HK", "")
            entry[key] = m.attrib['value']
        
        for r in c.iterchildren('Record'):
            _parse_record(correlation_records, r, correlation_id, prefix="Correlation")

        if entry['type'] not in correlations:
            correlations[entry['type']] = []    
        correlations[entry['type']].append(entry)
        correlation_id += 1
    
    logger.debug("Inserting correlations & correlation records into database")
    for key, data in correlations.items():
        _write_to_db(key, data)
    logger.debug("Correlations inserted")
    for key, data in correlation_records.items():
        _write_to_db(key, data)
    logger.debug("Correlation Records inserted")
    del correlations
    del correlation_records

    activity_summaries = []
    for c in health_data.iterchildren('ActivitySummary'):
        entry = dict(c.attrib)
        activity_summaries.append(entry)

    logger.debug("Inserting activity summaries into database")
    _write_to_db('ActivitySummary', activity_summaries)
    logger.debug("Activity Summaries inserted")
    del activity_summaries

    workouts = []
    workout_id = 0
    for c in health_data.iterchildren('Workout'):
        entry = dict(c.attrib)
        entry['workout_id'] = workout_id
        
        # Duplicated in v13, but this will eliminate it
        for m in c.iterchildren('MetadataEntry'):
            key = m.attrib['key'].replace("HKMetadataKey", "").replace("HK", "")
            entry[key] = m.attrib['value']
        
        entry['events'] = []
        for e in c.iterchildren('WorkoutEvent'):
            event = dict(e.attrib)
            event['workout_id'] = workout_id
            entry['events'].append(event)
        
        workouts.append(entry)

    logger.debug("Inserting workouts into database")
    _write_to_db('Workout', workouts)
    logger.debug("Workouts inserted")
    del workouts

    logger.debug("DB built")

    logger.debug("Writing DB to file")
    db.execute(f"vacuum main into '{db_path}'")
    logger.debug("DB written")

    logger.info("Record numbers:")
    for key, value in table_stats.items():
        logger.info(f"{key}: {value:,d} entries")
    

xml_file_path = 'export.xml'
db_file_path = 'apple_health4.db'

parser = argparse.ArgumentParser()
parser.add_argument("xml_file_path")
parser.add_argument("db_file_path")
args = parser.parse_args()

xml_file_path = args.xml_file_path
db_file_path = args.db_file_path

parse_xml_and_generate_tables(xml_file_path, db_file_path)
logger.debug("Done")
