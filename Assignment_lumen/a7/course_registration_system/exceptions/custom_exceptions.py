class CourseNotFoundError(Exception):
    """Raised when course ID does not exist."""
    pass



class StudentNotFoundError(Exception):
    """Raised when student ID does not exist."""
    pass



class CourseFullError(Exception):
    """Raised when no seats are available."""
    pass



class DataFileNotFoundError(Exception):
    """Raised when CSV file is missing."""
    pass