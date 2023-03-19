# APTAutomaticLinking

## Prerequisites

All prerequisites can be installed using pip with the `requirements.txt` file.

```pip install -r requirements.txt```

## Usage

1. Replace the default knowledgebase in `KnowledgeBase.csv` with your own, or continue to use it.
2. Supply an attack in `Attack.csv`. The program comes preloaded with the OceanLotus Campaign.
3. Run `run.bat`, or run `Launch.py` using Python from the `src` folder.
4. Enter a desired confidence level between 0.0 and 1.0.
5. Optionally, choose whether to attempt combinations to link procedures.
6. Edit the `config.cfg` file to modify program behavior.

## Configuration
Edit the `config.cfg` file to customize how the program runs. The `paths` section specifies the filepaths to the knowledgebase, output, and input files. The `weights` section specifies the weights for each match/mismatch in the alternative generator. The `other` section specifies other settings, such as whether to drop procedures that don't match the original operating system.

Note: The program may throw an error if the config.cfg file is not properly formatted. Be sure to check for any typos or errors in the file.

## Notes

For more information on the program's configuration, see the `README.md` file in the `src` folder.
