def get_subject_name(id: str) -> str:
    assert isinstance(id, str)
    if len(id) != len('01219114'):
        raise ValueError(f"Length of subject id is wrong! '{id}' (len={len(id)})")
    return f's{id}'


def get_student_name(id: str) -> str:
    assert isinstance(id, str)
    if len(id) != len('6110545619'):
        raise ValueError(f"Length of student id is wrong! '{id}' (len={len(id)})")
    return f'b{id}'


def get_enrollment_name(student_id: str, subject_id: str, year: str, semester: str) -> str:
    assert isinstance(year, (int, str))
    assert isinstance(semester, (int, str))
    year = int(year)
    semester = int(semester)
    if year > 9999:
        raise ValueError(f"Invalid year: '{year}'")
    if semester not in (1, 2):
        raise ValueError(f"Invalid semester: '{semester}'")
    return '_'.join([get_student_name(student_id), get_subject_name(subject_id), str(year), str(semester)])
