from wtforms import Form, StringField, IntegerField, RadioField, FileField, validators

class createProperty(Form):
    propertyname = StringField('Property Name: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    propertytype = StringField('Property Type: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    district = StringField('District: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    bedroom_no = IntegerField('No. of bedrooms: ', [validators.DataRequired()])
    price = IntegerField('Price ($): ', [validators.DataRequired()])
    psf = IntegerField('Square Feet (m): ', [validators.DataRequired()])
    image_url = FileField('Image: ', [validators.DataRequired()])