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

# Example usage:
# List of filenames and comments for each slide set
dir_list = ['./plots/5000data/LCFS',"./plots/5000data",'./plots/2000data/LCFS',"./plots/2000data",'./plots/1000data/LCFS',"./plots/1000data"]
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
comments1 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 5km from LCF, total: 1244 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 46 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 208 \\newline \\newline  Black: Neither sensor detected a strike: total: 112']

comments2 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -avgerage distance: 1524.4m \\newline    -missed 319 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -avgerage distance: 978.7m\\newline    -missed 158 LCFs',
             'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -avgerage distance: 1292.5m \\newline    -missed 27 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -avgerage distance: 875.9m\\newline    -missed 9 LCFs',
             'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -avgerage distance: 1465.7m \\newline    -missed 43 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -avgerage distance: 1371.3m\\newline    -missed 32 LCFs',
             'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -avgerage distance: 1485.4m \\newline    -missed 54 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -avgerage distance: 1001.1m\\newline    -missed 30 LCFs',
             'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -avgerage distance: 1643.6m \\newline    -missed 49 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -avgerage distance: 907.4m\\newline    -missed 14 LCFs',
             'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -avgerage distance: 1539.7m \\newline    -missed 96 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -avgerage distance: 885.1m\\newline    -missed 47 LCFs',
             'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -avgerage distance: 1662.8m \\newline    -missed 51 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -avgerage distance: 1009.9m\\newline    -missed 26 LCFs']

comments3 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 2km from LCF, total: 812 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 98 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 409 \\newline \\newline  Black: Neither sensor detected a strike: total: 291']

comments4 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308\\newline    -avgerage distance: 835.4m \\newline    -missed 698 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -avgerage distance: 583.6m\\newline    -missed 389 LCFs',
             'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -avgerage distance: 725.7m \\newline    -missed 57 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -avgerage distance: 479.3m\\newline    -missed 34 LCFs',
             'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -avgerage distance: 882.9m \\newline    -missed 81 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -avgerage distance: 891.6m\\newline    -missed 66 LCFs',
             'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -avgerage distance: 750.8m \\newline    -missed 126 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -avgerage distance: 512.8m\\newline    -missed 78 LCFs',
             'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -avgerage distance: 889.9m \\newline    -missed 95 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -avgerage distance: 616.1m\\newline    -missed 36 LCFs',
             'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -avgerage distance: 896.8m \\newline    -missed 222 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -avgerage distance: 546.4m\\newline    -missed 113 LCFs',
             'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -avgerage distance: 790.3m \\newline    -missed 119 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -avgerage distance: 590.7m\\newline    -missed 62 LCFs']

comments5 = ['All LCFs in BC in 2023 \\newline \\newline Green: Both sensors detected a strike within 1km from LCF, total: 475 \\newline \\newline Orange: AEM detected strike but CLDN did not, total: 110 \\newline \\newline Red: CLDN detected stike but AEM did not, total: 503 \\newline \\newline  Black: Neither sensor detected a strike, total: 522']

comments6 = ['BC, LCFs: 1610 \\newline \\newline AEM Sensor \\newline    -strikes detected: 228308 \\newline    -avgerage distance: 502.6m \\newline    -missed 1025 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 280117 \\newline    -avgerage distance: 363.9m\\newline    -missed 632 LCFs',
             'Cariboo region, LCFs: 167 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22868 \\newline    -avgerage distance: 454.0m \\newline    -missed 89 LCFs \\newline       \\newline CLDN Sensor \\newline    -strikes detected: 21876 \\newline    -avgerage distance: 300.6m\\newline    -missed 55 LCFs',
             'Coast region, LCFs: 192 \\newline \\newline AEM Sensor \\newline    -strikes detected: 7442 \\newline    -avgerage distance: 554.2m \\newline    -missed 121 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 6503 \\newline    -avgerage distance: 553.3m\\newline    -missed 114 LCFs',
             'Kamloops region, LCFs: 282 \\newline \\newline AEM Sensor \\newline    -strikes detected: 22474 \\newline    -avgerage distance: 429.0m \\newline    -missed 174 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 18022 \\newline    -avgerage distance: 323.7m\\newline    -missed 110 LCFs',
             'North West region, LCFs: 185 \\newline \\newline AEM Sensor \\newline    -strikes detected: 18725 \\newline    -avgerage distance: 522.1m \\newline    -missed 131 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 32917 \\newline    -avgerage distance: 404.1m\\newline    -missed 65 LCFs',
             'Prince George region, LCFs: 539 \\newline \\newline AEM Sensor \\newline    -strikes detected: 125712 \\newline    -avgerage distance: 515.9m \\newline    -missed 357 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 174992 \\newline    -avgerage distance: 359.2m\\newline    -missed 186 LCFs',
             'South East region, LCFs: 245 \\newline \\newline AEM Sensor \\newline    -strikes detected: 31087 \\newline    -avgerage distance: 552.5m \\newline    -missed 153 LCFs \\newline \\newline CLDN Sensor \\newline    -strikes detected: 25780 \\newline    -avgerage distance: 340.0m\\newline    -missed 102 LCFs']


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
                generate_slide_frames('LCFs with sensor detection with max radius: 5000m', slide_set1,comments1) + latex_mid + 
                generate_slide_frames('Strike distance from LCF with max radius: 5000m', slide_set2,comments2) +
                generate_slide_frames('LCFs with sensor detection with max radius: 2000m', slide_set3,comments3) + 
                generate_slide_frames('Strike distance from LCF with max radius: 2000m', slide_set4,comments4) + 
                generate_slide_frames('LCFs with sensor detection with max radius: 1000m', slide_set5,comments5) + 
                generate_slide_frames('Strike distance from LCF with max radius: 1000m', slide_set6,comments6) + 
                 latex_end
                ).replace('_','\\_')) 
    
os.system('pdflatex presentation.tex; open presentation.pdf')

