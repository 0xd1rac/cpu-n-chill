class Instruction:
    """Base class for an instruction"""
    def __init__(self, mnemonic, operands, line_num):
        self.mnemonic = mnemonic # opcode or the name of the assembly instruction, eg: MOV, ADD, SUB, JUMP
        self.operands = operands # arguments passed to the instruction,eg: in ADD R1, R2, the operands are R1 and R2
        self.line_num = line_num # line the src assembly file where this instruction appears

    """
    function to convert the assembly instruction to machine code (binary or hex repr)
    """
    def encode(self, label_addresses=None, current_address=0):
        """
        label_address: dictionary that stores labels and their corresponding mem addr
        current_address: current memmory address of the instruction being encoded
        """
        raise NotImplementedError("Subclasses must implement encode()")

class MovInstruction(Instruction):
    """
    MOV Rd, #imm
    Simplified encoding:
      bits [31:28] = 1 (opcode indicator for MOV)
      bits [27:16] = destination register number (Rd)
      bits [15:0]  = immediate value (lower 16 bits)
    """
    def __init__(self, rd, imm, line_num):
        super().__init__("MOV", [rd, imm], line_num)
        self.rd = rd       # e.g., "R0", "R1", etc.
        self.imm = imm     # integer value
    
    def encoder(self, label_address=None, current_address=0):
        rd_num = int(self.rd[1:])  # assume register format "R<number>"
        code = (1 << 28) | (rd_num << 16) | (self.imm & 0xFFFF)
        return code 
    
class AddInstruction(Instruction):
    """
    ADD Rd, Rn, Rm
    Simplified encoding:
      bits [31:28] = 2 (opcode indicator for ADD)
      bits [27:16] = destination register number (Rd)
      bits [15:8]  = first source register (Rn)
      bits [7:0]   = second source register (Rm)
    """
    def __init__(self, rd, rn, rm, line_num):
        super().__init__("ADD", [rd, rn, rm], line_num)
        self.rd = rd
        self.rn = rn
        self.rm = rm

    def encode(self, label_addresses=None, current_address=0):
        rd_num = int(self.rd[1:])
        rn_num = int(self.rn[1:])
        rm_num = int(self.rm[1:])
        code = (2 << 28) | (rd_num << 16) | (rn_num << 8) | rm_num
        return code

class SubInstruction(Instruction):
    """
    SUB Rd, Rn, Rm
    Simplified encoding:
      bits [31:28] = 3 (opcode indicator for SUB)
      bits [27:16] = destination register number (Rd)
      bits [15:8]  = first source register (Rn)
      bits [7:0]   = second source register (Rm)
    """
    def __init__(self, rd, rn, rm, line_num):
        super().__init__("SUB", [rd, rn, rm], line_num)
        self.rd = rd
        self.rn = rn
        self.rm = rm

    def encode(self, label_addresses=None, current_address=0):
        rd_num = int(self.rd[1:])
        rn_num = int(self.rn[1:])
        rm_num = int(self.rm[1:])
        code = (3 << 28) | (rd_num << 16) | (rn_num << 8) | rm_num
        return code
    
class BranchInstruction(Instruction):
    """
    B label
    Simplified encoding for branch:
      bits [31:28] = 4 (opcode for branch)
      bits [27:0]  = branch offset (in number of instructions, relative to next instruction)
    """
    def __init__(self, label, line_num):
        super().__init__("B", [label], line_num)
        self.label = label  # target label name

    def encode(self, label_addresses=None, current_address=0):
        if label_addresses is None or self.label not in label_addresses:
            raise ValueError(f"Label '{self.label}' not found (line {self.line_num}).")
        target_address = label_addresses[self.label]
        # Compute offset in bytes; subtract current_address and the size of the branch instruction (4 bytes)
        # Then convert to number of instructions (each 4 bytes)
        offset = (target_address - current_address - 4) // 4  
        code = (4 << 28) | (offset & 0x0FFFFFFF)
        return code