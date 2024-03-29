# oneragtime-challenge

## About

Django app to automate the sending of cash calls to the investor.

```
💡 A Cash call is an invoice we send to the user (in this example an investor), it groups a set of bills
```

- Generated bills are stored.
- Admin can group bills by investor.
- Once validated, generate invoice and email the investor.
- Keep check of status of cash call; validated, sent, paid, overdue

## Bills

### **Membership:**

If active and didn’t invest €50,000: €3000 per year.

### **Upfront**:

Pay all fees and bill once. Fee % x Amount Invested x 5

### **Yearly fees:**

Before April 2019

- 1st year: date / 365 x fee % x amount invested
- Following years: Fee perentage x amount invested

After April 2019

- 1st year: date / 365 x fee % x amount invested
- 2nd year: Fee perentage x amount invested
- 3rd year: (Fee perentage - .20%) x amount invested
- 4th Year: (Fee perentage - .50%) x amount invested
- Following Year: (Fee perentage - 1%) x amount invested
