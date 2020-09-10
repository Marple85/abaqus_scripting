# Automizing Abaqus: Change and run inp-file 

from subprocess import call

# open input file and split string into list of strings
with open('pull_plate.inp','r') as f:
    lines = f.read().split('\n')

def make_inp_file(lines,str_line,val_line):
    # copy the original lines
    lines_temp = lines[:]
    # where is the yield stress line?
    for i_line in range(len(lines_temp)):
        line = lines_temp[i_line]
        if '$'+str_line+'$' in line:
            print(line)
            print('found!')
            lines_temp[i_line] = line.replace('$'+str_line+'$',str(val_line))
    print(lines_temp)
    # export to new inp file
    inp_name = 'pull_plate_'+str_line+'_'+str(int(val_line))
    with open(inp_name+'.inp','w') as f:
        f.write('\n'.join(lines_temp))
    # run the inp file (subprocess.call)
    call('abaqus interactive job='+inp_name, shell=True)
    return inp_name

# call the function once
make_inp_file(lines,'sig_yield',380.)

# create list of sy values
sy_list = [500., 750., 1000., 1250., 1500.]

# run the inp-files for each sy value
for sy in sy_list:
    make_inp_file(lines,'sig_yield',sy)