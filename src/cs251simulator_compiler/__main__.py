"""
Author       : FYWinds i@windis.cn
Date         : 2025-01-10 18:28:09
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2025-01-10 19:25:50
FilePath     : /cs251simulator-compiler/src/cs251simulator_compiler/__main__.py
"""

import json
from pathlib import Path
from typing import Annotated

import typer

from .parser import parser as parser  # type: ignore

app = typer.Typer()


def _parse(file: Path) -> tuple:
    ast = None
    with open(file, "r") as f:
        ast = parser.parse(f.read())
    if ast is None:
        typer.echo("Parse failed.")
        raise typer.Exit(1)
    return ast


@app.command("parse")
def parse(file: Path) -> None:
    ast = _parse(file)
    typer.echo(ast)


op_map = {
    "ADDI": "AddI",
    "ADD": "Add",
    "SUBI": "SubI",
    "SUB": "Sub",
    "LDUR": "Load",
    "STUR": "Store",
    "B": "Branch",
    "CBZ": "BranchZero",
    "CBNZ": "BranchNotZero",
}


@app.command(
    "compile", help="Compile the assembly file to cs251simulator loadable json file."
)
def compile(
    file: Annotated[Path, typer.Argument(help="The assembly file.")],
    out: Annotated[Path | None, typer.Argument(help="The output file.")] = None,
    emit_register_setup: bool = True,
    emit_memory_setup: bool = True,
    pc: Annotated[int, typer.Option(help="The initial program counter.")] = 0,
) -> None:
    ast = _parse(file)
    if out is None:
        out = file.with_suffix(".json")

    memory = {}
    registers = {}
    instructions = {}

    for item in ast:
        if isinstance(item, tuple):
            match item[0]:
                case "memory_section":
                    if emit_memory_setup:
                        for _, mem, v in item[1]:
                            memory[mem // 8] = v
                case "register_section":
                    if emit_register_setup:
                        for _, reg, v in item[1]:
                            registers[reg] = v
                case "instruction_section":
                    for _, op, args in item[1]:
                        match len(args):
                            case 3:
                                instructions[op] = args
                            case 2:
                                if op in {"LDUR", "STUR"}:
                                    reg: int = args[0]  # type: ignore
                                    _, mem_reg, mem_offset = args[1]
                                    instructions[op] = [reg, [mem_reg, mem_offset]]
                                else:
                                    instructions[op] = args
                            case 1:
                                instructions[op] = args[0]

    output = {
        "registers": {"registers": [registers.get(i, 0) for i in range(31)], "pc": pc},
        "memory": {"memory": memory},
        "instructions": [{op_map[inst]: args} for inst, args in instructions.items()],
    }
    with open(out, "w") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    app()
