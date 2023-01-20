import time
import serial
import kociemba

color_ex = {
    "U": "214325521",
    "R": "342543334",
    "F": "616456112",
    "D": "661266345",
    "L": "153631554",
    "B": "534214622",
}


class CubeSolver:
    def __init__(self, serialPort="COM5", baudRate=115200):
        self.serialPort = serialPort
        self.baudRate = baudRate
        self.SerialUSB = serial.Serial(serialPort, baudRate, timeout=0.5)
        print("-----" * 9)
        if not self.SerialUSB.is_open:
            print("cannot open {}!".format(self.serialPort))
            quit()
        print("Successfully open {}!".format(self.serialPort))
        self.SerialUSB.write("[start]".encode("utf-8"))
        print(self.detectString(self.SerialUSB))

    def run(self, color):
        start_time = time.time()
        print("-----" * 27)
        try:
            self.SerialWrite(self.get_step(self.color_switch(color)))
        except ValueError:
            print("魔方无解，颜色识别错误")
            return False
        else:
            self.SerialWrite("end")
            self.time_record(start_time)
            print("-----" * 9)
            return True

    def color_switch(self, color):
        sequence = (
            color["U"] + color["R"] + color["F"] + color["D"] + color["L"] + color["B"]
        ).lower()
        U, R, F, D, L, B = sequence[4:53:9]
        dic = {U: "U", R: "R", F: "F", D: "D", L: "L", B: "B"}
        for char in dic:
            sequence = sequence.replace(char, dic[char])
        return sequence

    def get_step(self, sequence):
        SolveSteps = kociemba.solve(sequence).lower()
        SolveSteps = SolveSteps.replace("2", "3")
        SolveSteps = SolveSteps.replace("'", "2")
        SolveSteps = SolveSteps.split(" ")
        l = len(SolveSteps)
        for i in range(l):
            if len(SolveSteps[i]) == 1:
                SolveSteps[i] = SolveSteps[i] + "1"
        print("SolveSteps:")
        print(SolveSteps)
        return self.step_switch(SolveSteps)

    def step_switch(self, Steps):
        stepNum = len(Steps)
        for k in range(stepNum):
            if Steps[k][0] == "r":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "u":
                        Steps[j] = "r" + Steps[j][1]
                    elif Steps[j][0] == "r":
                        Steps[j] = "d" + Steps[j][1]
                    elif Steps[j][0] == "d":
                        Steps[j] = "l" + Steps[j][1]
                    elif Steps[j][0] == "l":
                        Steps[j] = "u" + Steps[j][1]
            elif Steps[k][0] == "u":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "u":
                        Steps[j] = "d" + Steps[j][1]
                    elif Steps[j][0] == "r":
                        Steps[j] = "l" + Steps[j][1]
                    elif Steps[j][0] == "d":
                        Steps[j] = "u" + Steps[j][1]
                    elif Steps[j][0] == "l":
                        Steps[j] = "r" + Steps[j][1]
            elif Steps[k][0] == "l":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "u":
                        Steps[j] = "l" + Steps[j][1]
                    elif Steps[j][0] == "r":
                        Steps[j] = "u" + Steps[j][1]
                    elif Steps[j][0] == "d":
                        Steps[j] = "r" + Steps[j][1]
                    elif Steps[j][0] == "l":
                        Steps[j] = "d" + Steps[j][1]
            elif Steps[k][0] == "b":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "f":
                        Steps[j] = "b" + Steps[j][1]
                    elif Steps[j][0] == "r":
                        Steps[j] = "l" + Steps[j][1]
                    elif Steps[j][0] == "b":
                        Steps[j] = "f" + Steps[j][1]
                    elif Steps[j][0] == "l":
                        Steps[j] = "r" + Steps[j][1]
            elif Steps[k][0] in ["f", "d"]:
                None
            else:
                print("{} goes wrong, please check!".format(Steps[k][0]))
                quit()
        print("SwitchSteps:")
        print(Steps)
        return Steps

    def detectString(self, com):
        while not com.in_waiting:
            continue
        rstr = str(com.readline(), encoding="utf-8")
        if rstr[0] == "[" and rstr[-3] == "]":
            return rstr[1:-3]
        else:
            print("Please check arduino!")
            return False

    def SerialWrite(self, Steps):
        if isinstance(Steps,str):
            Steps=[Steps]
        for step in Steps:
            self.SerialUSB.write(("[" + step + "]").encode("utf-8"))
            print(step, "successfully sent!")

    def time_record(self, start_time):
        while 1:
            step = self.detectString(self.SerialUSB)
            if step == "end":
                print("还原结束，总用时:", format(time.time() - start_time, ".3f"))
                break
            print(step, "用时:", format(time.time() - start_time, ".3f"))

    def close(self):
        self.SerialUSB.write("[close]".encode("utf-8"))
        print(self.detectString(self.SerialUSB))
        self.SerialUSB.close()
        print("-----" * 9)

if __name__ == '__main__':
    test = CubeSolver()
    test.SerialWrite("c")
    time.sleep(3)
    while 1:
        if not test.run(color_ex):
            print("重新识别")
        else:
            break
    test.close()
