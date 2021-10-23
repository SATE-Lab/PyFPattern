def test_alter_db_table_with_model_change(self):
    '\n        Tests when model and db_table changes, autodetector must create two\n        operations.\n        '
    before = self.make_project_state([self.author_with_db_table_options])
    after = self.make_project_state([self.author_renamed_with_new_db_table_options])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename_model': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel', 'AlterModelTable'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='Author', new_name='NewAuthor')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='newauthor', table='author_three')