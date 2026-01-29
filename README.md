# CodeAnalysisWithLLMs
This repository consists of two programs: A python program ("vularis") which reads files from a specified directory, formulates API requests to an LLM and generates a JSON vulnerability report. Furthermore, a web application ("reportviewer") that can be run locally to open the generated vulnerability report for inspection in a web browser.

## Vularis
Vularis is a command-line tool. It can be executed as follows:<br>
python.exe vularis.py --scfolder <scfolder> --llm gpt-4o --prompt basic

To display the help page, run:<br>
python.exe vularis.py --help

## Reportviewer
To test the report viewer:
1. Open index.html from reportviewer/src in a web browser.
2. Upload the provided sample vulnerability report located in vularis/report.
