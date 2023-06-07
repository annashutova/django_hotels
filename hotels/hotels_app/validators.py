from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import models
from re import findall
from datetime import date
from .config import CHARS_DEFAULT, PHONE_LENGTH


def validate_dates(check_in: date, check_out: date) -> None:
    if check_in < date.today():
        raise ValidationError('Check-in date cannot be in the past.')
    if check_out <= check_in:
        raise ValidationError('Check-out date cannot be before check in date.')


def validate_birth(birth: date) -> None:
    if birth >= date.today():
        raise ValidationError('Date of birth cannot be in the future.')


def validate_name(name: str) -> None:
    if findall('[0-9]', name):
        raise ValidationError('First name and last name cannot contain numbers')
    if len(name) > CHARS_DEFAULT:
        raise ValidationError(f'Name is too long. Maximum length is {CHARS_DEFAULT} digits.')


def validate_new_username(username: str) -> None:
    if len(username) > CHARS_DEFAULT:
        raise ValidationError(f'Username is too long. Maximum length is {CHARS_DEFAULT} digits.')
    try:
        models.User.objects.get(username=username)
    except ObjectDoesNotExist:
        return
    raise ValidationError('Username is already in use. Try again.')


def validate_phone(phone) -> None:
    cleaned_value = ''.join(filter(str.isdigit, phone))
    if len(cleaned_value) != PHONE_LENGTH or not cleaned_value.startswith(('7', '8')):
        raise ValidationError('Invalid phone number!')


def validate_passwords(pass1: str, pass2: str) -> None:
    if pass1 != pass2:
        raise ValidationError('Passwords does not match. Try again.')
