# A FUNCTION CREATED TO DEAL WITH SOME ISSUES IN GO-SHIP DATA: REMOVES SEPARATORS FROM A STRING
def remove_separators(value):
    if isinstance(value, str):
        stripped_value = value.strip()
        try:
            return int(stripped_value)
        except ValueError:
            try:
                return float(stripped_value)
            except ValueError:
                return stripped_value
    else:
        return value
