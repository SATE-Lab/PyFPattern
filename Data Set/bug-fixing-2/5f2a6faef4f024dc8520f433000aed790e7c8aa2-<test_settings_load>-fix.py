

def test_settings_load(self):
    self.browser.get(self.path1)
    self.browser.wait_until_not('.loading-indicator')
    self.browser.snapshot('project alert settings')
    self.browser.wait_until('.ref-plugin-enable-webhooks')
    self.browser.click('.ref-plugin-enable-webhooks')
    self.browser.wait_until('.ref-plugin-config-webhooks')
    self.browser.wait_until_not('.loading-indicator')
    self.browser.click_when_visible('[data-test-id="toast-success"]')
    self.browser.wait_until_not('[data-test-id="toast-success"]')
    self.browser.snapshot('project alert settings webhooks enabled')
