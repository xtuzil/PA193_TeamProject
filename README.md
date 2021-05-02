# PA193_TeamProject
Repository for team project in PA193 (Security Certificate Parser)
## Usage
Parsing is done by calling `parse.py`

`python parse.py <INPUT FILE> [<INPUT_FILE> ...]`

Arguments
```
  -h, --help            show help message and exit
  -p, --pretty-print [ title | versions | table_of_contents | revisions | bibliography | other ]
                        Pretty print. To Pretty print more keys stack multiple -p or --pretty-print arguments
                        e. g. -p title -p versions -p table_of_contents
  -o, --output-dir OUTPUT_DIR
                        Output directory (default: output)

```

## Assignment
* Input:TXTfile(PDFtransformedtoTXTfileviapdftotext)  
  * `Use –layout option with pdftotext`
* Output: Structured JSON with extracted information

#### Additional features:
* Support command line arguments for pretty-printing subparts of document
  * Title
  * Table of contents
  * Versions of used libraries • Revisions
  * Bibliography
* Support multiple input files at the same time – Focus on correct error handling


 #### Project phases
* Phase I – deadline 3rd week
  * Inspect assigned certificates and annotate data (solo work of everyone) – Form teams of 3 people (for next phases)
* Phase II – deadline 6th week – Design tool interface **Deadline 6.4.**
  * Setup automatic testing
  * Start implementation
  * Report (2 A4), brief overview at seminar group (5 minutes)
* Phase III – deadline 9th week
  * Finalize implementation
  * Presentation for seminar group (5-7 minutes)
* Phase IV – deadline 13th week
  * Analyze project of another group
  * Final presentation for lecture (10 minutes)
