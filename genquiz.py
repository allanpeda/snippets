#!/usr/bin/env python3

import sys
import json
import re

# print(sys.argv[1])

def main(question_file):
    raw_question_array = read_questions(question_file)
    question_array = chunk_questions(raw_question_array)
    json_array= []
    for qa_elem in question_array:
        json_array.append(jsonify_question(qa_elem))
    print(json.dumps(json_array))
    return

def jsonify_question(qchunk):
    jsq = {'question': None,
           'type' : None,
           'answers' : [] }
    correct_count = 0
    # use predefined schema which calls selections "answers"
    answers = []
    if 'q' in qchunk:
        jsq['question'] = re.sub(r'^\d+ +', '', qchunk['q'])
    if 'c' in qchunk:
        for sel in qchunk['c']:
            # this still has leading hyphen
            raw_answer = re.split(r"[\|\^]", sel)[0]
            selentry = {
                'answer'  : re.sub(r'^- +', '', raw_answer),
                'correct' : '???',
                'feedback' : '???'
            }
            if '|' in sel:
                selentry['correct'] = True
                selentry['feedback'] = sel.split('|', 1)[1]
                correct_count += 1
            if '^' in sel:
                selentry['correct'] = False
                selentry['feedback'] = sel.split('^', 1)[1]
            answers.append(selentry)
    if correct_count > 1:
        jsq['type'] = 'many_choice'
    elif correct_count == 1:
        jsq['type'] = 'multiple_choice'
    jsq['answers'] = answers
    return jsq

def read_questions(question_file):
    raw_question_array = []
    with open(question_file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            raw_question_array.append(line.strip())
    return(raw_question_array)

def chunk_questions(raw_question_array):
    line_ndx = 0
    qchoice_list = []
    while line_ndx < len(raw_question_array):
        buf = raw_question_array[line_ndx]
        # if we are at first line or prior line is blank
        # then we are in a new qchoice
        if ( line_ndx == 0
             or len( raw_question_array[line_ndx-1] ) == 0
             or raw_question_array[line_ndx-1].isspace() ):
            qc = {'q': buf, 'c': [] }
        if( len(buf) >= 1 and buf[0] == '-' ):
            qc['c'].append(buf)
        if( len( raw_question_array[line_ndx] ) == 0
            or raw_question_array[line_ndx].isspace() ):
            qchoice_list.append(qc)
        line_ndx += 1
    return(qchoice_list)

if __name__ == '__main__':
    main(sys.argv[1])

# 100 What is not a major category of computer crime?
# - Military installation attack|Correct; this is not a category, though a military intelligence attack is.
# - Business attack^This is one of seven categories
# - Grudge attack^This is one of seven categories
# - Terrorist attack^This is one of seven categories
