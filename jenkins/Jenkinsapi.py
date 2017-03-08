from jenkinsapi.jenkins import Jenkins

def get_server_instance():
    jenkins_url = 'http://192.168.62.200:10001'
    server = Jenkins(jenkins_url,username='admin',password='kbsonlong')
    server.keys()
    return server

def get_job_details():
    server = get_server_instance()
    for job_name,job_instance in server.get_jobs():
        print 'Job Nmae: %s' % (job_instance.name)
        print 'Job Description: %s' % (job_instance.get_description())
        print 'Is Job running: %s' % (job_instance.is_running())
        print 'Is Job enabled: %s' % (job_instance.is_enabled())

def disable_job():
    server = get_server_instance()
    for job_name, job_instance in server.get_jobs():
        if (server.has_job(job_name)):
            job_instance = server.get_job(job_name)
            job_instance.disable()
            print 'Name: %s , Is Job Enabled ? : %s' % (job_name,job_instance.is_enabled())

def create_jobtest():
    server = get_server_instance()
    job_name="myjob"
    job_xml="config.xml"
    create = server.create_job(job_name,job_xml)
    print create

def copy_jobtest():
    server = get_server_instance()
    job_name = "myjob"
    job_xml = "config.xml"
    copy = server.copy_job(job_name,job_xml)
    return copy


if __name__ == '__main__':
    print get_server_instance().version
    get_job_details()
    disable_job()
    for job_url,job_name in  get_server_instance().get_jobs_info():
        print job_url,job_name

    print copy_jobtest()
