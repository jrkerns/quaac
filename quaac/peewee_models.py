from __future__ import annotations

from pathlib import Path

from peewee import Model, CharField, SqliteDatabase, DateTimeField, ForeignKeyField


class User(Model):
    name = CharField()
    email = CharField()


class Equipment(Model):
    name = CharField()
    type = CharField()
    serial_number = CharField()
    manufacturer = CharField()
    model = CharField()

class DataPoint(Model):
    name = CharField()
    perform_datetime = DateTimeField()
    measurement_value = CharField()
    measurement_unit = CharField()
    reference_value = CharField(default='')
    description = CharField(max_length=1000, default="")
    procedure = CharField(max_length=1000, default="")
    performer = ForeignKeyField(User, backref='datapoints')
    reviewer = ForeignKeyField(User, backref='reviewer', null=True)
    primary_equipment = ForeignKeyField(Equipment, backref='datapoints')

class AncillaryEquipment(Model):
    """An M2M intermediate table since we can have multiple ancillary equipment pieces for a datapoint"""
    equipment = ForeignKeyField(Equipment)
    datapoint = ForeignKeyField(DataPoint)

class Attachment(Model):
    name = CharField()
    comment = CharField(default='')
    encoding = CharField()
    compression = CharField()
    file_name = CharField()

class DatapointAttachment(Model):
    datapoint = ForeignKeyField(DataPoint)
    attachment = ForeignKeyField(Attachment)



ALL_MODELS = [User, Equipment, DataPoint, AncillaryEquipment, DatapointAttachment, Attachment]
class PeeWeeMixin:
    _peewee_model: Model

    def _to_peewee(self, db_path: Path) -> int:
        """Convert the user to a peewee object."""
        return self._peewee_model.get_or_create(**self.dict(exclude={'hash'}))[0]

