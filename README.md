# Camera Ready Template Conformance Checker 
### by the CBSoft'26 Proceedings Co-Chairs

Tooling made to ease the manual validation of the camera ready papers accepted at the CBSoft symposia and workshops, responsible for checking whether the papers conform to the template expeted by the proceedings team.

## Installation

The script assumes you have access to `docker-compose` or an alternative container orchestration framework (such as `podman`). 

Additionally, the tester requires the TrueType font archives for the fonts checked in the template. These must be placed inside the `data/fonts/` dir.

## Configuration

Before executing the script, some conference-related adjustments are needed.

A file in the `data/ruleset/` includes information on the constraints to be checked for a given conference, as well as the track headers and page limits. Please follow carefully the syntax used on the example data included from past conferences, such as that seen in `data/ruleset/cbsoft26.json`.

## Checking a Single Paper

In order to check whether a single paper (possibly yours) conforms to the rules of any specific track, first ensure the a copy of paper's pdf is available in the `data/` directory.

Then, invoke the checker container by adapting the following line and executing it at the project's root dir (the one this README finds itself in):
```(bash)
$> docker compose run --remove-orphans -e CHECK_PAPER_AT=mock1.pdf -e TRACK=sbes_26_rt checker
```

The environment variable `CHECK_PAPER_AT` points to the paper to be checked. In the case presented, corresponding to the `data/mock1.pdf` file. Additionally, it is necessary to specify the track the paper pertains to. In the example, the paper is checked against the restrictions of the Research Track of SBES 2026. The available tracks can be read in the ruleset file specified in the `RULESET_FILE` variable of the `checker/src/constant.py` file (in the current case, `data/ruleset/cbsoft26.json`).

## Checking a Batch of Papers

The process applied to checking whether a set of papers conforms to the restrictions of a track is quite similar to that used for checking a single paper. 

First, ensure that a subdirectory of `data/` includes all papers to be reviewed in a single batch.

Then, adapt the following line and execute it at the project's root:
```(bash)
$> docker compose run --remove-orphans -e CHECK_PAPERS_AT=batchDirectory -e TRACK=sbes_26_rt checker
```

The environment variable `CHECK_PAPERS_AT` points to the subdirectory of `data/` containing the papers to be checked. In the case presented, corresponding to the `data/batchDirectory/` subdirectory. Similarly to what was done to check a single paper, it is necessary to specify the track the papers pertain to. In the example, the papers are checked against the restrictions of the Research Track of SBES 2026. The available tracks can be read in the ruleset file specified in the `RULESET_FILE` variable of the `checker/src/constant.py` file (in the current case, `data/ruleset/cbsoft26.json`).


The results are saved under the `data/` directory. For a batch saved in `data/batchDirectory/`, the results will be available in the file `data/batchDirectory_results.xlsx`.

## Testing

Run the tests associated with the checker script by running `docker compose up` in the `checker/tests` directory.

If you intend to use the return code of the tests as part of an automated pipeline CI/CD pipeline, consider running the test container as follows:

```(bash)
$> docker compose up --exit-code-from tester
```

### Debugging

When debugging, consider running a shell inside the checker container. To do so, make sure the `stdin_open:true` option in the `checker/compose.yaml` file is uncommented, and comment the `comand` line:

```
    [...]
    stdin_open: true
    #command: ["python3", "src/main.py"]
```

After running `docker compose up`, the main script will not run automatically. Instead, open a bash shell inside the container:

```(bash)
$> docker exec -it template_checker-checker-1  /bin/bash
```

The same debugging techique applies to the `tester` container.