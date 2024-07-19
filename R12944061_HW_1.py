import sys
import numpy as np
import numpy_financial as npf

def loan_amortization_swapping(V, m, n1, r1, n2, r2, F):
    # Calculate the monthly interest rate
    mr1 = r1 / m
    mr2 = r2 / m
    # Calculate the total number of payments
    total_payments = n1 * m
    cash_flows_swapped = [-V] + [0] * total_payments
    # Calculate the level payment for the original loan
    P = (V * mr1)/(1-(1+mr1) ** -total_payments)
    # Initialize variables for total principal and interest paid
    total_principal_paid = 0
    total_interest_paid = 0
    remaining_principal = V
    term_remaining = total_payments
    flow = 1
    # Calculate total principal and interest paid in the first n2 years
    for year in range(1, n2 + 1):
        for month in range(1, m + 1):
            # Calculate interest for the current month
            interest = remaining_principal * mr1
            cash_flows_swapped[flow] += P
            principal = P - interest
            # Update total interest paid
            remaining_principal -= principal
            total_interest_paid += interest
            # Update total principal paid
            total_principal_paid += principal
            term_remaining = term_remaining - 1
            flow = flow + 1
    output1 = total_principal_paid
    output2 = total_interest_paid
    remaining_principal_2 = remaining_principal
    #total interest paid from the end of year n2 (excluded) to the end of year n1 if the loan is not swapped (so the r1 interest rate is maintained)
    total_interest_paid_1 = 0

    for year in range(n2 + 1, n1 + 1):
        for month in range(1, m + 1):
            # Calculate interest for the current month
            interest = remaining_principal * mr1
            principal = P - interest
            # Update total interest paid
            remaining_principal -= principal
            total_interest_paid_1 += interest
            # Update total principal paid
            total_principal_paid += principal
            
    output3 = total_interest_paid_1

    #total interest paid from the end of year n2 (excluded) to the end of year n1 if the loan is swapped to the new r2 interest rate
    total_interest_paid_2 = 0
    P2 = (remaining_principal_2 * mr2)/(1-(1+mr2) ** -term_remaining)
    
    for year in range(n2 + 1, n1 + 1):
        for month in range(1, m + 1):
            # Calculate interest for the current month
            interest = remaining_principal_2 * mr2
            cash_flows_swapped[flow] += P2 
            principal = P2 - interest
            # Update total interest paid
            remaining_principal_2 -= principal
            total_interest_paid_2 += interest
            # Update total principal paid
            total_principal_paid += principal
            flow = flow + 1
    cash_flows_swapped[n2 * m] += F
    output4 = total_interest_paid_2 
    
    cash_flows = [-V] + [P] * total_payments
    irr_1 = npf.irr(cash_flows)
    irr_2 = npf.irr(cash_flows_swapped)
    irr_1 = irr_1 * m
    irr_2 = irr_2 * m
    if(irr_1 > irr_2):
        lower_irr = 1
    elif(irr_1 == irr_2):
        lower_irr = 0     
    else: 
        lower_irr = -1
        

      
    

    # Format and print the outputs
    outputs = [
        '{:.6f}'.format(output1),
        '{:.6f}'.format(output2),
        '{:.6f}'.format(output3),
        '{:.6f}'.format(output4),
        '{:.6f}'.format(irr_2),
         lower_irr
    ]
    print(", ".join(map(str, outputs)))

if __name__ == "__main__":
    # Parse command line arguments
    args = sys.argv[1:]
    V, m, n1, r1, n2, r2, F = map(float, args)

    # Run the loan amortization swapping function
    loan_amortization_swapping(V, int(m), int(n1), r1, int(n2), r2, F)
