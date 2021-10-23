def test_managed_to_unmanaged(self):
    before = self.make_project_state([self.author_empty, self.author_unmanaged_managed])
    after = self.make_project_state([self.author_empty, self.author_unmanaged])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelOptions'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='authorunmanaged', options={
        'managed': False,
    })