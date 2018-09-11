# Program to simulate retirement expenses based on corpus an expenditure and see how long the money would last
import sys


class retire :
    corpus = expense_annual = inflation = 0
    interest = 5
    yr = 1

    # a little money that would be earned during retirement
    # by doing odd jobs on the side, maybe as freelance work
    topup = 0
    increment_rate = 0
    def __init__(self, corpus, expense_annual, inflation, topup):
        self.corpus = int(corpus)
        self.expense_annual = int(expense_annual)
        self.inflation = int(inflation)
        self.topup = int(topup)
        self.increment_rate = int(self.inflation)
        self.yr = 0

    def sim_year(self):
        if (self.expense_annual > self.corpus):
            return False

        self.corpus = self.corpus - self.expense_annual
        self.expense_annual = int(self.expense_annual + ( self.expense_annual * self.inflation/100.0))
        self.corpus = int(self.corpus + (self.corpus * (self.interest/100.0)))
        self.corpus = self.corpus + self.topup
        self.topup = int(self.topup + (self.topup * (self.increment_rate/100.0)))

        self.yr += 1
        self.disp_report()
        return True

    def disp_report(self):
        word = [self.yr, self.corpus, self.expense_annual, self.topup]
        line = '{:>5} {:>12}  {:>12}  {:>12}'.format(word[0], word[1], word[2], word[3])
        print(line)


    def disp_report2(self):
        print("Year    :" + str(self.yr))
        print("Corpus  :" + str(self.corpus))
        print("Expenses:" + str(self.expense_annual))
        print("Topup:" + str(self.topup))

        #print("Inflation:" + str(self.inflation))


    def dosim(self):
        while (self.corpus > 0):
            res = self.sim_year()
            if (res == False):
                print("#" * 79) # prints a separator
                print("out of moolah")
                return


if __name__ == "__main__":
    if len(sys.argv) != 5:
        # python ./retirement.py 1200000 50000 7 5000
        print("Usage:" + sys.argv[0] + "<corpus> <expenses_annual> <inflation_rate> <annual_topup>")
        sys.exit(1)

    corpus = sys.argv[1]
    expense_annual = sys.argv[2]
    inflation = sys.argv[3]
    topup = sys.argv[4]

    print("corpus:" + str(corpus))
    print("Annual Expenses:" + str(expense_annual))
    print("Inflation:" + str(inflation))
    print("Topup annualy:" + str(topup))

    word = ['Year', 'corpus', 'expenses(yr)', 'topup(yr)']
    line = '{:>5} {:>12}  {:>12}  {:>12}'.format(word[0], word[1], word[2], word[3])
    print("#" * 81)
    print(line)
    print("#" * 81)

    r  = retire(corpus, expense_annual, inflation, topup)
    r.dosim()
