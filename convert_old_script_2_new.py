import os

new_folder = 'new_bat'

def parse_payload(payload):
    return list(map(lambda x:int(x, 16), payload.strip().split()))

def find_end_index(line, end):
    while line[end] != ' ' and line[end] != '>':
        end += 1

    return end

def progress(path, filename):
    with open(filename, 'r') as rf:
        lines = rf.readlines()
        with open(os.path.join(path, new_folder, filename), 'w') as wf:
            for line in lines:
                if 'write_reg' in line or 'read_reg' in line:
                    index = line.find('dsi:')
                    if index == -1:
                        continue
                    index += len('dsi:')
                    dsi = int(line[index])

                    index = line.find('cmd:')
                    if index == -1:
                        continue
                    index += len('cmd:')
                    end_index = find_end_index(line, index) #可能是' '或者是'>'直接结尾
                    print(line[index:end_index])
                    cmd = [int(line[index:end_index], 16)]
                    print(cmd)
                    num = 1
                    if 'write_reg' in line:
                        index = line.find('payload:')
                        if index != -1:
                            index += len('payload:')
                            end_index = line.find('>', index)
                            payload = parse_payload(line[index:end_index])
                            num += len(payload)
                            cmd += payload    
                            if num == 2:
                                cmd_type = '15'
                            elif num > 2:
                                cmd_type = '39'
                        else:
                            cmd_type = '05'
                        index = line.find('lp_mode:')
                        if index == -1:
                            continue
                        index += len('lp_mode:')
                        hs_mode = int(line[index])
                    elif 'read_reg' in line:
                        cmd_type = '06'
                        index = line.find('read_count:')
                        print('read')
                        if index == -1:
                            continue
                        index += len('read_count:')
                        end_index = line.find('>', index)
                        num = int(line[index:end_index], 16)
                        cmd += (num - 1) * [0]
                        hs_mode = 0
                    num_high = (num >> 8) & 0xFF
                    num_low = num & 0xFF
                    print(cmd)
                    cmd = ' '.join(map(lambda x:format(x, '0>2X'), cmd))
                    cmd = f"{cmd_type} 01 00 00 00 {format(num_high, '0>2X')} {format(num_low, '0>2X')} " + cmd
                    wf.write(f'adb shell "echo set_param_config:qcom,mdss-dsi-debug-commands dsi:{dsi} fps:60 hs_mode:{hs_mode} last_batch:1 cmd:{cmd} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg"\n')
                else:
                    wf.write(line)
try:
    os.mkdir(new_folder)
except Exception as e:
    pass
for filename in os.listdir(os.getcwd()):
    #print(os.getcwd(), filename)
    if filename.endswith('.bat'):
        # 将JSON文件添加到列表框中
        progress(os.getcwd(), filename)

# f.write(f'adb shell "echo set_param_config:{type} dsi:{screen} fps:{fps} hs_mode:{hs_mode} last_batch:{1 if i == code_segment - 1 else 0} cmd:%code_segment{i}% > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg"\n')

# adb shell mount -t debugfs none /d
# adb shell "echo write_reg:dsi:1 lp_mode:1 cmd:0xFE payload:0xC6 > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg"
# adb shell "echo read_reg:dsi:1 cmd:0x01 read_count:1 > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg"
# adb shell "cat /sys/kernel/debug/lcd-dbg/lcd_kit_dbg"
# adb shell "echo write_reg:dsi:1 lp_mode:1 cmd:0xFE payload:0x00 > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg"