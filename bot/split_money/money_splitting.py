from collections import defaultdict

def splitMoney(transactions):
    # Transactions in the form: (amount, who_paid, shared_among), where shared_among is an array
    balance = defaultdict(float)

    # Step 1: Calculate net balance for each person
    for amount, who_paid, shared_among in transactions:
        share = amount / len(shared_among)

        for person in shared_among:
            balance[person] -= share  # everyone owes their share

        balance[who_paid] += amount  # payer paid the full amount

    # Step 2: Separate creditors and debtors
    creditors = []
    debtors = []

    for person, amt in balance.items():
        if amt > 0:
            creditors.append([person, amt])   # is owed money
        elif amt < 0:
            debtors.append([person, -amt])    # owes money

    # Step 3: Settle debts
    result = []
    i = j = 0

    while i < len(debtors) and j < len(creditors):
        debtor, debt = debtors[i]
        creditor, credit = creditors[j]

        paid = min(debt, credit)

        result.append((debtor, creditor, round(paid, 2)))

        debtors[i][1] -= paid
        creditors[j][1] -= paid

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return result
