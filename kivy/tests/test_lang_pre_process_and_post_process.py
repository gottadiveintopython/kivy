cls_name = 'KvPrePost'


def setup_module():
    from textwrap import dedent
    from kivy.lang import Builder
    from kivy.factory import Factory

    assert cls_name not in Factory.classes
    Builder.load_string(
        dedent(f'''
        <{cls_name}>:
            text: 'class rule2'
        <{cls_name}>:
            text: 'class rule'
        '''),
        filename=__file__)


def teardown_module():
    from kivy.lang import Builder
    from kivy.factory import Factory

    Builder.unload_file(__file__)
    Factory.unregister(cls_name)


def test_the_methods_actually_called():
    from kivy.factory import Factory

    is_before_called = False
    is_after_called = False
    class KvPrePost(Factory.Widget):
        def before_class_rule(self):
            nonlocal is_before_called
            is_before_called = True
        def after_class_rule(self):
            nonlocal is_after_called
            is_after_called = True

    w = KvPrePost()
    assert is_before_called
    assert is_after_called
    Factory.unregister(cls_name)


def test_create_from_python_without_arg():
    from kivy.properties import StringProperty
    from kivy.factory import Factory

    class KvPrePost(Factory.Widget):
        text = StringProperty('default')
        def before_class_rule(self):
            assert self.text == 'default'
        def after_class_rule(self):
            assert self.text == 'class rule'

    w = KvPrePost()
    assert w.text == 'class rule'
    Factory.unregister(cls_name)


def test_create_from_python_with_arg():
    from kivy.properties import StringProperty
    from kivy.factory import Factory

    class KvPrePost(Factory.Widget):
        text = StringProperty('default')
        def before_class_rule(self):
            assert self.text == 'arg'
        def after_class_rule(self):
            assert self.text == 'arg'

    w = KvPrePost(text='arg')
    assert w.text == 'arg'
    Factory.unregister(cls_name)


def test_create_from_kv():
    from kivy.properties import StringProperty
    from kivy.factory import Factory
    from kivy.lang import Builder

    class KvPrePost(Factory.Widget):
        text = StringProperty('default')
        def before_class_rule(self):
            assert self.text == 'default'
        def after_class_rule(self):
            assert self.text == 'class rule'

    w = Builder.load_string(f"{cls_name}:\n\ttext: 'instance rule'")
    assert w.text == 'instance rule'
    Factory.unregister(cls_name)
