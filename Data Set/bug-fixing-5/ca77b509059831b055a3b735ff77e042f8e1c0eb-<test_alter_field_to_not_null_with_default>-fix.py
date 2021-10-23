@mock.patch('django.db.migrations.questioner.MigrationQuestioner.ask_not_null_alteration', side_effect=AssertionError('Should not have prompted for not null addition'))
def test_alter_field_to_not_null_with_default(self, mocked_ask_method):
    '\n        #23609 - Tests autodetection of nullable to non-nullable alterations.\n        '
    changes = self.get_changes([self.author_name_null], [self.author_name_default])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name', preserve_default=True)
    self.assertOperationFieldAttributes(changes, 'testapp', 0, 0, default='Ada Lovelace')