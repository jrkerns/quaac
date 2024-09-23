import base64
import json
import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from unittest import TestCase, skip

from pydantic import ValidationError

from quaac.common import create_hash_from_entry
from quaac import User, Equipment, Attachment, Document, DataPoint


def create_attachment(**kwargs) -> Attachment:
    # create random content
    random_content = base64.b64encode(os.urandom(32))
    return Attachment(name=kwargs.pop('name', 'test'), content=kwargs.pop('content', random_content), **kwargs)


def create_user(**kwargs) -> User:
    return User(name=kwargs.pop('name', 'Johnny'), email=kwargs.pop('email', 'j@j.com'), **kwargs)


def create_equipment(**kwargs) -> Equipment:
    return Equipment(
        name=kwargs.pop('name', 'TB'),
        serial_number=kwargs.pop('serial_number', '1234'),
        type=kwargs.pop('type', 'linac'),
        model=kwargs.pop('model', 'TrueBeam'),
        manufacturer=kwargs.pop('manufacturer', 'Varian'),
        **kwargs
    )


def create_datapoint(**kwargs) -> DataPoint:
    return DataPoint(
        name=kwargs.pop("name", "test"),
        perform_datetime=kwargs.pop("perform_datetime", "2021-01-01T00:00:00"),
        measurement_value=kwargs.pop("measurement_value", 1.0),
        measurement_unit=kwargs.pop("measurement_unit", "Gy"),
        reference_value=kwargs.pop("reference_value", 1.0),
        description=kwargs.pop("description", ""),
        procedure=kwargs.pop("procedure", ""),
        performer=kwargs.pop("performer", create_user()),
        performer_comment=kwargs.pop("performer_comment", ""),
        primary_equipment=kwargs.pop("primary_equipment", create_equipment()),
        reviewer=kwargs.pop("reviewer", None),
        ancillary_equipment=kwargs.pop("ancillary_equipment", []),
        attachments=kwargs.pop("attachments", []),
        parameters=kwargs.pop("parameters", {}),
        **kwargs
    )


class TestHasher(TestCase):

    def test_create_hash(self):
        entry = {'test data': [1, 2, 3]}
        hash = create_hash_from_entry(entry)
        self.assertEqual(hash, '5ef2d60d51b2dad78f9a6f5be9c6fa38')


class BaseModelTester(ABC):

    @abstractmethod
    def test_valid_create(self):
        pass

    @abstractmethod
    def test_invalid_create(self):
        pass

    @abstractmethod
    def test_extras(self):
        pass


class TestUserModel(BaseModelTester, TestCase):

    def test_valid_create(self):
        User(name="Johnny", email="j@j.com")

    def test_invalid_create(self):
        with self.assertRaises(ValidationError):
            User(name="Johnny")

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            User(name="Johnny", email="j@j")

    def test_extras(self):
        u = User(name="Johnny", email="j@j.com", role="admin")
        self.assertEqual(u.role, "admin")


class TestEquipmentModel(BaseModelTester, TestCase):

    def test_valid_create(self):
        Equipment(name="TB", serial_number="1234", type="linac", model="TrueBeam", manufacturer="Varian")

    def test_invalid_create(self):
        with self.assertRaises(ValidationError):
            Equipment(name="linac")

    def test_extras(self):
        e = Equipment(name="TB", serial_number="1234", type="linac", model="TrueBeam", manufacturer="Varian", location="1234")
        self.assertEqual(e.location, "1234")


class TestAttachmentModel(BaseModelTester, TestCase):

    def test_valid_create(self):
        Attachment(name="test", content=b"test")

    def test_invalid_create(self):
        with self.assertRaises(ValidationError):
            Attachment(name="test")

    def test_extras(self):
        a = Attachment(name="test", content=b"test", source="network share")
        self.assertEqual(a.source, "network share")

    def test_from_file(self):
        # create temp file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")

        a = Attachment.from_file(f.name)
        # the content is encoded in base64
        self.assertEqual(a.name, Path(f.name).name)

    def test_full_cycle(self):
        # create temp file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")

        # create attachment from file
        a = Attachment.from_file(f.name)
        with tempfile.NamedTemporaryFile(delete=False) as f2:
            a.to_file(f2.name)

        # read the file and compare the content
        a2 = Attachment.from_file(f2.name)
        self.assertEqual(a.content, a2.content)

    def test_to_file_no_name(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")
        a = Attachment.from_file(f.name)
        a.to_file()
        # should write to the current directory w/ name of the file it was created with.
        self.assertTrue((Path('.') / Path(f.name).name).exists())
        try:
            (Path('.') / Path(f.name).name).unlink()
        except FileNotFoundError:
            pass

    def test_no_compression(self):
        # create temp file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")

        a = Attachment.from_file(f.name, compression=None)
        # the content is only base64 encoded, no compression
        self.assertEqual(a.content, base64.b64encode(b"test"))


class TestDataPointModel(BaseModelTester, TestCase):

    def test_valid_create(self):
        create_datapoint()

    def test_invalid_create(self):
        with self.assertRaises(ValidationError):
            DataPoint(value=1.0)

    def test_extras(self):
        dp = create_datapoint(name="test", pylinac_version="3.20")
        self.assertEqual(dp.pylinac_version, "3.20")

    def test_ancillary_equipment(self):
        e1 = create_equipment(name='Catphan')
        e2 = create_equipment(name='Ion chamber')
        dp = create_datapoint(ancillary_equipment=[e1, e2])
        self.assertEqual(dp.ancillary_equipment, [e1, e2])

    def test_reviewer(self):
        performer= create_user(name="Johnny")
        reviewer = create_user(name="Hasan")
        dp = create_datapoint(reviewer=reviewer, performer=performer)
        self.assertEqual(dp.reviewer, reviewer)
        self.assertEqual(dp.performer, performer)
        self.assertNotEqual(dp.performer, reviewer)

    def test_parameters(self):
        dp = create_datapoint(parameters={"facet": "thingy", 'energy': 6})
        self.assertEqual(dp.parameters, {'facet': 'thingy', 'energy': 6})

    def test_serialize_primary_equipment(self):
        """Assert that when dumping to JSON that the hash is used for the primary equipment"""
        e = create_equipment()
        dp = create_datapoint(primary_equipment=e)
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['primary_equipment'], e.named_hash())

    def test_serialize_reviewer(self):
        """Assert that when dumping to JSON that the hash is used for the reviewer"""
        reviewer = create_user()
        dp = create_datapoint(reviewer=reviewer)
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['reviewer'], reviewer.named_hash())

    def test_serialize_no_reviewer(self):
        """Should be none if no reviewer"""
        dp = create_datapoint()
        self.assertEqual(dp.reviewer, None)
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['reviewer'], None)

    def test_serialize_ancillary_equipment(self):
        """Assert that when dumping to JSON that the hash is used for the ancillary equipment"""
        e1 = create_equipment(name='Catphan')
        e2 = create_equipment(name='Ion chamber')
        dp = create_datapoint(ancillary_equipment=[e1, e2])
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['ancillary_equipment'], [e1.named_hash(), e2.named_hash()])

    def test_serialize_no_ancillary_equipment(self):
        """Should be empty list if no ancillary equipment"""
        dp = create_datapoint()
        self.assertEqual(dp.ancillary_equipment, [])
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['ancillary_equipment'], [])

    def test_serialize_performer(self):
        """Assert that when dumping to JSON that the hash is used for the performer"""
        performer = create_user()
        dp = create_datapoint(performer=performer)
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['performer'], performer.named_hash())

    def test_serialize_attachments(self):
        """Assert that when dumping to JSON that the hash is used for the attachments"""
        a1 = create_attachment()
        a2 = create_attachment()
        dp = create_datapoint(attachments=[a1, a2])
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['attachments'], [a1.named_hash(), a2.named_hash()])

    def test_serialize_no_attachments(self):
        """Should be empty list if no attachments"""
        dp = create_datapoint()
        self.assertEqual(dp.attachments, [])
        json_data = json.loads(dp.model_dump_json())
        self.assertEqual(json_data['attachments'], [])


class TestDocumentModel(BaseModelTester, TestCase):

    def test_valid_create(self):
        Document(version="1.0", datapoints=[create_datapoint()])

    def test_invalid_create(self):
        with self.assertRaises(ValidationError):
            Document(version="1.0")

    def test_extras(self):
        d = Document(version="1.0", datapoints=[create_datapoint()], pylinac_version="3.20")
        self.assertEqual(d.pylinac_version, "3.20")

    def test_bad_version(self):
        with self.assertRaises(ValidationError):
            Document(version="3.9", datapoints=[create_datapoint()])

    def test_multiple_user_references_coalesce(self):
        u1 = create_user(name='Randle')
        u2 = create_user(name='Johnny')
        d = Document(version="1.0", datapoints=[create_datapoint(performer=u1, reviewer=u2), create_datapoint(performer=u2)])
        self.assertEqual(len(d.users), 2)
        self.assertEqual(d.users, {u1, u2})

    def test_user_hashes_match(self):
        u1 = create_user(name='Randle')
        u2 = create_user(name='Johnny')
        d = Document(version="1.0", datapoints=[create_datapoint(performer=u1, reviewer=u2), create_datapoint(performer=u2)])
        self.assertIn(u1.hash, [u.hash for u in d.users])
        self.assertIn(u2.hash, [u.hash for u in d.users])
        self.assertEqual(d.datapoints[0].performer.named_hash(), u1.named_hash())

    def test_equipment_coalesces(self):
        e1 = create_equipment(name='Catphan')
        e2 = create_equipment(name='Ion chamber')
        d = Document(version="1.0", datapoints=[create_datapoint(primary_equipment=e1, ancillary_equipment=[e2]), create_datapoint(primary_equipment=e2)])
        self.assertEqual(len(d.equipment), 2)
        self.assertEqual(d.equipment, {e1, e2})

    def test_equipment_hashes_match(self):
        e1 = create_equipment(name='Catphan')
        e2 = create_equipment(name='Ion chamber')
        d = Document(version="1.0", datapoints=[create_datapoint(primary_equipment=e1, ancillary_equipment=[e2]), create_datapoint(primary_equipment=e2)])
        equip = {e.name: e for e in d.equipment}
        # set order not guaranteed
        self.assertEqual(equip['Catphan'].hash, e1.hash)
        self.assertEqual(equip['Ion chamber'].hash, e2.hash)
        self.assertEqual(d.datapoints[0].primary_equipment.hash, e1.hash)

    def test_attachments_coalesce(self):
        a1 = create_attachment(name='a1')
        a2 = create_attachment(name='a2')
        d = Document(version="1.0", datapoints=[create_datapoint(attachments=[a1, a2]), create_datapoint(attachments=[a2])])
        self.assertEqual(len(d.attachments), 2)
        self.assertEqual(d.attachments, {a1, a2})

    def test_attachment_hashes_match(self):
        a1 = create_attachment(name='a1')
        a2 = create_attachment(name='a2')
        d = Document(version="1.0", datapoints=[create_datapoint(attachments=[a1, a2]), create_datapoint(attachments=[a2])])
        self.assertIn(a1.hash, [a.hash for a in d.attachments])

    def test_json_cycle(self):
        """Test going to JSON and back again"""
        d = Document(version="1.0", datapoints=[create_datapoint()])
        with tempfile.NamedTemporaryFile(delete=False) as f:
            d.to_json_file(f.name)
            d2 = Document.from_json_file(f.name)
        d1_data = json.loads(d.model_dump_json())
        d2_data = json.loads(d2.model_dump_json())
        self.assertEqual(d1_data, d2_data)

    def test_yaml_cycle(self):
        """Test going to YAML and back again"""
        d = Document(version="1.0", datapoints=[create_datapoint()])
        with tempfile.NamedTemporaryFile(delete=False) as f:
            d.to_yaml_file(f.name)
            d2 = Document.from_yaml_file(f.name)
        d1_data = json.loads(d.model_dump_json())
        d2_data = json.loads(d2.model_dump_json())
        self.assertEqual(d1_data, d2_data)

    def test_edited_file_does_not_validate(self):
        """Test that if the file is edited it will not validate"""
        d = Document(version="1.0", datapoints=[create_datapoint()])
        # first, write the file like normal
        with tempfile.NamedTemporaryFile(delete=False) as f:
            d.to_json_file(f.name)

        # edit the data
        with open(f.name, 'r') as f:
            data = json.loads(f.read())
            data['hash'] = 'bad hash'
        # save the file
        with open(f.name, 'w') as f:
            f.write(json.dumps(data))
        # ensure it doesn't validate

        with self.assertRaises(ValueError):
            Document.from_json_file(f.name)

    def test_editing_file_validates_with_check_false(self):
        """If we create and purposely edit the file, we can still load it if we pass check=False"""
        d = Document(version="1.0", datapoints=[create_datapoint()])
        # first, write the file like normal
        with tempfile.NamedTemporaryFile(delete=False) as f:
            d.to_json_file(f.name)

        # edit the data
        with open(f.name, 'r') as f:
            data = json.loads(f.read())
            data['hash'] = 'bad hash'
        # save the file
        with open(f.name, 'w') as f:
            f.write(json.dumps(data))
        # ensure it validates
        d2 = Document.from_json_file(f.name, check_hash=False)
        self.assertIsInstance(d2, Document)

    def test_merge_documents(self):
        u = create_user()
        u2 = create_user(name='Randle')
        d1 = Document(version="1.0", datapoints=[create_datapoint(name='test 1', performer=u)])
        d2 = Document(version="1.0", datapoints=[create_datapoint(name='test2', performer=u2)])
        d3 = d1.merge(documents=[d2])
        self.assertEqual(len(d3.datapoints), 2)
        self.assertEqual(d3.datapoints[0].performer, u)
        self.assertEqual(d3.datapoints[0].name, 'test 1')
        self.assertEqual(d3.datapoints[1].name, 'test2')
        self.assertEqual(len(d3.equipment), 1)
        self.assertEqual(len(d3.users), 2)

    @skip("Only v 1.0 allowed for now. As versions are added, we'll need to check this.")
    def test_merge_version_must_be_same(self):
        u = create_user()
        u2 = create_user(name='Randle')
        d1 = Document(version="1.0", datapoints=[create_datapoint(name='test 1', performer=u)])
        d2 = Document(version="2.0", datapoints=[create_datapoint(name='test2', performer=u2)])
        with self.assertRaises(ValidationError):
            d1.merge(documents=[d2])
