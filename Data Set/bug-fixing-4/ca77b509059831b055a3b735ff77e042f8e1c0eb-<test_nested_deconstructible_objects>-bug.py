def test_nested_deconstructible_objects(self):
    '\n        Nested deconstruction is applied recursively to the args/kwargs of\n        deconstructed objects.\n        '
    before = self.make_project_state([self.author_name_nested_deconstructible_1])
    after = self.make_project_state([self.author_name_nested_deconstructible_2])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(changes, {
        
    })
    before = self.make_project_state([self.author_name_nested_deconstructible_1])
    after = self.make_project_state([self.author_name_nested_deconstructible_changed_arg])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 1)
    before = self.make_project_state([self.author_name_nested_deconstructible_1])
    after = self.make_project_state([self.author_name_nested_deconstructible_extra_arg])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 1)
    before = self.make_project_state([self.author_name_nested_deconstructible_1])
    after = self.make_project_state([self.author_name_nested_deconstructible_changed_kwarg])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 1)
    before = self.make_project_state([self.author_name_nested_deconstructible_1])
    after = self.make_project_state([self.author_name_nested_deconstructible_extra_kwarg])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(len(changes), 1)