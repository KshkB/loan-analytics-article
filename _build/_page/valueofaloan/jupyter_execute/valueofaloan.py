#!/usr/bin/env python
# coding: utf-8

# # The value of a loan

# ## Definition
# 
# A loan $L$ is defined by three parameters:
# 
# - the principal amount $(P)$;
# - the rate of interest $(r)$;
# - compounding $(n)$.
# 
# It is important to set, at the outset, the units of time used to express the interest rate. Let $u$ be the unit of time (e.g., it could be days, months, years etc.). Interest is expressed in units $u$. Compounding refers to the number of times interest is applied on the loan principal. With compounding set to $1$, this means the interest is compounded once every $u$ times (e.g., once per year, if $u$ is *years*). This gives the interpretation of interest as the rate at which the principal value of the loan grows over one unit of time, $u$.  More generally, if compounding is $n$, then interest $r$ as expressed per unit $u$ is applied on the principal $n$-many times over a single time period $u$. This is equivalent to the interest $r/n$ being applied every $(1/n)$-time periods.
# 
# **Example.** *If $u$ is years, $r$ is expressed as "percent per year". If compounding is $n = 2$, then $r$ is applied twice per year. And so, over a year, the principle $P$ will grow to $P(1 + r/2)$ by the first half of the year. By the end of the year, it will be $P(1 + r/2)^2$.* 
# 
# The following code generates a **loan card** defining a loan.

# In[1]:


def new_loan(principal, interest, compounding):
    loan_card = {}
    interest = interest/100
    
    loan_card["Principal"] = principal
    loan_card["Interest rate"] = interest
    loan_card["Compounding"] = compounding
    
    return loan_card


# ## Loan value
# 
# Let $\nu_L(t)$ be the value of the loan after $t$ units of time have elapsed. Here $L$ refers to the loan which, recall, is defined by the parameters $(P, r, n)$ being the principal, the interest and compounding. At $t = 0$, $\nu_L(0)= P$. After $t = 1/n$ units of time have elapsed, the interest $r$ has been compounded once. This means $\nu_L(1/n) = P(1 + r/n)$. And after $t = 2/n$-units of elapsed time, $\nu_L(2/n) = P(1 + r/n)^2$. After $t = \lambda/n$ units of elapsed time, $\nu_L(\lambda/n) = P(1 + r/n)^{\lambda}$. Hence, for *any* amount of elapsed time $t$ we arrive at the analytic expression,
# 
# $$
# \begin{align}
# \nu_L(t) = P\left(1 + \frac{r}{n}\right)^{nt}.
# \end{align}
# $$
# 
# In the following code block, code for calculating the loan value $\nu_L(t)$ is given. This code passes in a loan card from `new_loan` and the elapsed time.

# In[2]:


def LoanValue(loan, time):
    
    principal = loan['Principal']
    interest = loan['Interest rate']
    compounding = loan['Compounding']
    
    exponent = compounding*time
    compounding_factor = (1 + interest/compounding)**exponent
    
    return principal * compounding_factor


# ## Loan value with repayments
# 
# Suppose now that regular repayments $R$ are made on the loan each unit of time $u$. E.g., if $u$ is years, then an $R$ amount is repaid on the loan each year. Let $\nu_{L, R}(t)$ denote the value of the loan $L$ after $t$ units of elapsed time with a repayment rate of $R$ per unit time. With the loan $L$ defined by parameters $(P, r, n)$, it will grow to $\nu_L(1) = P(1 + r/n)^n$ after one period $u$. At $t = 1$, a repayment of $R$ is made. Hence $\nu_{L, R}(1) = \nu_L(1) - R$. Then over the next year, the value of the loan on which interest is applied is *not* $\nu_L(1)$ but rather $\nu_{L, R}(1)$. And so, at $t = 2$ we find
# 
# $$
# \begin{align}
# \nu_{L, R}(2) 
# &= 
# \left(\nu_L(1) - R\right) \left(1 + \frac{r}{n}\right)^n - R
# \\
# &= 
# \nu_L(2) - R\left(1 + \frac{r}{n}\right)^n - R.
# \end{align}
# $$
# 
# Set for convenience $z = (1 + r/n)^n$. Note that the expression for the loan value simplifies to $\nu_L(t) = Pz^t$. As for the repaid loan value, at $t = 2$ this becomes $\nu_{L, R}(2) = Pz^2 - R( 1 + z)$. With a little thought, the general analytic expression for the repaid loan value is,
# 
# $$
# \begin{align}
# \nu_{L, R}(t)
# &=
# Pz^t - R\left( 1 + z + \cdots + z^{t-1}\right)
# \\
# &=
# Pz^t - R\frac{1 - z^t}{1-z}
# \end{align}
# $$
# 
# where in the latter we have used the analytic continuation over the domain $\{z\in \mathbb R\mid z>0\}$  of a familiar algebraic identity. Note that $z > 0$ whenever the interest $r > 0$.
# 
# **Note.** *If $R = 0$ above, then we simply recover the loan value $\nu_L(t)$ as expected, i.e., $\nu_{L, 0}(t) = \nu_L(t)$.*
# 
# Code implementing the loan value with repayments is as follows.

# In[3]:


def LoanWithRepayments(loan, time, repayments):
    interest = loan['Interest rate']
    compounding = loan['Compounding']
    z_factor = (1 + interest/compounding)**compounding
    
    loan_value = LoanValue(loan, time)
    repayments_value = repayments*(1 - z_factor**time)/(1-z_factor)
    
    val = loan_value - repayments_value
    if val > 0:
        return val
    return 0


# ## Loan lifetime
# 
# ### Critical repayment level 
# 
# The value of a loan $L$ changes exponentially in time. If no repayments are made, the lifetime of $L$ is infinite, i.e., it will never be repaid. Indeed, its lifetime will remain inifite if at least a certain amount of repayments are not made per unit of time. 
# 
# **Definition.** *The minimum amount of repayment on the loan per unit time, ensuring the loan will eventually be fully repaid, is refered to as the **critical repayment level**.*
# 
# The critical repayment level can be found as follows. The condition that a loan be fully repaid is simply the requirement that the value of the loan $\nu_L(t) = Pz^t$ grows more slowly than the value of repayments $R\frac{1 - z^t}{1-z}$. That is, the value $\nu_{R, L}(t)$ is a positive and decreasing as a function of elapsed time. As $\nu_{L, R}(t)$ is given analytically, the condition that it be decreasing is a condition on its gradient. That is, 
# 
# $$
# \begin{align}
# \left.\frac{\partial \nu_{L, R}(t)}{\partial t}\right|_{t = t_0}
# < 0
# \end{align}
# $$
# 
# for all $t_0 > 0$. The above inequality can be written,
# 
# \begin{align}
# t_0z^{t_0-1} \left( P + \frac{R}{1-z}\right) < 0
# \end{align}
# 
# for all $t_0$. This can only hold if $P + \frac{R}{1-z} < 0$, i.e., for $R > (z-1)P$. The **critical repayment level**, denoted $R_{crit.}$, is therefore 
# 
# $$
# \begin{align}
# R_{crit.} = (z-1)P = \left( \left(1 + \frac{r}{n}\right)^n - 1\right)P.
# \end{align}
# $$
# 
# If $R < R_{crit.}$, the loan $L$ will never be fully repaid.

# In[4]:


def criticalLevel(loan):
    principal = loan['Principal']
    interest = loan['Interest rate']
    compounding = loan['Compounding']
    z_factor = (1 + interest/compounding)**compounding
    
    return (z_factor-1)*principal


# ### The lifetime
# 
# If $t_0$ denotes the time elapsed until the loan with repayments is fully repaid, then $t_0$ is equivalently the elapsed time such that $\nu_{L, R}(t_0) = 0$. With the analytic expression for $\nu_{L, R}(t)$ above, setting $\nu_{L, R}(t_0) = 0$ and solving for $t_0$ gives,
# 
# $$
# \begin{align}
# t_0 = \frac{1}{\log z}\big(\log R - \log((1-z)P+R)\big).
# \end{align}
# $$
# 
# See that as $R$ limits to the critical repayment value $R \rightarrow R_{crit.}$, $t_0$ limits to $+\infty$. And so the lifetime of the loan tends toward infinity as the repayment amount tends to the critical level, as expected. 
# 
# The following code returns the lifetime of a loan with repayments, provided the repayments are above the critical level.

# In[5]:


from math import log

def LoanLifetime(loan, repayments):
    principal = loan['Principal']
    interest = loan['Interest rate']
    compounding = loan['Compounding']
    z_factor = (1 + interest/compounding)**compounding
    
    if repayments <= criticalLevel(loan):
        print("Infinite")
        return 
    return (1/log(z_factor))*(log(repayments) - log((1-z)*principal + repayments))


# ## Desired repayments
# 
# If an amount of time elapsed is specified after which the loan ought to be repaid, what should the period repayments be? The answer to this question can be obtained immediately upon inspection of the repaid loan value $\nu_{L, R}(t)$. Recall that *any* elapsted time $t_0>0$ can be specified. As long as $t_0 < \infty$, the desired, periodic repayments, denoted $R_{desired}$, will be greater than the critical repayment level $R_{crit.}$. And so, if $t_0$ denotes the time elapsed after which the loan must be fully repaid, then $R_{desired}$ is obtained by solving for $R_{desired}$ in the equation $\nu_{L, R_{desired}}(t_0) = 0$. It is given by,
# 
# $$
# \begin{align}
# R_{desired} = P \frac{z^{t_0}(1-z)}{1 - z^{t_0}}.
# \end{align}
# $$

# In[6]:


def DesiredRepayments(loan, time):
    principal = loan['Principal']
    interest = loan['Interest rate']
    compounding = loan['Compounding']
    z_factor = (1 + interest/compounding)**compounding
    
    return principal*(z_factor**time)*(1-z_factor)/(1 - z_factor**time)


# ## Continuous compounding
# 
# 
# ### Continuously compounded loan value
# 
# The exponential function has many equivalent characterisations. One relevent characterisation for our purposes here is as the limit,
# 
# $$
# \begin{align}
# Ae^{rt} = \lim_{n \rightarrow \infty} A\left(1 + \frac{r}{n}\right)^{nt}.
# \end{align}
# $$
# 
# where $A, r$ and $t$ are independent of $n$. Note the similarity with the expression for loan value $\nu_L(t)$. The limit $n \rightarrow \infty$ represents the interest being compounded infinitely many times per unit time, $u$. In this event it is said to be compounded *continuously*. The parameters $(P, r, \infty)$ defines a loan $L_\infty$ with continuously compounded interest. 

# In[7]:


def new_loan_cts(principal, interest):
    loan_card = {}
    interest = interest/100
    
    loan_card["Principal"] = principal
    loan_card["Interest rate"] = interest
    
    return loan_card


# Using the above characterisation of the exponential we see that the value of a continuously compounded loan $L_\infty$ is,
# 
# $$
# \begin{align}
# \nu_{L_\infty}(t) = Pe^{rt}.
# \end{align}
# $$
# 
# To express the above in terms of limits, let $L_n$ denote the loan $(P, r, n)$. Let $L_\infty$ denote its continuously compounded counterpart $(P, r, \infty)$. Then,
# 
# $$
# \begin{align}
# \nu_{L_\infty}(t) = \lim_{n\rightarrow \infty}\nu_{L_n}(t).
# \end{align}
# $$
# 
# With the exponential function, the value of a continuously compounded loan can be calculated straightforwardly.

# In[8]:


from math import exp

def cts_LoanValue(cts_loan, time):
    principal = cts_loan["Principal"]
    interest = cts_loan["Interest rate"]
    
    return princpal*exp(interest*time)


# ### Continuously compounded loan value with repayments
# 
# The expression of the value of the continuously compounded loans $\nu_{L_\infty}(t)$ as a limit is suggestive of the general case where periodic repayments are made. Indeed, we can now simply *define*,
# 
# $$
# \begin{align}
# \nu_{L_\infty, R}(t) := \lim_{n\rightarrow \infty} \nu_{L_n, R}(t).
# \end{align}
# $$
# 
# It remains to see that the above limit is well defined. Recall that $\nu_{L_n, R}(t) = \nu_{L_n}(t) - R\frac{1 - z^t}{1-z}$. The limit $\lim_{n\rightarrow \infty} \nu_{L_n, R}(t)$ will be well-defined if each summand is well-defined. We know already that the first summand is well defined and limits to $\nu_{L_\infty}(t)$. As for the second, recall that $z = (1 + r/n)^n$. This means $\lim_{n\rightarrow \infty}z = e^r$. And so, as long as $r> 0$,
# 
# $$
# \begin{align}
# \lim_{n \rightarrow\infty} R\frac{1 - z^t}{1-z}
# =
# R\frac{1 - e^{rt}}{1 - e^r}.
# \end{align}
# $$
# 
# Hence the value of a continuously compounded loan with period repayments $R$ is given by the expression,
# 
# $$
# \begin{align}
# \nu_{L_\infty, R}(t) 
# &= \lim_{n\rightarrow \infty} \nu_{L_n, R}(t)
# \\
# &=
# Pe^{rt} - R\frac{1 - e^{rt}}{1 - e^r}.
# \end{align}
# $$
# 
# The value $\nu_{L_\infty,R}(t)$ is coded below.

# In[9]:


def cts_LoanWithRepayments(cts_loan, time, repayment):
    loan_val = cts_LoanValue(cts_loan, time)
    
    interest = cts_loan["Interest rate"]
    repayment_val = repayment*(1 - exp(interest*time))/(1 - exp(interest))
    val = loan_val - repayment_val
    
    if val > 0:
        return val
    return 0


# ### Lifetime of continuously compounded loans
# 
# #### Critial repayment level
# 
# As in the discrete (non-continuous) case, the critical repayment level can be found by inspecting the differential inequality $\partial \nu_{L_\infty, R}(t)/\partial t|_{t = t_0} < 0$ for al $t_0>0$. Doing so leads to,
# 
# $$
# \begin{align}
# R_{crit.} 
# = 
# (e^r - 1) P.
# \end{align}
# $$
# 
# With $r> 0$, note that $e^r > 1$. Hence $R_{crit.}$ will always be positive.
# 

# In[10]:


def cts_criticalLevel(cts_loan):
    principal = cts_loan["Principal"]
    interest = cts_loan["Interest rate"]
    
    return (exp(interest) - 1)*principal


# #### Lifetime
# 
# Recall, the lifetime of a loan $L$ is the elapsed time $t_0$ such that $\nu_{L, R}(t_0) = 0$. The same notion holds for continuously compounded loans $L_\infty$. The loan lifetime is the elapsed time $t_0$ such that $\nu_{L_\infty, R}(t_0) = 0$. It can be expressed analytically as follows,
# 
# $$
# \begin{align}
# t_0
# =
# \frac{1}{r} \left(\log R - \log\left((1-e^r)P + R\right)\right).
# \end{align}
# $$
# 
# As in the non-continuous case, as $R \rightarrow R_{crit.}$, $t_0 \rightarrow +\infty$.

# In[11]:


def cts_LoanLifetime(cts_loan, repayment):
    principal = cts_loan["Principal"]
    interest = cts_loan["Interest rate"]
    crit_level = cts_criticalLevel(cts_loan)
    
    if repayment < crit_level:
        print("Infinite")
        return
    return (1/interest)*(log(repayment) - log((1-exp(interest))*principal + repayment))


# #### Desired repayment amount
# 
# In order to ensure the continuously compounded loan will be repaid within a specified, elapsed time $t_0$, the desired repayment amount is
# 
# $$
# \begin{align}
# R_{desired} 
# =
# P \frac{e^{rt_0} (1- e^r)}{1 - e^{rt_0}}.
# \end{align}
# $$
# 
# This is directly analogous to the discrete case above.

# In[12]:


def cts_DesiredRepayment(cts_loan, time):
    principal = cts_loan["Principal"]
    interest = cts_loan["Interest rate"]
    
    return principal*exp(interest*time)*(1 - exp(interest))/(1 - exp(interest*time))

