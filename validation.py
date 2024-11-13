import collections

def is_already_receiving_a_gift(name: str, assignments: dict[str, str]):
	return any(receiver == name for receiver in assignments.values())

def validate_assignments(assignments: dict[str, str], participant_matrix: dict[str, list[int]]) -> bool:
	print("Validating...")

	if len(assignments) != len(participant_matrix):
		print("There should be the same number of assignments ({}) as participants ({}). eek.".format(len(assignments), len(participant_matrix)))
		return False

	giver_counts = collections.defaultdict(int)
	receiver_counts = collections.defaultdict(int)

	for g, r in assignments.items():
		giver_counts[g] += 1
		receiver_counts[r] += 1

	for person, count in giver_counts.items():
		if count != 1:
			print("person {} has {} giver instances".format(person, count))
			return False

	for person, count in receiver_counts.items():
		if count != 1:
			print("person {} has {} receiver instances".format(person, count))
			return False

	print("validation complete. no errors")
	return True
