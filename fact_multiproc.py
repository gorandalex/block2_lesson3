import multiprocessing
import sys
from multiprocessing import cpu_count, Process


def factorize(*number):
    count_proc = multiprocessing.cpu_count()
    with multiprocessing.Pool(count_proc) as pool:
        return pool.map(factors_of_number, number)
      

def factors_of_number(number):
    print(f'{number=}')
    factors = []
    for i in range(1, number//2 + 1):
        if number % i == 0:
            factors.append(i)
    factors.append(number)

    return factors




def main():
#    a, b, c,d = factorize(128, 255, 99999, 10651060)
#    print(f'{a=},{b=},{c=},{d=}')
    
    if len(sys.argv) < 2:
        numbers = [int(i) for i in input('Entrer numbers: ').split(',')]    
    else:
        numbers = [int(i) for i in sys.argv.split(',')]
        
    result = factorize(*numbers)
    for i in range(len(numbers)):
        print(f'{numbers[i]} : {result[i]}')
    
        
        
    


if __name__ == "__main__":
    exit(main())