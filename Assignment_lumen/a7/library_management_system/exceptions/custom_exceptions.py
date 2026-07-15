class BookNotFoundError(Exception):
    pass


class MemberNotFoundError(Exception):
    pass


class BookAlreadyBorrowedError(Exception):
    pass


class BookNotBorrowedError(Exception):
    pass


class DataFileNotFoundError(Exception):
    pass