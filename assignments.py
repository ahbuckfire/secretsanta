import random

import emailing, parser, validation

def find_pairing(assignments: dict[str, str], participant_matrix: dict[str, list[int]], givers: list[str], current_idx: int) -> bool:
	if current_idx == len(givers):
		return len(assignments) == len(givers) # all assignments complete

	giver = givers[current_idx]
	possible_receivers = [receiver for receiver, can_give in zip(participant_matrix.keys(), participant_matrix[giver]) if can_give == 1]
	random.shuffle(possible_receivers)

	for receiver in possible_receivers:
		# if receiver has not already been assigned and would not create a mirrored pair
		if receiver not in assignments.values() and receiver != giver and assignments.get(receiver) != giver:
			assignments[giver] = receiver

			# recurse to determine if this is a valid pairing or if it creates an issue for subsequent pairings
			if find_pairing(assignments, participant_matrix, givers, current_idx + 1):
				return True # if no issue found, return True

			# otherwise, if pairing leads to dead end, remove key-value pair
			del assignments[giver]

	# if all possible receivers are exhausted, backtrack
	return False

def generate_pairings(participant_matrix: dict[str, list[int]]) -> dict[str, str]:
	assignments = {}
	givers = list(participant_matrix.keys())
	random.shuffle(givers) # randomize giving order

	if not find_pairing(assignments, participant_matrix, givers, 0):
		raise Exception("No valid pairing found for participant matrix and restrictions")
	for giver, receiver in assignments.items():
		print("assigned giver-receiver pair: {} -> {}".format(giver, receiver))
	return assignments


def main():
	participant_matrix = parser.parse_participant_matrix()	
	assignments = generate_pairings(participant_matrix)
	_ = validation.validate_assignments(assignments, participant_matrix)
	_ = emailing.send_assignments(assignments)


main()
