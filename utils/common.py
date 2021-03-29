import json
import os
import yaml
from datetime import datetime

from rest_framework.response import Response

from httprunner.task import HttpRunner
from debugtalks.models import DebugTalks
from configures.models import Configures
from testcases.models import Testcases
from reports.models import Reports


def generate_testcase_file(instance, env, testcase_dir_path):
    testcase_list = []
    # 构造公共的配置信息（如果在创建用例时，未选择关联的配置，那么就使用公共的config）
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)

    # 取出用例所属接口信息，并获取接口所属的项目名称
    interface_name = instance.interface.name
    project_name = instance.interface.project.name

    # 获取include，并解析所属的配置信息和前置用例信息
    include = json.loads(instance.include, encoding='utf-8')

    # 获取用例的request信息
    request = json.loads(instance.request, encoding='utf-8')

    # 拼接以项目名命名的路径
    testcase_dir_path = os.path.join(testcase_dir_path, project_name)

    # 如果要创建嵌套的多级目录时，往往使用os.makedirs
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        # 通过项目名称获取当前项目下的debugtalk.py文件的内容，并写入项目目录下
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj.debugtalk else ''
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as file:
            file.write(debugtalk)

    # 获取以接口命名的路径，如果不存在则创建
    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # 获取config
    config_id = include.get('config')
    if config_id is not None:
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            # 添加base_url
            config_request['config']['request']['base_url'] = env.base_url if env.base_url else ''
            # 替换全局默认的config
            testcase_list[0] = config_request

    # 获取前置用例
    prefix_testcase_list = include.get('testcases')
    if prefix_testcase_list:
        for testcase_id in prefix_testcase_list:
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue
            # 将前置用例的request数据添加到testcase_list中
            testcase_list.append(testcase_request)

    # 将当前用例的request，添加到testcase_list中
    testcase_list.append(request)

    testcase_dir_path = os.path.join(testcase_dir_path, instance.name + '.yaml')
    with open(testcase_dir_path, 'w', encoding='utf-8') as file:
        # 使用yaml.dump可以将python中的基本类型（字典、嵌套字典的列表）转化为yaml文件
        # 第一个参数为基本类型数据，第二个参数为文件对象
        yaml.dump(testcase_list, file, allow_unicode=True)


def generate_report(runner, instance):
    # 创建报告名称：用例名
    report_name = instance.name

    # 对时间戳进行转化
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    # 将summary中的所有字节类型转化为字符串类型
    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)
    # 生成报告
    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def run_testcase(instance, testcase_dir_path):
    # 1、创建HttpRunner对象
    runner = HttpRunner()
    try:
        # 2、运行用例
        runner.run(testcase_dir_path)
    except Exception as e:
        res = {'msg': '用例执行失败', 'code': '0'}
        return Response(res, status=400)

    # 3、创建报告
    report_id = generate_report(runner, instance)
    return Response({'id': report_id}, status=201)
