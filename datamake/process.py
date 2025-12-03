input_file = 'input.txt'
output_file = 'output.txt'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        parts = line.split(',', 2)  # 以第2个逗号为分隔
        if len(parts) > 2:
            line = parts[0] + ',' + parts[1] + '\n'  # 仅保留前两个部分
        outfile.write(line)
