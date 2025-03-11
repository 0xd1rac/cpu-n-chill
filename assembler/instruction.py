class Instruction:
    """Base class for an instruction."""
    
    def __init__(self, opcode, operands, line_number):
        """
        :param opcode: The name of the instruction (e.g., MOV, ADD, SUB, B)
        :param operands: The list of operands for the instruction
        :param line_number: The line number in the source assembly file
        """
        self.opcode = opcode
        self.operands = operands
        self.line_number = line_number

    def encode(self, label_addresses=None, current_address=0):
        """
        Converts the assembly instruction into machine code (binary/hex) - 32-bit binary representation.

        :param label_addresses: Dictionary mapping labels to their memory addresses
        :param current_address: Memory address of the instruction being encoded
        :return: Encoded machine code (integer representation)
        """
        raise NotImplementedError("Subclasses must implement encode()")


class MoveInstruction(Instruction):
    """
    MOV destination_register, immediate_value

    Encoding Bit Layout:
      bits [31:28] = 1 (opcode indicator for MOV)
      bits [27:16] = destination register number
      bits [15:0]  = immediate value (lower 16 bits)
    """

    def __init__(self, destination_register, immediate_value, line_number):
        super().__init__("MOV", [destination_register, immediate_value], line_number)
        self.destination_register = destination_register
        self.immediate_value = immediate_value

    def encode(self, label_addresses=None, current_address=0):
        dest_reg_number = int(self.destination_register[1:])  # Convert "R<number>" to an integer
        machine_code = (1 << 28) | (dest_reg_number << 16) | (self.immediate_value & 0xFFFF)
        return machine_code


class AddInstruction(Instruction):
    """
    ADD destination_register, source_register_1, source_register_2

    Encoding:
      bits [31:28] = 2 (opcode indicator for ADD)
      bits [27:16] = destination register number
      bits [15:8]  = first source register
      bits [7:0]   = second source register
    """

    def __init__(self, destination_register, source_register_1, source_register_2, line_number):
        super().__init__("ADD", [destination_register, source_register_1, source_register_2], line_number)
        self.destination_register = destination_register
        self.source_register_1 = source_register_1
        self.source_register_2 = source_register_2

    def encode(self, label_addresses=None, current_address=0):
        dest_reg_number = int(self.destination_register[1:])
        src1_reg_number = int(self.source_register_1[1:])
        src2_reg_number = int(self.source_register_2[1:])
        machine_code = (2 << 28) | (dest_reg_number << 16) | (src1_reg_number << 8) | src2_reg_number
        return machine_code


class SubtractInstruction(Instruction):
    """
    SUB destination_register, source_register_1, source_register_2

    Encoding:
      bits [31:28] = 3 (opcode indicator for SUB)
      bits [27:16] = destination register number
      bits [15:8]  = first source register
      bits [7:0]   = second source register
    """

    def __init__(self, destination_register, source_register_1, source_register_2, line_number):
        super().__init__("SUB", [destination_register, source_register_1, source_register_2], line_number)
        self.destination_register = destination_register
        self.source_register_1 = source_register_1
        self.source_register_2 = source_register_2

    def encode(self, label_addresses=None, current_address=0):
        dest_reg_number = int(self.destination_register[1:])
        src1_reg_number = int(self.source_register_1[1:])
        src2_reg_number = int(self.source_register_2[1:])
        machine_code = (3 << 28) | (dest_reg_number << 16) | (src1_reg_number << 8) | src2_reg_number
        return machine_code


class BranchInstruction(Instruction):
    """
    B label

    Encoding:
      bits [31:28] = 4 (opcode for branch)
      bits [27:0]  = branch offset (relative to the next instruction)
    """

    def __init__(self, label, line_number):
        super().__init__("B", [label], line_number)
        self.label = label  # Target label name

    def encode(self, label_addresses=None, current_address=0):
        if label_addresses is None or self.label not in label_addresses:
            raise ValueError(f"Label '{self.label}' not found (line {self.line_number}).")

        target_address = label_addresses[self.label]
        # Compute offset in bytes (subtract current address and size of branch instruction)
        # Convert to number of instructions (assuming each instruction is 4 bytes)
        offset = (target_address - current_address - 4) // 4  
        machine_code = (4 << 28) | (offset & 0x0FFFFFFF)
        return machine_code
