#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Go Namhyeon <gnh1201@gmail.com>
# Convert oracle dump data to mois opendata scheme

def main(args):
    process_rawdata()
    return 0

def process_token(token):
    tokens = []
    if token.startswith("Y ") or token.startswith("N "):
        tokens = token.split(" ")
    else:
        tokens.append(token)
    return tokens
    
def write_to_excel(data):
    return False

def process_lines(lines):
    tablename = ""
    num_col = 0
    #len_cols = []

    # step 1
    for line in lines:
        if line.startswith("@TABLENAME"):
            x = line.split(" ")
            tablename = x[1]

        if line.startswith("--"):
            x = line.split(" ")
            num_col = len(x)
            #for a in x:
            #    len_cols.append(len(a))
            
    # print step 1
    print("=== TABLENAME: " + str(tablename) + " ===")
    print("=== NUM OF COLS: " + str(num_col) + " ===")
    #print("lengths of each column: " + str(len_cols))

    # step 2
    rows = []
    for line in lines:
        if line.startswith("--") or line.startswith("@"):
            continue

        tokens = [x.strip() for x in line.replace("\t", " ").split("  ") if x != ""]
        tokens_afterword = []
        for token in tokens:
            d = process_token(token)
            tokens_afterword.extend(d)

        rows.append(tokens_afterword)
        #print "['" + "', '".join(tokens_afterword) + "']"
    
    # step 3
    data = {}
    if len(rows) > 1:
        for i, v in enumerate(rows[0]):
            if i < len(rows[1]):
                data[v] = rows[1][i]
    
    # step 4
    for k in data:
        print(k + "\t\t" + data[k])

    # step 5: write to excel
    write_to_excel(data)

    print("")

def process_rawdata():
    f = open("data/raw_output_2.txt", 'r')
    
    lines = []
    is_buf = False

    while True:
        raw_line = f.readline()
        line = raw_line.rstrip()

        # EOF
        if not raw_line:
            break
        elif not line:
            continue

        # if end dump
        if line == "@DUMPEND":
            #print("detected @DUMPEND")
            process_lines(lines)
            lines = [] # reset lines
            is_buf = False

        # store temporary lines
        if is_buf == True:
            lines.append(line)

        # if start dump
        if line == "@DUMPSTART":
            #print("detected @DUMPSTART")
            is_buf = True

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
