'''20240620 initial template to be modified accordingly'''
import os
import pickle

# def generate_slide_frames(title, filenames, comments):
#     # Initialize an empty string to accumulate LaTeX code
#     latex_content = ''

#     # Generate LaTeX code for each filename in the list
#     for i, filename in enumerate(filenames):
#         if os.path.exists(filename):
#             slide_number = os.path.splitext(os.path.basename(filename))[0]
#             slide_comment = comments[i] if i < len(comments) else ''
#             latex_content += rf'''
#     \begin{{frame}}[fragile]{{{title} - Slide {slide_number}}}
#         \frametitle{{{title} - Slide {slide_number}}}
#         \begin{{columns}}
#             \begin{{column}}{{0.6\textwidth}}
#                 \includegraphics[width=1.3\linewidth,height=0.8\textheight,keepaspectratio]{{{filename}}}
#             \end{{column}}
#             \begin{{column}}{{0.5\textwidth}}
#                 \raggedright
#                 \small
#                 {slide_comment}
#             \end{{column}}
#         \end{{columns}}
#     \end{{frame}}
#     '''

#     return latex_content

def generate_slide_frames(title, filenames, datas, titles):
    # Initialize an empty string to accumulate LaTeX code
    latex_content = ''

    # Generate LaTeX code for each filename in the list
    for i, filename in enumerate(filenames):
        if os.path.exists(filename):
            slide_number = titles[i]
            data = datas[i]
            latex_content += rf'''
    \begin{{frame}}[fragile]{{{slide_number}: {title}}}
        \frametitle{{{slide_number}: {title}}}
        \begin{{columns}}
            \begin{{column}}{{0.5\textwidth}}
                \includegraphics[width=1.3\linewidth,height=0.8\textheight,keepaspectratio]{{{filename}}}
            \end{{column}}
            \begin{{column}}{{0.5\textwidth}}
                \begin{{table}}[ht]
                    \centering
                    \begin{{tabular}}{{|c|c|c|}}
                        \hline
                        \multicolumn{{3}}{{|c|}}{{{slide_number}, LCFs: {data[0]}}} \\
                        \hline
                        \multicolumn{{1}}{{|c|}}{{Field}} & \multicolumn{{1}}{{|c|}}{{AEM}} & \multicolumn{{1}}{{|c|}}{{CLDN}} \\
                        \hline
                        \# LX ({slide_number}) & {data[1]} & {data[4]} \\
                        Average distance (m) & {data[2]} & {data[5]} \\
                        \# LCF w/o LX match & {data[3]} & {data[6]} \\
                        \hline
                    \end{{tabular}}
                \end{{table}}
            \end{{column}}
        \end{{columns}}
    \end{{frame}}
    '''

    return latex_content

def generate_slide_frames_double(title, filenames, comments):
    # Initialize an empty string to accumulate LaTeX code
    latex_content = ''

    # Generate LaTeX code for each filename in the list
    latex_content += rf'''
    \begin{{frame}}[fragile]{{{title}}}
        \frametitle{{{title}}}
        \begin{{columns}}
            \begin{{column}}{{0.5\textwidth}}
                \includegraphics[width=\linewidth,height=0.7\textheight,keepaspectratio]{{{filenames[1]}}}
                \parbox{{\linewidth}}{{ % Adjust width to the column width
                    \tiny % Adjust text size if needed
                    \text{{-LCF points colored to show matching with LX data \\ }} \\
                    -LCF fire is considered matched with LX data if there is a strike within "max radius", occurring in a three-week window up to and including the ignition date}}
            \end{{column}}
            \begin{{column}}{{0.5\textwidth}}
                \includegraphics[width=1.5\linewidth,height=\textheight,keepaspectratio]{{{filenames[0]}}}
            \end{{column}}
        \end{{columns}}
    \end{{frame}}
    '''

    return latex_content
# Example usage:
# List of filenames and comments for each slide set
dir_list = ['./plots/5000data/LCFS',"./plots/5000data",'./plots/2000data/LCFS',"./plots/2000data",'./plots/1000data/LCFS',"./plots/1000data",'./plots/500data/LCFS',"./plots/500data"]
slide_list = [[] for i in range(len(dir_list))]

for i in range(len(dir_list)):
    files = os.listdir(dir_list[i])
    file_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'png':
            file_list.append(f'{dir_list[i]}/{files[n]}')
        else:
            continue;
    slide_list[i] = [f for f in file_list]

slide_set1 = slide_list[0]
slide_set2 = slide_list[1]
slide_set3 = slide_list[2]
slide_set4 = slide_list[3]
slide_set5 = slide_list[4]
slide_set6 = slide_list[5]
slide_set7 = slide_list[6]
slide_set8 = slide_list[7]

titles = ['BC', 'Cariboo', 'Coast', 'Kamloops', 'North West', 'Prince George', 'South East']

order = ['BC', 'CARIBOO', 'COAST', 'KAM', 'NW', 'PG', 'SE']
with open(f'pickles/5000_data.pkl','rb') as f:
    data_5000_nonsort = pickle.load(f)

    print(data_5000_nonsort)

data_5000 = [0,0,0,0,0,0,0]
for entry in data_5000_nonsort:
    if entry[0] == 'BC':
        data_5000[0] = entry[1:]
    elif entry[0] == 'CARIBOO':
        data_5000[1] = entry[1:]
    elif entry[0] == 'COAST':
        data_5000[2] = entry[1:]
    elif entry[0] == 'KAM':
        data_5000[3] = entry[1:]
    elif entry[0] == 'NW':
        data_5000[4] = entry[1:]
    elif entry[0] == 'PG':
        data_5000[5] = entry[1:]
    elif entry[0] == 'SE':
        data_5000[6] = entry[1:]

with open(f'pickles/2000_data.pkl','rb') as f:
    data_2000_nonsort = pickle.load(f)

data_2000 = [0,0,0,0,0,0,0]
for entry in data_2000_nonsort:
    if entry[0] == 'BC':
        data_2000[0] = entry[1:]
    elif entry[0] == 'CARIBOO':
        data_2000[1] = entry[1:]
    elif entry[0] == 'COAST':
        data_2000[2] = entry[1:]
    elif entry[0] == 'KAM':
        data_2000[3] = entry[1:]
    elif entry[0] == 'NW':
        data_2000[4] = entry[1:]
    elif entry[0] == 'PG':
        data_2000[5] = entry[1:]
    elif entry[0] == 'SE':
        data_2000[6] = entry[1:]

with open(f'pickles/1000_data.pkl','rb') as f:
    data_1000_nonsort = pickle.load(f)

data_1000 = [0,0,0,0,0,0,0]
for entry in data_1000_nonsort:
    if entry[0] == 'BC':
        data_1000[0] = entry[1:]
    elif entry[0] == 'CARIBOO':
        data_1000[1] = entry[1:]
    elif entry[0] == 'COAST':
        data_1000[2] = entry[1:]
    elif entry[0] == 'KAM':
        data_1000[3] = entry[1:]
    elif entry[0] == 'NW':
        data_1000[4] = entry[1:]
    elif entry[0] == 'PG':
        data_1000[5] = entry[1:]
    elif entry[0] == 'SE':
        data_1000[6] = entry[1:]

with open(f'pickles/500_data.pkl','rb') as f:
    data_500_nonsort = pickle.load(f)

data_500 = [0,0,0,0,0,0,0]
for entry in data_500_nonsort:
    if entry[0] == 'BC':
        data_500[0] = entry[1:]
    elif entry[0] == 'CARIBOO':
        data_500[1] = entry[1:]
    elif entry[0] == 'COAST':
        data_500[2] = entry[1:]
    elif entry[0] == 'KAM':
        data_500[3] = entry[1:]
    elif entry[0] == 'NW':
        data_500[4] = entry[1:]
    elif entry[0] == 'PG':
        data_500[5] = entry[1:]
    elif entry[0] == 'SE':
        data_500[6] = entry[1:]


# data_5000 = [[1610, 228299, 1366.8, 188, 279427, 978.7, 156], [
# 167, 22868, 1098.9, 17, 21796, 875.9, 9], [
# 192, 7433, 1422.6, 31, 6035, 1371.3, 31], [
# 282, 22474, 1231.3, 25, 18005, 1001.1, 30], [
# 185, 18725, 1463.8, 22, 32839, 907.4, 14], [
# 539, 125712, 1429.1, 75, 174975, 885.1, 46], [
# 245, 31087, 1456.1, 19, 25777, 1009.9, 26]]

# data_2000 = [[1610, 228299, 803.3, 535, 279427, 583.6, 387], [
# 167, 22868, 729.1, 40, 21796, 479.3, 34], [
# 192, 7433, 858.4, 70, 6503, 891.6, 65], [
# 282, 22474, 703.7, 84, 18005, 512.8, 78], [
# 185, 18725, 807.4, 70, 32839, 616.1, 36], [
# 539, 125712, 873.4, 191, 174975, 546.4, 112], [
# 245, 31087, 787.4, 81, 25777, 590.7, 62]]

# data_1000 = [[1610, 228299, 493.6, 893, 279427, 363.9, 630], [
# 167, 22868, 469.0, 76, 21796, 300.6, 55], [
# 192, 7433, 542.2, 112, 6503, 553.3, 113], [
# 282, 22474, 409.2, 141, 18005, 323.7, 110], [
# 185, 18725, 500.4, 108, 32839, 404.1, 65], [
# 539, 125712, 510.3, 330, 174975, 359.2, 186], [
# 245, 31087, 547.1, 127, 25777, 340.0, 102]]

# data_500 = [[1610, 228299, 291.8, 1222, 279427, 241.6, 886],
# [167, 22868, 289.8, 114, 21796, 219.4, 74],
# [192, 7433, 274.4, 160, 6503, 300.9, 161],
# [282, 22474, 284.1, 182, 18005, 216.5, 147],
# [185, 18725, 317.7, 145, 32839, 290.4, 102],
# [539, 125712, 289.0, 434, 174975, 237.4, 272],
# [245, 31087, 303.6, 187, 25777, 247.4, 131]]


# comments1 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 5km from LCF, total: 1244 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 46 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 208 \\newline \\newline  Black: Neither sensor detected a strike: total: 112']

# comments2 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -average distance: 1366.8m \\newline    -missed 190 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -average distance: 978.7m\\newline    -missed 158 LCFs',
#              'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -average distance: 1098.9m \\newline    -missed 17 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -average distance: 875.9m\\newline    -missed 9 LCFs',
#              'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -average distance: 1422.6m \\newline    -missed 32 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -average distance: 1371.3m\\newline    -missed 32 LCFs',
#              'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -average distance: 1231.3m \\newline    -missed 25 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -average distance: 1001.1m\\newline    -missed 30 LCFs',
#              'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -average distance: 1463.8m \\newline    -missed 22 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -average distance: 907.4m\\newline    -missed 14 LCFs',
#              'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -average distance: 1429.1m \\newline    -missed 76 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -average distance: 885.1m\\newline    -missed 47 LCFs',
#              'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -average distance: 1456.1m \\newline    -missed 19 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -average distance: 1009.9m\\newline    -missed 26 LCFs']

# comments3 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 2km from LCF, total: 812 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 98 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 409 \\newline \\newline  Black: Neither sensor detected a strike: total: 291']

# comments4 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308\\newline    -average distance: 803.3m \\newline    -missed 537 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -average distance: 583.6m\\newline    -missed 389 LCFs',
#              'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -average distance: 729.1m \\newline    -missed 40 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -average distance: 479.3m\\newline    -missed 34 LCFs',
#              'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -average distance: 858.4m \\newline    -missed 71 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -average distance: 891.6m\\newline    -missed 66 LCFs',
#              'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -average distance: 703.7m \\newline    -missed 84 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -average distance: 512.8m\\newline    -missed 78 LCFs',
#              'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -average distance: 807.4m \\newline    -missed 70 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -average distance: 616.1m\\newline    -missed 36 LCFs',
#              'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -average distance: 873.4m \\newline    -missed 192 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -average distance: 546.4m\\newline    -missed 113 LCFs',
#              'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -average distance: 787.4m \\newline    -missed 81 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -average distance: 590.7m\\newline    -missed 62 LCFs']

# comments5 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 1km from LCF, total: 475 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 110 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 503 \\newline \\newline  Black: Neither sensor detected a strike, total: 522']

# comments6 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -average distance: 493.6m \\newline    -missed 895 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -average distance: 363.9m\\newline    -missed 632 LCFs',
#              'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -average distance: 469.0m \\newline    -missed 76 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -average distance: 300.6m\\newline    -missed 55 LCFs',
#              'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -average distance: 542.2m \\newline    -missed 113 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -average distance: 553.3m\\newline    -missed 114 LCFs',
#              'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -average distance: 409.2m \\newline    -missed 141 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -average distance: 323.7m\\newline    -missed 110 LCFs',
#              'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -average distance: 500.4m \\newline    -missed 108 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -average distance: 404.1m\\newline    -missed 65 LCFs',
#              'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -average distance: 510.3m \\newline    -missed 330 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -average distance: 359.2m\\newline    -missed 186 LCFs',
#              'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -average distance: 547.1m \\newline    -missed 127 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -average distance: 340.0m\\newline    -missed 102 LCFs']

# comments8 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -average distance: 291.8m \\newline    -missed 1222 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -average distance: 241.6m\\newline    -missed 886 LCFs',
#              'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -average distance: 289.8m \\newline    -missed 114 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -average distance: 219.4m\\newline    -missed 74 LCFs',
#              'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -average distance: 274.4m \\newline    -missed 160 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -average distance: 300.9m\\newline    -missed 161 LCFs',
#              'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -average distance: 284.1m \\newline    -missed 182 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -average distance: 216.5m\\newline    -missed 147 LCFs',
#              'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -average distance: 317.7m \\newline    -missed 145 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -average distance: 290.4m\\newline    -missed 102 LCFs',
#              'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -average distance: 289.0m \\newline    -missed 434 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -average distance: 237.4m\\newline    -missed 272 LCFs',
#              'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -average distance: 303.6m \\newline    -missed 187 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -average distance: 247.4m\\newline    -missed 131 LCFs']


# LaTeX preamble and end code
latex_preamble = r'''
\documentclass[aspectratio=169]{beamer}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{array}
\title{Lightning detector comparison}
\author{Sterling von Dehn and Ash Richardson}
\institute{B.C. Wildfire Service}
\date{\today}

\begin{document}

\begin{frame}
	\titlepage
\end{frame}

'''
# \begin{frame}
#     \frametitle{Map Details} % Sets the title of the slide
 
#     -Map of all LCFs in BC in 2023 \\
#     -Color of point implies which sensor detected it (see below) \\
#     -Fire was considered detected if there was a strike within the max radius of the fire point and the strike occurred within three weeks before the ignition date

# \end{frame}

 
latex_mid = r'''
\begin{frame}
    \frametitle{LX/LCF matches vs distance} % Sets the title of the slide
    - Find LX records in specified "max radius" of lightning caused fire (LCF) occurring within 3 weeks before the ignition date\\
    - Strikes detected: Total number of strikes detected by the sensor in the region \\
    - Average Distance: Average distance of matched LX to LCF \\
    - Missed: Total number of LCFs with no LX match (same criteria) \\
    - Note: Haversine formula used to calculate distances in Geographic coordinates (WGS84)


\end{frame}
'''

latex_end = r'''
\end{document}
'''

# Make the presentation

with open('presentation.tex', 'w') as file:
    file.write((latex_preamble +
                generate_slide_frames_double('LCFs with sensor detection with max radius: 5000m', slide_set1,[]) + latex_mid + 
                generate_slide_frames('LX/LCF matches/max radius: 5000m', slide_set2,data_5000, titles) +
                generate_slide_frames_double('LCFs with sensor detection with max radius: 2000m', slide_set3,[]) + 
                generate_slide_frames('LX/LCF matches/max radius: 2000m', slide_set4,data_2000, titles) + 
                generate_slide_frames_double('LCFs with sensor detection with max radius: 1000m', slide_set5,[]) + 
                generate_slide_frames('LX/LCF matches/max radius: 1000m', slide_set6,data_1000, titles) + 
                generate_slide_frames_double('LCFs with sensor detection with max radius: 500m', slide_set7,[]) + 
                generate_slide_frames('LX/LCF matches/max radius: 500m', slide_set8,data_500, titles) + 
                latex_end
                ).replace('_','\\_')) 
    
os.system('pdflatex presentation.tex')

