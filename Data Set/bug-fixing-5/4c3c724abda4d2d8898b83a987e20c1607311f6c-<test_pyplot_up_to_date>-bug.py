def test_pyplot_up_to_date():
    gen_script = (Path(mpl.__file__).parents[2] / 'tools/boilerplate.py')
    if (not gen_script.exists()):
        pytest.skip('boilerplate.py not found')
    orig_contents = Path(plt.__file__).read_text()
    try:
        subprocess.run([sys.executable, str(gen_script)], check=True)
        new_contents = Path(plt.__file__).read_text()
        assert (orig_contents == new_contents)
    finally:
        Path(plt.__file__).write_text(orig_contents)