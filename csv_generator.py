import csv
from random import randint

# just a quick and dirty csv data generator :)

stages = ['APPLIED', 'SCREENED', 'REJECTED_1', 'INTERVIEWED', 'REJECTED_2', 'GIVEN_OFFER', 'DECLINED', 'HIRED']

num_candidates = 1000

initial_time = 1404851070
max_applied_time = 1404851070 + (900 * 60 * 60 * 24)

max_time_between_stages = 10000
min_time_between_stages = 1000

rows = []
for candidate_id in range(num_candidates):
    last_stage = randint(0, len(stages) - 1)
    current_stage_time = randint(initial_time, max_applied_time)
    for j, stage in enumerate(stages[0:last_stage + 1]):
        # check if candidate has next stage - if so he/she couldn't reject/decline
        if (stage.startswith("REJECTED") or stage.startswith("DECLINED")) and j < last_stage:
            continue
        stage_time = randint(current_stage_time + min_time_between_stages, current_stage_time + max_time_between_stages)
        rows.append((str(stage_time), str(candidate_id), stage))
        current_stage_time = stage_time

print('time,applicant_id,stage')
for r in rows:
    print(','.join(r))
