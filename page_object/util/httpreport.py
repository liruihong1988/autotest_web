import os

from bottle import template
from page_object.dbconnect.DbSqlUtil import DBSqlUtil

class htmlreport(object):

    def report(self,start_time,end_time,testcase_number,passed_amount,failed_amount,version):

        uitl = DBSqlUtil('mysql')

        starttime = start_time
        endtime = end_time

        htmltestcasecount = str(testcase_number)
        htmlstarttime = str(starttime)
        htmlendtime = str(endtime)
        htmlpassednum = str(passed_amount)
        htmlfailednum = str(failed_amount)

        htmlpassingrate = str(round(passed_amount / testcase_number * 100)) + '%'
        appversion = version

        test_result_list = list(
            uitl.mysql_select_list("SELECT testTitle,result_name,result_color FROM pytest_ui_result WHERE version = %s",
                                   (version)))

        summary_tupe = (
            htmltestcasecount, htmlstarttime, htmlendtime, htmlpassednum, htmlfailednum, htmlpassingrate, appversion)

        summary = []
        summary.append(summary_tupe)

        articles = test_result_list

        template_demo = """
               <!DOCTYPE html>
               <html lang="en">
               <head>
               <meta charset="UTF-8">
               <title>测试结果</title>

               </head>
               <body>
               <table id='result_table' class=MsoTable15Grid6ColorfulAccent4 border=1 cellspacing=0 cellpadding=0 width=814 style='font-family:'微软雅黑',Helvetica,Arial,sans-serif;font-size:14px'>
                            % for htmltestcasecount,htmlstarttime,htmlendtime,htmlpassednum,htmlfailednum,htmlpassingrate,appversion in item:
                            <tr id="tr1" height=30>
                                <td width=132 valign=middle style='width:199.0pt;padding:0cm 5.4pt 0cm 5.4pt;'>
                                    <p class=MsoNormal><span id="span1">用例数：<span lang=EN-US>{{htmltestcasecount.strip()}}</span></span></p>
                                </td>
                                <td width=537 valign=middle style='width:477.5pt;padding:0cm 5.4pt 0cm 5.4pt;'>
                                    <p class=MsoNormal><span id="span1">开始时间：<span lang=EN-US>{{htmlstarttime}}</span></span></p>
                                </td>
                                <td width=545 valign=middle style='width:527.95pt;padding:0cm 5.4pt 0cm 5.4pt;'>
                                    <p class=MsoNormal><span id="span1">结束时间：<span lang=EN-US>{{htmlendtime}}</span></span></p>
                                 </td>
                            </tr>
                            <tr id="tr2" height=30>
                                <td width=132 valign=middle style='width:208.0pt;padding:0cm 5.4pt 0cm 5.4pt'>
                                    <p class=MsoNormal><span id="span1">成功用例数：<span lang=EN-US>{{htmlpassednum}}</span></span></p>
                                </td>
                                <td width=537 valign=middle style='width:177.5pt;padding:0cm 5.4pt 0cm 5.4pt'>
                                    <p class=MsoNormal><span id="span1">失败用例数：<span lang=EN-US>{{htmlfailednum}}</span></span></p>
                                </td>
                                <td width=545 valign=middle style='width:183.95pt;padding:0cm 5.4pt 0cm 5.4pt'>
                                    <p class=MsoNormal><span id="span1">通过率：<span lang=EN-US>{{htmlpassingrate}}</span></span></p>
                                </td>
                            </tr>
                            <tr id="tr1" height=30>
                                <td width=132 valign=middle style='width:199.0pt;padding:0cm 5.4pt 0cm 5.4pt;' colspan="3">
                                    <p class=MsoNormal><span id="span1">版本信息：<span lang=EN-US>{{appversion}}</span></span></p>
                                </td>
                            </tr>
                            <tr id='header_row' height=30 class="text-center success" style="font-weight: bold;font-size: 14px;">
                                <td width=545 valign=middle style='width:183.95pt;padding:0cm 5.4pt 0cm 5.4pt' colspan="3">
                                    <p class=MsoNormal><span id="span1">用例执行详情：<span lang=EN-US></span></span></p>
                                </td>
                            </tr>
                            </tr>
                            <tr id='header_row' height=30 class="text-center success" style="font-weight: bold;font-size: 14px;">
                                <td width=545 valign=middle style='width:183.95pt;padding:0cm 5.4pt 0cm 5.4pt' colspan="2">
                                    <p class=MsoNormal><span id="span1">用例名称<span lang=EN-US></span></span></p>
                                </td>
                                <td width=545 valign=middle style='width:183.95pt;padding:0cm 5.4pt 0cm 5.4pt' colspan="1">
                                    <p class=MsoNormal><span id="span1">测试结果<span lang=EN-US></span></span></p>
                                </td>
                            </tr>
                            %end
                            % for title,detail,color in items:
                            <tr class='failClass warning' height=30>
                                <td width=545 valign=middle style='width:183.95pt;padding:0cm 5.4pt 0cm 5.4pt' colspan="2">
                                    <p class=MsoNormal><span id="span1">{{title.strip()}}</span></p>
                                </td>
                                <td width=545 valign=middle style='width:183.95pt;padding:0cm 5.4pt 0cm 5.4pt' colspan="1">
                                    <p class=MsoNormal><span id="span1" {{color}}>{{detail}}</span></p>
                                </td>
                            </tr>
                            %end
                        </table>
               </body>
               </html>
               """

        html = template(template_demo, items=articles, item=summary)

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir = os.path.join(BASE_DIR, "http-report")

        file_name = dir + "\\test.html"

        with open(file_name, 'wb') as f:
            f.write(html.encode('utf-8'))

