import argparse
import os
import itertools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--inputFile', dest='input_file', required=True,
        help="Path to input index file"
    )
    parser.add_argument(
        '-o', '--outPath', dest='out_path', required=True,
        help="Path for output file"
    )

    args = parser.parse_args()

    input_file = os.path.abspath(args.input_file)
    out_path = os.path.abspath(args.out_path)

    base = os.path.basename(input_file)
    file_name = os.path.splitext(base)[0]

    if out_path.endswith("/"):
        out_path = out_path
    else:
        out_path = out_path + "/"

    index_file = open(input_file, 'r')

    index_list = []

    for index in index_file:
        index = index.rstrip()
        index_list.append(index)

    print(index_list)

    # Compare all of the index in the list with one another and store the value in a dictionary
    hamming_distance_dict = {}

    for base_index, compare_index in itertools.product(index_list, repeat=2):
        hamming_distance = compare_sequences(base_index, compare_index)
        if 3 < hamming_distance < 0:
            print(base_index + " and " + compare_index + " are less than 3 bp different")
        if base_index not in hamming_distance_dict.keys():
            hamming_distance_dict[base_index] = []
            hamming_distance_dict[base_index].append(str(hamming_distance))
        else:
            hamming_distance_dict[base_index].append(str(hamming_distance))

    result_file = open(out_path + file_name + "HammingDistance.csv", 'w')
    result_file.write(",")

    for index in index_list:
        result_file.write(index + ",")

    result_file.write("\n")

    for (key, val) in hamming_distance_dict.items():
        result_file.write(key + "," + ','.join(val) + "\n")

    index_file.close()
    result_file.close()


def compare_sequences(sequence1, sequence2):
    """
    Compares the similarity between sequence 1 and sequence 2
    The two sequences must be of the same length
    :param sequence1:
    :param sequence2:
    :return similarity_score: If the two sequences are identical, the similarity score would be 0
    """
    if (len(sequence1) == len(sequence2)):
        similarity_score = 0
        for nucleotide in range(len(sequence1)):
            if sequence1[nucleotide] != sequence2[nucleotide]:
                similarity_score += 1
        return similarity_score
    else:
        print(sequence1 + " and " + sequence2 + " must be the same length.")
        return


if __name__ == "__main__":
    main()
