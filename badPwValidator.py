from wtforms import ValidationError

def load_bad_passwords():
	with open('10-million-password-list-top-100000.txt', 'r') as file:
		return set(line.strip() for line in file)

BAD_PASSWORDS = load_bad_passwords()

def is_not_weak_password(form, field):
	if field.data in BAD_PASSWORDS:
		raise ValidationError('This password is too weak. Please choose a stronger password.')

