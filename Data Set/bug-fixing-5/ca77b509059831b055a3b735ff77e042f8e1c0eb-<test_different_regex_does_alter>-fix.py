def test_different_regex_does_alter(self):
    from_state = ModelState('testapp', 'model', [('id', models.AutoField(primary_key=True, validators=[RegexValidator(re.compile('^[a-z]+\\Z', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')]))])
    to_state = ModelState('testapp', 'model', [('id', models.AutoField(primary_key=True, validators=[validate_slug]))])
    changes = self.get_changes([from_state], [to_state])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])