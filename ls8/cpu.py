"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # register - 256 bytes of memory & 8 general purpose registers
        self.pc = 0
        self.running = True
        self.ram = {0: 0, 
                    1: 0, 
                    2: 0, 
                    3: 0,
                    4: 0, 
                    5: 0, 
                    6: 0, 
                    7: 0}
        self.register = {0: 0, 
                         1: 0, 
                         2: 0, 
                         3: 0,
                         4: 0, 
                         5: 0, 
                         6: 0, 
                         7: 0}

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            "10000010", # LDI R0,8
            "00000000",
            "00001000",
            "01000111", # PRN R0
            "00000000",
            "00000001", # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def binary_string_to_decimal(self, binary_string):
        value = 0

        # Add place values
        value += int(binary_string[7])
        value += int(binary_string[6]) * 2
        value += int(binary_string[5]) * 4
        value += int(binary_string[4]) * 8
        value += int(binary_string[3]) * 16
        value += int(binary_string[2]) * 32
        value += int(binary_string[1]) * 64
        value += int(binary_string[0]) * 128

        return value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        """
        Accepts a RAM address and returns the value stored there
        """
        return str(self.ram[address])

    def ram_write(self, value, address):
        """
        Accepts a value and RAM address, then overwrites the value at that address
        """
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        # Run until it halts
        while self.running:

            # Find the number of arguments
            # Looks like from source files, I'll get strings,
            # but hard-coded program has real binary values
            command = self.ram_read(self.pc)

            # Instantiate Instruction Register
            ir = [command]

            # Do we need more arguments from memory?
            if command[:2] == "00":
                # No arguments are needed
                # Just change the PC
                self.pc += 1
            elif command[:2] == "01":
                # One argument needed
                operand_a = self.ram_read(self.pc + 1)
                # Add to ir
                ir.append(operand_a)
                # Change the PC
                self.pc += 2
            elif command[:2] == "10":
                # Two arguments needed
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                # Add to ir
                ir.append(operand_a)
                ir.append(operand_b)
                # Change the PC
                self.pc += 3

            # Now everything for this operation is in ir

            # Execute Instructions

            # HLT
            if ir[0] == "00000001":
                # Change running to false
                self.running = False

            # LDI
            elif ir[0] == "10000010":
                # Get the vars
                register_address_binary_string = ir[1]
                value_binary_string = ir[2]

                # Convert vars to decimal value
                register_address = self.binary_string_to_decimal(register_address_binary_string)
                value = self.binary_string_to_decimal(value_binary_string)

                # Set register at address to specified value
                self.register[register_address] = value

            # PRN
            elif ir[0] == "01000111":
                # Get the var
                register_address_binary_string = ir[1]

                # Convert vars to decimal value
                register_address = self.binary_string_to_decimal(register_address_binary_string)

                # Set register at address to specified value
                print(self.register[register_address])