#coding:utf-8

from jenkinsapi.jenkins import Jenkins
import os

class CJenkinsAPI():
    '''
    均采用同步设置超时机制
    创建项目：输入：configid planid
    创建任务：输入：configid planid   返回:返回码 msg buildid  额外动作：不写SQL
    查询任务：输入：configid planid taskid  返回:返回码 msg buildid  额外动作：结束更新SQL（包括成功或失败），未结束则不处理
    终止任务：输入：configid planid taskid  返回:返回码 msg buildid  额外动作：终止成功写SQL

    '''
    __doc__ = '''Usage: \t\tCJenkinsAPI.createProject\t\tCJenkinsAPI.triggerBuild\t\t'''

    _strConfigTemplatePath = ""
    _strConfigDataPath = ""

    def __init__(self):
        import pycurl
        pass

    def __del__(self):
        pass

    @staticmethod
    def createProject(nPlanId, strConfigId):
        '''
        Return:返回码/返回信息
        先根据配置文件生成项目
        '''
        # 用于测试
        nPlanId = 14
        strConfigId = "D1057406"

        # 返回
        nRet, strMsg, nBuild = 0, "", 0

        # 配置文件模版
        strConfigTemplate = CJenkinsAPI._strConfigTemplatePath + "/config.template.xml"

        # 用planID和配置ID作为项目名
        strProjectName = "P%d-%s" % (nPlanId, strConfigId)

        # 访问数据库拿到构建节点IP和SVN
        strBuildNodeIP = ""
        strProjectSVN = ""

        oProxy = CSqlProxy("10.129.145.112", "ci_test", "ci_test", "ci_plat")
        # SVN从t_build_plan中取
        lSelectRet = CSqlProxy.selectFromTable(oProxy.m_oCon, "t_build_plan", ["f_svn"],
                                               " where f_plan_id='%d' " % nPlanId)
        strProjectSVN = lSelectRet[0]["f_svn"]
        # 配置信息从t_ci_config中取
        lSelectRet = CSqlProxy.selectFromTable(oProxy.m_oCon, "t_ci_config", ["f_node_ip", "f_run_param"],
                                               " where f_config_id='%s' " % strConfigId)
        strBuildNodeIP = lSelectRet[0]["f_node_ip"]
        strRunParam = lSelectRet[0]["f_run_param"]
        oProxy.close()

        strNodeFlag = {True: "", False: "slave_"}["10.129.145.112" in strBuildNodeIP]
        dReplaceInfo = {
            "PROJ_DESC": "This is generate by Ci-plat, with plan_id[%d] and config_id[%s]" % (nPlanId, strConfigId), \
            "SVN_URL": strProjectSVN.replace("http://tc-svn.tencent.com", "svn://172.27.198.49:8081"), \
            "BUILD_NODE_IP": strNodeFlag + strBuildNodeIP, \
            "BUILD_SCRIPT": '''sh build.sh %s ''' % strRunParam, \
            "JUNIT_TEST_PATH": "target/surefire-reports/*.xml", \
            "COVERAGE_PATH": "target/site/cobertura/", \
            }

        # 利用模版生成配置文件
        oConf = CCiConfig(strConfigTemplate, dReplaceInfo)
        strCurConfigXml = CJenkinsAPI._strConfigDataPath + "/" + strProjectName + ".config.xml"
        oConf.dump2file(strCurConfigXml)

        strCommand = 'curl -X POST http://10.129.145.112:8081/jenkins/createItem?name=%s --user peterguo:peterguo --data-binary "@%s" -H "Content-Type: text/xml"' % (
        strProjectName, strCurConfigXml)
        nRet = os.system(strCommand)
        strMsg = {True: "SucceedCreate,Url:", False: "FailedCreate,Url:"}[nRet == 0]
        print "%d|%s|%d" % (
        nRet, tran2UTF8(strMsg) + "[http://10.129.145.112:8081/jenkins/job/%s]" % strProjectName, nBuild)

    @staticmethod
    def triggerBuild(nPlanId, strConfigId):
        '''
        Return:
        触发前先更新配置文件，使用远程脚本
        触发前获取要出发的编号
        '''
        # 返回
        nRet, strMsg, nBuild = 0, "", 0

        # 配置文件模版
        strConfigTemplate = CJenkinsAPI._strConfigTemplatePath + "/config.template.xml"

        # 用planID和配置ID作为项目名
        strProjectName = "P%d-%s" % (nPlanId, strConfigId)

        # 访问数据库拿到构建节点IP和SVN
        strBuildNodeIP = ""
        strProjectSVN = ""

        oProxy = CSqlProxy("10.129.145.112", "ci_test", "ci_test", "ci_plat")
        # SVN从t_build_plan中取
        lSelectRet = CSqlProxy.selectFromTable(oProxy.m_oCon, "t_build_plan", ["f_svn"],
                                               " where f_plan_id='%d' " % nPlanId)
        strProjectSVN = lSelectRet[0]["f_svn"]
        # 配置信息从t_ci_config中取
        lSelectRet = CSqlProxy.selectFromTable(oProxy.m_oCon, "t_ci_config", ["f_node_ip", "f_run_param"],
                                               " where f_config_id='%s' " % strConfigId)
        strBuildNodeIP = lSelectRet[0]["f_node_ip"]
        strRunParam = lSelectRet[0]["f_run_param"]
        oProxy.close()

        strNodeFlag = {True: "", False: "slave_"}["10.129.145.112" in strBuildNodeIP]
        dReplaceInfo = {
            "PROJ_DESC": "This is generate by Ci-plat, with plan_id[%d] and config_id[%s]" % (nPlanId, strConfigId), \
            "SVN_URL": strProjectSVN.replace("http://tc-svn.tencent.com", "svn://172.27.198.49:8081"), \
            "BUILD_NODE_IP": strNodeFlag + strBuildNodeIP, \
            "BUILD_SCRIPT": '''sh build.sh %s ''' % strRunParam, \
            "JUNIT_TEST_PATH": "target/surefire-reports/*.xml", \
            "COVERAGE_PATH": "target/site/cobertura/", \
            }

        # 利用模版生成配置文件
        oConf = CCiConfig(strConfigTemplate, dReplaceInfo)
        strCurConfigXml = CJenkinsAPI._strConfigDataPath + "/" + strProjectName + ".config.xml"
        oConf.dump2file(strCurConfigXml)

        # 更新配置文件
        strCommand = 'curl -X POST http://10.129.145.112:8081/jenkins/job/%s/config.xml --user peterguo:peterguo --data-binary "@%s" -H "Content-Type: text/xml"' % (
        strProjectName, strCurConfigXml)
        nRet = os.system(strCommand)
        strMsg += {True: "更新配置成功", False: "更新配置失败"}[nRet == 0]

        # 获取下一次构建编号
        nBuild = Jenkins("http://10.129.145.112:8081/jenkins", "peterguo", "peterguo")[
            strProjectName.encode("utf8")].get_next_build_number()

        # 触发构建
        strCommand = 'curl -X POST http://10.129.145.112:8081/jenkins/job/%s/build --user peterguo:peterguo ' % (
        strProjectName)
        nRet = os.system(strCommand)
        strMsg = {True: "SucceedTrigger,Url:", False: "FailedTrigger,Url:"}[nRet == 0]
        print "%d|%s|%d" % (
        nRet, tran2UTF8(strMsg) + "[http://10.129.145.112:8081/jenkins/job/%s/%d]" % (strProjectName, nBuild), nBuild)

    @staticmethod
    def infoBuild(nPlanId, strConfigId, nTaskId):
        '''
        Return:
        '''
        strProjectName = "P%d-%s" % (nPlanId, strConfigId)
        oProxy = CSqlProxy("10.129.145.112", "ci_test", "ci_test", "ci_plat")
        strWhere = " where f_task_id='%d' " % int(nTaskId)
        lSelectRet = CSqlProxy.selectFromTable(oProxy.m_oCon, "t_build_task", ["f_build_id"], strWhere)
        oProxy.close()
        nBuildId = int(lSelectRet[0]["f_build_id"])

        oCurBuild = Jenkins("http://10.129.145.112:8081/jenkins", "peterguo", "peterguo")[
            strProjectName.encode("utf8")].get_build(nBuildId)
        bRunning = oCurBuild.is_running()
        if bRunning == True:
            print "1|Running|%d" % nBuildId
            return

        # 最重要更新的数据
        dResult2Sql = {}

        # 取测试用例结果的个数信息
        if oCurBuild.has_resultset():
            dResult = oCurBuild.get_actions()
        else:
            dResult = {"failCount": 0, "totalCount": 0, "skipCount": 0}

        oDeltaDur = oCurBuild.get_duration()
        oBuildBegin = utc2LocalDatetime(oCurBuild.get_timestamp())
        oBuildEnd = oBuildBegin + oDeltaDur
        dResult2Sql["f_case_fail"] = dResult['failCount']
        dResult2Sql["f_case_total"] = dResult['totalCount']
        dResult2Sql["f_case_skip"] = dResult['skipCount']
        dResult2Sql["f_build_duration"] = "%.3f" % (oDeltaDur.days * 24 * 60 + oDeltaDur.seconds / 60.0)
        dResult2Sql["f_build_url"] = oCurBuild.baseurl
        dResult2Sql["f_build_result"] = {True: 0, False: 1}[oCurBuild.is_good()]
        dResult2Sql["f_task_status"] = TASK_DONE
        dResult2Sql["f_build_time"] = oBuildBegin.strftime("%Y-%m-%d %H:%M:%S")
        dResult2Sql["f_build_end"] = oBuildEnd.strftime("%Y-%m-%d %H:%M:%S")
        dResult2Sql["f_msg_info"] = tran2GBK("任务完成，收集数据完成")

        # 任务已经完成，需要入库相关数据，更新相关状态
        oProxy = CSqlProxy("10.129.145.112", "ci_test", "ci_test", "ci_plat")
        strWhere = " where f_task_id='%d' " % int(nTaskId)
        CSqlProxy.updateValueToDBTable(oProxy.m_oCon, "t_build_task", dResult2Sql.keys(), dResult2Sql.values(),
                                       strWhere)
        oProxy.close()
        # for item in dResult2Sql.items():
        #    print item[0], str(item[1])
        print "%d|%s|%d" % (0, "SucceedUpdated", nBuildId)

    @staticmethod
    def stopBuild(nPlanId, strConfigId, nTaskId):
        '''
        Return:
        '''
        strProjectName = "P%d-%s" % (nPlanId, strConfigId)
        oProxy = CSqlProxy("10.129.145.112", "ci_test", "ci_test", "ci_plat")
        strWhere = " where f_task_id='%d' " % int(nTaskId)
        lSelectRet = CSqlProxy.selectFromTable(oProxy.m_oCon, "t_build_task", ["f_build_id"], strWhere)
        oProxy.close()
        nBuildId = int(lSelectRet[0]["f_build_id"])

        oCurBuild = Jenkins("http://10.129.145.112:8081/jenkins", "peterguo", "peterguo")[
            strProjectName.encode("utf8")].get_build(nBuildId)
        bRunning = oCurBuild.is_running()
        if bRunning == False:
            print "2|AlreadyStopped|%d" % nBuildId
            return

        # 触发停止命令
        oCurBuild.stop()

        # 等停止
        oCurBuild.block_until_complete()

        # 最重要更新的数据
        dResult2Sql = {}

        # 取测试用例结果的个数信息
        if oCurBuild.has_resultset():
            dResult = oCurBuild.get_actions()
        else:
            dResult = {"failCount": 0, "totalCount": 0, "skipCount": 0}

        oDeltaDur = oCurBuild.get_duration()
        oBuildBegin = utc2LocalDatetime(oCurBuild.get_timestamp())
        oBuildEnd = oBuildBegin + oDeltaDur
        dResult2Sql["f_case_fail"] = dResult['failCount']
        dResult2Sql["f_case_total"] = dResult['totalCount']
        dResult2Sql["f_case_skip"] = dResult['skipCount']
        dResult2Sql["f_build_duration"] = "%.3f" % (oDeltaDur.days * 24 * 60 + oDeltaDur.seconds / 60.0)
        dResult2Sql["f_build_url"] = oCurBuild.baseurl
        dResult2Sql["f_build_result"] = {True: 0, False: 1}[oCurBuild.is_good()]
        dResult2Sql["f_task_status"] = TASK_ABORTED
        dResult2Sql["f_build_time"] = oBuildBegin.strftime("%Y-%m-%d %H:%M:%S")
        dResult2Sql["f_build_end"] = oBuildEnd.strftime("%Y-%m-%d %H:%M:%S")
        dResult2Sql["f_msg_info"] = tran2GBK("TaskStopped")

        # 任务已经完成，需要入库相关数据，更新相关状态
        oProxy = CSqlProxy("10.129.145.112", "ci_test", "ci_test", "ci_plat")
        strWhere = " where f_task_id='%d' " % int(nTaskId)
        CSqlProxy.updateValueToDBTable(oProxy.m_oCon, "t_build_task", dResult2Sql.keys(), dResult2Sql.values(),
                                       strWhere)
        oProxy.close()
        # for item in dResult2Sql.items():
        #    print item[0], str(item[1])

        print "%d|%s|%d" % (1, tran2UTF8("SucceedStopped"), nBuildId)

    @staticmethod
    def deleteProject(nPlanId, strConfigId):
        '''
        Return:返回码/返回信息 curl -X POST http://10.129.145.112:8081/jenkins/job/JavaStd/doDelete --user peterguo:peterguo
        '''
        strProjectName = "P%d-%s" % (nPlanId, strConfigId)
        strCommand = 'curl -X POST http://10.129.145.112:8081/jenkins/job/%s/doDelete --user peterguo:peterguo' % (
        strProjectName)
        CColorPrint.colorPrintStr("CMD:[%s]" % strCommand, "green")

        nRet = os.system(strCommand)
        strMsg = {True: "SucceedDeleted", False: "FailedDeleted"}[nRet == 0]
        print nRet, tran2UTF8(strMsg), 0