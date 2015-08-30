
import random
import os

# generates code coverage files from source file
# n_files - number of files to be generated
# src - source file path
# dst - destination folder in which the code coverage files to be stored
# probabilities - list of probabilities. 0.05 means 5 percent of lines will be covered
def generate_coverage_files(n_files,probabilities,src,dst):
    src_file_ptr = open(src_file)
    src = src_file_ptr.read()
    src_file_ptr.close()
    for x in range(n_files):
        cvsrc=''
        for line in src.split('\n'):
            coverage = 0
            p = probabilities[x%len(probabilities)]
            r= random.random()
            if r <p:
                coverage = 1
            if line.strip() !='':
                cvsrc+=str(coverage)+line+"\n"
        filename=str(x+1)+'_coverage_'+str(p*100)+'_percent.txt'
        filep = open(dst+'/'+filename, "w")
        filep.write(cvsrc)
        

# iterates over all the files in this directory and subdirectory and creates a list
# directory - the directory to iterate
# file_extension - the coverage file extension like .txt or .log
def get_all_code_coverage_files(directory,file_extension):
    filepaths =[]
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(file_extension):
                filepaths.append(filepath)
    return filepaths

# get a dictionary with key: coverage file path and value : list of OR value and sum of ones like [16,1] or [15,4]
# coverage_directory - dir path containing coverage files
# extension - file extension of coverage files
def get_coverage_detail(coverage_directory,extension):
    filepaths = get_all_code_coverage_files(coverage_directory,extension)
    coverage_dict={}
    total_ornum = 0
    for filepath in filepaths:
        file_ornum=0
        sum_of_ones = 0
        file_ptr = open(filepath)
        filestr = file_ptr.read()
        file_ptr.close()
        line_counter = 0
        for line in filestr.split('\n'):
            if line.strip()!='':
                cov = int(line[0]) # first character of each nonempty line is coverage digit
                file_ornum+=cov*2**line_counter
                sum_of_ones+=cov
                line_counter+=1
        total_ornum|=file_ornum
        coverage_dict[filepath] = [file_ornum,sum_of_ones]
    return coverage_dict,total_ornum

# gets the file with maximum coverage ( maximum number of ones in the file)
# coverage_dict - a dictionary with key: coverage file path and value : list of OR value and sum of ones like [16,1] or [15,4]
def get_file_with_maximum_coverage(coverage_dict):
    maxval,filepath = 0,''
    for key,value in coverage_dict.iteritems():
        if value[1] > maxval:
            maxval = value[1]
            filepath=key
    return filepath

# for a given number get the number of set-bits eg. 16 gives 1, 15 gives 4, 10 gives 2
def get_number_ones(n):
    sum_ones = 0
    while n:
        sum_ones += n%2
        n=n/2
    return sum_ones

# gives the minimum set of test case files the same coverage as all the test case files
# coverage_directory - dir path containing coverage files
# extension - file extension of coverage files 
def get_test_case_files(coverage_dir,extension):
    coverage_dict,total_ornum = get_coverage_detail(coverage_dir,extension)
    filepath = get_file_with_maximum_coverage(coverage_dict)
    test_files = []
    test_files.append(filepath)
    
    # cumul_ornum - cumulative OR value of all coverage
    # cum_sum_ones - sum of ones the cumlative OR value cumul_ornum
    cumul_ornum,cum_sum_ones = coverage_dict.pop(filepath)
    
    # loop until cumulative bitwise OR value equals total bitwise OR value
    while cumul_ornum!=total_ornum:
        maxdiff = 0
        maxdiff_file = ''
        
        for  key,val in coverage_dict.iteritems():
            diff = get_number_ones(val[0]|cumul_ornum) - cum_sum_ones
            if diff > maxdiff:
                maxdiff_file = key
                maxdiff = diff
                
        # maxdiff_file - file which has the maximum difference in the sum of ones
        or_num,sum_ones = coverage_dict.pop(maxdiff_file)
        
        # update the cumulative OR value with the tes case file for which the maxmimum sum_of_ones difference is present
        cumul_ornum = cumul_ornum|or_num
        
        # update the cumulative sum_of_ones
        cum_sum_ones = get_number_ones(cumul_ornum)
        
        # add the test file to the list
        test_files.append(maxdiff_file)
        #print maxdiff_file
        if cumul_ornum == total_ornum:
            return test_files
        

probabilities = [0.3,0.2,0.1,0.01]
no_of_files = 500
src_file = '/Users/sathish/Desktop/cov/src.txt'
dst_path = '/Users/sathish/Desktop/cov/coverage'
generate_coverage_files(no_of_files,  probabilities,  src_file,  dst_path)  
test_files = get_test_case_files(dst_path,'.txt')

for test_file in test_files:
    print test_file