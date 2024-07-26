import csv

def print_cog(filename,f):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        next(reader)
        for arr in reader:
            f(arr)

def write_declare(arr):
    name = arr[0] + '_temp'
    numtype = arr[1]
    dim_clause = arr[2]

    dim = create_dim(count_dim(dim_clause) + 3)
    print("    %s, allocatable, target :: %s%s" % (numtype, name, dim))

def write_omp_declare(arr):
    name = arr[0] + '_temp'
    print("    !$omp declare target(%s)" % (name))

def write_alloc(arr):
    name = arr[0] + '_temp'
    numtype = arr[1]
    dim_clause = arr[2]
    dim_final = dim_clause[:-1] + ',its:ite,kts:kte,jts:jte)'
    print("    allocate( %s%s )" % (name, dim_final))

def write_omp_alloc(arr):
    name = arr[0] + '_temp'
    print("    !$omp target enter data map(alloc: %s)" % (name))

def write_declare_ptr(arr):
    name = arr[0]
    numtype = arr[1]
    dim_clause = arr[2]
    dim = create_dim(count_dim(dim_clause))
    print("    %s, pointer :: %s%s" % (numtype, name, dim))

def write_ptr(arr):
    ptr_name = arr[0]
    name = arr[0] + '_temp'
    numtype = arr[1]
    dim_clause = arr[2]

    dim = create_dim(count_dim(dim_clause))[:-1] + ',Iin,Kin,Jin)'
    print("    %s => %s%s" % (ptr_name, name, dim))

def count_dim(s):
    return s.count(',') + 1

def create_dim(n):
    s = '('
    for i in range(n):
        s = s + ':,'
    s = s[:-1] + ')'
    return s