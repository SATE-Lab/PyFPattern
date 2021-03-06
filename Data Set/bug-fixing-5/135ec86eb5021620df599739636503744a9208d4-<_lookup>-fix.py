def _lookup(self, name, *args, **kwargs):
    instance = self._lookup_loader.get(name.lower(), loader=self._loader, templar=self)
    if (instance is not None):
        wantlist = kwargs.pop('wantlist', False)
        allow_unsafe = kwargs.pop('allow_unsafe', C.DEFAULT_ALLOW_UNSAFE_LOOKUPS)
        errors = kwargs.pop('errors', 'strict')
        from ansible.utils.listify import listify_lookup_plugin_terms
        loop_terms = listify_lookup_plugin_terms(terms=args, templar=self, loader=self._loader, fail_on_undefined=True, convert_bare=False)
        try:
            ran = instance.run(loop_terms, variables=self._available_variables, **kwargs)
        except (AnsibleUndefinedVariable, UndefinedError) as e:
            raise AnsibleUndefinedVariable(e)
        except Exception as e:
            if self._fail_on_lookup_errors:
                msg = ("An unhandled exception occurred while running the lookup plugin '%s'. Error was a %s, original message: %s" % (name, type(e), to_text(e)))
                if (errors == 'warn'):
                    display.warning(msg)
                elif (errors == 'ignore'):
                    display.display(msg, log_only=True)
                else:
                    raise AnsibleError(to_native(msg))
            ran = None
        if (ran and (not allow_unsafe)):
            if wantlist:
                ran = wrap_var(ran)
            else:
                try:
                    ran = UnsafeProxy(','.join(ran))
                except TypeError:
                    if (not isinstance(ran, Sequence)):
                        raise AnsibleError(("The lookup plugin '%s' did not return a list." % name))
                    if (len(ran) == 1):
                        ran = wrap_var(ran[0])
                    else:
                        ran = wrap_var(ran)
            if self.cur_context:
                self.cur_context.unsafe = True
        return ran
    else:
        raise AnsibleError(('lookup plugin (%s) not found' % name))