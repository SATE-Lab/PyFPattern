def _edit_file_helper(self, filename, existing_data=None, force_save=False):
    (_, tmp_path) = tempfile.mkstemp()
    if existing_data:
        self.write_data(existing_data, tmp_path, shred=False)
    try:
        call(self._editor_shell_command(tmp_path))
    except:
        self._shred_file(tmp_path)
        raise
    tmpdata = self.read_data(tmp_path)
    if ((existing_data == tmpdata) and (not force_save)):
        self._shred_file(tmp_path)
        return
    enc_data = self.vault.encrypt(tmpdata.decode())
    self.write_data(enc_data, tmp_path)
    self.shuffle_files(tmp_path, filename)