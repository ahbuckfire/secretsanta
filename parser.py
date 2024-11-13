PARTICIPANT_MATRIX_PATH="participant_matrix.txt"

def parse_participant_matrix() -> dict[str, list[int]]:
	participant_matrix = {}

	with open(PARTICIPANT_MATRIX_PATH, "r") as f:
		participant_matrix = {}

		for i, line in enumerate(f.readlines()):
			parts = line.strip().split(':')
			if len(parts) != 2:
				raise Exception("participant matrix data not in correct format. check source file.")
			name, can_give_list = parts[0], parts[1].strip().split(',')

			participant_matrix[name] = [int(x) for x in can_give_list]

	return participant_matrix
