import math

def compare_model_dictionaries(data1, data2):
    diff_keys = data1.keys() ^ data2.keys()  #different keys

    # correction floating point numbers with math.isclose()
    diff_values = {}
    for key in data1:
        val1, val2 = data1.get(key), data2.get(key)
        if isinstance(val1, float) and isinstance(val2, float):
            if not math.isclose(val1, val2, rel_tol=1e-6):  # Comparison tollerance
                diff_values[key] = (val1, val2)
        elif val1 != val2:
            diff_values[key] = (val1, val2)


    if not diff_keys and not diff_values:
        print("No differences")
    else:
        print("Differences found:")
        
        if diff_values:
            print(" Differences in the values:")
            for key, (val1, val2) in diff_values.items():
                
                print(f"{key}' → Different values -> (CALCULATED) {val1} ≠ {val2} <- (SAVED ON BKCH)")





if __name__=="__main__":
    pass
