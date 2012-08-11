from datetime import datetime

SELL, BUY = range(2)

HISTORY_IMPORTANCE_RANGE = range(1, 11)
START_MONEY = 1000

def getPercentage(ammount) :
	return ammount * 100 / START_MONEY

def sell(date, price) :
	global currentOperation, currentMoney, currentStock

	if currentOperation == SELL :
		return

	currentOperation = SELL
	currentMoney += price * currentStock
	currentStock = 0
	registry.addRegistry(date, currentMoney)

def buy(date, price) :
	global currentOperation, currentMoney, currentStock

	if currentOperation == BUY :
		return

	currentOperation = BUY
	currentStock = int(currentMoney / price)
	currentMoney -= price * currentStock

def adjustHistory(history, price) :
	historyImportance = len(history)
	for i in range(historyImportance - 1):
		history[i] = history[i + 1]
	history[historyImportance - 1] = price

def execute(entries, historyImportance) :
	global currentOperation, currentStock, currentMoney, lastPrice, registry
	
	currentOperation = SELL
	currentMoney = START_MONEY
	currentStock = None
	lastPrice = 0
	
	registry = MoneyRegistry(entries[0].date, currentMoney)

	history = [0] * historyImportance

	for entry in entries :
		openPrice = entry.open
		closePrice = entry.close

		adjustHistory(history, closePrice - openPrice)

		balance = sum(history);
		if balance > 0:
			sell(entry.date, closePrice)
		else :
			buy(entry.date, closePrice)
		lastPrice = closePrice;

	finalMoney = currentMoney + currentStock * lastPrice
	print "%.2f (%.2f %%) com %d dias" % (finalMoney, getPercentage(finalMoney - START_MONEY), historyImportance)
	print "Max Ammount = %.2f em %s" % registry.getMaxValue()
	print "Max Gain = %.2f %% de %s a %s (%d dias)" % registry.getMaxGain()
	print "Average Gain = %.2f (%.2f %%) por dia" % registry.getAverageGain()
	print ""


class DayEntry():

	DATE_FORMAT = "%d-%b-%y"

	def __init__(self, date_str, open_str, close_str) :
		self.date = datetime.strptime(date_str, DayEntry.DATE_FORMAT)
		self.open = float(open_str)
		self.close = float(close_str)

class MoneyRegistry():
	def __init__(self, firstDate, initialMoney):
		self.timeHistory = [firstDate]
		self.moneyHistory = [initialMoney]

	def addRegistry(self, date, ammount):
		self.timeHistory.append(date)
		self.moneyHistory.append(ammount)

	def getCurrentAmmount():
		return moneyHistory[-1]

	def getMaxValue(self) :
		maxValue = 0.0
		maxTime = None
		for i in range(len(self.moneyHistory)) :
			if maxValue < self.moneyHistory[i] :
				maxValue = self.moneyHistory[i]
				maxTime = self.timeHistory[i]
		return maxValue, maxTime.strftime("%d-%b-%y")

	def getMaxGain(self) :
		minValue = 9999999
		minDate = None
		maxGain = 0
		maxDate = None

		for i in range(len(self.moneyHistory)) :
			current = self.moneyHistory[i]
			if minValue > current :
				minValue = current
				minDate = self.timeHistory[i]

			currentGain = current - minValue
			if currentGain > maxGain :
				maxGain = currentGain
				maxDate = self.timeHistory[i]

		return getPercentage(maxGain), minDate.strftime(DayEntry.DATE_FORMAT), maxDate.strftime(DayEntry.DATE_FORMAT), (maxDate - minDate).days

	def getAverageGain(self) :
		lastAmmount = self.moneyHistory[0]
		lastDate = self.timeHistory[0]
		average = lastAmmount - START_MONEY
		average /= max(1, (lastDate - START_DATE).days)
		for i in range(1, len(self.moneyHistory)) :
			current = (self.moneyHistory[i] - lastAmmount) / (self.timeHistory[i] - lastDate).days
			#FIXME 
			average += current
			average /= 2
			lastAmmount = self.moneyHistory[i]
			lastDate = self.timeHistory[i]
		return average, getPercentage(average)


data = open("../files/data.csv")
lines = data.readlines()

prices = []
for i in reversed(range(1, len(lines))) :
	split = lines[i].split(",")
	prices.append(DayEntry(split[0], split[1], split[4]))

START_DATE = prices[0].date

for i in HISTORY_IMPORTANCE_RANGE :
	execute(prices, i)



