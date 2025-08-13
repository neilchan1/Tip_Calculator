def calculate_tip_amount(bill_amount, tip_percentage):
    """Return the tip amount given a bill and tip percentage."""
    return bill_amount * (tip_percentage / 100)

def calculate_total_per_person(bill_amount, tip_percentage, number_of_people):
    """Return the total each person should pay."""
    if number_of_people <= 0:
        raise ValueError("Number of people must be greater than zero.")
    
    tip_amount = calculate_tip_amount(bill_amount, tip_percentage)
    total_bill = bill_amount + tip_amount
    return total_bill / number_of_people
