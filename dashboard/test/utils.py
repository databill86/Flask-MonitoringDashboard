"""
    Some useful functions for setting up the testing environment, adding data, etc..
"""
import datetime

NAME = 'main'
IP = '127.0.0.1'
GROUP_BY = '1'
EXECUTION_TIMES = [1000, 2000, 3000, 4000, 50000]
TIMES = [datetime.datetime.now()] * 5
for i in range(len(TIMES)):
    TIMES[i] += datetime.timedelta(seconds=i)
TEST_NAMES = ['test_name1', 'test_name2']


def set_test_environment():
    """ Override the config-object for a new testing environment. Module dashboard must be imported locally. """
    import dashboard
    dashboard.config.database_name = 'sqlite:///test-database.db'


def clear_db():
    """ Drops and creates the tables in the database. Module dashboard must be imported locally. """
    from dashboard.database import get_tables, engine
    for table in get_tables():
        table.__table__.drop(engine)
        table.__table__.create(engine)


def add_fake_data():
    """ Adds data to the database for testing purposes. Module dashboard must be imported locally. """
    from dashboard.database import session_scope, FunctionCall, MonitorRule, Tests, TestsGrouped
    from dashboard import config

    # Add functionCalls
    with session_scope() as db_session:
        for i in range(len(EXECUTION_TIMES)):
            call = FunctionCall(endpoint=NAME, execution_time=EXECUTION_TIMES[i], version=config.version,
                                time=TIMES[i], group_by=GROUP_BY, ip=IP)
            db_session.add(call)

    # Add MonitorRule
    with session_scope() as db_session:
        db_session.add(MonitorRule(endpoint=NAME, monitor=True, time_added=datetime.datetime.now(),
                                   version_added=config.version))

    # Add Tests
    with session_scope() as db_session:
        db_session.add(Tests(name=NAME, succeeded=True))

    # Add TestsGrouped
    with session_scope() as db_session:
        for test_name in TEST_NAMES:
            db_session.add(TestsGrouped(endpoint=NAME, test_name=test_name))


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)