#! /usr/bin/python3
import csv
import io
import subprocess
import re
import sys

# the function is called if a command "INSERT" is found
def dispatchjob( line ):
    if (line == 'INSERT_TC_NAME'):
        return '\\def\\TCNAME{' + my_tc_name + '}'
    elif (line == "INSERT_FULL_TC_NAME"):
        return '\\def\\TCFULLNAME{' + my_tc_full_name + '}'
    elif (line == "INSERT_CHAIR_NAME"):
        return '\\def\\CHAIRNAME{' + my_chair_name + '}'
    elif (line == "INSERT_CHAIRELECT_NAME"):
        return '\\def\\CHAIRELECTNAME{' + my_chairelect_name + '}'
    elif (line == "INSERT_VOTING_MEMBERS"):
        return table_voting_members
    elif (line == "INSERT_GEO_DISTRIBUTION"):
        return table_geo
    elif (line == "INSERT_AFF_DISTRIBUTION"):
        return table_aff
    elif (line == "INSERT_GENDER_DISTRIBUTION"):
        return table_gender
    elif (line == "INSERT_CONFERENCE_1"):
        return table_conference_1
    elif (line == "INSERT_CONFERENCE_2"):
        return table_conference_2
    elif (line == "INSERT_JOURNAL"):
        return table_journal
    elif (line == "INSERT_AWARD"):
        return table_award
    elif (line == "INSERT_KEYNOTE"):
        return table_keynote
    elif (line == "INSERT_OTHER_SERVICE"):
        return table_other_service
    elif (line == "INSERT_LEADERSHIP"):
        return table_leadership
    elif (line == "INSERT_PLAN"):
        return table_plan
    else:
        return ''

def proc_geo(geo_1, geo_7, geo_8, geo_9, geo_10):
    # idx: 5 for the first
    idx = 5                     # starting from 6
    my_geo = row[idx]
    
    # clean the region field, only keep numbers.
    row[idx] = re.sub("[^0-9]", "", row[idx])

    # print(geo_1, geo_7, geo_8, geo_9, geo_10)
    if (row[idx] == '1' or row[idx] == '2' or row[idx] == '3' or row[idx] == '4' or row[idx] == '5' or row[idx] == '6'):
        geo_1 = geo_1 + 1
    elif (row[idx] == '7'):
        geo_7 = geo_7 + 1
    elif (row[idx] == '8'):
        geo_8 = geo_8 + 1
    elif (row[idx] == '9'):
        geo_9 = geo_9 + 1
    elif (row[idx] == '10'):
        geo_10 = geo_10 + 1
    else:
        print("Error in Region number", my_geo)
        sys.exit(1)
    return (geo_1, geo_7, geo_8, geo_9, geo_10)

def proc_gender(gender_m, gender_f, gender_u):
    # idx: 6 for the first
    idx = 6                     # starting from 6
    if (row[idx] == 'Male'):
        gender_m = gender_m + 1
    elif (row[idx] == 'Female'):
        gender_f = gender_f + 1
    else:
        gender_u = gender_u + 1
    return (gender_m, gender_f, gender_u)

def proc_aff(aff_a, aff_i, aff_g):
    # idx: 7 for the first
    idx = 7                     # starting from 6
    if (row[idx] == 'Academia'):
        aff_a = aff_a + 1
    elif (row[idx] == 'Industry'):
        aff_i = aff_i + 1
    else:
        print(row[idx])
        aff_g = aff_g + 1
    return (aff_a, aff_i, aff_g)

def proc_conference_table_1( table_conference_1 ):
    # idx: 8, 9, 10 for the first
    idx = 8                     # starting from 6
    for _ in range(5):
        if (row[idx] == ''):
            break
        table_conference_1 = table_conference_1 + row[0] + ' ' + row[1] + '&' + row[idx] + '&' + row[idx+1] + '&' + row[idx+2] + '\\\\' + '\\hline' + '\n'
        idx = idx + 3
    return table_conference_1

def proc_conference_table_2( table_conference_2 ):
    # idx: 23, 24, 25 for the first
    idx = 23                    # starting from 6
    for _ in range(5):
        if (row[idx] == ''):
            break
        table_conference_2 = table_conference_2 + row[0] + ' ' + row[1] + '&' + row[idx] + '&' + row[idx+1] + '&' + row[idx+2] + '\\\\' + '\\hline' + '\n'
        idx = idx + 3
    return table_conference_2

def proc_journal( table_journal ):
    # idx: 38, 39, 40 for the first
    idx = 38                    # starting from 6
    for _ in range(5):
        if (row[idx] == ''):
            break
        table_journal = table_journal + row[0] + ' ' + row[1] + '&' + row[idx] + '&' + row[idx+1] + '&' + row[idx+2] + '\\\\' + '\\hline' + '\n'
        idx = idx + 3
    return table_journal

def proc_award( table_award ):
    # idx: 53, 54 for the first
    idx = 53                    # starting from 6
    for _ in range(5):
        if (row[idx] == ''):
            break
        table_award = table_award + row[0] + ' ' + row[1] + '&' + row[idx] + '&' + row[idx+1] + '\\\\' + '\\hline' + '\n'
        idx = idx + 2
    return table_award

def proc_keynote( table_keynote ):
    # idx: 63, 64, 65, 66 for the first
    idx = 63                    # starting from 6
    for _ in range(5):
        if (row[idx] == ''):
            break
        table_keynote = table_keynote + row[0] + ' ' + row[1] + '&' + row[idx] + '&' + row[idx+1] + '&' + row[idx+2] + '&' + row[idx+3] + '\\\\' + '\\hline' + '\n'
        idx = idx + 4
    return table_keynote

def proc_other_service( table_other_service ):
    # idx: 83, 84, 85 for the first
    idx = 83                    # starting from 6
    for _ in range(5):
        if (row[idx] == ''):
            break
        table_other_service = table_other_service + row[0] + ' ' + row[1] + '&' + row[idx] + '&' + row[idx+1] + '&' + row[idx+2] + '\\\\' + '\\hline' + '\n'
        idx = idx + 3
    return table_other_service

def summary_geo(geo_1, geo_7, geo_8, geo_9, geo_10, table_geo):
    total_number = geo_1 + geo_7 + geo_8 + geo_9 + geo_10
    print(geo_1, geo_7, geo_8, geo_9, geo_10, total_number)
    text_1 = io.StringIO()
    print("{0:0.1f}".format(100 * geo_1 / total_number), '\\%', file=text_1)
    table_geo = table_geo + 'Regions 1 - 6 (USA) & ' + '\\multicolumn{1}{c|}{' + text_1.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    text_7 = io.StringIO()
    print("{0:0.1f}".format(100 * geo_7 / total_number), '\\%', file=text_7)
    table_geo = table_geo + 'Regions 7 (Canada) & ' + '\\multicolumn{1}{c|}{' + text_7.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    text_8 = io.StringIO()
    print("{0:0.1f}".format(100 * geo_8 / total_number), '\\%', file=text_8)
    table_geo = table_geo + 'Regions 8 (Europe/Africa, Middle East) & ' + '\\multicolumn{1}{c|}{' + text_8.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    text_9 = io.StringIO()
    print("{0:0.1f}".format(100 * geo_9 / total_number), '\\%', file=text_9)
    table_geo = table_geo + 'Regions 9 (Central/South America) & ' + '\\multicolumn{1}{c|}{' + text_9.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    text_10 = io.StringIO()
    print("{0:0.1f}".format(100 * geo_10 / total_number), '\\%', file=text_10)
    table_geo = table_geo + 'Region 10 (Asia/Pacific) & ' + '\\multicolumn{1}{c|}{' + text_10.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    return table_geo

def summary_gender(gender_m, gender_f, gender_u, table_gender):
    total_number = gender_m + gender_f + gender_u
    print(gender_m, gender_f, gender_u, total_number)
    text_m = io.StringIO()
    print("{0:0.1f}".format(100 * gender_m / total_number), '\\%', file=text_m)
    table_gender = table_gender + 'Male & ' + '\\multicolumn{1}{c|}{' + text_m.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    text_f = io.StringIO()
    print("{0:0.1f}".format(100 * gender_f / total_number), '\\%', file=text_f)
    table_gender = table_gender + 'Female & ' + '\\multicolumn{1}{c|}{' + text_f.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    return table_gender

def summary_aff(aff_a, aff_i, aff_g, table_aff):
    total_number = aff_a + aff_i + aff_g
    text_a = io.StringIO()
    print("{0:0.1f}".format(100 * aff_a / total_number), '\\%', file=text_a)
    table_aff = table_aff + 'Academia & ' + '\\multicolumn{1}{c|}{' + text_a.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    text_i = io.StringIO()
    print("{0:0.1f}".format(100 * aff_i / total_number), '\\%', file=text_i)
    table_aff = table_aff + 'Industry & ' + '\\multicolumn{1}{c|}{' + text_i.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    text_g = io.StringIO()
    print("{0:0.1f}".format(100 * aff_g / total_number), '\\%', file=text_g)
    table_aff = table_aff + 'Government & ' + '\\multicolumn{1}{c|}{' + text_g.getvalue().rstrip() + '}' + '\\\\' + '\\hline' + '\n'
    return table_aff

# #########################
# Main function starts here
# #########################

# process variables
my_tc_name = "MSA"
my_tc_full_name = "Multimedia Systems and Applications"
my_chair_name = "Dong Tian"
my_chairelect_name = "Frederic Dufaux"

table_voting_members = ''
table_gender = ''
table_geo = ''
table_aff = ''
table_conference_1 = ''
table_conference_2 = ''
table_journal = ''
table_award = ''
table_keynotes = ''
table_other_service = ''
table_leadership = ''
table_plan = ''

(gender_m, gender_f, gender_u) = (0, 0, 0)
(geo_1, geo_7, geo_8, geo_9, geo_10) = (0, 0, 0, 0, 0)
(aff_a, aff_i, aff_g) = (0, 0, 0)

# ###################
# Load data from CSV
# ###################
csv_reader = open('../examples/survey_167184_Mar29.csv', 'r')
has_header = csv.Sniffer().has_header(csv_reader.read(1024))
csv_reader.seek(0)
my_db = csv.reader(csv_reader, delimiter=',',skipinitialspace=True)
if (has_header):
    next(my_db)
# until here the header in CSV is skipped

# ##########
# generate the opening text for each table
table_voting_members = '''\\begin{longtable}{|p{0.08\\textwidth}|p{0.08\\textwidth}|p{0.25\\textwidth}|p{0.25\\textwidth}|p{0.1\\textwidth}|p{0.07\\textwidth}|}
\\hline
\\bf{First Name} & \\bf{Last Name} & \\bf{Affiliation} & \\bf{Email} & \\bf{IEEE Grade} & \\hspace{0pt}\\bf{Region}\\\\
\\hline
'''
table_geo = '''\\begin{table}[H]
\\centering\\small
\\begin{tabular}{|p{0.4\\textwidth}|p{0.23\\textwidth}|}
\\hline
\\multicolumn{1}{|c|}{\\bf{Region}} & \\bf{Percentage of members} \\\\
\\hline
'''
table_gender = '''\\begin{table}[H]
\\centering\\small
\\begin{tabular}{|p{0.2\\textwidth}|p{0.23\\textwidth}|}
\\hline
\\multicolumn{1}{|c|}{\\bf{Gender}} & \\bf{Percentage of members} \\\\
\\hline
'''
table_aff = '''\\begin{table}[H]
\\centering\\small
\\begin{tabular}{|p{0.2\\textwidth}|p{0.23\\textwidth}|}
\\hline
\\multicolumn{1}{|c|}{\\bf{Category}} & \\bf{Percentage of members} \\\\
\\hline
'''
table_conference_1 = '''\\begin{longtable}{|p{0.15\\textwidth}|p{0.19\\textwidth}|p{0.40\\textwidth}|p{0.15\\textwidth}|}
\\hline
\\bf{Your Name} & \\bf{Conference/Event Sponsors} & \\bf{Conference/Event Title} & \\bf{Your Role}\\\\
\\hline
'''
table_conference_2 = '''\\begin{longtable}{|p{0.15\\textwidth}|p{0.19\\textwidth}|p{0.40\\textwidth}|p{0.15\\textwidth}|}
\\hline
\\bf{Your Name} & \\bf{Conference/Event Sponsors} & \\bf{Conference/Event Title} & \\bf{Your Role}\\\\
\\hline
'''
table_journal = '''\\begin{longtable}{|p{0.15\\textwidth}|p{0.19\\textwidth}|p{0.40\\textwidth}|p{0.15\\textwidth}|}
\\hline
\\bf{Your Name} & \\bf{Journal Sponsors} & \\bf{Journal Title} & \\bf{Your Role}\\\\
\\hline
'''
table_award = '''\\begin{longtable}{|p{0.15\\textwidth}|p{0.30\\textwidth}|p{0.15\\textwidth}|}
\\hline
\\bf{Your Name} & \\bf{Award / Honor / Recognition} & \\bf{Period}\\\\
\\hline
'''
table_keynote = '''\\begin{longtable}{|p{0.1\\textwidth}|p{0.15\\textwidth}|p{0.30\\textwidth}|p{0.20\\textwidth}|p{0.12\\textwidth}|}
\\hline
\\bf{Your Name} & \\bf{Invited By} & \\bf{Conference/Event Title} & \\bf{Talk Title} & \\bf{Date}\\\\
\\hline
'''
table_other_service = '''\\begin{table}[H]
\\centering\\small
\\begin{tabular}{|c|c|c|c|}
\\hline
\\bf{Your Name} & \\bf{Organization} & \\bf{Position / Activity} & \\bf{Period}\\\\
\\hline
'''

# ##########
# read data from CSV
for row in my_db:
    for i in range(len(row)):
        row[i] = row[i].replace('&', '\\&')

    # safeguard email address with "_"
    row[3] = re.sub("_", "\\_", row[3])
    
    table_voting_members = table_voting_members + '\\hspace{0pt}' + row[0] + '&' + '\\hspace{0pt}' + row[1] + '&' + row[2] + '& \\scriptsize{' + row[3] + '} &' + row[4] + '&' + row[5] + '\\\\' + '\\hline' + '\n'
    (geo_1, geo_7, geo_8, geo_9, geo_10) = proc_geo(geo_1, geo_7, geo_8, geo_9, geo_10)
    (gender_m, gender_f, gender_u) = proc_gender(gender_m, gender_f, gender_u)
    (aff_a, aff_i, aff_g) = proc_aff(aff_a, aff_i, aff_g)
    table_conference_1 = proc_conference_table_1( table_conference_1 )
    table_conference_2 = proc_conference_table_2( table_conference_2 )
    table_journal = proc_journal( table_journal )
    table_award = proc_award( table_award )
    table_keynote = proc_keynote( table_keynote )
    table_other_service = proc_other_service( table_other_service )
    table_leadership = table_leadership + row[0] + ' ' + row[1] + ': ' + row[98] + '\n' + '\n'
    table_plan = table_plan + row[0] + ' ' + row[1] + ': ' + row[99] + '\n' + '\n'

# ##########
# compute the geographical, gender and affiliation tables
table_geo = summary_geo(geo_1, geo_7, geo_8, geo_9, geo_10, table_geo)
table_gender = summary_gender(gender_m, gender_f, gender_u, table_gender)
table_aff = summary_aff(aff_a, aff_i, aff_g, table_aff)

# ##########
# append the closing text for each table
table_voting_members = table_voting_members + '''
\\caption{Voting Members}
\\label{tab:voting_members}
\\end{longtable}
'''
table_geo = table_geo + '''  \\end{tabular}
\\caption{Geographical Distribution}
\\label{tab:geo}
\\end{table}
'''
table_gender = table_gender + '''  \\end{tabular}
\\caption{Gender Distribution}
\\label{tab:gender}
\\end{table}
'''
table_aff = table_aff + '''  \\end{tabular}
\\caption{Affiliation Distribution}
\\label{tab:aff}
\\end{table}
'''
table_conference_1 = table_conference_1 + '''  
\\caption{IEEE Conference/Event - Technically and financially co-sponsored by the CAS Society}
\\label{tab:conference_1}
\\end{longtable}
'''
table_conference_2 = table_conference_2 + ''' 
\\caption{IEEE Conference/Event - financially co-sponsored by the CAS Society}
\\label{tab:conference_2}
\\end{longtable}
'''
table_journal = table_journal + ''' 
\\caption{IEEE Journal Editorship - (co-)sponsored by the CAS Society}
\\label{tab:journal}
\\end{longtable}
'''
table_award = table_award + ''' 
\\caption{Awards, Honors, and Recognitions}
\\label{tab:award}
\\end{longtable}
'''
table_keynote = table_keynote + '''
\\caption{Keynote Speeches / Invited Talks}
\\label{tab:keynote}
\\end{longtable}
'''
table_other_service = table_other_service + '''  \\end{tabular}
\\caption{Other Distinguished IEEE Services}
\\label{tab:otherservice}
\\end{table}
'''


# ##########
# process latex source file
reader = open('../examples/main_template.tex', 'r')
writer = open('../examples/main.tex', 'w')
for line in reader:
    line = line.rstrip()

    if (line.startswith('INSERT')):
        line = dispatchjob( line )
        writer.write(line+'\n')
    else:
        # print(line)
        writer.write(line+'\n')
    
reader.close()
writer.close()
csv_reader.close()
