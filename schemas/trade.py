from ma import ma
from models.trade import TradeModel


class TradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TradeModel
        dump_only = ('Id', )  # Fields to skip during deserialization
        load_only = ('quantity',)  # Fields exclude from serialized results.
        exclude = ('CreationId', 'DeletedId', 'LastModifierId', 'IsDeleted', 'DeletionTime', )
        load_instance = True,
        ordered = True

