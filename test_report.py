
import subprocess

command = 'C:\Program Files (x86)\Google\Chrome\Application\chrome --headless --disable-gpu '
command +='--print-to-pdf="D:/Documents/Projets/Python/Backtester/test.pdf"'
command += ' D:/Documents/Projets/Python/Backtester/report-template.html'


subprocess.run(command)
