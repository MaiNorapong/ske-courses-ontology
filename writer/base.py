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


def get_enrollment_name(student_id: str, subject_id: str) -> str:
    get_student_name(student_id)
    assert isinstance(id, str)
    if len(id) != len('01219114'):
        raise ValueError(f"Length of subject id is wrong! '{id}' (len={len(id)})")
    return f's{id}'
