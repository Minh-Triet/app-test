from ma import ma
from models.customer import CustomerModel


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerModel
        dump_only = ('Id',)  # Fields to skip during deserialization
        load_instance = True
        exclude = ('CreationId', 'DeletedId', 'LastModifierId', 'IsDeleted', 'DeletionTime', )
        ordered = True
