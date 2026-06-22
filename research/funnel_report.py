print("Candidates:", candidate_setup.sum())
print("Qualified:", qualified.sum())
print("Triggered:", trigger.sum())

print(
    "Candidate→Qualified:",
    round(
        qualified.sum() /
        candidate_setup.sum(),
        2
    )
)

print(
    "Qualified→Triggered:",
    round(
        trigger.sum() /
        qualified.sum(),
        2
    )
)