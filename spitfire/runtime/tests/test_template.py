import unittest
from spitfire.runtime import template
from spitfire.runtime import _template
from spitfire.runtime import baked


def is_skip():
  pass
is_skip.skip_filter = True


def no_skip():
  pass


class PySpitfireTemplate(template.SpitfireTemplate):

  def __init__(self, *args, **kwargs):
    super(PySpitfireTemplate, self).__init__(*args, **kwargs)
    self.filter_function = self.py_baked_filter_function


class CSpitfireTemplate(template.SpitfireTemplate):

  def __init__(self, *args, **kwargs):
    super(CSpitfireTemplate, self).__init__(*args, **kwargs)
    self.filter_function = self.baked_filter_function


# Do not inherit from unittest.TestCase to ensure that these tests don't run.
# Add tests here and they will be run for the C and Python implementations. This
# should make sure that both implementations are equivalent.
class _TemplateTest(object):

  template_cls = None

  def setUp(self):
    self.template = self.template_cls(baked=True)
    self.template._filter_function = lambda v: 'FILTERED'

  def test_skip_filter(self):
    self.assertEqual(self.template.filter_function('foo', is_skip), 'foo')

  def test_no_skip(self):
    self.assertEqual(self.template.filter_function('foo', no_skip), 'FILTERED')

  def test_str(self):
    self.assertEqual(self.template.filter_function('foo'), 'FILTERED')

  def test_sanitized(self):
    got = self.template.filter_function(baked.SanitizedPlaceholder('foo'))
    want = baked.SanitizedPlaceholder('foo')
    self.assertEqual(got, want)
    self.assertEqual(type(got), type(want))


class TestTemplateC(_TemplateTest, unittest.TestCase):
  template_cls = CSpitfireTemplate


class TestTemplatePy(_TemplateTest, unittest.TestCase):
  template_cls = PySpitfireTemplate


class TestTemplateBakedOff(unittest.TestCase):

  def setUp(self):
    self.template = template.SpitfireTemplate(baked=False)
    self.template._filter_function = lambda v: 'FILTERED'

  def test_filters_sanitized_placeholders(self):
    got = self.template.filter_function(baked.SanitizedPlaceholder('foo'))
    self.assertEqual(got, 'FILTERED')



if __name__ == '__main__':
  unittest.main()
