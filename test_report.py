import subprocess

command = 'C:\Program Files (x86)\Google\Chrome\Application\chrome --headless --disable-gpu '
command +='--print-to-pdf="D:/Documents/Projets/Python/autocall-backtester/test.pdf"'
command += ' D:/Documents/Projets/Python/autocall-backtester/report-template.html'


with open('create-pdf.sh','w') as f:
    f.write('#!/bin/sh\ngoogle-chrome-stable --headless --disable-gpu --print-to-pdf=reportD.pdf report-template.html')


exit_code = subprocess.call(['./create-pdf.sh'])

while True:
    exit_code = subprocess.call(['./create-pdf.sh'])

    try:
        exit_code = int(exit_code)

        if exit_code == 0:
            break
    except:
        pass

print('Finished')


