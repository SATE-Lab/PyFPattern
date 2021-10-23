@isolate_apps('schema')
def test_m2m_rename_field_in_target_model(self):

    class LocalTagM2MTest(Model):
        title = CharField(max_length=255)

        class Meta():
            app_label = 'schema'

    class LocalM2M(Model):
        tags = ManyToManyField(LocalTagM2MTest)

        class Meta():
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(LocalM2M)
        editor.create_model(LocalTagM2MTest)
    self.isolated_local_models = [LocalM2M, LocalTagM2MTest]
    self.assertEqual(len(self.column_classes(LocalM2M)), 1)
    old_field = LocalTagM2MTest._meta.get_field('title')
    new_field = CharField(max_length=254)
    new_field.contribute_to_class(LocalTagM2MTest, 'title1')
    self.assertEqual(len(new_field.model._meta.related_objects), 1)
    with connection.schema_editor() as editor:
        editor.alter_field(LocalTagM2MTest, old_field, new_field, strict=True)
    self.assertEqual(len(self.column_classes(LocalM2M)), 1)