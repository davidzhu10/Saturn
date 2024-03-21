from typing import List
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
    
    subprocess.run("pwd")
    subprocess.run("ls")
    subprocess.run(["ls","agbenchmark_config"])
    print(task_id)

    print(code)
    code = code.replace("\\n", "\n")
    print(code)

    nb = nbf.v4.new_notebook()
    code_cell = nbf.v4.new_code_cell(source=code)
    nb.cells = [code_cell]
    
    notebook_to_write = nbf.writes(nb)
    print(notebook_to_write)

    agent.workspace.write(task_id=task_id, path=file_path, data=notebook_to_write.encode())
    
    file_name = "agbenchmark_config/workspace/" + task_id
    subprocess.run(["ls", file_name])
    full_path = file_name + "/" + file_path
    # subprocess.run(["open", full_path])
    subprocess.Popen(["jupyter", "notebook"])
    
    # counter = 0
    # while True:
    #   stdout = process.stdout.read().decode()
    #   if "is running at" in stdout:
    #     break
    #   time.sleep(0.5)
    #   counter += 1
    #   if counter > 10:
    #     print("waited too long")
    #     break
    
    time.sleep(5)
    
    url = "http://localhost:8888/notebooks/" + full_path
    print(url)
    webbrowser.open_new_tab(url)
    
    return await agent.db.create_artifact(
        task_id=task_id,
        file_name=file_path.split("/")[-1],
        relative_path=file_path,
        agent_created=True,
    )
