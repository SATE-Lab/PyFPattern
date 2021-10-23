def test_concrete_field_changed_to_many_to_many(self):
    '\n        #23938 - Tests that changing a concrete field into a ManyToManyField\n        first removes the concrete field and then adds the m2m field.\n        '
    changes = self.get_changes([self.author_with_former_m2m], [self.author_with_m2m, self.publisher])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'RemoveField', 'AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Publisher')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='publishers', model_name='author')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='publishers', model_name='author')