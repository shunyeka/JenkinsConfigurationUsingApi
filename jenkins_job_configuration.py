import simplejson as json

import jenkins


class JenkinsApi:
    def __init__(self):
        self.j = jenkins.Jenkins('https://jenkins.bryceindustries.net', 'tejas', 'Trend@ut0heal')
        self.java_config_file = (open("java_config.xml", "rb")).read().decode('utf8')
        self.dotNet_config_file = (open("dotnet_config.xml", "rb")).read().decode('utf8')

    def create_job(self, job_name, project_type):
        try:
            jenkins_jobs = self.get_all_jobs()
            for job in jenkins_jobs:
                if job_name not in job["name"]:
                    if project_type == "java":
                        self.j.create_job(job_name, self.java_config_file)
                    else:
                        self.j.create_job(job_name, self.dotNet_config_file)
                    return json.dumps({"name": job_name,
                                       "project_type": project_type,
                                       "message": job_name + " Successfully created"})
                else:
                    return {"message": job_name + " already exists"}
        except BaseException as e:
            error = e
            return {"message": error}

    def build_job(self, job_name):
        try:
            jenkins_jobs = self.get_all_jobs()
            for job in jenkins_jobs:
                if job_name in job["name"]:
                    self.j.build_job(job_name)
                    return {"name": job_name,
                            "message": " successfully job built"}
        except BaseException as e:
            error = e
            return {"message": error}

    # def enable_job(self, job_name):
    #     try:
    #         jenkins_jobs = self.get_all_jobs()
    #         if job_name in jenkins_jobs:
    #             self.j.enable_job(job_name)
    #             return {"message": " successfully job enabled"}
    #         else:
    #             return {"message": job_name + " is not exists so you can't enable it!!!"}
    #     except BaseException as e:
    #         error = e
    #         return {"message": error}
    #
    # def disable_job(self, job_name):
    #     try:
    #         jenkins_jobs = self.get_all_jobs()
    #         if job_name in jenkins_jobs:
    #             self.j.disable_job(job_name)
    #             return {"message": " successfully job disabled"}
    #         else:
    #             return {"message": job_name + " is not exists so you can't disable it!!!"}
    #     except BaseException as e:
    #         error = e
    #         return {"message": error}

    def delete_job(self, job_name):
        try:
            jenkins_jobs = self.get_all_jobs()
            for job in jenkins_jobs:
                if job_name in job["name"]:
                    self.j.delete_job(job_name)
                    return {"message": job_name + " successfully job deleted"}
        except BaseException as e:
            error = e
            return {"message": error}

    def get_all_jobs(self):
        jobs = self.j.get_all_jobs()
        jenkins_jobs = []
        for job in jobs:
            if job.get("color"):
                jenkins_jobs.append({"name": job["name"], "color": job["color"], "url": job["url"]})
            else:
                jenkins_jobs.append({"name": job["name"], "color": None, "url": job["url"]})
        return jenkins_jobs

# api_helper = JenkinsApi()
# print(api_helper.create_job())
