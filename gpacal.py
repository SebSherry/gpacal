#Imports
from __future__ import division

import sys
import copy
import getopt
from collections import Counter

OPTIONS = [4,5,6,7] #The grade OPTIONS (We assume no failures)
MIN_GRADE = 4 #Lowest possible grade (We assume no failures)

#Calculate GPA
def calc_gpa(grades):
    """
        Calculates the GPA of a set of grades

        grades : list of ints used as scores to calculate a gpa score
    """
    return sum(grades) / len(grades) 

def calc_matrix(grades, subjects):
    """
        Calculates a matrix all the possible gpas based on previous semester results and all possible results for this semester

        grades : list of int scores for all subjects done up to this point
        subjects : amount of units being completed this semester
    """
    #Setup counting and base arrays
    base = [MIN_GRADE for x in range(subjects)]
    counts = copy.deepcopy(base)

    #Generate matrix
    matrix = []
    calc = True
    while calc:
        #create row and calculate GPA
        row = {"Scores" : copy.deepcopy(counts), "Total" : calc_gpa(grades+counts)}
        
        #add row to matrix
        matrix.append(row)

        #exit
        if counts == [7 for x in range(subjects)]:
            break
        
        #update counts
        counts[-1] += 1
        for i in range(len(counts)-1,-1,-1):
            if counts[i] == 8:
                if base[i] == 7 and i-1 >= 0:
                    base[i] = base[i-1] + 1
                else:
                    base[i] += 1

                counts[i] = base[i]
                if i-1 >= 0:
                    counts[i-1] += 1

    return matrix

def print_matrix(matrix, subjects):
    """
        Prints the matrix as a table

        matrix : matrix to print
        subjects : amount of units being completed this semester
    """
    #create format string 
    fmtstr = "{0:3} " #row number 
    for i in range(subjects):
        fmtstr += "{"
        fmtstr += "{}:4".format(i+1)
        fmtstr += "} "
    
    #Add GPA to format string
    fmtstr += "{"
    fmtstr += "{}:.3f".format(subjects+1)
    fmtstr += "}"
    
    #Print table header
    header = " " * 4
    for i in range(subjects):
        header += "SUB{} ".format(i+1)

    header += "GPA"
    print(header)
            
    #Print matrix 
    for i in range(len(matrix)):
        args = [i+1]
        args += matrix[i]["Scores"]
        args.append(matrix[i]["Total"]) 
        print(fmtstr.format(*args))

def calc_stats(gpas):
    """
        Calculates various basic stats for the results including range, mean, median, mode

        gpas : list of all the calculated GPAS
    """
    #Min and max
    min_gpa = min(gpas)
    max_gpa = max(gpas)
    
    #average
    avg_gpa = calc_gpa(gpas)

    #median
    med_gpa = median(gpas)

    #mode 
    mode_gpa = mode(gpas) 
    
    #Print results
    print("Your GPA can range from {0:.3f} to {1:.3f}".format(min_gpa, max_gpa))
    print("Average possible GPA: {0:.3f}".format(avg_gpa))
    print("Median: {0:.3f}".format(med_gpa))
    
    #Handle multiple modes
    mode_str = "Mode: "
    for score in sorted(mode_gpa):
        mode_str += "{0:.3f}, ".format(score)

    print(mode_str[:-2])


def median(gpas):
    """ 
        Calcuates the median ("Middle most value") of the calculated GPAS
        Taken from: Data Science from Scratch by Joel Grus

        gpas : list of calculated gpas 
    """
    length = len(gpas)
    ordered = sorted(gpas)
    midpoint = length // 2

    #If odd return the middle value
    if length % 2 == 1:
        return ordered[midpoint]

    #Else return average of the two middle values
    else:
        low = midpoint - 1
        return (ordered[low] + ordered[midpoint]) / 2

def mode(gpas):
    """ 
        Calcuates the mode ("Most common value(s)") of the calculated GPAS
        Taken from: Data Science from Scratch by Joel Grus

        gpas : list of calculated gpas 
    """
    counts = Counter(gpas)
    max_count = max(counts.values())
    return [x for x, count in counts.items() if count == max_count]


def get_subjects():
    """
        Gets all amount of subjects the user is taking this semeser

        Returns : int amount of subjects
    """
    subjects = input("How many subjects are you taking this semester? ")
    
    #Parse input
    try:
        if int(subjects) < 1:
            print("Invalid number of subjects. Exiting")
            sys.exit(1)
    except Exception as e:
        print("Invalid number of subjects. Exiting")
        sys.exit(1)

    return int(subjects)

def get_grades():
    """
        Gets all of the user's current grades to date

        Returns : list of the user's current grades
    """
    grades = []
    reading = True
    while reading:
        ipt = input("Enter your current grades 1 by 1 or x to stop: ")
        try:
            #If finished
            if ipt == "x":
                reading = False
                break
            #else check if valid input
            else:
                grade = int(ipt)
                if grade < 1 or grade > 7:
                    print("Invalid entry")
                else:
                    grades.append(grade)
        except:
            print("Invalid entry")

    return grades

def read_grades(filen):
    """
        Reads in all list of grades from a file

        filen : path to the file to read

        Returns : list of the user's current grades
    """
    grades = []
    with open(filen,'r') as f:
        for line in f.readlines():
            for i in line.strip().split(","):
                if i != '':
                    grades.append(int(i.replace(" ","")))

    return grades

def get_parameters(argv):
    """
        Gets the amount of subjects to test the current grades to date

        argv : command line arguments

        Returns : tuple (subjects, grades)
    """
    subjects = 0
    grades = []

    #Read command line arguments
    try:
        opts, args = getopt.getopt(argv,"hs:f:",[])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        #Usage
        if opt == '-h':
            usage()
        #Subject count
        elif opt == "-s":
            subjects = int(arg)
        #Grades
        elif opt == "-f":
            grades = read_grades(arg)

    #If argument ommitted, get via CLI 
    if subjects == 0:
        subjects = get_subjects()

    if grades == []:
        grades = get_grades()

    #Return subjects and grades
    return subjects, grades

def usage():
    """Prints command line arguments"""
    print("""Usage: main.py <args>
    -h          Displays this message
    -s          Amount of subjects to calculate for this semester
    -f          File containing current grades till this point""")
    sys.exit(2)

#Main
if  __name__ == "__main__":
    #Read in parameters
    subjects, grades = get_parameters(sys.argv[1:])
    
    #Calculate all possible GPAS
    print("Calculating gpas")
    matrix = calc_matrix(grades,subjects)
    
    #Print matrix
    print_matrix(matrix, subjects)

    #Calculate stats
    gpas = [x["Total"] for x in matrix]
    calc_stats(gpas)

