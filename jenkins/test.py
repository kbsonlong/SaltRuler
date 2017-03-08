import requests
import jenkins
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


def connectToJenkinsServer(url, username, password):
    server = jenkins.Jenkins(url,
                             username=username, password=password)
    return server


def connectDb():
    engine = create_engine('sqlite:///cli.db', echo=False)
    session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine)
    return session


def createJob(session, jlist):
    for j in jlist:
        session.add(j)
    session.commit()


def getPreviousJobId(session, name):
    job = session.query(JobsInfo).filter_by(name=name).order_by(JobsInfo.jen_id.desc()).first()
    if (job != None):
        return job.jen_id
    else:
        return None


class JobsInfo(Base):
    __tablename__ = 'JobsInfo'

    id = Column(Integer, primary_key=True)
    jen_id = Column(Integer)
    name = Column(String)
    timeStamp = Column(DateTime)

    estimatedDuration = Column(String)


def createJobDetails(start, lastBuildNumber, jobName):
    jList = []
    for i in range(start + 1, lastBuildNumber + 1):
        status = server.get_build_info(jobName, i)
        status_as_jobs = JobsInfo()
        status_as_jobs.jen_id = current['id']

        status_as_jobs.estimatedDuration = current['estimatedDuration']
        status_as_jobs.name = jobName

        status_as_jobs.timeStamp = datetime.datetime.fromtimestamp(long(status['timestamp']) * 0.001)
        jList.append(status_as_jobs)
    return jList


url = 'http://192.168.62.200:10001'
username = raw_input('Enter username: ')
password = raw_input('Enter password: ')
server = connectToJenkinsServer(url, username, password)

authenticated = false
try:
    server.get_whoami()
    authenticated = true
except jenkins.JenkinsException as e:
    print 'Authentication error'
    authenticated = false

if authenticated:
    session = connectDb()

    jobs = server.get_all_jobs()
    for j in jobs:
        jobName = j['name']

        lastJobId = getPreviousJobId(session, jobName)
        lastBuildNumber = server.get_job_info(jobName)['lastBuild']['number']

        if lastJobId == None:
            start = 0

        else:
            start = lastJobId

        jlist = createJobDetails(start, lastBuildNumber, jobName)

        createJob(session, jlist)