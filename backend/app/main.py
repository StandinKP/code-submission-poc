import subprocess
from fastapi import FastAPI
import os
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote
from pydantic import BaseModel

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def handle_python_submission(code: str) -> str:
    """
    Handles the submission of a python script.
    """
    print("Code Initial>>>>>>>>", code)
    code = (
        unquote(code)
        .replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace("\\r", "\r")
        .replace('\\"', '"')
        .replace("\\'", "'")
        .replace("\\", "")
        .replace("\\\\", "\\")
    )
    print("Code After Replace>>>>>>>>", code)
    p = Path("temp/")
    p.mkdir(parents=True, exist_ok=True)
    fn = "test.py"  # I don't know what is your fn
    filepath = p / fn
    # Create a temporary file to store the code
    with open(filepath, "w") as f:
        f.write("from typing import *\n")
        f.write(code)
        f.write("\n")
        # f.write("s = Solution()\n")
        # f.write("res = s.twoSum(nums=[2, 7, 11, 15], target=9)\n")
        # f.write("print(res)\n")

        subprocess.run(["black", "--quiet", fn], cwd=p)

    # Run the code
    # output = subprocess.check_output(["python3", filepath])
    # print("Output>>>>>>>>", output)
    # output = output.decode("utf-8")
    with open(filepath, "r") as f:
        script = f.read()
        print("Script>>>>>>>>", script)
        try:
            output = exec(script)
            print("Output>>>>>>>>", output)
        except Exception as e:
            output = str(e)
            print("Output>>>>>>>>", output)

    # Delete the temporary file
    # os.remove(filepath)

    return output


def handle_c_submission(code: str) -> str:
    """
    Handles the submission of a C script.
    """
    code = (
        code.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace("\\r", "\r")
        .replace('\\"', '"')
        .replace("\\'", "'")
        .replace("\\", "")
        .replace("\\\\", "\\")
    )
    p = Path("temp/")
    p.mkdir(parents=True, exist_ok=True)
    fn = "test.c"  # I don't know what is your fn
    filepath = p / fn
    # Create a temporary file to store the code
    with open(filepath, "w") as f:
        f.write("#include <stdlib.h>\n")
        f.write("#include <stdio.h>\n")
        f.write("\n")
        f.write(code)
        f.write("\n")
        f.write(
            """
        int main()
{
    int resSize = 5;
    int *res = twoSum(
        (int[]){2, 7, 11, 15},
        4,
        9,
        &resSize

    );
    printf("%d %d\n", res[0], res[1]);
    return 0;
}
        """
        )

        subprocess.run(["gcc", fn], cwd=p)

    # Run the code
    output = subprocess.check_output(["a.out"], cwd=p)
    output = output.decode("utf-8")

    # Delete the temporary file
    # os.remove(filepath)
    # os.remove("a.out")

    return output


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Code(BaseModel):
    typed_code: str
    language: str


@app.post("/accept")
async def accept(code: Code):
    typed_code, language = code.typed_code, code.language
    language_functions = {
        "python": handle_python_submission,
        "c": handle_c_submission,
    }
    return (
        language_functions[language](typed_code)
        if language in language_functions
        else {"error": "Language not supported"}
    )


@app.post("/run")
async def run():
    p = Path("temp/")
    p.mkdir(parents=True, exist_ok=True)
    fn = "test.py"
    filepath = p / fn
    # os.system(f"python3 {filepath}")
    result = subprocess.run(["python3", filepath], stdout=subprocess.PIPE)
    print("Result>>>>>>>>", result.stdout.decode("utf-8"))
    return {"message": result.stdout.decode("utf-8").strip()}
