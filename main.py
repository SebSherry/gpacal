#Imports
import copy
from collections import Counter

#Current grades to date 
cur_grades = [
    #INSERT GRADES HERE
]

#The grade options (We assume no failures)
options = [4,5,6,7]

#Calculate GPA
def calc_gpa(grades):
    """
        Calculates the GPA of a set of grades

        grades : list of ints used as scores to calculate a gpa score
    """
    total = 0
    for grade in grades:
        total += grade
    
    gpa = float(total) / len(grades)
    return gpa

def gen_matrix(subjects):
    """
        Generates a list of dictonaries to hold all possible grade outcomes for a semester

        subjects : list of string codes for all the subjects in the semester
    """
    #Create base dictonary
    base = {"Total" : 0}
    for unit in subjects:
        base[unit] = 0

    #Calculate the number of rows in the matrix
    # 4 to the power of the amount of subjects in the unit
    rows = 4 ** len(subjects)

    #Setup counting array
    counts = [0 for x in subjects]

    print(counts,base)
    #Generate matrix
    matrix = []
    for i in range(rows):
        #create row
        row = copy.deepcopy(base)
        
        #Loop over subjects and apply grades
        for idx, unit in enumerate(subjects):
            row[unit] = 4 + counts[idx]
        
        #update counts
        counts[-1] += 1
        for i in range(len(counts)-1,-1,-1):
            if counts[i] == 4:
                counts[i] = 0
                if i-1 >= 0:
                    counts[i-1] += 1

        #add row to matrix
        matrix.append(row)

    return matrix

def calc_matrix(matrix, grades):
    """ 
        Calculates all the possible gpas based on previous semester results and all possible results for this semester

        matrix : list of dicts containing all possible grade out comes of for a semester
        grades : list of int scores for all subjects done up to this point
    """
    #Loop over the matrix
    for row in matrix:
        #Get a list of all the grades in the row
        outcomes = []
        for key in row:
            if key != "Total":
                outcomes.append(row[key])

        #Calculate the gpa for this outcome
        row["Total"] = calc_gpa(grades+outcomes)

def print_matrix(matrix, subjects):
    """
        Prints the matrix as a table

        matrix : matrix to print
        subjects : list of string codes for all the subjects in the semester
    """
    #create format string 
    fmtstr = "{0:3} " #row number 
    for idx, key in enumerate(subjects):
        fmtstr += "{"
        fmtstr += "{}:{}".format(idx+1,len(key))
        fmtstr += "} "
    
    #Print table header
    print((fmtstr+"GPA").format(*([" "]+subjects)))
    
    #Add GPA to format string
    fmtstr += "{"
    fmtstr += "{}:.3f".format(len(subjects)+1)
    fmtstr += "}"
            
    #Print matrix 
    for i in range(len(matrix)):
        args = [i+1]
        for unit in subjects:
            args.append(matrix[i][unit])
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
    sorted_gpas = sorted(gpas)
    mid = int(len(gpas)/2)
    if mid % 2 == 1:
        med_gpa = sorted_gpas[mid]
    else:
        med_gpa = (sorted_gpas[mid-1] + sorted_gpas[mid]) / 2

    #mode 
    counts = Counter(gpas)
    mode_gpa = counts.most_common(1)[0][0] 
    
    #Print results
    print("Your GPA can range from {0:.3f} to {1:.3f}".format(min_gpa, max_gpa))
    print("Average possible GPA: {0:.3f}".format(avg_gpa))
    print("Median: {0:.3f}".format(med_gpa))
    print("Mode: {0:.3f}".format(mode_gpa))


#Main
if  __name__ == "__main__":
    #Generate matrix
    subjects = ["SUB001", "SUB002", "SUB003"]
    print("Generating matrix")
    matrix = gen_matrix(subjects)
    
    #Calculate all possible GPAS
    print("Calculating gpas")
    calc_matrix(matrix,cur_grades)
    
    #Print matrix
    print_matrix(matrix, subjects)

    #Calculate stats
    gpas = [x["Total"] for x in matrix]
    calc_stats(gpas)

