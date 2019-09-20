"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # make a 256 byte ram
        self.ram = [0] * 256

        #  make the register R0 - R8
        self.reg = [0] * 8

        # make a pc
        self.pc = self.reg[0]

        self.fl = [0] * 8

        # self.commands = {
        #     0b00000001: self.hlt,
        #     0b10000010: self.ldi,
        #     0b01000111: self.prn,
        #     0b10100010: self.mul
        #     0b10100111: self.cmp,
        #     0b01010100: self.jmp,
        #     0b01010101: self.jeq,
        #     0b01010110: self.jne
        # }

    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(program) as f:
            for line in f:
                comment_split = line.split('#')
                number = comment_split[0].strip()

                try:
                    self.ram_write(int(number, 2), address)
                    address += 1
                except ValueError:
                    pass

        for instruction in program:
                self.ram[address] = instruction
                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    # def hlt(self, operand_a, operand_b):
    #     return (0, False)

    # def ldi(self, operand_a, operand_b):
    #     self.reg[operand_a] = operand_b
    #     return (3, True)

    # def prn(self, operand_a, operand_b):
    #     print(self.reg[operand_a])
    #     return (2, True)

    # def mul(self, operand_a, operand_b):
    #     self.alu("MUL", operand_a, operand_b)
    #     return (3, True)


    def alu(self, op, operand_a, operand_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[operand_a] += self.reg[operand_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[operand_a] = (self.reg[operand_a] * self.reg[operand_b])

        elif op == "CMP":
            
            if self.reg[operand_a] < self.reg[operand_b]:
                self.fl[-3] = 1
            elif self.reg[operand_a] > self.reg[operand_b]:
                self.fl[-2] = 1
            elif self.reg[operand_a] == self.reg[operand_b]:
                self.fl[-1] = 1

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

    def run(self):
        """Run the CPU."""
        running = True

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        while running:
            
            ir = self.ram[self.pc]
        
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # register = self.reg[operand_a]

        #     try:
        #         operation_output = self.commands[ir](operand_a, operand_b)
        #         running = operation_output[1]
        #         self.pc += operation_output[0]

            if ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            
            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            
            elif ir == JMP:
                self.pc = self.reg[operand_a]
            
            elif ir == JEQ:
                if self.fl[-1] == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif ir == JNE:
                if self.fl[-1] == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif ir == HLT:
                running = False
    
            else:
                print(f"Unknown command: {ir}")
                sys.exit()
