"""
Author       : FYWinds i@windis.cn
Date         : 2025-01-10 18:54:14
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2025-01-10 19:02:25
FilePath     : /cs251simulator-compiler/src/cs251simulator_compiler/model.py
"""

from pydantic import BaseModel


class Registers(BaseModel):
    registers: list[int]
    pc: int


class Memory(BaseModel):
    memory: dict[int, int]


class Instruction(BaseModel):
    pass


class ADDI(Instruction):
    AddI: tuple[int, int, int]


class Add(Instruction):
    Add: tuple[int, int, int]


class SUBI(Instruction):
    SubI: tuple[int, int, int]


class SUB(Instruction):
    Sub: tuple[int, int, int]


class LDUR(Instruction):
    Load: tuple[int, tuple[int, int]]


class STUR(Instruction):
    Store: tuple[int, tuple[int, int]]


class B(Instruction):
    B: int


class CBZ(Instruction):
    BranchZero: tuple[int, int]


class CBNZ(Instruction):
    BranchNotZero: tuple[int, int]


class Output(BaseModel):
    registers: Registers
    memory: Memory
    instructions: list[Instruction]
