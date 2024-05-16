MCP9808_I2CADDR_DEFAULT = 0x18
MCP9808_REG_AMBIENT_TEMP = 0x05

class MCP9808:
    def __init__(self, i2c, addr=MCP9808_I2CADDR_DEFAULT):
        self.i2c = i2c
        self.addr = addr

    def read_temp_c(self):
        temp = self.i2c.readfrom_mem(self.addr, 0x05, 2)
        temp_val = temp[0] << 8 | temp[1]
        temperature = temp_val & 0x0FFF
        temperature /= 16.0
        if temp_val & 0x1000:
            temperature -= 256.0
        return temperature

    def read_temp_f(self):
        temp_c = self.read_temp_c()
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f
