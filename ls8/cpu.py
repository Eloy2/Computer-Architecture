"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[6] = 244 # stack pointer R7 is pointing to 0xF4 
        self.pc = 0
        # self.ir = self.ram_read(self.pc) # Instruction Register DID NOT WORK. WHY?
        # self.operand_a = self.ram_read(self.pc + 1) # reads next operation incase it needs it DID NOT WORK. WHY?
        # self.operand_b = self.ram_read(self.pc + 2) # reads next operation incase it needs it DID NOT WORK. WHY?

    def load(self):
        """Load a program into memory."""

        address = 0

        program = []
        # For now, we've just hardcoded a program:
        with open(sys.argv[1]) as f:
            for line in f:
                # Split the line on the comment character (#)
                line_split = line.split('#')
                # Extract the command from the split line        
                # It will be the first value in our split line
                command = line_split[0].strip()
                if command == '':
                    continue
                # specify that the number is base 10
                command_num = int(command, 2)
                program.append(command_num)

        # for i in program:
        #     print(i)
        
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
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
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        HLT = 1
        LDI = 130
        PRN = 71
        MUL = 162
        PUSH = 69
        POP = 70
        CALL= 80
        RET = 17
        ADD = 160

        running = True
        while running:
            ir = self.ram[self.pc] # Instruction Register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if ir == LDI:
                self.reg[operand_a] = operand_b # Set the value of a register to an integer
                self.pc += 3
            elif ir == PRN:
                print(self.reg[operand_a]) # Print numeric value stored in the given register
                self.pc += 2
            elif ir == HLT:
                running = False
                self.pc += 1
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == ADD:
                self.alu("ADD",operand_a, operand_b)
                self.pc += 3
            elif ir == PUSH:
                self.reg[6] -= 1 # Decrement the Stack Pointer
                self.ram_write(self.reg[6], self.reg[operand_a]) # get value in register and put it in top of stack
                self.pc += 2
            elif ir == POP:
                self.reg[operand_a] = self.ram_read(self.reg[6]) # get value in top of stack and put it in register
                self.reg[6] += 1 # Increment the Stack Pointer
                self.pc += 2
            elif ir == CALL:
                self.reg[6] -= 1 # Decrement the Stack Pointer
                self.ram_write(self.reg[6], self.pc + 2) # Write the value of the next line to return to in the code
                self.pc = self.reg[operand_a] # Set the PC to whatever is given to us in the register
            elif ir == RET:
                self.pc = self.ram_read(self.reg[6]) # Pop the top of the stack and set the PC to the value of what was popped
                self.reg[6] += 1 # Increment the Stack Pointer


