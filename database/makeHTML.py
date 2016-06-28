#!/usr/bin/env python

################################
#
# check.py
#
#  Script to check status of requests and save in database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse
import sys
import math
sys.path.append('../')
import mcmscripts_config


def display_number(n):
    if n == 0:
        return "0"
    else:
        prefix = ['', 'k', 'M']
        n = float(n)
        prefix_id = max(0, min(2, int(math.floor(math.log10(abs(n))/3.0))))
        return "{0:.5g}{1}".format(n/10**(3*prefix_id), prefix[prefix_id]);


def writeRequests(page, fout, c, super_campaign, request_set, instance):
    campaign_classes = ["lhe", "gs", "dr", "miniaod"]

    c.execute("""\
SELECT Campaigns.Name,
       New,
       Validating,
       Validated,
       Defined,
       Approved,
       Submitted,
       Done
FROM Requests
INNER JOIN Instance_Requests USING(RequestsID)
INNER JOIN Campaigns USING(CampaignID)
WHERE InstanceID = {0}
ORDER BY Level""".format(instance[0]))
    requests = c.fetchall()
    class_offset = 0
    if len(requests) < 4:
        fout.write("    <td class=\"lhe\">&nbsp;</td>\n")
        class_offset = 1
    for i in range(len(requests)):
        if page == 0:
            #ccccff,cc99ff,727272,98fb98,ff6666,ffc570,66aa66,ff4500
            # fout.write("    <td class=\"{0}\"><a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={1}&member_of_campaign={2}&page=-1\" class=\"status\">{3}<br>{4}<br>{5}<br>{6}<br>{7}<br>{8}<br>{9}/{10}</a><br><img src=\"http://chart.apis.google.com/chart?chbh=a,0&amp;chs=100x30&amp;cht=bhs:nda&amp;chco=ccccff,cc99ff,6ba6e8,52fbc4,ffeba4,ffc570,66aa66,ff4500&amp;chds=0,{10},0,{10},0,{10},0,{10},0,{10},0,{10},0,{10},0,{10}&amp;chd=t:{3}|{4}|{5}|{6}|{7}|{8}|{9}|0\" alt=\"{3} {4} {5} {6} {7} {8} {9} / {10}\" title=\"{3} {4} {5} {6} {7} {8} {9} / {10}\">".format(
            #         campaign_classes[i + class_offset], request_set[2],
            #         requests[i][0], requests[i][1], requests[i][2],
            #         requests[i][3], requests[i][4], requests[i][5],
            #         requests[i][6], requests[i][7], request_set[4]))
            fout.write("    <td class=\"{0}\">\n".format(campaign_classes[i + class_offset]))
            # fout.write("        <a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={0}&member_of_campaign={1}&page=-1\" class=\"status\">{2}<br>{3}<br>{4}<br>{5}<br>{6}<br>{7}<br>{8}/{9}</a>\n".format(
            #         request_set[2], requests[i][0], requests[i][1],
            #         requests[i][2], requests[i][3], requests[i][4],
            #         requests[i][5], requests[i][6], requests[i][7],
            #         request_set[4]))
            fout.write("        <a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={0}&member_of_campaign={1}&page=-1\" class=\"status\" target=\"_blank\"><img src=\"http://chart.apis.google.com/chart?chbh=a,0&amp;chs=100x30&amp;cht=bhs:nda&amp;chco=ccccff,cc99ff,6ba6e8,52fbc4,ffeba4,ffc570,66aa66,ff4500&amp;chds=0,{9},0,{9},0,{9},0,{9},0,{9},0,{9},0,{9},0,{9}&amp;chd=t:{2}|{3}|{4}|{5}|{6}|{7}|{8}|0\" alt=\"{2} {3} {4} {5} {6} {7} {8} / {9}\" title=\"{2} {3} {4} {5} {6} {7} {8} / {9}\"></a>\n".format(
                    request_set[2], requests[i][0], requests[i][1],
                    requests[i][2], requests[i][3], requests[i][4],
                    requests[i][5], requests[i][6], requests[i][7],
                    request_set[4]))
            #<img src=\"http://chart.apis.google.com/chart?chbh=a,0&amp;chs=130x26&amp;cht=bhs:nda&amp;chco=ffc570,ccccff,727272,cc99ff,66aa66,ff6666,98FB98,FF4500&amp;chds=0,{10},0,{10},0,{10},0,{10},0,{10},0,{10},0,{10},0,{10}&amp;chd=t:{3}|{4}|{5}|{6}|{7}|{8}|{9}|0\">
            # fout.write("    <td class=\"{0}\"><a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={1}&member_of_campaign={2}&page=-1\" class=\"status\">{3}<br>{4}<br>{5}<br>{6}<br>{7}<br>{8}<br>{9}/{10}</a><br>".format(
#                     campaign_classes[i + class_offset], request_set[2],
#                     requests[i][0], requests[i][1], requests[i][2],
#                     requests[i][3], requests[i][4], requests[i][5],
#                     requests[i][6], requests[i][7], request_set[4]))
#             chart_name = "{0}{1}".format(request_set[2], requests[i][0]).replace("-", "")

#             fout.write("""\
#          <script type="text/javascript">
#              google.charts.setOnLoadCallback(draw{0});
#              function draw{0}() {{
#              var data = google.visualization.arrayToDataTable([
#                  ['Campaign', 'New', 'Validating', 'Validated', 'Defined', 'Approved', 'Submitted', 'Done', 'Unkown'],
#                  ['', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}],
#              ]);
#              var options = {{
#                  isStacked: 'percent',
#                  height: 100,
#                  width: 150,
#                  legend: {{
#                      position: 'none'
#                  }},
#                  hAxis: {{
#                      gridlines: {{count: 0}}
#                  }},
#                  vAxis:{{
#                      baselineColor: '#fff',
#                      gridlineColor: '#fff',
#                      textPosition: 'none'
#                  }},
#                  colors:['#ccccff', '#cc99ff', '#727272', '#98FB98', '#ff6666', '#ffc570', '#66aa66', '#FF4500']
#              }};
#              var chart = new google.visualization.BarChart(document.getElementById('chart_span_{0}'));
#              chart.draw(data, options);
#          }}
#     </script>
#     <a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={9}&member_of_campaign={10}&page=-1\" class=\"status\" target="_blank"><span id="chart_span_{0}" style="width: 150px; height: 100px; background-color:#00ff00;"></span></a>
# """.format(chart_name, requests[i][1], requests[i][2], requests[i][3],
#            requests[i][4], requests[i][5], requests[i][6], requests[i][7],
#            abs(requests[i][1] + requests[i][2] + requests[i][3] + requests[i][4] + requests[i][5] + requests[i][6] + requests[i][7] - request_set[4]),
#            request_set[2], requests[i][0]))
            fout.write("    </td>\n")
        elif page == 1:
            # fout.write("    <td class=\"{0}\"><a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={1}&member_of_campaign={2}&page=-1\" class=\"status\">{3}/{4}</a></td>\n".format(
            #         campaign_classes[i + class_offset], request_set[2],
            #         requests[i][0], requests[i][7], request_set[4]))
            fout.write("    <td class=\"{0}\">\n".format(campaign_classes[i + class_offset]))
            fout.write("        <a href=\"https://cms-pdmv.cern.ch/mcm/requests?tags={0}&member_of_campaign={1}&page=-1&shown=274877909023\" class=\"status\" target=\"_blank\"><img src=\"http://chart.apis.google.com/chart?chbh=a,0&amp;chs=100x30&amp;cht=bhs:nda&amp;chco=ccccff,cc99ff,6ba6e8,52fbc4,ffeba4,ffc570,66aa66,ff4500&amp;chds=0,{6},0,{6},0,{6},0,{6},0,{6},0,{6},0,{6},0,{6}&amp;chd=t:{2}|0|0|0|{3}|{4}|{5}|0\" alt=\"{2} {3} {4} {5} / {6}\" title=\"{2} preparation, {3} approved, {4} running, {5} done / {6}\"></a>\n".format(
                    request_set[2], requests[i][0],
                    requests[i][1] + requests[i][2] + requests[i][3] + requests[i][4],
                    requests[i][5], requests[i][6], requests[i][7],
                    request_set[4]))
            fout.write("    </td>\n")
    return


def writeInstances(page, fout, c, super_campaign, request_set):
    c.execute("""\
SELECT InstanceID,
       DisplayName,
       Requesters.Name,
       Requesters.Email,
       CampaignChains.Name
FROM Instances
INNER JOIN Contacts USING(ContactID)
INNER JOIN Requesters USING(RequesterID)
INNER JOIN CampaignChains USING(CampaignChainID)
WHERE SetID = {0}
  AND SuperCampaignID = {1};""".format(request_set[0], super_campaign[0]))
    instances = c.fetchall()
    for instance in instances:
        fout.write("<tr>\n")
        if page == 0:
            fout.write("""\
    <td class="process">{0}</td>
    <td class="tag">{1}</td>
    <td class="requester"><a href="mailto:{2}">{3}</a></td>
    <td class="contact">{4}</td>
    <td class="events">{5}</td>
""".format(request_set[1], request_set[2], instance[3], instance[2],
           instance[1], display_number(request_set[3])))
        elif page == 1:
            fout.write("""\
    <td class="process">{0}</td>
    <td class="requester"><a href="mailto:{1}">{2}</a></td>
""".format(request_set[1], instance[3], instance[2]))
        writeRequests(page, fout, c, super_campaign, request_set, instance)
        if page == 0:
            if request_set[6] == "":
                fout.write("    <td class=\"spreadsheet empty\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"spreadsheet\"><a href=\"{0}\" target=\"_blank\"><img src=\"table.gif\" alt=\"X\" class=\"spreadsheet_icon\"></a></td>\n".format(
                        request_set[6]))
            if request_set[5] == "":
                fout.write("    <td class=\"notes\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"notes\">{0}</td>\n".format(request_set[5]))
        elif page == 1:
            if request_set[6] == "":
                fout.write("    <td class=\"spreadsheet empty\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"spreadsheet\"><a href=\"{0}\" target=\"_blank\"><img src=\"table.gif\" alt=\"X\" class=\"spreadsheet_icon\"></a></td>\n".format(
                        request_set[6]))
            if request_set[5] == "":
                fout.write("    <td class=\"notes\">&nbsp;</td>\n")
            else:
                fout.write("    <td class=\"notes\">{0}</td>\n".format(request_set[5]))
        fout.write("</tr>\n")
    return


def writeRequestSets(page, fout, c, super_campaign):
    c.execute("""\
SELECT DISTINCT SetID,
                Process,
                Tag,
                Events,
                RequestMultiplicity,
                Notes,
                Spreadsheet
FROM RequestSets
INNER JOIN Instances USING(SetID)
INNER JOIN CampaignChains USING(CampaignChainID)
WHERE SuperCampaignID = {0};""".format(super_campaign[0]))
    request_sets = c.fetchall()
    for request_set in request_sets:
        writeInstances(page, fout, c, super_campaign, request_set)
    return


def writeSuperCampaigns(page, fout, c):
    c.execute("""\
SELECT SuperCampaignID,
       Name
FROM SuperCampaigns
ORDER BY Active;""")
    super_campaigns = c.fetchall()
    for super_campaign in super_campaigns:
        fout.write("""\
<h2 class="campaign">{0}</h2>
<table>
<tr class="table_header">
""".format(super_campaign[1]))
        if page == 0:
            fout.write("""\
    <th class="process">Process</th>
    <th class="tag">Tag</th>
    <th class="requester">Requester</th>
    <th class="contact">Contact</th>
    <th class="events">Events</th>
    <th class="lhe">LHE</th>
    <th class="gs">GS</th>
    <th class="dr">DR</th>
    <th class="miniaod">MiniAOD</th>
    <th class="spreadsheet">Spreadsheet</th>
    <th class="notes">Notes</th>
""")
        elif page == 1:
            fout.write("""\
    <th class="process">Process</th>
    <th class="requester">Requester</th>
    <th class="lhe">LHE</th>
    <th class="gs">GS</th>
    <th class="dr">DR</th>
    <th class="miniaod">MiniAOD</th>
    <th class="spreadsheet">Spreadsheet</th>
    <th class="notes">Notes</th>
""")
        fout.write("</tr>\n")

        writeRequestSets(page, fout, c, super_campaign)

        fout.write("</table>\n")

    return


def makeAnalyzerHTML():
    fout = open('{0}analyzer.html'.format(mcmscripts_config.html_location), 'w')
    campaign_classes = ["lhe", "gs", "dr", "miniaod", "miniaodv2"]

    fout.write("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Exotica MC Status for Analyzers</title>

    <link rel="stylesheet" type="text/css" href="global.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

<table><tr>
    <td class="gs" style="background-color:#ccccff">Preparing requests</td>
    <td class="gs" style="background-color:#ffeba4">Approved to run</td>
    <td class="gs" style="background-color:#ffc570">Running</td>
    <td class="gs" style="background-color:#66aa66">Done</td>
</tr></table>

""")

    conn = sqlite3.connect(mcmscripts_config.database_location)

    c = conn.cursor()
    writeSuperCampaigns(1, fout, c)

    c.execute("""\
SELECT Value
FROM Settings
WHERE SettingID = 1""")
    check_time = c.fetchone()
    fout.write("""\
</table>
<p class="update-time">Updated {0}</p>
</div>

</body>
</html>
""".format(check_time[0]))
    fout.close()

    print "Generated analyzer page"

    return


def makeContactHTML():
    fout = open('{0}contact.html'.format(mcmscripts_config.html_location), 'w')
    campaign_classes = ["lhe", "gs", "dr", "miniaod", "miniaodv2"]

    fout.write("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Exotica MC Status for Contacts</title>

    <link rel="stylesheet" type="text/css" href="global.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<body>

<div class="wrapper">
<h1>Exotica MC</h1>

<table><tr>
    <td class="gs" style="background-color:#ccccff">New</td>
    <td class="gs" style="background-color:#cc99ff">Validating</td>
    <td class="gs" style="background-color:#6ba6e8">Validated</td>
    <td class="gs" style="background-color:#52fbc4">Defined</td>
    <td class="gs" style="background-color:#ffeba4">Approved</td>
    <td class="gs" style="background-color:#ffc570">Submitted</td>
    <td class="gs" style="background-color:#66aa66">Done</td>
</tr></table>

""")

    # <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    # <script type="text/javascript">
    #     google.charts.load('current', {packages: ['corechart', 'bar']});
    # </script>

    conn = sqlite3.connect(mcmscripts_config.database_location)

    c = conn.cursor()
    writeSuperCampaigns(0, fout, c)

    c.execute("""\
SELECT Value
FROM Settings
WHERE SettingID = 1""")
    check_time = c.fetchone()
    fout.write("""\
</table>
<p class="update-time">Updated {0}</p>
</div>

</body>
</html>
""".format(check_time[0]))
    fout.close()

    print "Generated contact page"

    return


def main():
    makeAnalyzerHTML()
    makeContactHTML()

    return


if __name__ == '__main__':
    main()
