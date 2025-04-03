from cmath import inf

def judgeTypeHead(codes):
    list = ['06', '05', '15', '39']
    for code in codes:
        if code[0] not in list:
            return False

    return True

def deleteComment(lines):
    ret = []
    for line in lines:
        line = line.split('//')
        ret.append(line[0])

    return ret

# 这里是不是有漏洞？ hex最末尾是'F'，不是'z'，fix me
def isHexChar(ch):
    return ch.isdigit() or (ch >= 'A' and ch <= 'F')

def parseCodeHex(lines):
    ret = []
    letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    for line in lines:
        index = 0
        if "DELAY" in line: # 这段代码在处理delay
            bigOne = inf
            for ch in letters[0:10]:
                a = line.find(ch, index)
                bigOne = min(bigOne, a if a != -1 else bigOne)
            myDelay = findNext(line, bigOne)
            if ret and ret[-1]:
                ret[-1][-2] = myDelay
            continue
        
        tmp = []
        while line.find('0X', index) != -1:
            index = line.find('0X', index) #这里怎么优化一下，find了两次
            # 修复了0x后面只有一位数的问题
            if index + 4 <= len(line):
                s = line[index + 2 : index + 4] if isHexChar(line[index + 3]) else line[index + 2 : index + 3]
            elif index + 3 <= len(line):
                s = line[index + 2 : index + 3]
            else:
                continue
            s = format(int(s, base=16), '0>2X')
            tmp.append(s)
            index += 4

        if tmp: #修复了空行也有东西输出的问题
            tmp.append("00") # 倒数第二个是延时
            tmp.append('read' if 'REGR' in line else 'write')
            ret.append(tmp)

    return ret

def findNext(line, bigOne):
    num = 0
    #print(bigOne)
    while bigOne < len(line) and line[bigOne].isdigit():
        num *= 10
        num += int(line[bigOne])
        bigOne += 1

    return format(num, '0>2X')

def parseCode(lines):
    ret = []
    letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    for line in lines:
        index = 0
        if "DELAY" in line: # 这段代码在处理delay
            bigOne = inf
            for ch in letters[0:10]:
                a = line.find(ch, index)
                bigOne = min(bigOne, a if a != -1 else bigOne)
            myDelay = findNext(line, bigOne)
            if ret and ret[-1]:
                ret[-1][-2] = myDelay
            continue
        tmp = []
        while any(line.find(ch, index) != -1 for ch in letters):
            #找到第一个十六进制数
            bigOne = inf
            for ch in letters:
                a = line.find(ch, index)
                bigOne = min(bigOne, a if a != -1 else bigOne)
            index = bigOne
            # 场景1：REGR(0A) 会识别到 'E'，从而识别到'EG'，后面逻辑无法转换为十六进制数
            if index + 1 < len(line) and line[index + 1] not in letters:
                index += 2
                continue
            # 修复了0x后面只有一位数的问题
            if index + 2 <= len(line):
                s = line[index : index + 2] if isHexChar(line[index + 1]) else line[index : index + 1]
            elif index + 1 <= len(line):
                s = line[index : index + 1]
            else:
                continue
            s = format(int(s, base=16), '0>2X')
            tmp.append(s)
            index += 2

        if tmp: #修复了空行也有东西输出的问题
            tmp.append("00") # 倒数第二个是延时
            tmp.append('read' if 'REGR' in line else 'write')
            ret.append(tmp)

    return ret

def generateResult(codes, isTypeHead):
    ret = ""
    for code in codes:
        # code is like ['15', '01', '02', '00'], the last data is delay time
        #print('hcc', code)
        typeHead = None
        if isTypeHead:
            typeHead = code[0]
            del code[0]
        myDelay = code[-2]
        del code[-2]
        read_or_write = code[-1]
        del code[-1]
        type = '39' if len(code) > 2 else '15' if len(code) == 2 else '05'
        # 场景1：REGR(0A) -> 06 01 00 00 00 00 01 0A
        # 场景2：06 0A -> 06 01 00 00 00 00 01 0A
        if read_or_write == "read" or (isTypeHead and typeHead == '06'):
            type = '06'
        cntHigh = len(code) >> 8
        cntLow = len(code) & 0xFF
        code.insert(0, format(cntLow, '0>2X'))
        code.insert(0, format(cntHigh, '0>2X')) #右对齐，补全0
        s = " ".join(code)
        s = type + " 01 00 00 " + myDelay + " " + s + "\n"
        ret += s
    return ret

def lines2codes(lines):
    #全部变成大写
    lines = map(str.upper, lines)
    #print(lines)
    #删除注释后面的东西
    lines = deleteComment(lines)
    #判断有没有 0x
    hexHead = any('0X' in line for line in lines)
    if hexHead:
        codes = parseCodeHex(lines)
    else:
        codes = parseCode(lines)
    typeHead = judgeTypeHead(codes)
    codes = generateResult(codes, typeHead)
    return codes

def process(path):
    try:
        with open(f"{path}test.txt", 'r', encoding="utf-8") as f1:
            lines = f1.readlines()
            codes = lines2codes(lines)
            dtsi2debug(codes)
            dtsi2w6(codes)
            with open(f"{path}out.txt", 'w') as f2:
                f2.write(codes)
    except FileNotFoundError:
        print(f"{path}text.txt is not found\n")
        return False

    return True

testFilePath = './test case/test'
testFileName = 'text.txt'
expectedFileName = 'expectedResult.txt'
outFileName = 'out.txt'

# 利用命令判断有多少个test文件夹, fix me
def test():
    for i in range(1, 10):
        filePath = testFilePath + str(i) +'/'
        # Can not find this file 
        if not process(filePath):
            break

        with open(f"{filePath}{expectedFileName}", 'r') as f1:
            with open (f"{filePath}{outFileName}", 'r') as f2:
                a1 = f1.readlines()
                a2 = f2.readlines()
                if len(a1) != len(a2):
                    print(f"file{i} length is not the same")
                    return
                for j in range(len(a1)):
                    if a1[j] != a2[j]:
                        print(f"file{i} differ on line{j + 1}")
                        return

        print(f"file{i} are the same as each other")  

def dtsi2debug(codes:str):
    """
    把整个dtsi文本转化成debug格式的文本
    """
    lines = codes.split('\n')
    ret = ""
    for line in lines:
        line = line.split()
        if line:
            delayTime = int(line[4], base=16)
            line = line[7:]
            n = len(line)
            ret += f'adb shell "echo write_reg:dsi:0 lp_mode:1 cmd:0x' + line[0] + " "
            if n > 1:
                ret += "payload:"
                for i in range(1,len(line)):
                    ret += f"0x{line[i]}" + " "
            ret += '> /sys/kernel/debug/lcd-dbg/lcd_kit_dbg"'
            ret += '\n'
            if delayTime:
                ret += f"adb shell sleep {delayTime / 1000}s\n"
    #print(ret)
    return ret

def dtsi2w6(codes:str):
    """
    把整个dtsi文本转化成w6g治具格式的文本
    """
    lines = codes.split('\n')
    ret = ""
    for line in lines:
        line = line.split()
        if line:
            delayTime = int(line[4], base=16)
            line = line[7:]
            n = len(line)
            ret += "REGS.WRITE(0, 0x39"
            for word in line:
                ret += ", 0x" + word
            ret += '\n'
            if delayTime:
                ret += f"TIME.DELAY({delayTime})\n"
            
    #print(ret)
    return ret

if __name__ == '__main__':
    print("Modify original file name to test.txt' and run 'run.bat', the result is saved as 'out.txt'")
    print("Any question please contact with me h00018334")
    process('./')
    test() # 写了测试用例，修改代码后应该让全部测试用例通过，如果通不过，就删除该测试用例 :)