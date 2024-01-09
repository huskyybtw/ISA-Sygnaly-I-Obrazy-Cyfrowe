import scipy.stats as stats
import math

ki_values = [2,7,3,1,0]

# 1. Prawdopodobieństwo zarejestrowania X = ki dla lambda = 1
lambda_1 = 1
prob_1 = [stats.poisson.pmf(k, lambda_1) for k in ki_values]

# 2. Prawdopodobieństwo zarejestrowania X = 0 dla lambda = ki
prob_2 = [stats.poisson.pmf(0, k) for k in ki_values]

# 3. Prawdopodobieństwo zarejestrowania co najmniej sumy ki fotonów
Lambda = sum(ki_values)
prob_3 = 1 - sum([stats.poisson.pmf(k, Lambda) for k in range(Lambda)])

# 4. Prawdopodobieństwo zarejestrowania nie więcej niż sumy ki fotonów z QE = π/4
QE = math.pi / 4
effective_Lambda = QE * Lambda
prob_4 = sum([stats.poisson.pmf(k, effective_Lambda) for k in range(Lambda + 1)])

print("1. Prawdopodobieństwa dla X = ki:", prob_1)
print("2. Prawdopodobieństwa dla X = 0 przy lambda = ki:", prob_2)
print("3. Prawdopodobieństwo dla co najmniej sumy ki:", prob_3)
print("4. Prawdopodobieństwo dla nie więcej niż sumy ki z QE:", prob_4)
