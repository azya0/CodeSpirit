from wtforms.validators import ValidationError


class WhiteSpaceBanned(object):
    def __call__(self, form, field):
        data = field.data
        if ' ' in data:
            raise ValidationError(f'there shouldn\'t be a space in the field')


class Login(object):
    def __init__(self, num: int = 30, banned_chars: str = '@'):
        self.num = num
        self.banned_chars = banned_chars

    def __call__(self, form, field):
        data = field.data
        if len(data) > self.num:
            raise ValidationError(f'Too many characters for login ({self.num} max)')
        for char in self.banned_chars:
            if char in data:
                raise ValidationError(f'\'{char}\' can\'t be used in login field')


class SelfLength(object):
    """
    Validates SelfLength.
    """

    def __init__(self, obj_name: str, min_length=-1, max_length=-1):
        self.obj = obj_name
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, form, field):
        data = field.data
        if len(data) < self.min_length and self.min_length >= 0:
            raise ValidationError(f'{self.obj.capitalize()} must be more than {self.min_length} characters')
        if len(data) > self.max_length > 0:
            raise ValidationError(f'{self.obj.capitalize()} must be less than {self.max_length} characters')


class Tag(object):
    """
    Validates Tags.

    :param: tags_count: int, show how many tags user can enter
    :param: tags_len: int, show how many symbols can be used in per tag
    """

    def __init__(self, tags_count=6, tags_len=15):
        self.count = tags_count
        self.length = tags_len

    def __call__(self, form, field):
        tags = field.data.split()
        print(tags)
        if len(tags) > self.count:
            raise ValidationError(f'Too much tags ({self.count} maximum)')
        filtered = list(filter(lambda x: len(x) > self.length, tags))
        if filtered:
            filtered = map(lambda x: f'"{x}"', filtered)
            raise ValidationError(f'Tags: {", ".join(filtered)} too long')
