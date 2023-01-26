import csv
import sys
import pandas as pd

def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    data = sys.argv[1]
    sequence = sys.argv[2]

    #Read database file into a dataframe
    df = pd.read_csv(data)

    # Read DNA sequence file into a variable
    with open(sequence, "r") as f:
       dna_sequence = f.read()

    # Find longest match of each STR in DNA sequence
    STR_matches = {}
    for column in df.columns[1:]:
        longest_match_value = longest_match(dna_sequence, column)
        STR_matches[column] = longest_match_value

    # Check database for matching profiles
    for index, row in df.iterrows():
        match = True
        for column in df.columns[1:]:
            if row[column] != STR_matches[column]:
                match = False
                break
        if match:
            print(f"{row['name']}\n")
            return
    print("No match\n")
    return

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
