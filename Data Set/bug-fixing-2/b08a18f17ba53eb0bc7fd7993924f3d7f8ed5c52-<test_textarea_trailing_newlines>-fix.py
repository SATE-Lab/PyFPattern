

def test_textarea_trailing_newlines(self):
    "\n        A roundtrip on a ModelForm doesn't alter the TextField value\n        "
    article = Article.objects.create(content='\nTst\n')
    self.selenium.get((self.live_server_url + reverse('article_form', args=[article.pk])))
    self.selenium.find_element_by_id('submit').click()
    article = Article.objects.get(pk=article.pk)
    self.assertEqual(article.content, '\r\nTst\r\n')
