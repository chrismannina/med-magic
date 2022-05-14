def validate_email(self, email):
	user = Registration.query.filter_by(email = email.data).first()
	if user is not None:
		raise ValidationError('Please use a different email address')
    
def validate_username(self, username):
	user = Registration.query.filter_by(username = username.data).first()
	if user is not None:
		raise ValidationError('Please use a different email address')