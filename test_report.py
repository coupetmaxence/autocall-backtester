import subprocess

command = 'C:\Program Files (x86)\Google\Chrome\Application\chrome --headless --disable-gpu '
command +='--print-to-pdf="D:/Documents/Projets/Python/autocall-backtester/test.pdf"'
command += ' D:/Documents/Projets/Python/autocall-backtester/report-template.html'


with open('create-pdf.sh') as f:
    f.write('#!bin/sh \n google-chrome-stable --headless --disable-gpu --print-to-pdf=reportD.pdf report-template.html')


exit_code = subprocess.call(['./create-pdf.sh'])
