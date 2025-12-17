# Camera Ready Template Conformance Checker 
## CBSoft'26 Proceedings Co-Chairs

W.i.P.

Tooling made to ease the manual validation of the camera ready papers accepted at the CBSoft symposia and workshops, responsible for checking whether the papers conform to the template expeted by the proceedings team.

### Installation

The script assumes you have access to `docker-compose` or an alternative container orchestration framework (such as `podman`). 

### Running

Run the script by running `docker compose up` in the `checker` directory.

#### Debugging

When debugging, consider running a shell inside the checker container. To do so, make sure the `stdin_open:true` option in the `checker/compose.yaml` file is uncommented, and comment the `comand` line:

```
    [...]
    stdin_open: true
    #command: ["python3", "src/main.py"]
```

After running `docker compose up`, the main script will not run automatically. Instead, open a bash shell inside the container:

```(bash)
docker exec -it template_checker-checker-1  /bin/bash
```