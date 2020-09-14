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
    
def make_inp_file(sig_yield):
    # use the yield stress in the job name
    job_name = 'plate-s_yield-'+str(sig_yield)
    # create the string for the parameters.inp file
    # '\n' denotes a line break
    par_string = '*Parameter\nsig_yield={}'.format(sig_yield)
    # write to the parameters.inp file
    with open('parameters.inp','w') as f:
        f.write(par_string)
    # write to the ..._par.inp file
    with open(job_name+'_par.inp','w') as f:
        f.write(par_string)
    # run the inp file (subprocess.call)
    call('abaqus interactive input=pull_plate job='+job_name, shell=True)
    # read from the dat-file
    rf2 = evaluate_rf2(job_name)
    print('Model with sig_yield = {} MPa: rf2 = {} N'.format(sig_yield,rf2))
    return rf2

# call the function once
#make_inp_file(lines,'sig_yield',380.)

# create list of sy values
sy_list = [500., 750., 1000., 1250., 1500.]
result_dict = {}

# run the inp-files for each sy value
for sy in sy_list:
    result_dict[sy] = make_inp_file(sy)

print(result_dict)