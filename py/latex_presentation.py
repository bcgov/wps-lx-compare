'''20240620 initial template to be modified accordingly'''
import os

def generate_slide_frames(title, filenames, comments):
    # Initialize an empty string to accumulate LaTeX code
    latex_content = ''

    # Generate LaTeX code for each filename in the list
    for i, filename in enumerate(filenames):
        if os.path.exists(filename):
            slide_number = os.path.splitext(os.path.basename(filename))[0]
            slide_comment = comments[i] if i < len(comments) else ''
            latex_content += rf'''
    \begin{{frame}}[fragile]{{{title} - Slide {slide_number}}}
        \frametitle{{{title} - Slide {slide_number}}}
        \begin{{columns}}
            \begin{{column}}{{0.6\textwidth}}
                \includegraphics[width=1.3\linewidth,height=0.8\textheight,keepaspectratio]{{{filename}}}
            \end{{column}}
            \begin{{column}}{{0.5\textwidth}}
                \raggedright
                \small
                {slide_comment}
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
                \includegraphics[width=\linewidth,height=\textheight,keepaspectratio]{{{filenames[1]}}}
            \end{{column}}
            \begin{{column}}{{0.5\textwidth}}
                \includegraphics[width=1.3\linewidth,height=\textheight,keepaspectratio]{{{filenames[0]}}}
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
comments1 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 5km from LCF, total: 1244 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 46 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 208 \\newline \\newline  Black: Neither sensor detected a strike: total: 112']

comments2 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -avgerage distance: 1366.8m \\newline    -missed 190 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -avgerage distance: 978.7m\\newline    -missed 158 LCFs',
             'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -avgerage distance: 1098.9m \\newline    -missed 17 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -avgerage distance: 875.9m\\newline    -missed 9 LCFs',
             'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -avgerage distance: 1422.6m \\newline    -missed 32 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -avgerage distance: 1371.3m\\newline    -missed 32 LCFs',
             'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -avgerage distance: 1231.3m \\newline    -missed 25 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -avgerage distance: 1001.1m\\newline    -missed 30 LCFs',
             'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -avgerage distance: 1463.8m \\newline    -missed 22 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -avgerage distance: 907.4m\\newline    -missed 14 LCFs',
             'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -avgerage distance: 1429.1m \\newline    -missed 76 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -avgerage distance: 885.1m\\newline    -missed 47 LCFs',
             'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -avgerage distance: 1456.1m \\newline    -missed 19 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -avgerage distance: 1009.9m\\newline    -missed 26 LCFs']

comments3 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 2km from LCF, total: 812 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 98 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 409 \\newline \\newline  Black: Neither sensor detected a strike: total: 291']

comments4 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308\\newline    -avgerage distance: 803.3m \\newline    -missed 537 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -avgerage distance: 583.6m\\newline    -missed 389 LCFs',
             'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -avgerage distance: 729.1m \\newline    -missed 40 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -avgerage distance: 479.3m\\newline    -missed 34 LCFs',
             'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -avgerage distance: 858.4m \\newline    -missed 71 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -avgerage distance: 891.6m\\newline    -missed 66 LCFs',
             'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -avgerage distance: 703.7m \\newline    -missed 84 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -avgerage distance: 512.8m\\newline    -missed 78 LCFs',
             'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -avgerage distance: 807.4m \\newline    -missed 70 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -avgerage distance: 616.1m\\newline    -missed 36 LCFs',
             'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -avgerage distance: 873.4m \\newline    -missed 192 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -avgerage distance: 546.4m\\newline    -missed 113 LCFs',
             'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -avgerage distance: 787.4m \\newline    -missed 81 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -avgerage distance: 590.7m\\newline    -missed 62 LCFs']

comments5 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 1km from LCF, total: 475 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 110 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 503 \\newline \\newline  Black: Neither sensor detected a strike, total: 522']

comments6 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -avgerage distance: 493.6m \\newline    -missed 895 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -avgerage distance: 363.9m\\newline    -missed 632 LCFs',
             'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -avgerage distance: 469.0m \\newline    -missed 76 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -avgerage distance: 300.6m\\newline    -missed 55 LCFs',
             'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -avgerage distance: 542.2m \\newline    -missed 113 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -avgerage distance: 553.3m\\newline    -missed 114 LCFs',
             'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -avgerage distance: 409.2m \\newline    -missed 141 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -avgerage distance: 323.7m\\newline    -missed 110 LCFs',
             'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -avgerage distance: 500.4m \\newline    -missed 108 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -avgerage distance: 404.1m\\newline    -missed 65 LCFs',
             'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -avgerage distance: 510.3m \\newline    -missed 330 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -avgerage distance: 359.2m\\newline    -missed 186 LCFs',
             'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -avgerage distance: 547.1m \\newline    -missed 127 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -avgerage distance: 340.0m\\newline    -missed 102 LCFs']

comments8 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -avgerage distance: 291.8m \\newline    -missed 1222 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -avgerage distance: 241.6m\\newline    -missed 886 LCFs',
             'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -avgerage distance: 289.8m \\newline    -missed 114 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -avgerage distance: 219.4m\\newline    -missed 74 LCFs',
             'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -avgerage distance: 274.4m \\newline    -missed 160 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -avgerage distance: 300.9m\\newline    -missed 161 LCFs',
             'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -avgerage distance: 284.1m \\newline    -missed 182 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -avgerage distance: 216.5m\\newline    -missed 147 LCFs',
             'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -avgerage distance: 317.7m \\newline    -missed 145 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -avgerage distance: 290.4m\\newline    -missed 102 LCFs',
             'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -avgerage distance: 289.0m \\newline    -missed 434 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -avgerage distance: 237.4m\\newline    -missed 272 LCFs',
             'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -avgerage distance: 303.6m \\newline    -missed 187 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -avgerage distance: 247.4m\\newline    -missed 131 LCFs']


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


\begin{frame}
    \frametitle{Map Details} % Sets the title of the slide
 
    -Map of all LCFs in BC in 2023\\-Color of point implies which sensor detected it (see below)\\-Fire was considered detected if there was a stike within the max radius of the fire point and the strike occured within three weeks before the ignition date
\end{frame}
'''
 
latex_mid = r'''
\begin{frame}
    \frametitle{Histogram Details} % Sets the title of the slide
 
    -Searches for stikes within a max radius of the lightning caused fire (LCF)\\-Only uses stikes which occured within 3 weeks before the ignition date\\-Uses Haversine method to calculate distance from lat and long\\ -Stikes detected: Total number of stikes detected by the sensor in the region \\ -Average Distance: Average distance from the strike to the LCF \\ -Missed: Total number of LCFs where the sensor did not detect a strike within max radius
\end{frame}
'''

latex_end = r'''
\end{document}
'''

# Make the presentation

with open('presentation.tex', 'w') as file:
    file.write((latex_preamble +
                generate_slide_frames_double('LCFs with sensor detection with max radius: 5000m', slide_set1,[]) + latex_mid + 
                generate_slide_frames('Strike distance from LCF with max radius: 5000m', slide_set2,comments2) +
                generate_slide_frames_double('LCFs with sensor detection with max radius: 2000m', slide_set3,[]) + 
                generate_slide_frames('Strike distance from LCF with max radius: 2000m', slide_set4,comments4) + 
                generate_slide_frames_double('LCFs with sensor detection with max radius: 1000m', slide_set5,[]) + 
                generate_slide_frames('Strike distance from LCF with max radius: 1000m', slide_set6,comments6) + 
                generate_slide_frames_double('LCFs with sensor detection with max radius: 500m', slide_set7,[]) + 
                generate_slide_frames('Strike distance from LCF with max radius: 500m', slide_set8,comments8) + 
                latex_end
                ).replace('_','\\_')) 
    
os.system('pdflatex presentation.tex')

