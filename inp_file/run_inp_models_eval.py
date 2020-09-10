# Automizing Abaqus: Change and run inp-file 

from subprocess import call

# open input file and split string into list of strings
with open('pull_plate.inp','r') as f:
    lines = f.read().split('\n')

def evaluate_rf2(dat_file):
    # open the dat file with results in it
    with open(dat_file+'.dat','r') as f:
        lines = f.read().split('\n')
    # take the lines with reference point results
    rp_lines = []
    for line in lines:
        if line.startswith('         91 '):
            rp_lines += [line]
    # result for last frame
    res_line = rp_lines[-1]
    # split ste string and delete empty strings from list
    res_line = [i for i in res_line.split(' ') if i != '']
    # take the second from last string (RF2) and convert it to a float
    return float(res_line[-2])
    
def make_inp_file(lines,string,value):
    # copy the original lines
    lines_temp = lines[:]
    # where is the yield stress line?
    for i_line in range(len(lines_temp)):
        line = lines_temp[i_line]
        if '$'+string+'$' in line:
            lines_temp[i_line] = line.replace('$'+string+'$',str(value))
    # export to new inp file
    inp_name = 'pull_plate_'+string+'_'+str(int(value))
    with open(inp_name+'.inp','w') as f:
        f.write('\n'.join(lines_temp))
    # run the inp file (subprocess.call)
    call('abaqus interactive job='+inp_name, shell=True)
    # read from the dat-file
    rf2 = evaluate_rf2(inp_name)
    print('Model with {} = {} MPa: rf2 = {} N'.format(string,value,rf2))
    return rf2

# call the function once
#make_inp_file(lines,'sig_yield',380.)

# create list of sy values
sy_list = [500., 750., 1000., 1250., 1500.]

result_dict = {}

# run the inp-files for each sy value
for sy in sy_list:
    result_dict[sy] = make_inp_file(lines,'sig_yield',sy)

print(result_dict)