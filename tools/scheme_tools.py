from langchain_core.tools import tool

@tool
def check_eligibility(age: int, occupation: str, land_acres: float = 0.0):
    """
    Checks eligibility for Telangana schemes like Rythu Bandhu.
    Args:
        age: User's age in years.
        occupation: Job type (e.g., 'farmer', 'student', 'worker').
        land_acres: Amount of land owned in acres (default 0).
    """
    # Logic for Rythu Bandhu
    if occupation.lower() == "farmer":
        if 0 < land_acres < 10:
            return "ELIGIBLE: You qualify for Rythu Bandhu (₹5000/acre)."
        return "NOT ELIGIBLE: You must own between 1 and 10 acres of land."
    
    # Logic for Aasara Pension
    if age > 57:
        return "ELIGIBLE: You qualify for Aasara Pension (Senior Citizen)."
        
    return "NOT ELIGIBLE: We could not find a matching scheme for your profile."

@tool
def get_scheme_details(scheme_name: str):
    """Retrieves details about a specific government scheme."""
    db = {
        "rythu bandhu": "Rythu Bandhu is a welfare program to support farming investment.",
        "aasara": "Aasara pensions provide financial security to senior citizens."
    }
    # Simple fuzzy match
    for key, value in db.items():
        if key in scheme_name.lower():
            return value
            
    return "Scheme details not found."