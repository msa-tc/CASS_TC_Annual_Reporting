# annual_report_script

## Example
An quick example report is temporarily put here:

https://drive.google.com/drive/folders/1jEj8Ptl4tw3PWDp56Rx_iGjo3dhcSM89?usp=sharing

## Main script
* `scripts/main.py`

This python script creates a file named as `examples/main.tex` ready to be compiled. It puts the survey results from TC members into a draft report. The draft report is intended as a starting point for the Chair to finish the Annual report.

## Supporting files
* `examples/main_template.tex`

This file serves as a template of the annual report. It is not compilable, but as an input to the main script to reference.

* `examples/tcmeetings.tex`
* `examples/votingmembers.tex`
* `examples/leadership.tex`
* `examples/plan.tex`

This list of files are input to the final report. The Chair needs to write down their text in these files. They will be imported by the `examples/main.tex` and won't be ovewritten when `examples/main.tex` is re-generated.

* `examples/survey.csv`
The survey data. The format has to be strictly followed. See https://4eyes.io/s/1Hu0w/ for a supported survey.