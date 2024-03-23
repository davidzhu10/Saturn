import subprocess
import webbrowser
import time

from ..registry import action
import nbformat as nbf

@action(
    name="write_jupyter_notebook",
    description="Write code to a jupyter notebook",
    parameters=[
        {
            "name": "file_path",
            "description": "Path to the jupyter notebook",
            "type": "string",
            "required": True,
        },
        {
            "name": "code",
            "description": "Code to write to the jupyter notebook",
            "type": "string",
            "required": True,
        },
    ],
    output_type="None",
)
async def write_jupyter_notebook(agent, task_id: str, file_path: str, code: str):
    """
    Write code to a jupyter notebook
    """

    # reformat \\n into \n
    code = code.replace("\\n", "\n")

    nb = nbf.v4.new_notebook()
    code_cell = nbf.v4.new_code_cell(source=code)
    nb.cells = [code_cell]
    
    notebook_to_write = nbf.writes(nb)

    # create the jupyter notebook and write the contents
    agent.workspace.write(task_id=task_id, path=file_path, data=notebook_to_write.encode())
    
    file_path_prefix = "agbenchmark_config/workspace/" + task_id
    full_path = file_path_prefix + "/" + file_path
    
    # execute the "jupyter notebook" command
    subprocess.Popen(["jupyter", "notebook"])
    
    # hacky, sleep for 5 seconds to allow time for the jupyter notebook command to execute
    time.sleep(5)
    
    url = "http://localhost:8888/notebooks/" + full_path

    # open the actual .ipynb notebook itself
    webbrowser.open_new_tab(url)
    
    return await agent.db.create_artifact(
        task_id=task_id,
        file_name=file_path.split("/")[-1],
        relative_path=file_path,
        agent_created=True,
    )
